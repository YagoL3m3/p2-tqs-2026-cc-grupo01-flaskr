"""Ensaio de aceitação por IA, executado apenas quando solicitado explicitamente."""

import json
import os
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condicao
from werkzeug.security import generate_password_hash

from flaskr.db import get_db
from test_fluxos import (
    ARTIGOS,
    BOTAO_FORMULARIO,
    LINK_INICIO,
    MENU_USUARIO,
    TITULO_PAGINA,
    clicar,
    obter_artigo,
    preencher,
)

MASSA = Path(__file__).resolve().parents[1] / "dados" / "massa_etapa4.json"
DADOS = json.loads(MASSA.read_text(encoding="utf-8"))
CONTA_A, CONTA_B = DADOS["usuarios"]
LOGIN = (By.LINK_TEXT, "Log In")
LOGOUT = (By.LINK_TEXT, "Log Out")
EDITAR = (By.LINK_TEXT, "Edit")
EXCLUIR = (By.CSS_SELECTOR, "input[value='Delete']")


@pytest.fixture
def publicacoes_iniciais(app_grupo):
    with app_grupo.app_context():
        banco = get_db()
        with banco:
            autores = {
                conta["nome"]: banco.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (conta["nome"], generate_password_hash(conta["senha"])),
                ).lastrowid
                for conta in DADOS["usuarios"]
            }
            banco.executemany(
                "INSERT INTO post (author_id, title, body, created) VALUES (?, ?, ?, ?)",
                [
                    (autores[post["autor"]], post["titulo"], post["corpo"], post["criacao"])
                    for post in DADOS["publicacoes"]
                ],
            )


@pytest.fixture
def capturar(navegador):
    pasta = os.environ.get("FLASKR_ACEITACAO_CAPTURAS")

    def salvar(nome):
        if pasta:
            destino = Path(pasta) / f"{nome}.png"
            destino.parent.mkdir(parents=True, exist_ok=True)
            with destino.open("xb") as arquivo:
                arquivo.write(navegador.get_screenshot_as_png())

    return salvar


def titulo_pagina(espera, titulo):
    espera.until(
        lambda driver: driver.execute_script(
            "return document.querySelector(arguments[0])?.textContent.trim();",
            TITULO_PAGINA[1],
        ) == titulo,
        f"Título de página esperado: {titulo}",
    )


def enviar_credenciais(espera, conta):
    preencher(espera, "username", conta["nome"])
    preencher(espera, "password", conta["senha"])
    clicar(espera, BOTAO_FORMULARIO)


def iniciar_sessao(espera, conta, origem):
    enviar_credenciais(espera, conta)
    espera.until(condicao.url_to_be(f"{origem}/"))
    titulo_pagina(espera, "Posts")
    assert espera.until(condicao.visibility_of_element_located(MENU_USUARIO)).text == conta["nome"]


def conferir_post(espera, titulo, corpo):
    artigo = obter_artigo(espera, titulo)
    assert artigo.find_element(By.CSS_SELECTOR, ".body").text == corpo
    assert artigo.find_element(By.CSS_SELECTOR, ".about").text.startswith(
        f"by {CONTA_A['nome']} on "
    )
    return artigo


def titulos(navegador):
    return [artigo.find_element(By.CSS_SELECTOR, "header h1").text for artigo in navegador.find_elements(*ARTIGOS)]


def editar_post_a(espera):
    artigo = obter_artigo(espera, "Post A")
    espera.until(condicao.element_to_be_clickable(artigo.find_element(*EDITAR))).click()
    titulo_pagina(espera, 'Edit "Post A"')


def test_ac_01_publicar_como_novo_autor(navegador, servidor_selenium, espera, capturar):
    navegador.get(servidor_selenium)
    assert titulos(navegador) == []
    clicar(espera, (By.LINK_TEXT, "Register"))
    enviar_credenciais(espera, CONTA_A)
    espera.until(condicao.url_to_be(f"{servidor_selenium}/auth/login"))
    titulo_pagina(espera, "Log In")
    iniciar_sessao(espera, CONTA_A, servidor_selenium)
    clicar(espera, (By.LINK_TEXT, "New"))
    preencher(espera, "title", "Primeiro aviso QA")
    corpo = "Publicação fictícia para a atividade."
    preencher(espera, "body", corpo)
    clicar(espera, BOTAO_FORMULARIO)

    espera.until(condicao.url_to_be(f"{servidor_selenium}/"))
    titulo_pagina(espera, "Posts")
    conferir_post(espera, "Primeiro aviso QA", corpo)
    capturar("AC-01_autor")
    clicar(espera, LOGOUT)
    assert espera.until(condicao.visibility_of_element_located(LOGIN))
    conferir_post(espera, "Primeiro aviso QA", corpo)
    capturar("AC-01_visitante_apos_sair")
    print("AC-01 | Cadastro encaminhou ao login. O aviso com título, corpo e autoria apareceu após publicar e após sair.")


@pytest.mark.usefixtures("publicacoes_iniciais")
def test_ac_02_ler_o_aviso_mais_recente(navegador, servidor_selenium, espera, capturar):
    navegador.get(servidor_selenium)
    titulo_pagina(espera, "Posts")
    assert espera.until(condicao.visibility_of_element_located(LOGIN))
    assert titulos(navegador) == ["Post B", "Post A"]
    conferir_post(espera, "Post B", "Corpo B")
    conferir_post(espera, "Post A", "Corpo A")
    capturar("AC-02_ordem_como_visitante")
    print("AC-02 | Sem sessão, Post B apareceu antes de Post A. Os dois títulos, corpos e autorias estavam visíveis.")


@pytest.mark.usefixtures("publicacoes_iniciais")
def test_ac_03_corrigir_como_autor(navegador, servidor_selenium, espera, capturar):
    navegador.get(servidor_selenium)
    clicar(espera, LOGIN)
    iniciar_sessao(espera, CONTA_A, servidor_selenium)
    editar_post_a(espera)
    titulo, corpo = "Post A atualizado", "Corpo atualizado pelo autor."
    preencher(espera, "title", titulo)
    preencher(espera, "body", corpo)
    clicar(espera, (By.CSS_SELECTOR, "input[value='Save']"))

    espera.until(condicao.url_to_be(f"{servidor_selenium}/"))
    titulo_pagina(espera, "Posts")
    conferir_post(espera, titulo, corpo)
    conferir_post(espera, "Post B", "Corpo B")
    assert titulos(navegador) == ["Post B", titulo]
    capturar("AC-03_publicacao_corrigida_pelo_autor")
    clicar(espera, LOGOUT)
    clicar(espera, LOGIN)
    iniciar_sessao(espera, CONTA_B, servidor_selenium)
    assert not conferir_post(espera, titulo, corpo).find_elements(*EDITAR)
    conferir_post(espera, "Post B", "Corpo B")
    capturar("AC-03_publicacao_vista_pela_segunda_conta")
    print("AC-03 | Edição substituiu título e corpo do Post A, conservou a autoria e o Post B. Conta B leu a revisão com a ação Edit ausente.")


@pytest.mark.usefixtures("publicacoes_iniciais")
def test_ac_04_cancelar_e_confirmar_exclusao(navegador, servidor_selenium, espera, capturar):
    navegador.get(servidor_selenium)
    clicar(espera, LOGIN)
    iniciar_sessao(espera, CONTA_A, servidor_selenium)
    editar_post_a(espera)
    clicar(espera, EXCLUIR)
    espera.until(condicao.alert_is_present()).dismiss()
    titulo_pagina(espera, 'Edit "Post A"')
    clicar(espera, LINK_INICIO)
    titulo_pagina(espera, "Posts")
    conferir_post(espera, "Post A", "Corpo A")
    conferir_post(espera, "Post B", "Corpo B")
    assert titulos(navegador) == ["Post B", "Post A"]
    capturar("AC-04_depois_de_cancelar")

    editar_post_a(espera)
    clicar(espera, EXCLUIR)
    espera.until(condicao.alert_is_present()).accept()
    espera.until(condicao.url_to_be(f"{servidor_selenium}/"))
    titulo_pagina(espera, "Posts")
    assert titulos(navegador) == ["Post B"]
    conferir_post(espera, "Post B", "Corpo B")
    capturar("AC-04_depois_de_confirmar")
    print("AC-04 | Cancelar preservou os dois avisos. Confirmar retirou o Post A e conservou o Post B, seu corpo e autoria.")
