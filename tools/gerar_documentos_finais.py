"""Gera o relatório, a ficha de identificação e os formulários em DOCX."""
import argparse
import json
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
ENTREGA = ROOT / "entrega"
GRUPO = (
    "Henrique Motta Canho",
    "Yago da Silva Leme",
    "Guilherme Tamelini Bertozzo",
    "Victor Hugo de Deus Machado",
)
GITHUB = "https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr"
UPSTREAM = "https://github.com/pallets/flask/releases/tag/3.1.3"
PROFESSOR = "Prof. Dr. Elvio Gilberto da Silva"
BASE = "22d924701a6ae2e4cd01e9a15bbaf3946094af65"


def document():
    doc = Document()
    doc.core_properties.author = "Turma B · Grupo 1 · UNISAGRADO"
    doc.core_properties.subject = "Projeto Integrado P2 de Testes e Qualidade de Software"
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.left_margin = section.right_margin = Cm(2.35)
    section.top_margin, section.bottom_margin = Cm(2.1), Cm(2)
    section.header_distance, section.footer_distance = Cm(0.82), Cm(0.82)
    section.different_first_page_header_footer = True
    for name, size in [("Normal", 11), ("Title", 27), ("Subtitle", 13), ("Heading 1", 16), ("Heading 2", 12)]:
        style = doc.styles[name]
        style.font.name, style.font.size = "Liberation Sans", Pt(size)
        style.font.color.rgb = RGBColor(0, 0, 0)
    normal = doc.styles["Normal"].paragraph_format
    normal.space_after, normal.line_spacing = Pt(8), 1.15
    title_style = doc.styles["Title"]
    title_style.paragraph_format.space_after = Pt(10)
    border = title_style.element.find(".//" + qn("w:pBdr"))
    if border is not None:
        border.getparent().remove(border)
    style = doc.styles.add_style("Legenda técnica", WD_STYLE_TYPE.PARAGRAPH)
    style.base_style = doc.styles["Normal"]
    style.font.size = Pt(9)
    style.font.italic = True
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = footer.add_run("UNISAGRADO · Turma B · Grupo 1     /     ")
    r.font.size = Pt(8.5)
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    footer._p.append(field)
    return doc


def title(doc, name):
    doc.add_paragraph(name, "Title")
    doc.add_paragraph("Projeto Integrado P2 · Testes e Qualidade de Software", "Subtitle")


def table(doc, headers, rows, widths):
    widget = doc.add_table(rows=1, cols=len(headers))
    widget.style = "Table Grid"
    widget.autofit = False
    for col, width in zip(widget.columns, widths):
        col.width = Cm(width)
    for row_data in [headers, *rows]:
        if row_data is headers:
            row = widget.rows[0]
            header = OxmlElement("w:tblHeader")
            row._tr.get_or_add_trPr().append(header)
        else:
            row = widget.add_row()
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for idx, (cell, value) in enumerate(zip(row.cells, row_data)):
            cell.width = Cm(widths[idx])
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.05
            r = p.add_run(str(value))
            r.font.size = Pt(9.5)
            if row_data is headers:
                r.bold = True
                r.font.color.rgb = RGBColor.from_string("FFFFFF")
                shading = OxmlElement("w:shd")
                shading.set(qn("w:fill"), "244A61")
                cell._tc.get_or_add_tcPr().append(shading)
    doc.add_paragraph("").paragraph_format.space_after = Pt(1)


def save(doc, folder, name):
    output = ENTREGA / folder / f"{name}.docx"
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.core_properties.title = name.replace("_", " ")
    doc.save(output)


def forms():
    doc = document()
    title(doc, "Ficha de proposta e aprovação do Flaskr")
    doc.add_paragraph(f"UNISAGRADO · Ciência da Computação · Turma B · Grupo 1 · {PROFESSOR}")
    table(doc, ("Campo", "Preenchimento"), [
        ("Integrantes", "\n".join(GRUPO)),
        ("Sistema e origem", "Flaskr 1.0.0. Exemplo examples/tutorial do projeto Flask, tag 3.1.3."),
        ("Repositório do grupo", GITHUB),
        ("Revisão upstream", BASE),
        ("Licença", "BSD de três cláusulas. Avisos originais preservados."),
        ("Tecnologias", "Python, Flask, Jinja, SQLite. pytest, Postman, Selenium, GitHub Actions e Sonar para testes e análise."),
        ("Como executar", "Siga a instalação e os comandos do README na pasta 00."),
        ("Fluxos", "Cadastro, login e logout. Listagem, criação, edição e exclusão de posts."),
        ("Integrações", "Rotas HTTP e formulários HTML, sessão Flask e persistência em SQLite."),
        ("Justificativa", "Aplicação pequena, com regras verificáveis, banco local e código disponível."),
        ("Viabilidade", "Dados fictícios e banco descartável. O navegador e o driver de interface precisam ser compatíveis."),
        ("Decisão e data", "[PENDENTE-HUMANO: anexar a decisão, a data e eventuais ajustes registrados pelo professor | grupo]"),
    ], [4.2, 12.1])
    save(doc, "00_IDENTIFICACAO_E_README", "Ficha_de_Proposta_e_Aprovacao_Flaskr")

    doc = document()
    title(doc, "Diário de participação do Grupo 1")
    doc.add_paragraph("Preencha uma linha por contribuição efetiva. Registre autor, colaboração, duração e uma evidência que permita localizar o trabalho, como commit, documento ou execução. A relação de integrantes identifica o grupo.")
    doc.add_paragraph(" · ".join(GRUPO))
    table(doc, ("Data", "Atividade", "Responsável", "Colaboradores", "Tempo", "Evidência"), [
        ("", "", "", "", "", "") for _ in range(9)
    ], [1.7, 4.1, 2.9, 2.9, 1.4, 3.3])
    doc.add_paragraph("[PENDENTE-HUMANO: registrar e revisar as contribuições reais e os tempos | quatro integrantes]")
    save(doc, "15_DIARIO_DE_PARTICIPACAO", "Diario_de_Participacao_Flaskr")

    doc = document()
    title(doc, "Declaração final do grupo")
    doc.add_paragraph("Ao assinar, declaramos que as contribuições de cada integrante e a assistência de IA estão identificadas, os resultados registrados decorrem de execuções documentadas, os dados usados nos testes são fictícios e as permissões e licenças aplicáveis foram respeitadas.")
    doc.add_paragraph("O projeto teve assistência do Codex na preparação de testes e documentos, na execução registrada e na organização das evidências. Os integrantes são responsáveis pela revisão, pela explicação dos resultados e pela verificação das declarações que assinarem.")
    for nome in GRUPO:
        doc.add_paragraph(f"{nome}\nAssinatura __________________________________   Data ____ / ____ / ______")
    doc.add_paragraph("[PENDENTE-HUMANO: revisar e assinar as declarações | quatro integrantes]")
    save(doc, "15_DIARIO_DE_PARTICIPACAO", "Declaracao_Final_do_Grupo")

    doc = document()
    title(doc, "Comprovante de entrega")
    doc.add_paragraph("Modelo para completar depois do envio oficial no Google Drive fornecido pelo professor.")
    doc.add_paragraph("Data ____ / ____ / ______     Hora __________     Fuso __________")
    doc.add_paragraph("Link da pasta oficial ________________________________________________")
    table(doc, ("Confirmação", "Marcação"), [
        ("Pasta oficial com estrutura 00 a 16 e arquivos íntegros", "☐"),
        ("Permissões de visualização e download verificadas", "☐"),
        ("Links de repositório, Issues, pipeline e vídeo revisados", "☐"),
        ("PDF e DOCX finais conferidos e backup preservado", "☐"),
    ], [14, 2.3])
    for nome in GRUPO:
        doc.add_paragraph(f"{nome}\nAssinatura digital _________________________________________________")
    doc.add_paragraph("[PENDENTE-HUMANO: enviar, verificar acesso, registrar horário e assinar | quatro integrantes]")
    save(doc, "16_BACKUP_ENTREGA", "COMPROVANTE_DE_ENTREGA")


def section(doc, heading, *paragraphs):
    page = doc.add_heading(heading, level=1)
    for item in paragraphs:
        doc.add_paragraph(item)
    return page


def figures(doc, d, work):
    from PIL import Image, ImageDraw, ImageFont

    work.mkdir(parents=True, exist_ok=True)
    capture = ROOT / "evidencias/etapa4b/capturas/CT-014_2026-11-19.jpg"
    screenshot = work / "ct014_recorte.png"
    with Image.open(capture) as screen:
        screen.crop((464, 0, 1456, 248)).save(screenshot)

    chart = work / "indicadores.png"
    img = Image.new("RGB", (1230, 425), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=29)
    axes = 421, 1104
    values = [
        ("Execução", d["executados"] / len(d["casos"])),
        ("Aprovação", d["aprovados"] / d["executados"]),
        ("Reprovação", d["reprovados"] / d["executados"]),
        ("Cobertura de requisitos", d["cobertura"] / len(d["requisitos"])),
        ("Automação integral", d["automatizados"] / d["candidatos"]),
    ]
    for part in (0, 0.25, 0.5, 0.75, 1):
        x = round(axes[0] + part * (axes[1] - axes[0]))
        draw.line((x, 54, x, 375), fill="#D9E4EA", width=2)
        draw.text((x, 385), f"{part:.0%}", font=font, fill="#244A61", anchor="mt")
    for i, (label, frac) in enumerate(values):
        y = 82 + i * 64
        draw.text((15, y), label, font=font, fill="#172C36", anchor="lm")
        if frac:
            stop = round(axes[0] + frac * (axes[1] - axes[0]))
            draw.rectangle((axes[0], y - 14, stop, y + 14), fill="#25777A")
        texto = f"{100 * frac:.1f}%".replace(".", ",")
        draw.text((1215, y), texto, font=font, fill="#172C36", anchor="rm")
    img.save(chart)
    return screenshot, chart


def report(d, work):
    doc = document()
    screenshot, chart = figures(doc, d, work)
    name = "Relatorio_Final_Flaskr"
    planned = len(d["casos"])
    requirements = len(d["requisitos"])
    pct_auto = f'{100 * d["automatizados"] / d["candidatos"]:.1f}'.replace(".", ",")
    doc.add_paragraph("UNISAGRADO\nCIÊNCIA DA COMPUTAÇÃO\nTESTES E QUALIDADE DE SOFTWARE").paragraph_format.space_after = Pt(105)
    doc.add_paragraph("Relatório final de testes do Flaskr", "Title")
    doc.add_paragraph("Projeto Integrado P2 · Turma B · Grupo 1", "Subtitle")
    doc.add_paragraph("\n".join(GRUPO))
    doc.add_paragraph(PROFESSOR)
    doc.add_paragraph("Bauru\n2026").paragraph_format.space_before = Pt(118)

    doc.add_page_break()
    section(doc, "Identificação e participação",
            "Flaskr 1.0.0, distribuído como exemplo do Flask 3.1.3. Avaliação em ambiente de desenvolvimento local com contas fictícias e SQLite descartável.")
    doc.add_paragraph("Repositório e documentos técnicos\n" + GITHUB)
    doc.add_paragraph("Execuções do pipeline\n" + GITHUB + "/actions")
    doc.add_paragraph("O Codex auxiliou na preparação dos testes, nas execuções registradas, no código da evolução e na redação. O diário individual e a declaração de participação estão na pasta 15 para validação e assinatura dos integrantes.")
    doc.add_paragraph("[PENDENTE-HUMANO: complementar diário e assinar a declaração de participação | quatro integrantes]")
    section(doc, "Sumário")
    table(doc, ("Seções", "Página"), [
        ("1. Introdução · 2. Caracterização do sistema · 3. Escopo, requisitos e riscos", 3),
        ("4. Planejamento dos testes · 5. Especificação dos casos", 4),
        ("6. Execução manual e defeitos · 7. Automação · 8. Integração e sistema", 5),
        ("9. Aceitação e não funcionais · 10. Métricas e indicadores", 6),
        ("11. TDD, CI/CD e melhoria contínua", 7),
        ("12. Discussão · 13. Conclusão · Referências · Apêndices", 8),
    ], [14, 2.3])

    doc.add_page_break()
    section(doc, "1. Introdução",
            "O Flaskr concentra em poucos fluxos regras de autenticação, autorização e persistência. O objetivo do projeto foi construir um plano rastreável, verificar cada requisito escolhido com evidência e demonstrar uma evolução pequena guiada por testes.",
            "A avaliação inclui a linha de base oficial do tutorial e uma revisão do grupo. O resultado da avaliação sustenta o uso acadêmico do Flaskr no ambiente descrito neste relatório.")
    section(doc, "2. Caracterização do sistema",
            "Visitantes leem publicações. Usuários com conta podem iniciar sessão e criar posts. Os autores podem editar e excluir seus próprios artigos. O navegador acessa rotas HTTP e envia dados por formulários. Flask e Jinja processam a solicitação e geram HTML. SQLite armazena contas e publicações em um arquivo local.",
            f"A linha de base é o exemplo examples/tutorial da tag 3.1.3 do Flask, revisão {BASE}. O material mantém a licença BSD de três cláusulas.")
    section(doc, "3. Escopo, requisitos e riscos",
            f"A matriz contém {requirements} requisitos testáveis. RF-01 a RF-07 cobrem cadastro, autenticação, encerramento de sessão e operações de publicação. RNF-01 a RNF-03 cobrem armazenamento da senha, persistência e navegação com teclado. Avaliação em produção, carga pesada, integrações externas e uma auditoria de segurança completa ficaram fora do escopo.",
            f"A matriz prioriza {len(d['riscos'])} riscos segundo probabilidade e impacto. Os riscos de maior impacto incluem acesso a posts de outro autor, perda de conteúdo e inconsistência de sessão. A tabela abaixo mostra como os casos apoiam decisões do plano.")
    table(doc, ("Risco selecionado", "Vínculo", "Verificação"), [
        ("R-01 · Acesso a publicação de outro autor", "RF-06 e RF-07", "CT-020 e CT-025, com contas distintas."),
        ("R-03 · Perda de conteúdo", "RNF-02", "CT-027 e NF-02, com reinício controlado."),
        ("R-04 · Sessão inconsistente", "RF-02 e RF-03", "CT-006 a CT-009, com sessão e saída."),
    ], [5.4, 3.0, 7.9])

    doc.add_page_break()
    section(doc, "4. Planejamento dos testes",
            "A execução manual validou fluxos e comportamento visível. pytest verificou regras do código, tratamento de erros e persistência. Newman verificou contratos das rotas HTML e estado de sessão. Selenium executou fluxos ponta a ponta no Chrome. A estratégia de aceitação reserva decisões para um representante do usuário.",
            "Os procedimentos recriam a base e as contas de acordo com cada precondição. Os testes Python usam arquivos SQLite temporários. Newman opera sobre um servidor local com massa própria. Selenium cria um servidor, uma sessão de navegador e um banco por cenário.",
            "Os critérios de saída do recorte incluem execução conclusiva dos casos previstos e rastreabilidade da evidência. Para os testes automatizados, cada cenário precisa executar as verificações e gerar um relatório. A aceitação depende das decisões do representante.")
    table(doc, ("Nível", "Ambiente comprovado"), [
        ("Manual", "macOS 26.4, Python 3.12.14, Chrome 157 e Safari 26.4."),
        ("Automação local", "macOS 26.4, Python 3.12.13, Flask 3.1.3, Newman 6.2.1 e Selenium 4.53.0."),
        ("Pipeline", "Ubuntu 24.04 e Python 3.12 no GitHub Actions. As versões de execução constam nos logs."),
    ], [4.2, 12.1])
    section(doc, "5. Especificação dos casos",
            f"O catálogo descreve {planned} casos com entrada, preparação, sequência e resultado esperado. As técnicas incluem particionamento de equivalência em credenciais de login, valor-limite em títulos e nomes, e transição de estados para sessão e cancelamento.",
            "CT-014 usa uma conta autenticada e uma publicação com título e corpo. O passo final verifica título, corpo e autoria na listagem. O catálogo vincula o caso a RF-05 e aos riscos de validação e perda de conteúdo.",
            "A matriz da pasta 04 liga requisito, risco, caso, execução e evidência. A coluna de defeito recebe o identificador do registro quando houver ocorrência validada.")

    doc.add_page_break()
    section(doc, "6. Execução manual e defeitos",
            f"O resultado mais recente de cada caso teve {d['aprovados']} aprovações, {d['reprovados']} reprovações e nenhum bloqueio. Os {d['historico_manual']} registros preservam o bloqueio inicial de CT-028 e a execução EX-029 aprovada no Safari após configurar o foco por Tab. As capturas e os logs identificam a rodada.",
            "A sessão manual foi operada com apoio de IA na interface local. Nenhum defeito foi registrado nessa rodada. A pasta 06 reúne a exportação e o procedimento para triagem e reteste. A falha controlada do ciclo TDD é reportada na seção 11.")
    doc.add_picture(str(screenshot), width=Cm(15.6))
    doc.add_paragraph("Figura 1. CT-014 / EX-014. Recorte da captura original na pasta de evidências da Etapa 4B.", "Legenda técnica")
    section(doc, "7. Automação",
            "Na linha de base, a suíte original do Flask passou 24 testes. O grupo adicionou 8 testes unitários isolados, todos aprovados. As duas suítes juntas passaram 32 testes e cobriram 178 de 178 linhas e 42 de 42 ramos do Python do Flaskr.",
            "Em separado, os testes do grupo cobriram 154 de 178 linhas e 22 de 42 ramos. As diferenças decorrem do subconjunto de regras exercitadas. O ciclo de TDD acrescentou dois cenários de regressão à suíte do grupo.")
    section(doc, "8. Integração e sistema",
            f"Newman aprovou {d['integracao']['cenarios']} cenários em {d['integracao']['requisicoes']} requisições com {d['integracao']['assercoes']} asserções. O conjunto verifica a interação entre formulários HTTP, sessão, HTML e persistência. Os JSON exportados estão na pasta 08.",
            f"Selenium aprovou {d['interface']} cenários com esperas explícitas e captura na falha. A suíte verifica na interface cadastro, senha incorreta, criação, título vazio, edição, cancelamento de exclusão e exclusão confirmada.")

    doc.add_page_break()
    section(doc, "9. Aceitação e não funcionais",
            "AC-01 a AC-04 propõem ao representante publicar o primeiro aviso, encontrar o aviso mais recente como visitante, corrigir um aviso e remover somente o aviso selecionado. As quatro fichas aguardam execução e decisão independente.",
            "Sete verificações em cinco categorias atenderam aos critérios. Foram observados armazenamento da senha como hash, preservação de posts após reinício, teclado no Safari, integridade de UTF-8 e listagem em Chrome e Safari. As medições locais registraram p95 de 2,159 ms na listagem de 50 posts (30 amostras, limite de 200 ms) e 86,199 ms no login (15 amostras, limite de 750 ms).")
    section(doc, "10. Métricas e indicadores")
    table(doc, ("Indicador", "Cálculo", "Resultado"), [
        ("Execução", f"{d['executados']} / {planned}", "100%"),
        ("Aprovação", f"{d['aprovados']} / {d['executados']}", "100%"),
        ("Reprovação", f"{d['reprovados']} / {d['executados']}", "0%"),
        ("Cobertura de requisitos", f"{d['cobertura']} / {requirements}", "100%"),
        ("Taxa de automação", f"{d['automatizados']} / {d['candidatos']}", f"{pct_auto}%"),
        ("Defeitos por severidade", "Contagem por categoria", "Zero em todas"),
        ("Defeitos por status", "Contagem por estado", "Zero em todos"),
        ("Reabertura", "0 reabertos / 0 retestados", "Não aplicável"),
    ], [6.2, 6.2, 3.9])
    doc.add_picture(str(chart), width=Cm(15.2))
    doc.add_paragraph("Figura 2. Cinco indicadores percentuais da rodada. Fonte: planilha de métricas da pasta 11.", "Legenda técnica")
    doc.add_paragraph(f"O denominador da automação inclui os {d['candidatos']} candidatos do catálogo. Cinco têm cobertura parcial. Os testes de integração e de interface podem cobrir o mesmo caso e testar partes de outros casos. Por isso o total de testes aprovados difere da quantidade de candidatos integralmente automatizados.")

    doc.add_page_break()
    section(doc, "11. TDD, CI/CD e melhoria contínua",
            "A evolução valida se o título de uma publicação possui conteúdo visível. A validação reutiliza a mensagem original ao detectar um título formado apenas por espaços e preserva o conteúdo fornecido quando há texto.",
            "O RED acrescentou dois casos antes da implementação. Ambos falharam ao receber redirecionamento HTTP 302 onde se esperava o formulário com HTTP 200. O GREEN validou o título em criação e edição. O REFACTOR compartilhou a regra em uma função. A suíte final cobriu 178 linhas e 40 ramos, todos exercitados.")
    table(doc, ("Fase", "Commit", "Resultado observado"), [
        ("Linha de base", "eae6f81", "Actions 44590163560 aprovado em todas as suítes."),
        ("RED", "7a63c30", "Actions 44590229007 com duas falhas esperadas no pytest."),
        ("GREEN", "1c5577c", "34 testes Python aprovados localmente."),
        ("REFACTOR", "d7c225c", "Actions 44590346309 aprovado. 34 Python, 11 Newman e 7 Selenium."),
    ], [3.5, 2.7, 10.1])
    doc.add_paragraph("O workflow instala dependências e publica JUnit e cobertura tanto nas rodadas aprovadas quanto no RED. Os arquivos baixados, os registros de console e os links de execução estão na pasta 12 e nas evidências da Etapa 9.")
    doc.add_heading("Análise de qualidade", level=2)
    doc.add_paragraph("O SonarQube Community Build registrou cobertura de 100%, duplicação de 0%, zero bugs e uma ocorrência de segurança estática nas duas revisões. O Quality Gate retornou OK nas duas execuções. A ocorrência S4502 solicita revisão da proteção CSRF em formulários e permanece como ação de qualidade. O projeto SonarQube Cloud do grupo aguarda configuração.")
    table(doc, ("Prioridade", "Ação", "Critério"), [
        ("Alta", "Revisar a proteção dos formulários.", "Revisão defensiva do código e nova análise estática."),
        ("Alta", "Concluir aceitação independente.", "Decisão e evidência registradas para cada cenário."),
        ("Média", "Ampliar a cobertura de casos candidatos.", "Novos vínculos CT a AUT com execução aprovada."),
    ], [2.5, 6.4, 7.4])

    doc.add_page_break()
    section(doc, "12. Discussão dos resultados",
            "Os cenários da rodada acompanharam os fluxos mais importantes da aplicação e geraram vínculos auditáveis. A execução de navegador inclui Chrome e Safari em versões específicas. O ambiente local, as massas pequenas e as sessões controladas limitam comparações com uma aplicação exposta ou com acessos concorrentes.",
            "O bloqueio e a reexecução do teclado mostram a influência da preparação do navegador. A ausência de defeitos no registro descreve apenas a rodada executada. O achado de análise estática, a cobertura parcial de candidatos e a aceitação pendente são riscos residuais.")
    section(doc, "13. Conclusão",
            "Os cenários executados sustentam o uso didático do Flaskr em ambiente local. A suíte final e o pipeline comprovam a evolução de título e a regressão dos fluxos selecionados. A validação acadêmica final depende da aceitação, dos registros de participação, da confirmação do ambiente SonarQube Cloud do grupo e da submissão pelo canal oficial.")
    section(doc, "Referências",
            "UNISAGRADO. Testes e Qualidade de Software. Manual do Projeto Integrado P2. Ciência da Computação, 2026.",
            "PALLETS. Flask 3.1.3, exemplo de tutorial Flaskr. " + UPSTREAM,
            "GRUPO 1. Repositório Flaskr, planilhas e evidências. " + GITHUB,
            "SONARSOURCE. Python test coverage para SonarQube Community Build. https://docs.sonarsource.com/sonarqube-community-build/analyzing-source-code/test-coverage/python-test-coverage")
    section(doc, "Apêndices e anexos",
            "Pastas 00 a 06: ficha do sistema, plano, riscos, catálogo, rastreabilidade, execução e defeitos. Pastas 07 a 12: suites, aceitação, indicadores, análises e ciclo TDD. Pastas 14 a 16: apresentação, vídeo, diário, declarações e modelo de comprovante.")
    save(doc, "13_RELATORIO_FINAL", name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dados", type=Path)
    parser.add_argument("--figuras", type=Path)
    args = parser.parse_args()
    forms()
    if args.dados:
        if not args.figuras:
            parser.error("--figuras é obrigatório com --dados")
        report(json.loads(args.dados.read_text(encoding="utf-8")), args.figuras)
