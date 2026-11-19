"""Gera o DOCX do Marco 1. Execute com Python e python-docx instalado."""
from pathlib import Path
from shutil import copyfile

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

RAIZ = Path(__file__).resolve().parents[1]
NOME = "Marco_1_Fundamentos_Flaskr.docx"


def elemento(pai, tag, **atributos):
    item = OxmlElement(f"w:{tag}")
    for chave, valor in atributos.items():
        item.set(qn(f"w:{chave}"), valor)
    pai.append(item)
    return item


def quadro(doc, cabecalhos, larguras, linhas):
    tabela = doc.add_table(rows=0, cols=len(cabecalhos))
    tabela.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabela.autofit = False
    for coluna, largura in zip(tabela.columns, larguras):
        coluna.width = Inches(largura)
    bordas = elemento(tabela._tbl.tblPr, "tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        elemento(bordas, lado, val="single", sz="4", color="D9D9D9")
    margens = elemento(tabela._tbl.tblPr, "tblCellMar")
    for lado in ("top", "bottom", "left", "right"):
        elemento(margens, lado, w="95", type="dxa")
    for indice, valores in enumerate([cabecalhos, *linhas]):
        linha = tabela.add_row()
        propriedades = linha._tr.get_or_add_trPr()
        elemento(propriedades, "cantSplit")
        if indice == 0:
            elemento(propriedades, "tblHeader")
        for celula, largura, valor in zip(linha.cells, larguras, valores):
            celula.width = Inches(largura)
            celula.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if indice == 0:
                elemento(celula._tc.get_or_add_tcPr(), "shd", fill="E8EFF6")
            paragrafo = celula.paragraphs[0]
            paragrafo.paragraph_format.space_after = Pt(0)
            texto = paragrafo.add_run(valor)
            texto.font.size = Pt(10)
            texto.bold = indice == 0


def gerar():
    doc = Document()
    doc.core_properties.title = "Fundamentos de teste do Flaskr"
    doc.core_properties.author = "UNISAGRADO · Grupo 1"
    pagina = doc.sections[0]
    pagina.page_width, pagina.page_height = Inches(8.5), Inches(11)
    pagina.left_margin = pagina.right_margin = Inches(0.8)
    pagina.top_margin = pagina.bottom_margin = Inches(0.7)
    for nome, tamanho in (("Normal", 11), ("Title", 28), ("Heading 1", 17), ("Heading 2", 12)):
        estilo = doc.styles[nome]
        estilo.font.name = "Calibri"
        estilo.font.size = Pt(tamanho)
        estilo.font.color.rgb = RGBColor(0, 0, 0)
    for borda in doc.styles["Title"].element.xpath(".//w:pBdr"):
        borda.getparent().remove(borda)
    normal = doc.styles["Normal"].paragraph_format
    normal.space_after = Pt(7)
    normal.line_spacing = 1.10
    rodape = pagina.footer.paragraphs[0]
    rodape.add_run("Projeto Integrado P2  •  Grupo 1                                        ")
    elemento(rodape._p, "fldSimple", instr="PAGE")

    doc.add_paragraph("Fundamentos de teste do Flaskr", "Title")
    doc.add_paragraph("Marco 1  •  Testes e Qualidade de Software  •  UNISAGRADO")
    doc.add_paragraph(
        "O grupo testará o Flaskr 1.0.0, tutorial do projeto Pallets na tag Flask 3.1.3 "
        "(commit 22d9247). As referências flaskr/ e tests/ são relativas a flaskr-app/."
    )
    doc.add_heading("Justificativa da escolha", 1)
    doc.add_paragraph(
        "Escolhemos o Flaskr porque ele reúne, em uma aplicação que o grupo pode instalar "
        "localmente, formulários, autenticação, autorização por autoria e persistência. "
        "O cadastro em flaskr/auth.py → register() usa SQLite e o formulário "
        "flaskr/templates/auth/register.html. A edição em flaskr/blog.py → update() consulta "
        "get_post() para verificar a autoria antes de alterar a publicação. Esses fluxos "
        "permitem observar o resultado na interface e conferir o estado armazenado."
    )
    doc.add_paragraph(
        "As regras de negócio concentram-se em poucos pontos, como unicidade do usuário, "
        "título obrigatório e permissão por autoria. Para ampliar a cobertura, o grupo "
        "vai combinar variações de entrada, estados da sessão e perfis de acesso. O Flaskr carece de API REST. A interface "
        "HTTP usa formulários, páginas HTML e redirecionamentos, como em flaskr/auth.py → "
        "login() e flaskr/blog.py → create(). Os testes com Postman vão verificar esses "
        "contratos HTTP e a continuidade da sessão por cookie. O SQLite temporário de "
        "tests/conftest.py → app() permite repetir os testes com dados fictícios."
    )
    doc.add_heading("Níveis de teste aplicados", 1)
    quadro(doc, ("Nível", "Finalidade e aplicação planejada"), (1.02, 5.88), [
        ("Unitário", "Isolar decisões e efeitos de uma função com pytest. Em flaskr/auth.py → login_required(), usar contexto controlado e uma função substituta para verificar a decisão de redirecionar ou chamar a rota. Em flaskr/blog.py → get_post(), substituir get_db() para verificar as decisões de existência e autoria."),
        ("Integração", "Verificar a comunicação entre rotas, sessão, templates e SQLite. Usar Postman nas rotas HTML com dados fictícios e cookie de sessão. Exercitar cadastro e login (flaskr/auth.py → register(), login()) e criação, edição e exclusão (flaskr/blog.py → create(), update(), delete())."),
        ("Sistema", "Percorrer a aplicação em execução com Selenium e verificar resultados visíveis. Cobrir cadastro, autenticação, criação de post e edição ou exclusão pelo autor. As rotas de flaskr/auth.py → register(), login() e flaskr/blog.py → create(), update(), delete() ligam a interface às operações."),
        ("Aceitação", "Validar se tarefas de leitor e autor atendem ao uso esperado. Um integrante que não escreveu os testes valida leitura pública, cadastro e acesso, publicação e manutenção restrita ao autor. O escopo abrange flaskr/blog.py → index(), create(), update(), delete() e flaskr/auth.py → register(), login()."),
    ])

    doc.add_page_break()
    doc.add_heading("Verificação do item 5.3 do manual", 1)
    doc.add_paragraph("Manual do Projeto Integrado P2, UNISAGRADO, seção 5.3, página 5. Os critérios abaixo seguem a ordem do manual.")
    quadro(doc, ("Critério", "Evidência no projeto", "Avaliação"), (1.85, 3.5, 1.55), [
        ("1. Código disponível para instalar, executar, automatizar, aplicar TDD e analisar a qualidade",
         "pyproject.toml define o pacote instalável. flaskr/__init__.py → create_app() aceita configuração de teste. tests/conftest.py → app() e client() dão suporte à automação. A licença BSD está em LICENSE-FLASK.txt na raiz.",
         "Atende. O código local permite TDD e análise de qualidade nas etapas previstas."),
        ("2. Execução local, de homologação ou de testes",
         "flaskr/__init__.py → create_app() configura a instância. flaskr/db.py → init_db_command() prepara o banco. A Etapa 0 registrou resposta HTTP 200 do servidor local.",
         "Atende em ambiente local. Inicializar apenas bancos de teste descartáveis."),
        ("3. Quatro fluxos relevantes e duas entradas de dados",
         "flaskr/auth.py → register(), login() e flaskr/blog.py → index(), create(), update(), delete(). Os formulários estão em templates/auth/ e templates/blog/, dentro de flaskr/.",
         "Atende. Cadastro, login, criação e edição já fornecem quatro formulários."),
        ("4. Persistência ou integração de dados",
         "flaskr/db.py → get_db() abre SQLite e init_db() executa flaskr/schema.sql. flaskr/blog.py → create(), update(), delete() gravam e confirmam as alterações.",
         "Atende. O banco persiste usuários e publicações."),
        ("5. Integração entre componentes",
         "flaskr/blog.py → index() consulta SQLite e entrega os resultados a flaskr/templates/blog/index.html. flaskr/auth.py → load_logged_in_user() liga sessão e banco.",
         "Atende por integração interna. O Postman cobre respostas HTML e cookies."),
        ("6. Dados fictícios e testes repetíveis",
         "tests/conftest.py → app() cria um SQLite temporário, aplica flaskr/db.py → init_db(), carrega tests/data.sql e remove o arquivo ao fim do teste.",
         "Atende. Usar instâncias locais e massa fictícia nas execuções do grupo."),
        ("7. Disponibilidade durante todo o semestre",
         "A cópia local fixa a origem em 22d9247. flaskr/__init__.py → create_app() e flaskr/db.py → get_db() permitem operação local após instalar as dependências.",
         "[CONFIRMAR] O grupo precisa manter acesso à cópia e às instruções durante o semestre."),
        ("8. Instruções de instalação existentes ou viáveis",
         "README.rst e pyproject.toml documentam o tutorial e seu empacotamento. flaskr/db.py → init_db_command() e flaskr/__init__.py → create_app() sustentam os comandos da Etapa 0.",
         "Atende. A instalação editável e a execução local foram verificadas na Etapa 0."),
    ])

    doc.add_page_break()
    doc.add_heading("Fluxos selecionados e integrações reais", 1)
    quadro(doc, ("Fluxo", "Rota e implementação", "Resultado a verificar"), (1.12, 2.62, 3.16), [
        ("Cadastro", "GET e POST /auth/register\nflaskr/auth.py → register()",
         "Formulário auth/register.html, inclusão em user com senha armazenada como hash e redirecionamento para login. Validar dados vazios e usuário duplicado."),
        ("Entrada e saída", "GET e POST /auth/login\nGET /auth/logout\nflaskr/auth.py → login(), logout()",
         "Login usa auth/login.html, verifica credenciais no SQLite e inicia a sessão. Logout a limpa. Conferir mensagens para usuário desconhecido e senha incorreta."),
        ("Leitura pública", "GET /\nflaskr/blog.py → index()",
         "A consulta une post e user, ordena por data de criação decrescente e entrega os dados a blog/index.html. Conferir conteúdo e autoria na listagem."),
        ("Criação", "GET e POST /create\nflaskr/blog.py → create()",
         "blog/create.html recebe título e corpo. Conferir gravação com a autoria da sessão, rejeição de título vazio e redirecionamento para login quando anônimo."),
        ("Edição", "GET e POST /<id>/update\nflaskr/blog.py → update(), get_post()",
         "blog/update.html mostra o post. Conferir alteração persistida, validação de título e bloqueio para outro usuário (403) ou registro inexistente (404)."),
        ("Exclusão", "POST /<id>/delete\nflaskr/blog.py → delete(), get_post()",
         "O formulário em blog/update.html pede confirmação visual. Após POST válido, verificar remoção no SQLite e retorno à lista. Conferir 403 e 404."),
    ])
    doc.add_heading("Pontos de integração", 2)
    doc.add_paragraph(
        "HTTP e Jinja. flaskr/__init__.py → create_app() registra os blueprints. "
        "As funções de rota renderizam os templates sob flaskr/templates/. base.html exibe "
        "a navegação a partir de g.user e mostra as mensagens de validação."
    )
    doc.add_paragraph(
        "Sessão e SQLite. flaskr/auth.py → load_logged_in_user() carrega o usuário da sessão "
        "em g.user. login_required() protege as rotas de escrita. flaskr/db.py → get_db() "
        "reutiliza a conexão no contexto e close_db() a fecha no encerramento."
    )
    doc.add_heading("Rastreio aos testes originais", 2)
    doc.add_paragraph(
        "tests/test_auth.py → test_register(), test_login(), test_logout(). "
        "tests/test_blog.py → test_index(), test_create(), test_update(), test_delete(), "
        "test_login_required(), test_author_required(), test_exists_required(). "
        "tests/test_db.py → test_get_close_db(), test_init_db_command(). "
        "tests/test_factory.py → test_config(), test_hello()."
    )

    sistema = RAIZ / "entrega/01_SISTEMA_ALVO" / NOME
    requisitos = RAIZ / "entrega/02_REQUISITOS_ESCOPO_RISCOS" / NOME
    doc.save(sistema)
    copyfile(sistema, requisitos)
    print(sistema)
    print(requisitos)


if __name__ == "__main__":
    gerar()
