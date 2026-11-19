"""Executa o Newman contra uma instância HTTP descartável do Flaskr."""

import argparse
from importlib.metadata import version
from pathlib import Path
from secrets import token_hex
import shlex
import shutil
import sqlite3
import subprocess
from tempfile import TemporaryDirectory
from threading import Thread

from werkzeug.serving import make_server

from flaskr import create_app
from flaskr.db import init_db

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVOS = RAIZ / "testes_grupo" / "integracao_postman"
HOST = "127.0.0.1"
NEWMAN = "newman@6.2.1"


def executar_newman(argumentos, url):
    comando = [
        "npx",
        "--yes",
        NEWMAN,
        "run",
        str(ARQUIVOS / "Flaskr.postman_collection.json"),
        "--environment",
        str(ARQUIVOS / "Flaskr_Local.postman_environment.json"),
        "--env-var",
        f"baseUrl={url}",
        "--ignore-redirects",
        "--timeout-request",
        "10000",
        "--color",
        "off",
    ]
    relatores = ["cli"]
    for relator, destino in (
        ("json", argumentos.relatorio_json),
        ("junit", argumentos.junitxml),
    ):
        if destino is not None:
            destino.parent.mkdir(parents=True, exist_ok=True)
            relatores.append(relator)
            comando.extend([f"--reporter-{relator}-export", str(destino)])
    comando.extend(["--reporters", ",".join(relatores)])
    if argumentos.pasta:
        comando.extend(["--folder", argumentos.pasta, "--bail", "folder"])

    print(shlex.join(comando), flush=True)
    return subprocess.run(comando, check=False).returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--relatorio-json", type=Path, help="Caminho do relatório JSON do Newman.")
    parser.add_argument("--junitxml", type=Path, help="Caminho do relatório JUnit XML do Newman.")
    parser.add_argument("--pasta", help="Executa somente a pasta com este nome na coleção.")
    parser.add_argument(
        "--servir",
        action="store_true",
        help="Serve em 127.0.0.1:5002 para execução pelo aplicativo Postman.",
    )
    argumentos = parser.parse_args()
    if not argumentos.servir and shutil.which("npx") is None:
        parser.error("Instale Node.js e npm para disponibilizar o npx no PATH.")

    with TemporaryDirectory(prefix="flaskr-postman-") as pasta:
        app = create_app({"DATABASE": Path(pasta) / "flaskr.sqlite", "SECRET_KEY": token_hex(32)})
        with app.app_context():
            init_db()

        with make_server(HOST, 5002 if argumentos.servir else 0, app) as servidor:
            url = f"http://{HOST}:{servidor.server_port}"
            print(
                f"Flask {version('Flask')} | Werkzeug {version('Werkzeug')} | "
                f"SQLite {sqlite3.sqlite_version} | {url}",
                flush=True,
            )
            if argumentos.servir:
                try:
                    servidor.serve_forever()
                except KeyboardInterrupt:
                    return 0

            tarefa = Thread(target=servidor.serve_forever, daemon=True)
            tarefa.start()
            try:
                return executar_newman(argumentos, url)
            finally:
                servidor.shutdown()
                tarefa.join()


if __name__ == "__main__":
    raise SystemExit(main())
