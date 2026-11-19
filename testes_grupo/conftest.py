import pytest

from flaskr import create_app
from flaskr.db import init_db


@pytest.fixture
def app_grupo(tmp_path):
    """Prepara um banco SQLite vazio e exclusivo para cada teste do grupo."""
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "flaskr-teste.sqlite"),
            "SECRET_KEY": "chave-ficticia-dos-testes",
        }
    )
    with app.app_context():
        init_db()
    return app
