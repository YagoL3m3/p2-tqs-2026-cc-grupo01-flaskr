# Ciclo de TDD e pipeline do Flaskr

A evolução exige conteúdo visível no título ao criar ou editar uma publicação. Um título composto apenas por espaços e tabulação mantém o formulário aberto, exibe a mensagem de título obrigatório e preserva o estado do banco. A validação usa `strip()` somente para decidir se há conteúdo.

| Fase | Commit | Resultado local | GitHub Actions |
| --- | --- | --- | --- |
| Linha de base | [eae6f81](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/commit/eae6f811c9ff3cdb8c2424a6be640a48a0c8fe60) | 32 testes Python na suíte de referência | [44590163560 · aprovado](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/actions/runs/44590163560) |
| RED | [7a63c30](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/commit/7a63c3046c6b963ccf42e1f707c77b28da84cfdb) | 2 casos novos falharam com HTTP 302 onde se esperava HTTP 200 | [44590229007 · falha controlada](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/actions/runs/44590229007) |
| GREEN | [1c5577c](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/commit/1c5577c3991a9ac1f84e726598b00cb5db26b61b) | 34 aprovações após a validação nas duas rotas | Execução local registrada |
| REFACTOR | [d7c225c](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/commit/d7c225cf16e504fdfb92c9235762bf6ba3f0dc19) | 34 aprovações após centralizar a validação. 178/178 linhas e 40/40 ramos | [44590346309 · aprovado](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/actions/runs/44590346309) |

A branch `etapa-9-demonstracao-red` aponta para o commit RED. No Actions ela terminou com 32 aprovações e duas falhas esperadas no pytest. Newman e Selenium passaram nessa mesma execução. No refactor, as três suítes terminaram com código zero. O workflow publicou relatórios também na execução com falha.

[Teste novo](../../testes_grupo/unitarios/test_tdd_titulo.py) · [Código da regra](../../flaskr-app/flaskr/blog.py) · [Configuração do Actions](../../.github/workflows/ci.yml) · [Relatórios baixados e registros](../../evidencias/etapa9)

Após instalar as dependências do README, reproduza a execução na raiz com `bash tools/executar_ci.sh`. Os relatórios saem em `artefatos-ci/`.
