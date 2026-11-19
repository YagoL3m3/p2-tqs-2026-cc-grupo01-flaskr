# Verificações não funcionais do Flaskr

UNISAGRADO · Projeto Integrado P2 · Turma B, Grupo 1 · Etapa 7 · 19/11/2026

As sete verificações atenderam aos critérios em cinco categorias. Seis foram executadas nesta etapa. A verificação de teclado usa o registro do Safari da Etapa 4B.

| ID | Categoria | Critério principal | Resultado |
| --- | --- | --- | --- |
| NF-01 | Segurança básica | Um hash verificável e zero ocorrências da senha no HTML | Atende |
| NF-02 | Confiabilidade | Preservar os dois posts e a edição no mesmo SQLite após reinício | Atende |
| NF-03 | Usabilidade e acessibilidade | Completar cadastro, login e publicação por teclado no Safari configurado | Atende |
| NF-04 | Desempenho básico | Listagem de 50 posts com p95 de até 200 ms | Atende · p95 de 2,159 ms |
| NF-05 | Desempenho básico | Login válido com p95 de até 750 ms | Atende · p95 de 86,199 ms |
| NF-06 | Confiabilidade | Preservar o texto UTF-8 no SQLite e no HTML público | Atende |
| NF-07 | Compatibilidade | Exibir o título da página, o título do post e o corpo em Chrome e Safari | Atende |

## Ambiente e método

Flaskr 1.0.0 do tutorial Flask 3.1.3, commit de origem `22d9247`, código testado na revisão do grupo `9d8d906`. As seis verificações locais registram macOS 26.4 (25E246), ARM64, Python 3.12.14, Flask 3.1.3, Werkzeug 3.1.9 e SQLite 3.53.1. O navegador da verificação local foi Chrome 157.0.8103.79, em modo headless. A execução reaproveitada usou Safari 26.4.

O script usa HTTP em `127.0.0.1`, uma porta efêmera por servidor, contas fictícias e um SQLite descartável por verificação. Nas duas medições de desempenho, o cronômetro mede da emissão da solicitação à leitura e decodificação do HTML, incluindo o redirecionamento do login. As solicitações são sequenciais. Cada medição tem três aquecimentos excluídos dos cálculos. Para o p95, os tempos são ordenados e toma-se a posição `⌈0,95 × n⌉`. Os limites de 200 e 750 ms foram definidos antes da coleta para uma listagem pequena e uma autenticação local. O limite de login dá margem para a verificação do hash da senha. A interpretação se restringe a esse ambiente, massa e volume de requisições.

- [Evidência bruta da rodada válida, com versões e amostras](../../evidencias/etapa7/2026-11-19_testes_nao_funcionais_reexecucao.txt)
- [Script de verificação](../../tools/verificar_nao_funcionais.py)
- [Primeira tentativa, bloqueada na inicialização do executor](../../evidencias/etapa7/2026-11-19_testes_nao_funcionais.txt)

A primeira tentativa foi interrompida em cada verificação local porque o executor chamou `make_server()` com `handler`, um argumento inválido nessa versão do Werkzeug. O executor foi corrigido para usar `request_handler`. A nova rodada gerou o registro acima em arquivo separado.

## NF-01 · Armazenamento e exposição da senha

**Objetivo e rastreabilidade** · Confirmar que a senha fictícia é guardada como hash verificável e fica ausente da resposta HTML após cadastro. RNF-01 · CT-026 · R-05.

**Procedimento e critério** · Cadastrar uma conta fictícia em base vazia, seguir até **Log In** e fazer uma leitura SQLite somente leitura. Esperar um registro, hash diferente da entrada que confirme a senha e zero ocorrências da senha no HTML. Código de referência em `auth.py`, função `register()`, e `schema.sql`, tabela `user`.

**Resultado** · Um registro, hash diferente e válido, zero ocorrências no HTML HTTP 200. **Atende.** [Evidência NF-01](../../evidencias/etapa7/2026-11-19_testes_nao_funcionais_reexecucao.txt)

## NF-02 · Persistência após reinício do processo

**Objetivo e rastreabilidade** · Confirmar que os posts e as edições sobrevivem ao reinício do aplicativo. RNF-02 · CT-027 · R-03.

**Procedimento e critério** · Criar dois posts e alterar título e corpo de um deles. Encerrar o processo e iniciar outro com o mesmo banco, uma vez. Esperar um PID diferente e o mesmo inode do SQLite. A listagem deve retornar HTTP 200 com o post revisado e o de controle e apresentar somente os valores novos do post revisado. Código de referência em `db.py`, função `get_db()`, e `blog.py`, funções `create()`, `update()` e `index()`.

**Resultado** · Processo `32081` encerrado por SIGTERM e substituído pelo `32096`. Inode `57955821` preservado. O HTTP 200 exibiu os dois posts com os valores esperados. **Atende.** [Evidência NF-02](../../evidencias/etapa7/2026-11-19_testes_nao_funcionais_reexecucao.txt)

## NF-03 · Conclusão do fluxo por teclado

**Objetivo e rastreabilidade** · Verificar uma jornada de cadastro, login e publicação somente por teclado. RNF-03 · CT-028 · R-08 e R-12.

**Procedimento e critério** · No Safari com a opção de realçar cada item com Tab habilitada, alcançar os campos e botões necessários, acionar os controles pelo teclado e confirmar o post na listagem. Uma jornada com conta e publicação fictícias. Código de referência nos formulários `templates/auth/register.html`, `templates/auth/login.html`, `templates/blog/create.html` e na navegação de `templates/base.html`.

**Resultado** · O EX-029 registrou foco nos controles, inclusive **Save**, e exibiu **Teclado QA** com o corpo **Publicado com teclado.** A preferência do navegador foi restaurada após a execução. O EX-028 permanece como bloqueio inicial de ambiente. **Atende na condição configurada.** [Registro EX-029](../../evidencias/etapa4b/2026-11-19_CT-028_EX-029_safari.txt) · [Foco em Save](../../evidencias/etapa4b/capturas/CT-028_2026-11-19_EX-029_01_foco_save.jpg) · [Post publicado](../../evidencias/etapa4b/capturas/CT-028_2026-11-19_EX-029_02_post_publicado.jpg)

## NF-04 · Tempo de resposta da listagem

**Objetivo e rastreabilidade** · Quantificar a resposta da listagem com massa local fixa. RF-04 · R-11.

**Procedimento e critério** · Preparar 50 posts fictícios com horários distintos e fazer 30 solicitações anônimas `GET /` após três aquecimentos. Conferir HTTP 200 e os 50 títulos em cada resposta. Critério de p95 de até 200 ms. Código de referência em `blog.py`, função `index()`, e `templates/blog/index.html`.

**Resultado** · 30/30 amostras válidas, além dos três aquecimentos válidos. Mediana de 1,551 ms e p95 de 2,159 ms. **Atende.** [Tempos por solicitação e critérios de NF-04](../../evidencias/etapa7/2026-11-19_testes_nao_funcionais_reexecucao.txt)

## NF-05 · Tempo de resposta do login

**Objetivo e rastreabilidade** · Quantificar quanto leva para uma conta válida chegar à página autenticada. RF-02 · R-04.

**Procedimento e critério** · Autenticar a conta fictícia válida 15 vezes, cada vez em um cliente novo, após três aquecimentos. Conferir que cada `POST /auth/login` termina em `GET /` com HTTP 200, nome da conta e **Log Out**. Critério de p95 de até 750 ms. Código de referência em `auth.py`, funções `login()` e `load_logged_in_user()`.

**Resultado** · 15/15 amostras válidas, além dos três aquecimentos válidos. Mediana de 66,826 ms e p95 de 86,199 ms. Com 15 amostras, o p95 pelo método selecionado coincide com o máximo. **Atende.** [Tempos por solicitação e critérios de NF-05](../../evidencias/etapa7/2026-11-19_testes_nao_funcionais_reexecucao.txt)

## NF-06 · Integridade de texto UTF-8

**Objetivo e rastreabilidade** · Confirmar que um post mantém caracteres da língua portuguesa, emoji e quebra de linha da publicação à leitura pública. RF-05 e RF-04 · R-03 e R-11.

**Procedimento e critério** · Publicar uma vez o título `São João — café ☕` e duas linhas de corpo com texto acentuado e emoji. Comparar título e corpo caractere por caractere com o registro SQLite e com o HTML HTTP 200 obtido por um visitante sem sessão. Código de referência em `blog.py`, funções `create()` e `index()`, e `templates/blog/index.html`.

**Resultado** · A comparação foi exata no banco e no HTML público, incluindo a quebra de linha e os caracteres especiais. **Atende.** [Texto lido e comparação em NF-06](../../evidencias/etapa7/2026-11-19_testes_nao_funcionais_reexecucao.txt)

## NF-07 · Listagem em Chrome e Safari

**Objetivo e rastreabilidade** · Verificar se os elementos essenciais de leitura de um post estão presentes nos dois navegadores usados pelo grupo. RF-04 · R-11.

**Procedimento e critério** · Preparar **Teclado QA** com corpo **Publicado com teclado.** na base local. Conferir título da página, título e corpo do post uma vez no DOM do Chrome 157 com perfil limpo e sem sessão. Comparar os mesmos itens com o registro do Safari 26.4 no EX-029, feito após publicar com sessão ativa. Código de referência em `blog.py`, função `index()`, e `templates/blog/index.html`.

**Resultado** · Ambos exibiram **Posts - Flaskr**, **Teclado QA** e **Publicado com teclado.** A comparação se limita à presença dos três textos nessas duas sessões. **Atende.** [DOM do Chrome em NF-07](../../evidencias/etapa7/2026-11-19_testes_nao_funcionais_reexecucao.txt) · [Leitura do Safari em EX-029](../../evidencias/etapa4b/2026-11-19_CT-028_EX-029_safari.txt)

## Reproduzir as seis verificações locais

Na raiz do repositório, com Python 3.12 ou superior e Google Chrome instalado, use um ambiente virtual e aponte para o executável do Chrome se ele estiver fora do caminho padrão do macOS.

```sh
python -m pip install 'Flask==3.1.3' 'Werkzeug==3.1.9'
PYTHONPATH=flaskr-app python -u -B tools/verificar_nao_funcionais.py
```

O argumento opcional `--chrome` recebe o caminho do executável. Caso seja necessário registrar outra execução, salve a saída em um novo arquivo com `tee` e inclua a data, a revisão e as versões do ambiente no cabeçalho. Para repetir a verificação de teclado, siga o cenário CT-028 do catálogo com a configuração descrita no EX-029. [Catálogo de requisitos e casos](../04_CASOS_E_RASTREABILIDADE/Requisitos_Casos_e_Rastreabilidade_Flaskr.xlsx)
