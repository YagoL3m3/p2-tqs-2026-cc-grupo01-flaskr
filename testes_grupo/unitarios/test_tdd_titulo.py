"""Regressão da regra de título com conteúdo visível (RF-05 e RF-06)."""

import pytest

from flaskr.db import get_db


@pytest.mark.parametrize(
    ("caminho", "titulo_original"),
    [("/create", None), ("/1/update", "Título inicial")],
    ids=["AUT-U-09-criacao", "AUT-U-10-edicao"],
)
def test_recusa_titulo_composto_apenas_por_espacos(app_grupo, caminho, titulo_original):
    cliente = app_grupo.test_client()
    credenciais = {"username": "qa_tdd_autor", "password": "Senha-Ficticia-TDD!"}
    assert cliente.post("/auth/register", data=credenciais).status_code == 302
    assert cliente.post("/auth/login", data=credenciais).status_code == 302

    if titulo_original:
        post = {"title": titulo_original, "body": "Conteúdo inicial"}
        assert cliente.post("/create", data=post).status_code == 302

    resposta = cliente.post(caminho, data={"title": "  \t  ", "body": "Rascunho"})
    assert resposta.status_code == 200, "Título composto de espaços deve manter o formulário aberto."
    assert b"Title is required." in resposta.data

    with app_grupo.app_context():
        titulos = [linha["title"] for linha in get_db().execute("SELECT title FROM post")]
    assert titulos == ([titulo_original] if titulo_original else [])
