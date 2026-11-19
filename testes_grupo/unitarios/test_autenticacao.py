import pytest
from flask import get_flashed_messages, session
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr import auth
from flaskr.db import get_db


@pytest.fixture
def conta_original(app_grupo):
    conta = {"id": 41, "username": "qa_original", "password": "Senha-QA-Original!"}
    with app_grupo.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO user (id, username, password) VALUES (?, ?, ?)",
            (conta["id"], conta["username"], generate_password_hash(conta["password"])),
        )
        db.commit()
    return conta


def test_aut_u_01_cadastro_armazena_hash_da_senha(app_grupo):
    """AUT-U-01 · CT-005 / RF-01 · CT-026 / RNF-01."""
    senha = "Senha-QA-Nova!"
    with app_grupo.test_request_context(
        "/auth/register", method="POST", data={"username": "q", "password": senha}
    ):
        resposta = auth.register()
        assert resposta.status_code == 302
        assert resposta.location == "/auth/login"

    with app_grupo.app_context():
        registros = get_db().execute("SELECT username, password FROM user").fetchall()
        assert len(registros) == 1
        usuario = registros[0]
        assert usuario["username"] == "q"
        assert usuario["password"] != senha
        assert check_password_hash(usuario["password"], senha)


def test_aut_u_02_duplicata_preserva_credencial_original(app_grupo, conta_original):
    """AUT-U-02 · CT-004 / RF-01."""
    senha_alternativa = "Senha-QA-Alternativa!"
    nome = conta_original["username"]
    with app_grupo.test_request_context(
        "/auth/register",
        method="POST",
        data={"username": nome, "password": senha_alternativa},
    ):
        auth.register()
        assert get_flashed_messages() == [f"User {nome} is already registered."]

    with app_grupo.app_context():
        registros = get_db().execute("SELECT id, username, password FROM user").fetchall()
        assert len(registros) == 1
        usuario = registros[0]
        assert (usuario["id"], usuario["username"]) == (conta_original["id"], nome)
        assert check_password_hash(usuario["password"], conta_original["password"])
        assert not check_password_hash(usuario["password"], senha_alternativa)


def test_aut_u_03_login_substitui_dados_da_sessao(app_grupo, conta_original):
    """AUT-U-03 · CT-006 / RF-02."""
    with app_grupo.test_request_context(
        "/auth/login",
        method="POST",
        data={"username": conta_original["username"], "password": conta_original["password"]},
    ):
        session.update(user_id=7, anotacao="sessão anterior de teste")
        resposta = auth.login()

        assert resposta.status_code == 302
        assert resposta.location == "/"
        assert dict(session) == {"user_id": conta_original["id"]}


def test_aut_u_04_logout_limpa_todos_os_dados_da_sessao(app_grupo):
    """AUT-U-04 · CT-009 / RF-03."""
    with app_grupo.test_request_context("/auth/logout"):
        session.update(user_id=41, anotacao="valor fictício da sessão ativa")
        resposta = auth.logout()

        assert resposta.status_code == 302
        assert resposta.location == "/"
        assert dict(session) == {}
