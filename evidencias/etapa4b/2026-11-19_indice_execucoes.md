# Execuções manuais do Flaskr

Projeto Integrado P2 · Turma B, Grupo 1 · Etapa 4B · 19/11/2026

**27 aprovados, 1 bloqueado e 0 reprovados.** Nenhum defeito do Flaskr foi constatado nesta rodada. O bloqueio do CT-028 é uma condição do ambiente de teste. Não houve reteste de correção.

Execução assistida por IA. O Codex operou os formulários e controles na interface, em bases SQLite descartáveis e com dados fictícios. A massa das pré-condições foi preparada separadamente por caso. Nenhuma execução foi atribuída a um integrante do grupo.

Flaskr 1.0.0, Flask 3.1.3, revisão do grupo `ef5f88f`, tutorial de origem `22d9247`, macOS 26.4 (25E246), Python 3.12.14. CT-001 a CT-027 usaram Chrome 157.0.8103.79. O teste de teclado usou Safari 26.4 em janela privativa.

CT-010 e CT-027 verificaram o acesso no Chrome com a sessão deslogada. No CT-028, Option+Tab permitiu alcançar os controles que Tab pulou. A preferência do Safari permaneceu na configuração original e a publicação pelo procedimento prescrito não foi confirmada.

[Observações da interface](2026-11-19_observacoes_navegador.json) · [Requisições HTTP registradas](2026-11-19_http_execucoes.txt)

| Execução | Caso | Resultado | Observação | Evidência |
| --- | --- | --- | --- | --- |
| EX-001 | CT-001 | Aprovado | Cadastro redirecionou para Log In. Com a mesma conta, Posts exibiu qa_autor_a e Log Out. | [Captura 1](capturas/CT-001_2026-11-19_01.jpg), [Captura 2](capturas/CT-001_2026-11-19.jpg) |
| EX-002 | CT-002 | Aprovado | Register permaneceu aberto e o foco foi para Username, identificado como obrigatório e vazio. Nenhum envio ocorreu. | [Captura 1](capturas/CT-002_2026-11-19.jpg) |
| EX-003 | CT-003 | Aprovado | Register permaneceu aberto e o foco foi para Password, identificado como obrigatório e vazio. Nenhum envio ocorreu. | [Captura 1](capturas/CT-003_2026-11-19.jpg) |
| EX-004 | CT-004 | Aprovado | Register mostrou “User qa_autor_a is already registered.”. A senha original manteve o acesso à conta. | [Captura 1](capturas/CT-004_2026-11-19_01.jpg), [Captura 2](capturas/CT-004_2026-11-19.jpg) |
| EX-005 | CT-005 | Aprovado | O cadastro com Username q conduziu a Log In e a conta de um caractere foi autenticada. | [Captura 1](capturas/CT-005_2026-11-19_01.jpg), [Captura 2](capturas/CT-005_2026-11-19.jpg) |
| EX-006 | CT-006 | Aprovado | Posts exibiu qa_autor_a e Log Out antes e depois do recarregamento. | [Captura 1](capturas/CT-006_2026-11-19_01.jpg), [Captura 2](capturas/CT-006_2026-11-19.jpg) |
| EX-007 | CT-007 | Aprovado | A tela permaneceu em Log In, exibiu “Incorrect username.” e não apresentou Log Out. | [Captura 1](capturas/CT-007_2026-11-19.jpg) |
| EX-008 | CT-008 | Aprovado | A tela permaneceu em Log In, exibiu “Incorrect password.” e não apresentou Log Out. | [Captura 1](capturas/CT-008_2026-11-19.jpg) |
| EX-009 | CT-009 | Aprovado | New Post abriu com sessão. Após Log Out, o menu mostrou Register e Log In, e /create redirecionou de volta a Log In. | [Captura 1](capturas/CT-009_2026-11-19_01.jpg), [Captura 2](capturas/CT-009_2026-11-19.jpg) |
| EX-010 | CT-010 | Aprovado | Com sessão anônima, Posts exibiu Post A, Corpo A e autoria qa_autor_a datada de 2026-01-10. O menu apresentou Log In. | [Captura 1](capturas/CT-010_2026-11-19.jpg) |
| EX-011 | CT-011 | Aprovado | A primeira publicação foi criada e houve intervalo superior a dois segundos antes da segunda. Segundo QA apareceu acima de Primeiro QA. | [Captura 1](capturas/CT-011_2026-11-19_01.jpg), [Captura 2](capturas/CT-011_2026-11-19.jpg) |
| EX-012 | CT-012 | Aprovado | Posts foi exibida sem artigos e sem mensagem de erro em uma base vazia. | [Captura 1](capturas/CT-012_2026-11-19.jpg) |
| EX-013 | CT-013 | Aprovado | A conta B viu os dois posts. Edit apareceu apenas no Post B, da própria conta. | [Captura 1](capturas/CT-013_2026-11-19.jpg) |
| EX-014 | CT-014 | Aprovado | Posts exibiu Rotina QA, o corpo esperado e autoria da conta A. | [Captura 1](capturas/CT-014_2026-11-19.jpg) |
| EX-015 | CT-015 | Aprovado | A publicação com título de um caractere foi salva e mostrou o corpo Fronteira QA. | [Captura 1](capturas/CT-015_2026-11-19.jpg) |
| EX-016 | CT-016 | Aprovado | A publicação foi salva com o título Sem corpo QA e o parágrafo do corpo ficou vazio. | [Captura 1](capturas/CT-016_2026-11-19.jpg) |
| EX-017 | CT-017 | Aprovado | O formulário permaneceu em New Post, focou Title vazio e não publicou o rascunho. Posts permaneceu sem artigos. | [Captura 1](capturas/CT-017_2026-11-19_01.jpg), [Captura 2](capturas/CT-017_2026-11-19.jpg) |
| EX-018 | CT-018 | Aprovado | Posts exibiu Post A revisado e Corpo A revisado sob autoria de qa_autor_a. O título antigo não apareceu. | [Captura 1](capturas/CT-018_2026-11-19.jpg) |
| EX-019 | CT-019 | Aprovado | O formulário bloqueou o título vazio e manteve o editor aberto. A listagem conservou o título Post A e o corpo Corpo A. | [Captura 1](capturas/CT-019_2026-11-19_01.jpg), [Captura 2](capturas/CT-019_2026-11-19.jpg) |
| EX-020 | CT-020 | Aprovado | Ao abrir o endereço Edit pela conta B, o Flaskr exibiu Forbidden. A conta A voltou a ver Post A e Corpo A intactos. Log HTTP confirmou 403. | [Captura 1](capturas/CT-020_2026-11-19_01.jpg), [Captura 2](capturas/CT-020_2026-11-19.jpg) |
| EX-021 | CT-021 | Aprovado | A rota /1/update para um post inexistente exibiu Not Found e não abriu o editor. Log HTTP confirmou 404. | [Captura 1](capturas/CT-021_2026-11-19.jpg) |
| EX-022 | CT-022 | Aprovado | O diálogo de confirmação abriu e foi cancelado. O editor permaneceu aberto e Posts preservou Post A e Post B. | [Captura 1](capturas/CT-022_2026-11-19_01.jpg), [Captura 2](capturas/CT-022_2026-11-19_02.jpg), [Captura 3](capturas/CT-022_2026-11-19.jpg) |
| EX-023 | CT-023 | Aprovado | Após confirmar, Post A saiu da lista. Post B permaneceu com Corpo B e a autoria original. | [Captura 1](capturas/CT-023_2026-11-19_01.jpg), [Captura 2](capturas/CT-023_2026-11-19.jpg) |
| EX-024 | CT-024 | Aprovado | A primeira exclusão retirou Post A da lista. Confirmar pelo editor desatualizado exibiu Not Found e preservou Post B. Log HTTP confirmou 404. | [Captura 1](capturas/CT-024_2026-11-19_01.jpg), [Captura 2](capturas/CT-024_2026-11-19_02.jpg), [Captura 3](capturas/CT-024_2026-11-19.jpg) |
| EX-025 | CT-025 | Aprovado | Mudei para a conta B em outra aba da mesma sessão. O envio pelo editor antigo exibiu Forbidden. Post A e Corpo A permaneceram. Log HTTP confirmou 403. | [Captura 1](capturas/CT-025_2026-11-19_01.jpg), [Captura 2](capturas/CT-025_2026-11-19_02.jpg), [Captura 3](capturas/CT-025_2026-11-19.jpg) |
| EX-026 | CT-026 | Aprovado | O cadastro redirecionou a Log In. O HTML retornado não continha a senha. SQLite confirmou um único registro, armazenamento diferente da entrada e hash verificável. | [Captura 1](capturas/CT-026_2026-11-19.jpg), [Log 1](2026-11-19_CT-026_validacao_sqlite_html.txt) |
| EX-027 | CT-027 | Aprovado | Após encerrar e iniciar outro processo com o mesmo SQLite, Posts sem sessão exibiu Post A persistente, Corpo persistente e Post B com Corpo B. | [Captura 1](capturas/CT-027_2026-11-19_01.jpg), [Captura 2](capturas/CT-027_2026-11-19.jpg), [Log 1](2026-11-19_CT-027_reinicio.txt), [Log 2](2026-11-19_CT-027_novo_processo.txt) |
| EX-028 | CT-028 | Bloqueado | No Safari 26.4, Tab alcançou os campos, mas pulou links e o botão Register. Option+Tab deu foco visível aos controles e permitiu cadastro e login. A publicação usando Tab na configuração prevista ficou pendente. | [Captura 1](capturas/CT-028_2026-11-19_04_register_botao.jpg), [Captura 2](capturas/CT-028_2026-11-19_01_register_link.jpg), [Captura 3](capturas/CT-028_2026-11-19_02_username.jpg), [Captura 4](capturas/CT-028_2026-11-19_03_password.jpg), [Captura 5](capturas/CT-028_2026-11-19_05_register_option_tab.jpg), [Captura 6](capturas/CT-028_2026-11-19_06_login_botao.jpg) |
