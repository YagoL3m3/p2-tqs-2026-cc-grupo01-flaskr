# Reteste e regressão do Flaskr

Projeto Integrado P2 · Turma B, Grupo 1 · Etapa 4B

Use este modelo quando uma correção estiver disponível para um defeito confirmado. A execução que detectou o defeito deve permanecer no [registro de execução](../05_EXECUCAO_MANUAL/Registro_de_Execucao_Manual_Flaskr.xlsx).

## Reteste da correção

1. Localize o defeito no GitHub e confirme a versão em que a correção será verificada.
2. Prepare a massa e a sessão descritas no caso que detectou o problema. Siga o [guia de execução](../05_EXECUCAO_MANUAL/Guia_de_Execucao_Manual.md).
3. Repita o caso na revisão corrigida. Compare o que aconteceu com o resultado esperado e registre uma nova execução `EX-XXX`.
4. Use **Aprovado**, **Reprovado**, **Bloqueado** ou **Não executado**. Registre o motivo de um bloqueio. Se a falha persistir, o grupo confirma a reprodução e atualiza a issue para **Reaberto**.

| Defeito e issue | Requisito | Caso | Execução original | Nova execução | Data e revisão corrigida | Executor e ambiente |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

| Massa e pré-condições | Resultado esperado | Resultado obtido | Situação | Evidência | Decisão do grupo |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Regressão do fluxo afetado

Abra a aba **Rastreabilidade** do [catálogo da Etapa 3](../04_CASOS_E_RASTREABILIDADE/Requisitos_Casos_e_Rastreabilidade_Flaskr.xlsx). Parta do requisito e do risco do defeito. Selecione casos que exercitam a mesma regra ou um fluxo diretamente afetado pela mudança.

| Área afetada pela correção | Casos do catálogo para avaliar |
| --- | --- |
| Cadastro e autenticação | CT-001 a CT-009. Inclua CT-026 se a mudança afetar a gravação ou a verificação da senha. |
| Listagem ou visibilidade de ações | CT-010 a CT-013. Inclua CT-020 se a mudança também afetar a autorização do editor. |
| Criação, edição ou exclusão de posts | CT-014 a CT-025. Inclua CT-027 se a mudança afetar a persistência. |
| Navegação por teclado | CT-028 quando a alteração afetar campos, botões ou ordem de foco dos formulários. |

| Caso e requisito | Risco e motivo da seleção | Nova execução | Data, revisão e executor | Resultado obtido e situação | Evidência | Defeito vinculado |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Acrescente as novas execuções ao registro com IDs únicos. Para distinguir capturas do mesmo caso no mesmo dia, use o ID da execução no fim do nome, no formato `CT-XXX_AAAA-MM-DD_EX-XXX.png`. Atualize a matriz com as referências da execução, do defeito e da evidência. Na issue, preencha **Reteste e conclusão** conforme o [modelo de defeito](../../.github/ISSUE_TEMPLATE/defeito.md).

[PENDENTE-HUMANO: fornecer as execuções manuais e as evidências. Quando houver correção, validar o reteste e registrar a decisão sobre a issue | Grupo 1]
