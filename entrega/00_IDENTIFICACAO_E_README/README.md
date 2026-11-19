# Projeto Integrado P2 · Flaskr

UNISAGRADO · Ciência da Computação · Testes e Qualidade de Software · 2026

Turma B · Grupo 1 · Prof. Dr. Elvio Gilberto da Silva

## Integrantes

- Henrique Motta Canho
- Yago da Silva Leme
- Guilherme Tamelini Bertozzo
- Victor Hugo de Deus Machado

## Sistema e versão

Flaskr 1.0.0, exemplo `examples/tutorial` do Flask 3.1.3. Linha de base upstream `22d924701a6ae2e4cd01e9a15bbaf3946094af65`, sob licença BSD de três cláusulas. A evolução do grupo é registrada nos commits da Etapa 9.

[Release oficial do Flask 3.1.3](https://github.com/pallets/flask/releases/tag/3.1.3) · [Licença](../../LICENSE-FLASK.txt)

## Repositório

[Código e histórico do Grupo 1 no GitHub](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr)

## Tecnologias

Python, Flask, Jinja e SQLite no sistema. pytest e pytest-cov nos testes Python, Postman e Newman nas rotas HTML, Selenium no navegador, GitHub Actions no pipeline e Sonar na análise estática.

## Pré-requisitos

- Git e Python 3.12 para reproduzir o ambiente automatizado. A matriz desta entrega usa a versão instalada em cada execução, registrada nos respectivos logs.
- Node.js, npm e acesso ao registro npm para Newman. Chrome instalado e ChromeDriver compatível para os testes de interface. Selenium Manager pode resolver o driver.
- Ambiente manual registrado em [Etapa 4B](../../evidencias/etapa4b/2026-11-19_indice_execucoes_atualizado.md). Chrome e Safari foram usados.

## Instalação

Na raiz do checkout:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-test.txt
```

## Configuração

A porta nos exemplos é 5050 e pode ser alterada. Use o servidor local com dados fictícios. Os testes automatizados criam ambientes temporários próprios.

## Banco e dados

Inicialize um banco descartável. Os perfis são `vazia`, `contas` e `publicacoes`. Use `contas` para testar as credenciais de exemplo ou `publicacoes` para iniciar com posts.

```bash
export FLASKR_QA_DIR="$(python tools/resetar_banco_etapa4.py --massa publicacoes)"
```

## Execução

```bash
python -m flask --app tools.resetar_banco_etapa4:criar_app run --host 127.0.0.1 --port 5050
```

Abra `http://127.0.0.1:5050`.

## Execução dos testes

```bash
python -m pytest flaskr-app/tests testes_grupo/unitarios --cov --cov-config=.coveragerc
python tools/executar_postman.py --relatorio-json artefatos-ci/postman.json --junitxml artefatos-ci/postman.xml
python -m pytest testes_grupo/sistema_selenium --junitxml=artefatos-ci/selenium.xml
```

Os testes em `flaskr-app/tests/` são do Flask. As suítes do grupo ficam em `testes_grupo/`. Para execução manual, use o [guia de execução](../../entrega/05_EXECUCAO_MANUAL/Guia_de_Execucao_Manual.md).

## Pipeline

O workflow executa as três suítes e publica cobertura, JUnit e capturas quando disponíveis. Ao rodar localmente, use `bash tools/executar_ci.sh` na raiz.

[GitHub Actions do Grupo 1](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/actions) · [Falha controlada](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/actions/runs/44590229007) · [Execução aprovada](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/actions/runs/44590346309)

## Documentos

As pastas numeradas em [entrega](../../entrega) seguem a estrutura do manual. Os dados de execução ficam em [evidências](../../evidencias). Requisitos, casos e vínculos estão na [planilha de rastreabilidade](../../entrega/04_CASOS_E_RASTREABILIDADE/Requisitos_Casos_e_Rastreabilidade_Flaskr.xlsx).

## Credenciais fictícias

| Conta | Senha de teste |
| --- | --- |
| `qa_autor_a` | `Senha-QA-A-2026!` |
| `qa_autor_b` | `Senha-QA-B-2026!` |

## Problemas conhecidos e contato

A execução manual mais recente aprovou 28 casos. A primeira tentativa de CT-028 ficou bloqueada pela configuração de navegação por Tab do Safari. O reteste EX-029 passou após ajuste temporário, posteriormente restaurado. As duas tentativas estão no [registro da Etapa 4B](../../evidencias/etapa4b/2026-11-19_indice_execucoes_atualizado.md).

A aceitação aguarda um representante independente. A linha de base e a refatoração foram analisadas no SonarQube local e no SonarQube Cloud. A implementação da regra de título e a análise estão na [pasta 12](../../entrega/12_TDD_CICD_MELHORIA) e na [pasta 11](../../entrega/11_METRICAS_E_QUALIDADE).

[Contato do grupo no GitHub Issues](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/issues)
