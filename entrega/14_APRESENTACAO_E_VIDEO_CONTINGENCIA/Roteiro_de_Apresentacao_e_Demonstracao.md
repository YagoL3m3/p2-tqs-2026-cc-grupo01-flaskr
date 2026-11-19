# Roteiro de apresentação e demonstração do Flaskr

Duração planejada de 13 min 15 s mais até 5 min de perguntas. A divisão é uma proposta para o ensaio do grupo.

| Tempo | Integrante | Slides | Demonstração |
| --- | --- | --- | --- |
| 0:00–3:05 | Victor Hugo de Deus Machado | 1–3 | Apresentar o Flaskr, delimitar o escopo e mostrar o vínculo de um risco à matriz. |
| 3:05–6:40 | Henrique Motta Canho | 4–5 | Abrir CT-014 e EX-014. Demonstrar pytest e Newman ou abrir os logs correspondentes. |
| 6:40–9:35 | Guilherme Tamelini Bertozzo | 6–7 | Mostrar a ficha de aceitação, interpretar os p95 e calcular a taxa de automação. |
| 9:35–13:15 | Yago da Silva Leme | 8–10 | Mostrar Red, Green e Refactor, comparar os resultados do Actions e explicar o achado Sonar. |

## Preparação da demonstração

Abra o repositório na branch final e instale as dependências indicadas no README. Deixe os links e a planilha preparados. Para contingência, o MP4 usa capturas da interface e saídas reais com narração sintética.

1. Abra a planilha de rastreabilidade no RF-05. Leia a linha do CT-014 e a captura EX-014. Destaque o título, o texto e a autoria na listagem.
2. Rode `python -m pytest flaskr-app/tests testes_grupo/unitarios -q`. Mostre a contagem e o teste parametrizado do TDD.
3. Rode `python tools/executar_postman.py --relatorio-json artefatos-ci/postman.json --junitxml artefatos-ci/postman.xml`. Abra a pasta AUT-I-02 da coleção e explique a validação das credenciais após o cadastro duplicado.
4. Compare os checks [RED](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/actions/runs/44590229007) e [refatoração](https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr/actions/runs/44590346309). Mostre os relatórios de cobertura e JUnit.
5. Use o PDF e o MP4 locais se a conexão falhar. Os dados da demonstração são fictícios.

## Perguntas para o ensaio

1. **Por que o Flaskr foi escolhido?** O sistema é pequeno e demonstrável, com regras suficientes de autenticação, autoria e persistência.
2. **Qual versão foi avaliada?** Flaskr 1.0.0 no exemplo de Flask 3.1.3, upstream `22d9247`, e a revisão do grupo que inclui a evolução de título.
3. **Qual risco tem relação com a autoria?** R-01. Dois usuários fictícios permitem verificar as restrições em edição e exclusão.
4. **Por que há 29 registros para 28 casos?** CT-028 teve uma tentativa bloqueada e foi aprovado no reteste EX-029. O histórico guarda os dois eventos.
5. **O bloqueio de CT-028 foi defeito?** A navegação dependia da opção de Tab do Safari. A execução passou após o preparo do navegador, e a preferência foi restaurada.
6. **O que o pytest verificou?** Funções isoladas com SQLite temporário e, na evolução de título, o comportamento das rotas com o cliente de testes do Flask.
7. **Por que usar Postman em uma aplicação HTML?** As rotas têm contratos HTTP. O Newman verifica respostas, redirecionamentos, sessão, conteúdo e persistência.
8. **Qual cenário exige navegador?** CT-022 verifica a ação de cancelar no diálogo de exclusão e a preservação do post.
9. **Por que testes de aceitação seguem pendentes?** O roteiro aguarda observação e decisão de um representante independente.
10. **Como foi obtido o p95?** Aquecimentos ficam fora da série. Ordenam-se os tempos e toma-se a posição de índice arredondado para cima de 0,95 × n.
11. **Por que 39,1% de automação?** Nove dos 23 candidatos cobrem integralmente os critérios. Testes de níveis distintos podem cobrir o mesmo caso.
12. **Como são diferentes cobertura do código e cobertura de requisitos?** A primeira conta linhas e ramos exercitados. A segunda conta requisitos com pelo menos um caso executado.
13. **Por que fazer o RED antes de alterar o código?** A falha registra que o teste detectava a ausência da nova regra.
14. **O que o refactor alterou?** Criar e editar passaram a chamar uma função de validação comum. A saída e a persistência esperadas se mantiveram.
15. **O que o Quality Gate indica?** O perfil utilizado aprovou as duas análises locais. A ocorrência estática sobre proteção de formulários continua registrada e o grupo precisa configurar o SonarQube Cloud.
