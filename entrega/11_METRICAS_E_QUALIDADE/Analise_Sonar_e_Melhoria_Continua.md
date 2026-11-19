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

[PENDENTE-HUMANO: importar o repositório no projeto SonarQube Cloud do grupo, configurar acesso e validar as duas análises na conta oficial | responsável pelo repositório e pela qualidade]

A análise local documenta a linha de base e a versão final. O job de nuvem do workflow fica disponível para execução manual após a configuração de `SONAR_ORGANIZATION` e `SONAR_PROJECT_KEY` nas variáveis do repositório e `SONAR_TOKEN` nos secrets do Actions. O proprietário deve definir o processo que aceite as duas revisões de referência no plano contratado. Se o dispatch pelo portal ainda não estiver disponível, a configuração do workflow precisa estar primeiro na branch padrão.

## Ações priorizadas

| Prioridade | Ação e papel sugerido | Critério de verificação |
| --- | --- | --- |
| Alta | Revisar a proteção de formulários identificada pela análise estática. Automação e qualidade. | Revisão do código e nova análise. Registre o tratamento do achado sob o perfil definido pelo grupo. |
| Alta | Conduzir aceitação independente. Coordenação. | Registrar execução, observação e decisão nos quatro cenários. |
| Média | Ampliar a automação dos candidatos que hoje são parciais. Automação e qualidade. | Atualizar rastreabilidade e comprovar aprovação também no Actions. |
| Média | Publicar a análise no projeto SonarQube Cloud do grupo. Responsável do repositório. | Guardar os dois resultados com revisão, data e identificação da análise. |
