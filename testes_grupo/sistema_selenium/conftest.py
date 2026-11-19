"""Servidor real, Chrome e captura diagnóstica dos testes de sistema."""

from datetime import datetime
import os
from pathlib import Path
from threading import Thread

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from werkzeug.serving import make_server


@pytest.fixture
def servidor_selenium(app_grupo):
    with make_server("127.0.0.1", 0, app_grupo) as servidor:
        tarefa = Thread(target=servidor.serve_forever, daemon=True)
        tarefa.start()
        try:
            yield f"http://127.0.0.1:{servidor.server_port}"
        finally:
            servidor.shutdown()
            tarefa.join()


@pytest.fixture
def navegador():
    opcoes = Options()
    opcoes.add_argument("--headless")
    opcoes.add_argument("--window-size=1440,900")
    if binario := os.environ.get("FLASKR_CHROME_BINARY"):
        opcoes.binary_location = binario

    with webdriver.Chrome(options=opcoes) as driver:
        driver.set_page_load_timeout(15)
        print(
            f"Chrome {driver.capabilities['browserVersion']} | "
            f"ChromeDriver {driver.capabilities['chrome']['chromedriverVersion']}",
            flush=True,
        )
        yield driver


@pytest.fixture
def espera(navegador):
    return WebDriverWait(navegador, 10)


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    relatorio = yield
    navegador = item.funcargs.get("navegador")
    if relatorio.failed and relatorio.when in ("setup", "call") and navegador is not None:
        pasta = Path(os.environ.get("FLASKR_SELENIUM_SCREENSHOTS", "artefatos/selenium/capturas"))
        instante = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        arquivo = pasta / f"{item.name}_{relatorio.when}_{instante}.png"
        try:
            pasta.mkdir(parents=True, exist_ok=True)
            arquivo.write_bytes(navegador.get_screenshot_as_png())
            relatorio.sections.append(("Captura do Selenium", str(arquivo)))
        except (OSError, WebDriverException) as erro:
            relatorio.sections.append(("Captura do Selenium", f"Falha ao salvar a captura: {erro}"))
    return relatorio
