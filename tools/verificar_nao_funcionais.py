"""Executa seis verificações locais da Etapa 7 em bancos descartáveis."""

import argparse
from contextlib import closing, contextmanager
from http.cookiejar import CookieJar
import math
from pathlib import Path
import re
import secrets
import sqlite3
import statistics
import subprocess
import sys
import tempfile
from time import perf_counter_ns
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPCookieProcessor, ProxyHandler, build_opener

import flaskr
from flaskr.db import get_db, init_db
from werkzeug.security import check_password_hash
from werkzeug.serving import WSGIRequestHandler, make_server


CONTA = {"username": "qa_etapa7", "password": "Senha-Ficticia-NF-2026!"}
CHROME_MAC = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
AQUECIMENTO = 3


class RequisicaoLocal(WSGIRequestHandler):
    def log_request(self, code="-", size="-"):
        # A evidência registra status, conteúdo verificado e tempos no cliente.
        pass


def criar_app(banco):
    return flaskr.create_app({"DATABASE": banco, "SECRET_KEY": secrets.token_hex(32)})


def novo_banco(banco):
    with criar_app(banco).app_context():
        init_db()


def servir(banco):
    with make_server("127.0.0.1", 0, criar_app(banco), request_handler=RequisicaoLocal) as http:
        print(http.server_port, flush=True)
        http.serve_forever()


@contextmanager
def servidor(banco):
    processo = subprocess.Popen(
        [sys.executable, "-B", str(Path(__file__).resolve()), "--servir", str(banco)],
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        porta = int(processo.stdout.readline().strip())
        origem = f"http://127.0.0.1:{porta}"
        print(f"Servidor iniciado: PID={processo.pid}, URL={origem}, SQLite={banco.name}")
        yield origem, processo.pid
    finally:
        if processo.poll() is None:
            processo.terminate()
        try:
            processo.wait(timeout=5)
        except subprocess.TimeoutExpired:
            processo.kill()
            processo.wait(timeout=5)
        processo.stdout.close()
        print(f"Servidor encerrado: PID={processo.pid}, código={processo.returncode}")


def cliente():
    return build_opener(ProxyHandler({}), HTTPCookieProcessor(CookieJar()))


def navegar(opener, origem, caminho, dados=None):
    formulario = None if dados is None else urlencode(dados).encode("utf-8")
    with opener.open(origem + caminho, data=formulario, timeout=4) as resposta:
        return resposta.status, urlsplit(resposta.url).path, resposta.read().decode("utf-8")


def cadastrar(origem):
    status, caminho, html = navegar(cliente(), origem, "/auth/register", CONTA)
    assert (status, caminho) == (200, "/auth/login"), (status, caminho)
    assert "<h1>Log In</h1>" in html
    return html


def entrar(origem):
    sessao = cliente()
    status, caminho, html = navegar(sessao, origem, "/auth/login", CONTA)
    assert (status, caminho) == (200, "/"), (status, caminho)
    assert "Log Out" in html and f"<span>{CONTA['username']}</span>" in html
    return sessao


def salvar(sessao, origem, caminho, titulo, corpo):
    status, destino, html = navegar(
        sessao, origem, caminho, {"title": titulo, "body": corpo}
    )
    assert (status, destino) == (200, "/"), (status, destino)
    assert f"<h1>{titulo}</h1>" in html and f'<p class="body">{corpo}</p>' in html
    print(f"{caminho} → {destino}: HTTP {status}; título e corpo presentes")
    return html


def verificar_senha(banco):
    with servidor(banco) as (origem, _):
        html = cadastrar(origem)
    with closing(sqlite3.connect(banco.as_uri() + "?mode=ro", uri=True)) as conexao:
        registros = conexao.execute(
            "SELECT password FROM user WHERE username = ?", (CONTA["username"],)
        ).fetchall()
    senha = CONTA["password"]
    ocorrencias = html.count(senha)
    diferente = len(registros) == 1 and registros[0][0] != senha
    valido = len(registros) == 1 and check_password_hash(registros[0][0], senha)
    print(f"Cadastro → /auth/login: HTTP 200; ocorrências da senha no HTML: {ocorrencias}")
    print(f"Registros da conta: {len(registros)}; hash diferente: {diferente}; verificável: {valido}")
    assert ocorrencias == 0 and diferente and valido


def verificar_reinicio(banco):
    with servidor(banco) as (origem, pid_inicial):
        cadastrar(origem)
        sessao = entrar(origem)
        html = salvar(sessao, origem, "/create", "Aviso inicial", "Texto anterior.")
        link = re.search(r'href="(/[0-9]+/update)">Edit', html)
        assert link, "Editor do post não localizado na listagem."
        salvar(sessao, origem, link[1], "Aviso revisado", "Texto revisado.")
        salvar(sessao, origem, "/create", "Aviso de controle", "Texto de controle.")
        inode_inicial = banco.stat().st_ino
    with servidor(banco) as (origem, pid_novo):
        status, destino, html = navegar(cliente(), origem, "/")
        inode_novo = banco.stat().st_ino
        revisado = "<h1>Aviso revisado</h1>" in html and "Texto revisado." in html
        controle = "<h1>Aviso de controle</h1>" in html and "Texto de controle." in html
        original = "Aviso inicial" in html or "Texto anterior." in html
        print(f"Processos: {pid_inicial} → {pid_novo}; inodes: {inode_inicial} → {inode_novo}")
        print(f"GET {destino}: HTTP {status}; revisado={revisado}; controle={controle}; original={original}")
        assert pid_novo != pid_inicial and inode_novo == inode_inicial
        assert (status, destino) == (200, "/") and revisado and controle and not original


def medir(origem, caminho, formulario, repeticoes, limite_ms, marcadores):
    tempos = []
    validade = []
    print(f"Rota={caminho}; aquecimentos={AQUECIMENTO}; amostras={repeticoes}; p95 limite={limite_ms} ms")
    for rodada in range(1, AQUECIMENTO + repeticoes + 1):
        sessao = cliente()
        inicio = perf_counter_ns()
        status, destino, html = navegar(sessao, origem, caminho, formulario)
        duracao = (perf_counter_ns() - inicio) / 1_000_000
        valida = (status, destino) == (200, "/") and all(item in html for item in marcadores)
        fase = "aquecimento" if rodada <= AQUECIMENTO else "amostra"
        print(f"{rodada:02d} {fase}: {duracao:.6f} ms; HTTP {status}; conteúdo={valida}")
        validade.append(valida)
        if rodada > AQUECIMENTO:
            tempos.append(duracao)
    p95 = sorted(tempos)[math.ceil(0.95 * len(tempos)) - 1]
    print(f"Mínimo={min(tempos):.6f} ms; mediana={statistics.median(tempos):.6f} ms; p95={p95:.6f} ms; máximo={max(tempos):.6f} ms")
    print(f"Respostas conferidas={sum(validade)}/{len(validade)}")
    assert all(validade) and p95 <= limite_ms


def verificar_latencia_listagem(banco):
    with servidor(banco) as (origem, _):
        cadastrar(origem)
        with criar_app(banco).app_context():
            conexao = get_db()
            autor_id = conexao.execute("SELECT id FROM user").fetchone()[0]
            with conexao:
                conexao.executemany(
                    "INSERT INTO post (author_id, title, body, created) VALUES (?, ?, ?, ?)",
                    [(autor_id, f"Publicação NF {n:02d}", f"Texto fictício {n:02d}.",
                      f"2026-01-10 09:00:{n:02d}") for n in range(1, 51)],
                )
        marcadores = [f"<h1>Publicação NF {n:02d}</h1>" for n in range(1, 51)]
        medir(origem, "/", None, 30, 200, marcadores)


def verificar_latencia_login(banco):
    with servidor(banco) as (origem, _):
        cadastrar(origem)
        marcadores = (f"<span>{CONTA['username']}</span>", "Log Out")
        medir(origem, "/auth/login", CONTA, 15, 750, marcadores)


def verificar_unicode(banco):
    titulo = "São João — café ☕"
    corpo = "Ação e coração em português.\nAté amanhã! 🌱"
    with servidor(banco) as (origem, _):
        cadastrar(origem)
        salvar(entrar(origem), origem, "/create", titulo, corpo)
        status, destino, html = navegar(cliente(), origem, "/")
        encontrado = f"<h1>{titulo}</h1>" in html and f'<p class="body">{corpo}</p>' in html
    with closing(sqlite3.connect(banco.as_uri() + "?mode=ro", uri=True)) as conexao:
        textos = conexao.execute("SELECT title, body FROM post").fetchall()
    print(f"GET {destino}: HTTP {status}; título e corpo exatos no HTML={encontrado}")
    print(f"SQLite: {textos!r}")
    assert (status, destino) == (200, "/") and encontrado and textos == [(titulo, corpo)]


def verificar_chrome(banco, chrome):
    versao = subprocess.run([str(chrome), "--version"], capture_output=True, text=True, check=True)
    print(versao.stdout.strip())
    with servidor(banco) as (origem, _):
        cadastrar(origem)
        salvar(entrar(origem), origem, "/create", "Teclado QA", "Publicado com teclado.")
        resultado = subprocess.run(
            [str(chrome), "--headless", "--no-first-run", "--disable-background-networking",
             "--disable-component-update", f"--user-data-dir={banco.parent / 'chrome'}",
             "--dump-dom", origem + "/"],
            capture_output=True, text=True, check=True, timeout=25,
        )
    html = resultado.stdout
    print("DOM público observado pelo Chrome:")
    print(html.rstrip())
    assert "<title>Posts - Flaskr</title>" in html
    assert "<h1>Teclado QA</h1>" in html and '<p class="body">Publicado com teclado.</p>' in html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chrome", type=Path, default=CHROME_MAC)
    parser.add_argument("--servir", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.servir:
        servir(args.servir)
        return 0

    raiz = Path(__file__).resolve().parents[1]
    assert Path(flaskr.__file__).resolve().is_relative_to(raiz / "flaskr-app")
    print(f"Código importado: {Path(flaskr.__file__).resolve().relative_to(raiz)}; SQLite {sqlite3.sqlite_version}")
    verificacoes = (
        ("NF-01", verificar_senha),
        ("NF-02", verificar_reinicio),
        ("NF-04", verificar_latencia_listagem),
        ("NF-05", verificar_latencia_login),
        ("NF-06", verificar_unicode),
        ("NF-07", lambda banco: verificar_chrome(banco, args.chrome)),
    )
    atendidas = 0
    for identificador, verificar in verificacoes:
        print(f"\n{identificador} | Início")
        with tempfile.TemporaryDirectory(prefix=f"flaskr-etapa7-{identificador.lower()}-") as pasta:
            try:
                banco = Path(pasta) / "flaskr.sqlite"
                novo_banco(banco)
                verificar(banco)
            except AssertionError as falha:
                print(f"{identificador} | Não atende | {falha or 'Consulte os dados acima.'}")
            except (OSError, subprocess.SubprocessError, ValueError) as erro:
                print(f"{identificador} | Bloqueado | {erro}")
            else:
                atendidas += 1
                print(f"{identificador} | Atende")
    print(f"\nVerificações locais que atendem ao critério: {atendidas}/{len(verificacoes)}")
    return int(atendidas != len(verificacoes))


if __name__ == "__main__":
    sys.exit(main())
