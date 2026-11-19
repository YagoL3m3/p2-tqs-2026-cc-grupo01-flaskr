"""Verifica a preparação dos bancos da Etapa 4A sem uso do navegador."""

import os
import re
import sqlite3
import subprocess
import sys
import tempfile
from contextlib import closing
from pathlib import Path
from urllib.request import urlopen

from werkzeug.security import check_password_hash

RAIZ = Path(__file__).resolve().parents[1]

def comando(*args, env=None):
    return subprocess.run([sys.executable, *args], check=False, env=env,
                          text=True, capture_output=True, cwd=RAIZ, timeout=15)

def consultar(diretorio, sql):
    with closing(sqlite3.connect(diretorio / "flaskr.sqlite")) as banco:
        return banco.execute(sql).fetchall()

def main():
    with tempfile.TemporaryDirectory(prefix="verificacao-flaskr-etapa4-") as area:
        env = dict(os.environ, TMPDIR=area, TMP=area, TEMP=area)
        cli = "tools/resetar_banco_etapa4.py"
        factory = "tools.resetar_banco_etapa4:criar_app"

        def preparar(massa):
            result = comando(cli, "--massa", massa, env=env)
            assert result.returncode == 0, f"Preparar {massa} falhou: {result.stderr.strip()}"
            directory = Path(result.stdout.strip())
            assert directory.is_dir() and directory.parent.resolve() == Path(area).resolve()
            return directory

        vazia = preparar("vazia")
        assert consultar(vazia, 'SELECT COUNT(*) FROM user') == [(0,)]
        assert consultar(vazia, 'SELECT COUNT(*) FROM post') == [(0,)]
        print("Massa vazia: sem usuários e publicações.")

        contas = preparar("contas")
        usuarios = dict(consultar(contas, 'SELECT username, password FROM user'))
        assert set(usuarios) == {'qa_autor_a', 'qa_autor_b'}
        assert check_password_hash(usuarios['qa_autor_a'], 'Senha-QA-A-2026!')
        assert check_password_hash(usuarios['qa_autor_b'], 'Senha-QA-B-2026!')
        assert consultar(contas, 'SELECT COUNT(*) FROM post') == [(0,)]
        print("Massa contas: duas contas fictícias com hashes válidos e nenhum post.")

        publicacoes = preparar("publicacoes")
        assert consultar(publicacoes, 'SELECT title, body, username FROM post JOIN user ON user.id = post.author_id ORDER BY created DESC') == [
            ('Post B', 'Corpo B', 'qa_autor_a'), ('Post A', 'Corpo A', 'qa_autor_a')]
        assert consultar(publicacoes, 'SELECT COUNT(DISTINCT created) FROM post') == [(2,)]
        assert len({vazia, contas, publicacoes}) == 3
        assert consultar(vazia, 'SELECT COUNT(*) FROM user') == [(0,)]
        print("Massa publicações: a preparação criou um terceiro banco com dois posts ordenáveis.")

        invalido = Path(area) / 'banco-que-nao-e-de-qa'
        invalido.mkdir()
        rejected = comando("-m", "flask", "--app", factory, "routes",
                           env=dict(env, FLASKR_QA_DIR=str(invalido)))
        assert rejected.returncode != 0 and "ambiente" in rejected.stderr.lower()
        assert list(invalido.iterdir()) == []
        print("Uma pasta fora do padrão foi rejeitada sem criar banco.")

        env_app = dict(env, FLASKR_QA_DIR=str(publicacoes))
        for numero in (1, 2):
            server = subprocess.Popen(
                [sys.executable, "-m", "flask", "--app", factory, "run",
                 "--host", "127.0.0.1", "--port", "0", "--no-reload"],
                env=env_app, cwd=RAIZ, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            try:
                logs = []
                for line in server.stdout:
                    logs.append(line)
                    address = re.search(r'http://127\.0\.0\.1:\d+', line)
                    if address:
                        break
                else:
                    raise AssertionError("Servidor não iniciou:\n" + "".join(logs))
                with urlopen(address.group() + '/', timeout=5) as resposta:
                    body = resposta.read().decode()
                    assert resposta.status == 200 and 'Post A' in body and 'Post B' in body
                    assert body.index('Post B') < body.index('Post A')
                print(f"Inicialização {numero}: HTTP 200 e as mesmas publicações na mesma ordem.")
            finally:
                if server.poll() is None:
                    server.terminate()
                server.wait(timeout=10)
                server.stdout.close()


if __name__ == "__main__":
    main()
