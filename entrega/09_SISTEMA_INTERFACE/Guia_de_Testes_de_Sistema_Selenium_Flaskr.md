# Etapa 6 — Sistema e interface com Selenium

Os testes percorrem as telas do Flaskr em Chrome headless. Cada caso recebe um servidor HTTP em `127.0.0.1` com porta própria, um banco SQLite temporário e uma sessão nova do navegador. Os dados prévios são contas ou posts fictícios. O fluxo em avaliação usa a interface, com seletores de IDs e links, esperas explícitas do Selenium e asserções sobre o estado da página.

- [Fluxos e asserções](../../testes_grupo/sistema_selenium/test_fluxos.py)
- [Servidor, navegador e captura de falha](../../testes_grupo/sistema_selenium/conftest.py)

## Como reproduzir

Na raiz do repositório, com Python em um ambiente virtual ativo e Google Chrome disponível, execute:

```bash
python -m pip install -r requirements-test.txt -e ./flaskr-app
FLASKR_SELENIUM_SCREENSHOTS=artefatos/selenium/capturas \
  python -m pytest -v -s testes_grupo/sistema_selenium \
    --junitxml=artefatos/selenium/selenium.xml
```

O Selenium Manager localiza o ChromeDriver compatível e pode precisar de acesso à rede na primeira execução. Para indicar um driver instalado, use `SE_CHROMEDRIVER`. Para escolher outro binário do Chrome, use `FLASKR_CHROME_BINARY`. O pytest salva o PNG em `FLASKR_SELENIUM_SCREENSHOTS` quando falha um cenário com navegador disponível. O diretório padrão é `artefatos/selenium/capturas`.

## Rastreabilidade

| Automação | Catálogo | Requisito | Resultado observado na interface |
|---|---|---|---|
| AUT-S-01 | CT-001 | RF-01 | Cadastro leva a Log In e a nova conta aparece autenticada em Posts. |
| AUT-S-02 | CT-008 | RF-02 | Senha incorreta mantém o formulário de login com a mensagem e o menu anônimo. |
| AUT-S-03 | CT-014 | RF-05 | Publicação aparece com título, corpo e a autoria da sessão. |
| AUT-S-04 | CT-017 | RF-05 | O campo obrigatório recebe foco em estado inválido. A listagem fica vazia após tentar salvar sem título. |
| AUT-S-05 | CT-018 | RF-06 | O editor grava título e corpo revisados e o outro artigo continua presente. |
| AUT-S-06 | CT-022 | RF-07 | Cancelar mantém o editor aberto e preserva os dois posts. |
| AUT-S-07 | CT-023 | RF-07 | Confirmar elimina o alvo e preserva título, corpo e autoria do post de controle. |

## Resultado registrado em 19/11/2026

O pytest aprovou **7 de 7 casos** em **86,37 s**. A rodada usou macOS 26.4 (25E246) em arm64, Python 3.12.13, pytest 9.2.0, Selenium 4.53.0, Chrome 157.0.8103.79 e ChromeDriver 157.0.8103.78. Todos os casos passaram, por isso nenhum PNG de falha foi gerado.

- [Saída do pytest com as versões do navegador e do driver](../../evidencias/etapa6/2026-11-19_selenium.txt)
- [Relatório JUnit XML](../../evidencias/etapa6/2026-11-19_selenium.xml)
