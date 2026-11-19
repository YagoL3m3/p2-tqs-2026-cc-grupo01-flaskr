"""Prepara um banco descartável para os casos manuais do Flaskr."""

import argparse
import json
import os
from pathlib import Path
import secrets
import tempfile

from click import ClickException
from werkzeug.security import generate_password_hash

from flaskr import create_app
from flaskr.db import get_db, init_db

PREFIXO = "flaskr-etapa4-"
NOME_BANCO = "flaskr.sqlite"
NOME_CONFIG = "ambiente_etapa4.json"
MASSA = Path(__file__).resolve().parents[1] / "testes_grupo" / "dados" / "massa_etapa4.json"


def preparar_banco(massa):
    """Gera uma pasta temporária exclusiva e retorna seu caminho."""
    pasta = Path(tempfile.mkdtemp(prefix=PREFIXO)).resolve()
    chave = secrets.token_hex(32)
    app = create_app({"DATABASE": pasta / NOME_BANCO, "SECRET_KEY": chave})

    with app.app_context():
        init_db()
        if massa != "vazia":
            dados = json.loads(MASSA.read_text(encoding="utf-8"))
            banco = get_db()
            autores = {}
            with banco:
                for usuario in dados["usuarios"]:
                    registro = banco.execute(
                        "INSERT INTO user (username, password) VALUES (?, ?)",
                        (usuario["nome"], generate_password_hash(usuario["senha"])),
                    )
                    autores[usuario["nome"]] = registro.lastrowid
                if massa == "publicacoes":
                    banco.executemany(
                        "INSERT INTO post (author_id, title, body, created) VALUES (?, ?, ?, ?)",
                        [
                            (autores[post["autor"]], post["titulo"], post["corpo"], post["criacao"])
                            for post in dados["publicacoes"]
                        ],
                    )

    (pasta / NOME_CONFIG).write_text(json.dumps({"secret_key": chave}), encoding="utf-8")
    return pasta


def criar_app():
    """Abre o banco indicado por FLASKR_QA_DIR sem inicializar os dados."""
    caminho = os.environ.get("FLASKR_QA_DIR")
    if not caminho:
        raise ClickException("Defina FLASKR_QA_DIR com o caminho produzido na preparação do ambiente.")
    pasta = Path(caminho).resolve()
    if pasta.parent != Path(tempfile.gettempdir()).resolve() or not pasta.name.startswith(PREFIXO):
        raise ClickException("FLASKR_QA_DIR precisa apontar para um ambiente temporário da Etapa 4.")

    banco = pasta / NOME_BANCO
    config = pasta / NOME_CONFIG
    if any(arquivo.is_symlink() or not arquivo.is_file() for arquivo in (banco, config)):
        raise ClickException("O ambiente temporário está incompleto. Prepare outro banco.")
    chave = json.loads(config.read_text(encoding="utf-8"))["secret_key"]
    return create_app({"DATABASE": banco, "SECRET_KEY": chave})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--massa",
        choices=("vazia", "contas", "publicacoes"),
        default="vazia",
        help="Cria uma base vazia, com duas contas, ou com duas contas e dois posts.",
    )
    print(preparar_banco(parser.parse_args().massa))
