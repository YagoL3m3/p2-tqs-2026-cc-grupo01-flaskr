"""Fluxos de usuário em um navegador real contra o Flaskr local."""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condicao
from werkzeug.security import generate_password_hash

from flaskr.db import get_db

USUARIO = "qa_selenium_autor"
SENHA = "Senha-Ficticia-Selenium-2026!"
BOTAO_FORMULARIO = (By.CSS_SELECTOR, "form input[type='submit']")
TITULO_PAGINA = (By.CSS_SELECTOR, "section.content > header > h1")
LINK_INICIO = (By.CSS_SELECTOR, "nav h1 a")
ARTIGOS = (By.CSS_SELECTOR, "article.post")
MENU_USUARIO = (By.CSS_SELECTOR, "nav li span")


@pytest.fixture
def conta_exemplo(app_grupo):
    with app_grupo.app_context():
        banco = get_db()
        with banco:
            registro = banco.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (USUARIO, generate_password_hash(SENHA)),
            )
        return registro.lastrowid


@pytest.fixture
def dois_posts(app_grupo, conta_exemplo):
    with app_grupo.app_context():
        banco = get_db()
        with banco:
            banco.executemany(
                "INSERT INTO post (author_id, title, body) VALUES (?, ?, ?)",
                (
                    (conta_exemplo, "Post A", "Corpo A"),
                    (conta_exemplo, "Post B", "Corpo B"),
                ),
            )


def clicar(espera, localizador):
    espera.until(condicao.element_to_be_clickable(localizador)).click()


def preencher(espera, campo, valor):
    elemento = espera.until(condicao.visibility_of_element_located((By.ID, campo)))
    elemento.clear()
    elemento.send_keys(valor)


def enviar_credenciais(espera, senha):
    preencher(espera, "username", USUARIO)
    preencher(espera, "password", senha)
    clicar(espera, BOTAO_FORMULARIO)


def entrar(espera):
    clicar(espera, (By.LINK_TEXT, "Log In"))
    enviar_credenciais(espera, SENHA)
    assert espera.until(condicao.visibility_of_element_located(MENU_USUARIO)).text == USUARIO


def obter_artigo(espera, titulo):
    def localizar_titulo(driver):
        for artigo in driver.find_elements(*ARTIGOS):
            if artigo.find_element(By.CSS_SELECTOR, "header h1").text == titulo:
                return artigo
        return False

    return espera.until(localizar_titulo, f"Artigo ausente: {titulo}")


def titulos_publicados(navegador):
    return {
        titulo.text
        for titulo in navegador.find_elements(By.CSS_SELECTOR, "article.post header h1")
    }


def verificar_conteudo(artigo, corpo):
    assert artigo.find_element(By.CSS_SELECTOR, ".body").text == corpo
    assert artigo.find_element(By.CSS_SELECTOR, ".about").text.startswith(f"by {USUARIO} on ")


def abrir_editor(espera):
    artigo = obter_artigo(espera, "Post A")
    link = artigo.find_element(By.LINK_TEXT, "Edit")
    espera.until(condicao.element_to_be_clickable(link)).click()
    assert espera.until(condicao.visibility_of_element_located(TITULO_PAGINA)).text == 'Edit "Post A"'


def test_aut_s_01_cadastro_aceita_nova_conta(navegador, espera, servidor_selenium):
    """AUT-S-01 | CT-001 | RF-01 — Cadastrar uma conta inédita."""
    navegador.get(servidor_selenium)
    clicar(espera, (By.LINK_TEXT, "Register"))
    enviar_credenciais(espera, SENHA)

    espera.until(condicao.url_to_be(f"{servidor_selenium}/auth/login"))
    assert espera.until(condicao.visibility_of_element_located(TITULO_PAGINA)).text == "Log In"
    enviar_credenciais(espera, SENHA)
    espera.until(condicao.url_to_be(f"{servidor_selenium}/"))
    assert espera.until(condicao.visibility_of_element_located(MENU_USUARIO)).text == USUARIO
    assert espera.until(condicao.visibility_of_element_located((By.LINK_TEXT, "Log Out")))


@pytest.mark.usefixtures("conta_exemplo")
def test_aut_s_02_login_rejeita_senha_errada(navegador, espera, servidor_selenium):
    """AUT-S-02 | CT-008 | RF-02 — Rejeitar senha errada de conta existente."""
    navegador.get(servidor_selenium)
    clicar(espera, (By.LINK_TEXT, "Log In"))
    enviar_credenciais(espera, "Senha-Incorreta-QA!")

    alerta = espera.until(condicao.visibility_of_element_located((By.CSS_SELECTOR, ".flash")))
    assert alerta.text == "Incorrect password."
    assert navegador.current_url == f"{servidor_selenium}/auth/login"
    assert navegador.find_element(By.LINK_TEXT, "Register").is_displayed()
    assert not navegador.find_elements(By.LINK_TEXT, "Log Out")


@pytest.mark.usefixtures("conta_exemplo")
def test_aut_s_03_publica_titulo_corpo_e_autoria(navegador, espera, servidor_selenium):
    """AUT-S-03 | CT-014 | RF-05 — Publicar título e corpo como a conta ativa."""
    navegador.get(servidor_selenium)
    entrar(espera)
    clicar(espera, (By.LINK_TEXT, "New"))
    preencher(espera, "title", "Rotina QA")
    preencher(espera, "body", "Texto fictício da rotina.")
    clicar(espera, BOTAO_FORMULARIO)

    espera.until(condicao.url_to_be(f"{servidor_selenium}/"))
    verificar_conteudo(obter_artigo(espera, "Rotina QA"), "Texto fictício da rotina.")


@pytest.mark.usefixtures("conta_exemplo")
def test_aut_s_04_formulario_bloqueia_titulo_vazio(navegador, espera, servidor_selenium):
    """AUT-S-04 | CT-017 | RF-05 — Bloquear o envio sem título no navegador."""
    navegador.get(servidor_selenium)
    entrar(espera)
    clicar(espera, (By.LINK_TEXT, "New"))
    preencher(espera, "body", "Este rascunho não deve aparecer.")
    clicar(espera, BOTAO_FORMULARIO)

    espera.until(condicao.visibility_of_element_located((By.CSS_SELECTOR, "#title:invalid:focus")))
    assert navegador.current_url == f"{servidor_selenium}/create"
    assert (
        navegador.find_element(By.ID, "body").get_property("value")
        == "Este rascunho não deve aparecer."
    )
    clicar(espera, LINK_INICIO)
    assert espera.until(condicao.visibility_of_element_located(TITULO_PAGINA)).text == "Posts"
    assert not navegador.find_elements(*ARTIGOS)


@pytest.mark.usefixtures("dois_posts")
def test_aut_s_05_autor_edita_publicacao(navegador, espera, servidor_selenium):
    """AUT-S-05 | CT-018 | RF-06 — Editar título e corpo na interface."""
    navegador.get(servidor_selenium)
    entrar(espera)
    abrir_editor(espera)
    preencher(espera, "title", "Post A revisado")
    preencher(espera, "body", "Corpo A revisado")
    clicar(espera, (By.CSS_SELECTOR, "input[value='Save']"))

    espera.until(condicao.url_to_be(f"{servidor_selenium}/"))
    verificar_conteudo(obter_artigo(espera, "Post A revisado"), "Corpo A revisado")
    assert titulos_publicados(navegador) == {"Post A revisado", "Post B"}


@pytest.mark.usefixtures("dois_posts")
def test_aut_s_06_cancelar_dialogo_conserva_publicacoes(navegador, espera, servidor_selenium):
    """AUT-S-06 | CT-022 | RF-07 — Cancelar o diálogo e conservar os posts."""
    navegador.get(servidor_selenium)
    entrar(espera)
    abrir_editor(espera)
    clicar(espera, (By.CSS_SELECTOR, "input[value='Delete']"))
    espera.until(condicao.alert_is_present()).dismiss()

    assert espera.until(condicao.visibility_of_element_located(TITULO_PAGINA)).text == 'Edit "Post A"'
    clicar(espera, LINK_INICIO)
    assert espera.until(condicao.visibility_of_element_located(TITULO_PAGINA)).text == "Posts"
    assert titulos_publicados(navegador) == {"Post A", "Post B"}


@pytest.mark.usefixtures("dois_posts")
def test_aut_s_07_confirmar_exclusao_remove_so_o_alvo(navegador, espera, servidor_selenium):
    """AUT-S-07 | CT-023 | RF-07 — Confirmar exclusão só do post selecionado."""
    navegador.get(servidor_selenium)
    entrar(espera)
    abrir_editor(espera)
    clicar(espera, (By.CSS_SELECTOR, "input[value='Delete']"))
    espera.until(condicao.alert_is_present()).accept()

    espera.until(condicao.url_to_be(f"{servidor_selenium}/"))
    verificar_conteudo(obter_artigo(espera, "Post B"), "Corpo B")
    assert titulos_publicados(navegador) == {"Post B"}
