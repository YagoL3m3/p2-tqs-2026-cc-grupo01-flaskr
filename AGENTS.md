# AGENTS.md — Projeto Integrado P2 (Testes e Qualidade de Software)

## 1. Contexto do projeto

- Instituição: UNISAGRADO — Curso de Ciência da Computação
- Disciplina: Testes e Qualidade de Software — Prof. Dr. Elvio Gilberto da Silva
- Projeto: Projeto Integrado P2 (2026). Entrega final na data oficial da P2, via Google Drive.
- Turma: B | Grupo: 1 (quarteto, autorizado por escrito pelo professor)
- Integrantes:
  1. Yago da Silva Leme
  2. Henrique Motta Canho
  3. Guilherme Tamelini Bertozzo
  4. Victor Hugo de Deus Machado
- Sistema testado: **Flaskr** (exemplo `examples/tutorial` do repositório `pallets/flask`), versão Flaskr 1.0.0, tag 3.1.3, commit `22d9247` (confirmado na [release oficial](https://github.com/pallets/flask/releases/tag/3.1.3) em 19/11/2026). Licença BSD de 3 cláusulas: preservar os avisos de licença.
- Repositório do grupo: `https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr`
- Ambiente de testes: `MacOS, python 3.13.15 e Safari `. Nesta preparação, `sw_vers` informou macOS 27.2 (26B123) e `python3 --version` informou Python 3.16.0a1.
- Nome da pasta de entrega no Drive: `P2_TQS_2026_CC_GRUPO01_FLASKR`

### Stack aprovada pelo professor
Python, Flask, Jinja, SQLite, **pytest** (unitário e integração), **Selenium para Python** (sistema/interface), **Postman nas rotas HTML do Flaskr** (integração), **GitHub Issues** (defeitos), **GitHub Actions** (CI/CD), **SonarCloud + pytest-cov** (qualidade), planilha **XLSX** (casos, execuções, rastreabilidade e métricas), **DOCX + PDF** (relatório), **PPTX + PDF** (apresentação).

## 2. Regras inegociáveis

1. **Nunca invente resultados.** Não fabrique execuções, defeitos, métricas, capturas de tela, logs, hashes de commit, saídas de pipeline, resultados do Sonar, tempos de resposta ou decisões de aceitação. Resultado de teste só entra em documento se vier de um comando que você executou (salvo em `evidencias/`) ou se um integrante colou. O manual trata dado fabricado como irregularidade acadêmica.
2. **Tudo que depende de pessoa vira pendência explícita.** Use o marcador `[PENDENTE-HUMANO: o que fazer | responsável]` em vez de preencher. São de responsabilidade humana: criar o repositório e convidar colaboradores, tokens e segredos (Sonar, GitHub), **execução dos casos manuais**, decisão de que algo é defeito, abertura das issues, **execução dos cenários de aceitação por pessoa que não escreveu os testes**, prints feitos na interface, Diário de Participação, assinaturas e envio ao Drive.
3. **Leia o código antes de afirmar comportamento.** Não suponha como o Flaskr se comporta. Abra `auth.py`, `blog.py`, `db.py`, `schema.sql`, templates e testes originais e cite arquivo e função. Se algo for hipótese, marque `[CONFIRMAR]`.
4. **Não force defeitos.** Se o sistema não falhar, registre isso. Você pode sugerir pontos de atenção, nunca "defeitos prováveis" como se estivessem registrados.
5. **Não altere o código do Flaskr** fora da etapa de TDD (Etapa 9). Fora dela, o sistema é objeto de teste. Os testes originais em `flaskr-app/tests/` permanecem intactos e identificados como "autoria do projeto Flask". Os testes do grupo ficam em `testes_grupo/`.
6. **Qualidade de automação:** todo teste tem asserts reais, nome descritivo, uma intenção principal, rastreio a requisito/caso, dados controlados, banco temporário e instruções de execução. Selenium usa esperas explícitas (`WebDriverWait`), nunca `sleep` fixo, e salva captura de tela em caso de falha. Teste que só navega ou clica sem validar é proibido.
7. **Somente dados fictícios.** Nenhuma senha, e-mail ou documento real. Credenciais de exemplo ficam no README como fictícias.
8. **Sem testes invasivos ou destrutivos** (carga pesada, invasão, exploração). Segurança básica = validações, mensagens e controle de acesso.
9. **Verifique, não confie.** A tag `3.1.3` e o hash `22d9247` vieram de uma ficha preenchida pelo grupo. Confira no repositório oficial. Se não baterem, pare e informe.
10. **Idioma:** documentos, commits, issues e comentários explicativos em português do Brasil.
11. **Uso de IA:** o projeto é assistido por IA e isso será declarado conforme o item 15 do manual e a orientação do professor. Explique o porquê das decisões em linguagem simples, porque cada integrante precisa saber explicar tudo na apresentação.
12. **Sem links ou arquivos fantasmas.** Só referencie arquivos e URLs que existam.

## 3. Mínimos obrigatórios do manual

| Item | Mínimo |
|---|---|
| Requisitos no escopo | 8 (≥6 funcionais e ≥2 não funcionais), todos testáveis |
| Riscos documentados | 8, priorizados |
| Casos manuais / execuções manuais | 24 / 24 |
| Testes unitários automatizados | 6 |
| Testes de integração (Postman nas rotas HTML) | 5, com fluxo positivo e negativo nas operações críticas |
| Testes de sistema/interface (Selenium) | 4 |
| Cenários de aceitação | 4 |
| Testes não funcionais | 6 em ≥3 categorias |
| Métricas | 8 (as da seção 9.13 do manual) |
| Evolução por TDD | 1, com Red, Green e Refactor em commits separados |
| Pipeline CI/CD | 1 com execução aprovada e uma execução com falha controlada seguida de correção |
| Análise Sonar | 2 execuções (linha de base e final) |

Não crie casos repetidos só para bater quantidade.

## 4. Convenções de identificadores

`RF-01`, `RNF-01` (requisitos) · `R-01` (riscos) · `CT-001` (casos) · `EX-001` (execuções) · `BUG-001` (defeitos; use o mesmo ID no título da issue) · `AUT-U-01` (unitário) · `AUT-I-01` (integração) · `AUT-S-01` (sistema) · `AC-01` (aceitação) · `NF-01` (não funcional).

Cada requisito deve se ligar a risco, caso, execução, evidência e, se houver, defeito. Cada teste automatizado indica o caso ou requisito que representa.

## 5. Estrutura do repositório

```
/
├── AGENTS.md
├── README.md                    # instruções completas (ver Etapa 5)
├── LICENSE-FLASK.txt            # licença BSD do Flask preservada
├── flaskr-app/                  # cópia de examples/tutorial (versão testada)
│   └── tests/                   # testes ORIGINAIS do projeto Flask (não editar)
├── testes_grupo/
│   ├── conftest.py
│   ├── unitarios/               # AUT-U-xx
│   ├── integracao_postman/      # coleção e ambiente em JSON
│   └── sistema_selenium/        # AUT-S-xx
├── evidencias/                  # saídas reais de comandos, por etapa
├── tools/                       # scripts que geram XLSX/DOCX/PPTX
├── entrega/                     # espelho da estrutura 00 a 16 do Drive
│   ├── 00_IDENTIFICACAO_E_README
│   ├── 01_SISTEMA_ALVO
│   ├── 02_REQUISITOS_ESCOPO_RISCOS
│   ├── 03_PLANO_DE_TESTES
│   ├── 04_CASOS_E_RASTREABILIDADE
│   ├── 05_EXECUCAO_MANUAL
│   ├── 06_DEFEITOS
│   ├── 07_AUTOMACAO_UNITARIA
│   ├── 08_INTEGRACAO_API
│   ├── 09_SISTEMA_INTERFACE
│   ├── 10_ACEITACAO_NAO_FUNCIONAIS
│   ├── 11_METRICAS_E_QUALIDADE
│   ├── 12_TDD_CICD_MELHORIA
│   ├── 13_RELATORIO_FINAL
│   ├── 14_APRESENTACAO_E_VIDEO_CONTINGENCIA
│   ├── 15_DIARIO_DE_PARTICIPACAO
│   └── 16_BACKUP_ENTREGA
├── .github/
│   ├── workflows/ci.yml
│   └── ISSUE_TEMPLATE/defeito.md
├── requirements-test.txt
└── sonar-project.properties
```

## 6. Como evidências devem ser geradas

- Salve a saída real de cada comando em `evidencias/<etapa>/<AAAA-MM-DD>_<descricao>.txt`, usando `tee`, com a primeira linha contendo o comando, a data/hora e as versões (`python --version`, `pip freeze` quando relevante).
- Relatórios de teste: `pytest --junitxml=...` e cobertura em `coverage.xml`.
- Capturas do Selenium são evidências reais geradas pelo teste. Prints feitos à mão são dos integrantes.
- Nunca edite uma evidência salva. Se repetir um teste, gere um novo arquivo.
- Todo número em documento deve poder ser rastreado até um arquivo em `evidencias/` ou a uma planilha de dados reais.
- Registre versões utilizadas (SO, Python, navegador, driver, dependências) no README.
- Mantenha histórico: não sobrescreva versões parciais sem registrar data e versão.

## 7. Regras de Git

- Uma branch por etapa: `etapa-N-descricao-curta`. Abra Pull Request para `main`. Quem aprova é um integrante diferente do responsável da etapa.
- Faça commits pequenos, com mensagem em português e prefixo da etapa. Exemplos: `[E5] Adiciona testes unitários de autenticação`, `[E9-RED] Teste falhando para limite de título`.
- Os commits de Red, Green e Refactor são **separados, em ordem**, e o teste do Red é escrito **antes** da implementação.
- Não faça `git push --force`, não reescreva histórico, não apague branches.
- Antes de cada commit, mostre o resumo das mudanças e pergunte quem é o responsável humano. O histórico precisa refletir a participação real dos 4 integrantes.

## 8. Divisão de responsabilidades

| Papel (manual, item 4.2) | Integrante |
|---|---|
| Coordenação e planejamento | `[PENDENTE-HUMANO: indicar o integrante responsável por este papel | grupo]` |
| Análise e execução manual | `[PENDENTE-HUMANO: indicar o integrante responsável por este papel | grupo]` |
| Automação e qualidade | `[PENDENTE-HUMANO: indicar o integrante responsável por este papel | grupo]` |
| Documentação, relatório e apresentação | `[PENDENTE-HUMANO: indicar o integrante responsável por este papel | grupo]` |

Todos devem compreender o projeto completo e responder perguntas na apresentação.

## 9. Forma de trabalhar em cada etapa

1. Leia este arquivo e o prompt da etapa. Liste o plano antes de alterar arquivos.
2. Execute apenas o que a etapa pede.
3. Salve evidências conforme a seção 6.
4. Ao terminar, entregue um resumo com: o que foi feito, arquivos criados ou alterados, comandos que rodaram e o resultado real, `[PENDENTE-HUMANO]` abertos, dúvidas e riscos.
5. **Pare e aguarde confirmação humana** antes de iniciar a próxima etapa.

Se um comando falhar, mostre o erro real e diagnostique. Não finja que passou.