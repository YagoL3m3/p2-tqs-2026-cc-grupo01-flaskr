# Indicadores da rodada de referência

| Indicador | Base de cálculo | Resultado |
| --- | --- | --- |
| Percentual de execução | 28 casos com resultado conclusivo / 28 planejados | 100% |
| Taxa de aprovação | 28 aprovados / 28 executados | 100% |
| Taxa de reprovação | 0 reprovados / 28 executados | 0% |
| Cobertura de requisitos | 10 requisitos com caso executado / 10 no escopo | 100% |
| Taxa de automação | 9 casos automatizados integralmente / 23 candidatos | 39,1% |
| Defeitos por severidade | Contagem por severidade | 0 em cada categoria |
| Defeitos por status | Contagem por situação | 0 em cada estado |
| Taxa de reabertura | 0 reabertos / 0 retestados | Não aplicável |

O resultado mais recente de cada caso foi usado na leitura manual. O arquivo preserva 29 registros, incluindo a tentativa bloqueada de CT-028 e o reteste EX-029 aprovado. A cobertura de requisitos mede se pelo menos um caso vinculado teve execução conclusiva. A seleção de casos e o ambiente local delimitam o que esses resultados sustentam.

A automação considera os critérios verificáveis do catálogo. Os cenários HTTP contam quando verificam os resultados esperados do caso, incluindo persistência ou estado de sessão quando exigidos. Casos com interação visual obrigatória contam quando cobertos na interface. Cinco candidatos têm cobertura parcial e nove seguem sem automação mapeada. CT-017 está automatizado no Selenium e consta fora da seleção original de 23 candidatos. Isso preserva o denominador do planejamento.

A cobertura de código da suíte Python original mais os testes do grupo foi de 178/178 linhas e 42/42 ramos na linha de base. Esse percentual mede execução de instruções e caminhos do código Python, com o escopo declarado em `.coveragerc`.

[Planilha de indicadores](Metricas_do_Flaskr.xlsx) · [Dados apurados](../../evidencias/etapa8/2026-11-19_dados_metricas.json) · [Consulta a Issues](../../evidencias/etapa8/2026-11-19_github_issues.txt) · [Cobertura da linha de base](../../evidencias/etapa5/coverage.xml)
