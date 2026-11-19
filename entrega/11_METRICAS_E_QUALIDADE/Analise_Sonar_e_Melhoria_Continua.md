# Análise Sonar e melhoria contínua

Foram realizadas duas análises com o SonarQube Community Build 26.11.0.134175 em contêiner local. O Scanner para Python leu o código do Flaskr e o XML do pytest-cov. A linha de base corresponde ao código anterior à mudança de regra e a análise final ao commit de refatoração.

| Medida do Sonar | Linha de base `9db2f3c` | Final `d7c225c` |
| --- | ---: | ---: |
| Linhas de código reportadas | 428 | 428 |
| Cobertura importada | 100% | 100% |
| Linhas duplicadas | 0% | 0% |
| Bugs | 0 | 0 |
| Problemas de manutenibilidade | 0 | 0 |
| Ocorrências de segurança classificadas pelo analisador | 1 | 1 |
| Quality Gate | OK | OK |

A ocorrência é a regra Python S4502, sobre revisão da proteção CSRF. Trata-se de um achado de análise estática. O teste não tentou reproduzir exploração. O gate ficou OK no perfil usado e a ocorrência continua aberta para revisão. Ela está fora da alteração de título e deve ser tratada antes de qualquer exposição do tutorial além do ambiente local.

[Saída da linha de base](../../evidencias/etapa9/2026-11-19_sonar_base.txt) · [Medidas da linha de base](../../evidencias/etapa9/2026-11-19_sonar_base.json) · [Saída final](../../evidencias/etapa9/2026-11-19_sonar_final.txt) · [Medidas finais](../../evidencias/etapa9/2026-11-19_sonar_final.json)

## SonarQube Cloud

A linha de base e a refatoração foram analisadas na nuvem pelo GitHub Actions. O scanner usou o diretório `flaskr-app/flaskr` como base e importou o XML dos testes Python. As métricas abaixo comparam as duas revisões com o mesmo escopo no Cloud.

| Medida do SonarQube Cloud | Linha de base `eae6f81` | Refatoração `d7c225c` |
| --- | ---: | ---: |
| Quality Gate | OK | OK |
| Cobertura | 100% | 100% |
| Linhas a cobrir | 178 | 178 |
| Condições a cobrir | 42 | 40 |
| Linhas descobertas | 0 | 0 |
| Condições descobertas | 0 | 0 |
| Duplicação de linhas | 0% | 0% |
| Ocorrências na categoria Bugs | 1 | 1 |
| Ocorrências na categoria Vulnerabilidades | 1 | 1 |

A primeira execução da linha de base ampliou o escopo para o repositório inteiro e registrou 0% de cobertura porque o scanner não conseguiu associar os caminhos do XML aos arquivos. A correção delimitou o diretório analisado e ajustou os caminhos em uma cópia do XML. Os contadores gerados pelo pytest foram preservados.

[SonarQube Cloud do Flaskr](https://sonarcloud.io/project/overview?id=YagoL3m3_p2-tqs-2026-cc-grupo01-flaskr) · [Linha de base no GitHub Actions](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/actions/runs/44637775144) · [Refatoração no GitHub Actions](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/actions/runs/44638085612)

[Dados públicos da linha de base](../../evidencias/etapa10/2026-11-19_sonarcloud_linha_de_base.json) · [Dados públicos da refatoração](../../evidencias/etapa10/2026-11-19_sonarcloud_refatoracao.json) · [Histórico do escopo inicial](../../evidencias/etapa10/2026-11-19_sonarcloud_escopo_inicial.json)

### Reprodução da análise

O workflow utiliza as variáveis `SONAR_ORGANIZATION` e `SONAR_PROJECT_KEY` e o secret `SONAR_TOKEN` do GitHub Actions. Execute **Testes Flaskr** manualmente com a opção `linha-de-base` e aguarde o resultado antes de escolher `refatoracao`. Cada opção seleciona a revisão indicada na tabela tanto para os testes quanto para a análise.

## Ações priorizadas

| Prioridade | Ação e papel sugerido | Critério de verificação |
| --- | --- | --- |
| Alta | Revisar a proteção de formulários identificada pela análise estática. Automação e qualidade. | Revisão do código e nova análise. Registre o tratamento do achado sob o perfil definido pelo grupo. |
| Alta | Conduzir aceitação independente. Coordenação. | Registrar execução, observação e decisão nos quatro cenários. |
| Média | Ampliar a automação dos candidatos que hoje são parciais. Automação e qualidade. | Atualizar rastreabilidade e comprovar aprovação também no Actions. |
| Média | Reexecutar a análise do SonarQube Cloud após alterações relevantes. Automação e qualidade. | Guardar os dois resultados com revisão, data e identificação da análise. |
