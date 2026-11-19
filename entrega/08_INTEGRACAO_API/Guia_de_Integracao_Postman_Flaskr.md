# Etapa 6 — Integração HTTP com Postman

A coleção envia os formulários do Flaskr por HTTP com `application/x-www-form-urlencoded` e valida status, cabeçalho `Location`, HTML e continuidade da sessão. Os fluxos exercitam as rotas de autenticação e do blog, a renderização Jinja e a persistência SQLite. A massa usa contas, senhas e publicações fictícias.

- [Coleção Postman v2.1](Flaskr.postman_collection.json)
- [Ambiente Flaskr Local](Flaskr_Local.postman_environment.json)
- [Executor local com Newman](../../tools/executar_postman.py)
- Autenticação em `register()`, `login()`, `logout()` e `login_required()`. [auth.py](../../flaskr-app/flaskr/auth.py)
- Blog em `index()`, `create()`, `update()`, `delete()` e `get_post()`. [blog.py](../../flaskr-app/flaskr/blog.py)

## Como reproduzir com Newman

Na raiz do repositório, com Python em um ambiente virtual ativo e Node.js com npm no `PATH`, execute:

```bash
python -m pip install -r requirements-test.txt -e ./flaskr-app
python tools/executar_postman.py \
  --relatorio-json artefatos/integracao/newman.json \
  --junitxml artefatos/integracao/newman.xml
```

O executor inicializa um arquivo SQLite temporário, inicia o Flaskr em uma porta livre de `127.0.0.1`, executa a coleção com Newman 6.2.1 e encerra o servidor ao final. Cada pasta usa nomes de usuário e títulos próprios e faz a sua preparação via HTTP. As requisições encadeadas usam o cookie de sessão do cliente. Nos casos de edição e exclusão, o ID do post vem do link **Edit** do artigo preparado e fica em uma variável da execução. O cabeçalho `Location` é verificado antes da navegação seguinte.

Para reproduzir um fluxo isoladamente, informe o nome completo da pasta. O executor cria outra base temporária para a execução:

```bash
python tools/executar_postman.py --pasta "AUT-I-10 Tratar nova exclusão do mesmo post"
```

## Como reproduzir no Postman

1. Inicie `python tools/executar_postman.py --servir` na raiz do repositório. O ambiente exportado usa `http://127.0.0.1:5002`.
2. Importe os dois JSON e selecione o ambiente **Flaskr Local | Etapa 6**. Mantenha os cookies habilitados e desative o seguimento automático de redirecionamentos para examinar as respostas `302`.
3. Rode a coleção ou uma pasta inteira no Collection Runner, na ordem apresentada e com uma iteração. As primeiras requisições da pasta preparam os dados usados pelas seguintes.
4. Encerre o servidor com **Ctrl+C**. Reinicie-o antes de repetir a execução para obter uma base vazia. Limpe os cookies de `127.0.0.1` no Postman ao iniciar outra rodada.

## Rastreabilidade

| Automação | Catálogo | Requisito | Verificação HTTP |
|---|---|---|---|
| AUT-I-01 | CT-001 | RF-01 | Cadastro inédito direciona a Log In e a credencial recém-criada abre a sessão. |
| AUT-I-02 | CT-004 | RF-01 | Cadastro duplicado exibe o aviso de unicidade e a senha original continua válida. |
| AUT-I-03 | CT-006 | RF-02 | Login válido preserva a conta em duas consultas à listagem. |
| AUT-I-04 | CT-008 | RF-02 | Senha incorreta exibe a mensagem de validação e `/create` continua exigindo login. |
| AUT-I-05 | CT-014 | RF-05 | A listagem exibe título, corpo e autoria da nova publicação. |
| AUT-I-06 | CT-017, parcial | RF-05 | O servidor rejeita o título vazio e o rascunho fica ausente da listagem. A validação nativa do campo aparece no AUT-S-04. |
| AUT-I-07 | CT-018 | RF-06 | A edição pelo autor substitui o título e o corpo do artigo selecionado. |
| AUT-I-08 | CT-019, parcial | RF-06 | O servidor rejeita a edição com título vazio e conserva os dados originais. O caso manual observa a validação nativa do formulário. |
| AUT-I-09 | CT-023, parcial | RF-07 | O POST remove o alvo e preserva o artigo de controle. A confirmação do diálogo aparece no AUT-S-07. |
| AUT-I-10 | CT-024, parcial | RF-07 | O segundo POST para o mesmo ID retorna `404` e preserva o controle. O caso manual parte de um editor desatualizado. |
| AUT-I-11 | CT-009 | RF-03 | Logout encerra a sessão e `/create` volta a redirecionar para Log In. |

## Resultado registrado em 19/11/2026

O Newman aprovou **11 casos**, com **56 requisições**, **168 asserções executadas** e **zero falhas**. A rodada usou macOS 26.4 (25E246) em arm64, Python 3.12.13, Flask 3.1.3, Werkzeug 3.1.9, SQLite 3.53.4, Node.js 24.18.0, npm 11.16.0 e Newman 6.2.1. A saída registrou um aviso de depreciação do Node.js sobre `fs.F_OK`. O código de saída foi zero.

A execução isolada do AUT-I-10 aprovou **8 requisições** e **24 asserções**.

- [Saída da coleção completa](../../evidencias/etapa6/2026-11-19_newman.txt)
- [Relatório JSON](../../evidencias/etapa6/2026-11-19_newman.json)
- [Relatório JUnit XML](../../evidencias/etapa6/2026-11-19_newman.xml)
- [Saída do AUT-I-10 executado isoladamente](../../evidencias/etapa6/2026-11-19_newman_pasta_isolada.txt)
