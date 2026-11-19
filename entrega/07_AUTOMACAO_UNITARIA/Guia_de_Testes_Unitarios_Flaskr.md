# Etapa 5 · Automação unitária do Flaskr

Os oito testes do grupo chamam funções de autenticação e publicações em contextos Flask, sem servidor HTTP ou navegador. A fixture `app_grupo` cria um SQLite exclusivo por teste com o esquema do Flaskr e dados fictícios. A ordenação usa datas fixas e um dublê da renderização para observar os registros entregues ao template. Os 24 testes originais são de autoria do projeto Flask. [Fixture](../../testes_grupo/conftest.py) · [Testes do grupo](../../testes_grupo/unitarios) · [Testes originais](../../flaskr-app/tests)

## Rastreabilidade

Cada vínculo com um CT representa a verificação da regra indicada na última coluna. A execução integral do caso de interface permanece registrada no catálogo manual. [Catálogo de requisitos e casos](../04_CASOS_E_RASTREABILIDADE/Requisitos_Casos_e_Rastreabilidade_Flaskr.xlsx)

| Automação | Caso e requisito | Função | Verificação |
| --- | --- | --- | --- |
| AUT-U-01 | CT-005 / RF-01 e CT-026 / RNF-01 | `auth.register()` | Aceita nome de um caractere, redireciona a Log In e armazena um único registro com hash válido e diferente da senha informada. |
| AUT-U-02 | CT-004 / RF-01 | `auth.register()` | Emite o aviso de duplicidade e preserva o único registro e sua senha original. |
| AUT-U-03 | CT-006 / RF-02 | `auth.login()` | O login válido direciona à página inicial e deixa na sessão apenas a identidade autenticada. |
| AUT-U-04 | CT-009 / RF-03 | `auth.logout()` | O logout limpa todos os dados da sessão e direciona à página inicial. |
| AUT-U-05 | CT-011 / RF-04 | `blog.index()` | Entrega as publicações ao template da mais recente à mais antiga, com datas e IDs em ordens distintas. |
| AUT-U-06 | CT-014 e CT-016 / RF-05 | `blog.create()` | Salva a publicação com corpo vazio e o ID da conta ativa como autor. |
| AUT-U-07 | CT-019 / RF-06 | `blog.update()` | Ao receber título vazio, emite a mensagem do servidor e preserva título, corpo e autoria. |
| AUT-U-08 | CT-023 / RF-07 | `blog.delete()` | Remove a publicação selecionada e conserva ID, título, corpo e autoria da publicação de controle. |

## Execução

Execute a partir da raiz do repositório. O ambiente registrado usou macOS 26.4 (25E246), Apple Silicon, Python 3.12.13, SQLite 3.53.4, Flask 3.1.3, pytest 9.2.0 e pytest-cov 7.1.0. [Ambiente](../../evidencias/etapa5/2026-11-19_ambiente.txt) · [Instalação em ambiente limpo](../../evidencias/etapa5/2026-11-19_instalacao_requirements.txt)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-test.txt
saida=$(mktemp -d)
export COVERAGE_FILE="$saida/.coverage"

python -m pytest -q -ra -c flaskr-app/pyproject.toml --rootdir=. \
  --cov --cov-config=.coveragerc --cov-report=term-missing \
  --cov-report="xml:$saida/coverage_original.xml" --junitxml="$saida/original.xml" \
  flaskr-app/tests

python -m pytest -q -ra -c flaskr-app/pyproject.toml --rootdir=. \
  --cov --cov-config=.coveragerc --cov-report=term-missing \
  --cov-report="xml:$saida/coverage_grupo.xml" --junitxml="$saida/grupo.xml" \
  testes_grupo/unitarios

python -m pytest -q -ra -c flaskr-app/pyproject.toml --rootdir=. \
  --cov --cov-config=.coveragerc --cov-report=term-missing \
  --cov-report="xml:$saida/coverage.xml" --junitxml="$saida/conjunto.xml" \
  flaskr-app/tests testes_grupo/unitarios

printf 'Relatórios em %s\n' "$saida"
```

## Resultados de 19/11/2026

| Suíte | Aprovados | Falhas, erros e ignorados | Linhas cobertas | Ramos cobertos |
| --- | ---: | --- | ---: | ---: |
| Originais do Flask | 24/24 | 0, 0 e 0 | 178/178 (100%) | 42/42 (100%) |
| Unitários do grupo | 8/8 | 0, 0 e 0 | 154/178 (86,52%) | 22/42 (52,38%) |
| Originais e grupo | 32/32 | 0, 0 e 0 | 178/178 (100%) | 42/42 (100%) |

- Originais · [Saída do pytest](../../evidencias/etapa5/2026-11-19_pytest_original.txt) · [JUnit](../../evidencias/etapa5/2026-11-19_pytest_original.xml) · [Cobertura XML](../../evidencias/etapa5/coverage_original.xml)
- Grupo · [Saída do pytest](../../evidencias/etapa5/2026-11-19_pytest_grupo.txt) · [JUnit](../../evidencias/etapa5/2026-11-19_pytest_grupo.xml) · [Cobertura XML](../../evidencias/etapa5/coverage_grupo.xml)
- Conjunto · [Saída do pytest](../../evidencias/etapa5/2026-11-19_pytest_conjunto.txt) · [JUnit](../../evidencias/etapa5/2026-11-19_pytest_conjunto.xml) · [Cobertura XML](../../evidencias/etapa5/coverage.xml)

A cobertura mede os quatro arquivos Python de `flaskr-app/flaskr`. A suíte original já percorria todas as linhas e ramos medidos. A contribuição do grupo foi acrescentar verificações de resultado, como conservação da credencial anterior, limpeza total da sessão e preservação da publicação de controle. [Resumo em JSON](../../evidencias/etapa5/2026-11-19_resumo.json) · [Verificação dos relatórios e da integridade do Flaskr](../../evidencias/etapa5/2026-11-19_verificacao.txt)

Na primeira tentativa, dois testes passaram o ID como argumento posicional a funções decoradas que recebem `**kwargs`. Os testes passaram a chamar essas funções com `id=21` e foram executados de novo. [Saída da tentativa inicial](../../evidencias/etapa5/2026-11-19_pytest_grupo_tentativa_inicial.txt)
