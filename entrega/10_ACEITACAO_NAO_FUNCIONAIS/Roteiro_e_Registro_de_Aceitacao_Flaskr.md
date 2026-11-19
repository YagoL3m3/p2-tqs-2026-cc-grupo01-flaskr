# Aceitação do Flaskr

UNISAGRADO · Projeto Integrado P2 · Turma B, Grupo 1 · Etapa 7

O ensaio executado por IA verificou os quatro cenários no navegador. A execução com representante independente, as decisões e as assinaturas ainda aguardam registro. [Resultados do ensaio](Ensaio_de_Aceitacao_Flaskr.md)

[PENDENTE-HUMANO: convidar uma pessoa que não elaborou os testes e combinar a execução dos quatro cenários | Grupo 1]

## Preparação

O Grupo 1 sobe o Flaskr local em uma base SQLite descartável e separada para cada cenário. O participante usa o navegador e registra o que conseguiu fazer, o que encontrou de difícil e sua decisão. Quando não houver um usuário real, a seção 9.11 do manual permite convidar um representante de outro grupo.

1. Abra a página `http://127.0.0.1:5001/` em uma janela privativa, salvo quando o cenário exigir trocar de conta na mesma janela. Use a porta informada por quem preparou o ambiente.
2. Confirme a base indicada no cenário. As contas fictícias A (`qa_autor_a`) e B (`qa_autor_b`) e suas senhas de teste estão na massa da Etapa 4.
3. Faça uma cópia do registro ao final para cada cenário, inclusive se a execução for interrompida. Salve uma captura do resultado sem mostrar senhas e identifique o arquivo com o ID do cenário e a data, como `AC-01_AAAA-MM-DD.png`.

- [Guia para subir o Flaskr e escolher a base](../05_EXECUCAO_MANUAL/Guia_de_Execucao_Manual.md)
- [Contas e publicações fictícias](../../testes_grupo/dados/massa_etapa4.json)
- [Catálogo de requisitos e casos](../04_CASOS_E_RASTREABILIDADE/Requisitos_Casos_e_Rastreabilidade_Flaskr.xlsx)
- [Ficha editável e imprimível](Ficha_de_Aceitacao_Flaskr.docx)

## AC-01 · Publicar o primeiro aviso como nova pessoa autora

**Objetivo do usuário** · Quero criar minha conta e colocar um aviso no blog.

**Base e dados** · Base `vazia`. Conta A. Título `Primeiro aviso QA`. Corpo `Publicação fictícia para a atividade.`

1. Selecione **Register**, preencha **Username** e **Password** e finalize o cadastro.
2. Entre pela tela **Log In** com a mesma conta.
3. Abra **New**, preencha **Title** e **Body** com os dados acima e selecione **Save**.
4. Confira a publicação em **Posts** e selecione **Log Out**.

**Critério de sucesso** · O cadastro abre **Log In**. Após entrar, **Posts** mostra `qa_autor_a` no menu. O aviso aparece com o título, corpo e autoria esperados. Depois de sair, **Posts** volta a oferecer **Log In** e o aviso continua visível.

Rastreabilidade · RF-01, RF-02, RF-03 e RF-05 · CT-001, CT-006, CT-009 e CT-014 · R-02, R-03, R-04 e R-07.

## AC-02 · Encontrar o aviso mais recente como visitante

**Objetivo do usuário** · Quero consultar a notícia mais recente sem criar uma conta.

**Base e dados** · Base `publicacoes`. **Post A** (`Corpo A`) é o aviso anterior. **Post B** (`Corpo B`) é o aviso mais recente. Ambos são da conta A e têm horários distintos na massa.

1. Abra a página inicial em janela privativa e identifique o primeiro artigo.
2. Leia o título, o corpo e a autoria dos dois artigos e verifique se o menu oferece **Log In**.

**Critério de sucesso** · **Post B** aparece antes de **Post A**. O corpo e a autoria `qa_autor_a` dos dois artigos são legíveis enquanto a janela está sem sessão.

Rastreabilidade · RF-04 · CT-010 e CT-011 · R-11.

## AC-03 · Corrigir uma informação mantendo a autoria

**Objetivo do usuário** · Quero corrigir um aviso publicado por mim e deixar a revisão visível para outra pessoa.

**Base e dados** · Base `publicacoes`. Contas A e B. Edite **Post A** para `Post A atualizado` e `Corpo atualizado pelo autor.`. **Post B** será a referência de que a edição atingiu o artigo certo.

1. Entre com a conta A. No **Post A**, selecione **Edit**, substitua **Title** e **Body** e salve.
2. Confira a listagem e a autoria. Saia da conta A e entre com a conta B.
3. Localize **Post A atualizado** e observe as ações oferecidas no artigo.

**Critério de sucesso** · A revisão mantém `qa_autor_a` como autor e os valores antigos do artigo são substituídos. **Post B** continua com `Corpo B`. A conta B lê o artigo revisado e o respectivo cartão não apresenta a ação **Edit**.

Rastreabilidade · RF-04 e RF-06 · CT-013 e CT-018 · R-01 e R-03.

## AC-04 · Retirar somente o aviso selecionado

**Objetivo do usuário** · Quero retirar um aviso meu e poder desistir se abrir a confirmação por engano.

**Base e dados** · Base `publicacoes`. Conta A. **Post A** é o alvo. **Post B** (`Corpo B`) deve permanecer disponível.

1. Entre com a conta A. Em **Post A**, abra **Edit**, selecione **Delete** e cancele a confirmação.
2. Volte à lista pelo link **Flaskr** e confira a presença dos dois artigos.
3. Abra novamente **Edit** em **Post A**, selecione **Delete** e confirme.
4. Confira **Posts**, inclusive o conteúdo do **Post B**.

**Critério de sucesso** · Após cancelar, os dois artigos continuam na lista. Após confirmar, **Post A** desaparece e **Post B** permanece com `Corpo B` e autoria `qa_autor_a`.

Rastreabilidade · RF-07 · CT-022 e CT-023 · R-01 e R-06.

## Registro para copiar por cenário

As opções de decisão são **Aceito**, **Aceito com ressalvas** e **Não aceito**. Em uma execução interrompida, registre o motivo e deixe a decisão pendente até ter condições de avaliar.

```text
Flaskr · Aceitação · Turma B, Grupo 1
Cenário (AC-01 a AC-04) =
Participante independente e grupo/papel =
Data e horário da execução =
SO, navegador/versão e revisão do repositório =
Resultado observado e passos concluídos =
Dificuldades e observações =
Evidência(s) =
Decisão =
Ressalvas ou justificativa da decisão =
Assinatura do participante e data =
```

[PENDENTE-HUMANO: executar AC-01, AC-02, AC-03 e AC-04, preencher os quatro registros e anexar as evidências reais | Representante do usuário independente]

[PENDENTE-HUMANO: registrar e assinar as decisões de aceitação após as execuções | Representante do usuário independente]
