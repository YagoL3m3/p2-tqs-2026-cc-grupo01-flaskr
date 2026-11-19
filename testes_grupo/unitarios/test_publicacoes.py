import pytest
from flask import g, get_flashed_messages

from flaskr import blog
from flaskr.db import get_db


@pytest.fixture
def banco_blog(app_grupo):
    with app_grupo.app_context():
        db = get_db()
        db.executescript(
            """
            INSERT INTO user (id, username, password) VALUES
                (41, 'qa_autor', 'valor-ficticio-da-massa'),
                (42, 'qa_leitor', 'valor-ficticio-da-massa');
            INSERT INTO post (id, author_id, created, title, body) VALUES
                (21, 41, '2026-11-19 10:00:00', 'Primeiro QA', 'Corpo A'),
                (12, 41, '2026-11-19 11:00:00', 'Segundo QA', 'Corpo B');
            """
        )
    return app_grupo


def test_aut_u_05_listagem_ordena_pela_data_da_publicacao(banco_blog, monkeypatch):
    """AUT-U-05 · CT-011 / RF-04."""

    def capturar_dados(template, posts):
        assert template == "blog/index.html"
        return [(post["id"], post["title"]) for post in posts]

    monkeypatch.setattr(blog, "render_template", capturar_dados)

    with banco_blog.app_context():
        assert blog.index() == [(12, "Segundo QA"), (21, "Primeiro QA")]


def test_aut_u_06_criacao_aceita_corpo_vazio_e_atribui_autoria(banco_blog):
    """AUT-U-06 · CT-014 e CT-016 / RF-05."""
    titulo = "Sem corpo QA"
    with banco_blog.test_request_context(
        "/create", method="POST", data={"title": titulo, "body": ""}
    ):
        g.user = get_db().execute("SELECT id FROM user WHERE id = 42").fetchone()
        resposta = blog.create()
        assert resposta.status_code == 302
        assert resposta.location == "/"

    with banco_blog.app_context():
        publicacoes = get_db().execute(
            "SELECT body, author_id FROM post WHERE title = ?", (titulo,)
        ).fetchall()
        assert [tuple(post) for post in publicacoes] == [("", 42)]


def test_aut_u_07_edicao_sem_titulo_preserva_publicacao(banco_blog):
    """AUT-U-07 · CT-019 / RF-06."""
    with banco_blog.test_request_context(
        "/21/update", method="POST", data={"title": "", "body": "Rascunho alterado"}
    ):
        g.user = get_db().execute("SELECT id FROM user WHERE id = 41").fetchone()
        blog.update(id=21)
        assert get_flashed_messages() == ["Title is required."]

    with banco_blog.app_context():
        registros = get_db().execute(
            "SELECT title, body, author_id FROM post WHERE id = 21"
        ).fetchall()
        assert [tuple(post) for post in registros] == [("Primeiro QA", "Corpo A", 41)]


def test_aut_u_08_exclusao_preserva_publicacao_de_controle(banco_blog):
    """AUT-U-08 · CT-023 / RF-07."""
    with banco_blog.test_request_context("/21/delete", method="POST"):
        g.user = get_db().execute("SELECT id FROM user WHERE id = 41").fetchone()
        resposta = blog.delete(id=21)
        assert resposta.status_code == 302
        assert resposta.location == "/"

    with banco_blog.app_context():
        registros = get_db().execute("SELECT id, title, body, author_id FROM post").fetchall()
        assert [tuple(post) for post in registros] == [(12, "Segundo QA", "Corpo B", 41)]
