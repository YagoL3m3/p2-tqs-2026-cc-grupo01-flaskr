"""Gera o plano do Marco 2 com python-docx."""
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor

from gerar_marco1 import elemento, quadro

RAIZ = Path(__file__).resolve().parents[1]


def gerar():
    doc = Document()
    doc.core_properties.title = "Plano de testes do Flaskr"
    doc.core_properties.author = "UNISAGRADO · Grupo 1"
    secao = doc.sections[0]
    secao.page_width, secao.page_height = Inches(8.5), Inches(11)
    secao.left_margin = secao.right_margin = Inches(0.8)
    secao.top_margin = Inches(0.64)
    secao.bottom_margin = Inches(0.62)
    for nome, tamanho in (("Normal", 11), ("Title", 27), ("Heading 1", 17), ("Heading 2", 12)):
        estilo = doc.styles[nome]
        estilo.font.name = "Calibri"
        estilo.font.size = Pt(tamanho)
        estilo.font.color.rgb = RGBColor(0, 0, 0)
    for nome in ("Heading 1", "Heading 2"):
        formato = doc.styles[nome].paragraph_format
        formato.space_before = Pt(9)
        formato.space_after = Pt(4)
    for borda in doc.styles["Title"].element.xpath(".//w:pBdr"):
        borda.getparent().remove(borda)
    doc.styles["Normal"].paragraph_format.space_after = Pt(5)
    rodape = secao.footer.paragraphs[0]
    rodape.add_run("Projeto Integrado P2  •  Grupo 1  •  Plano v1.0                         ")
    elemento(rodape._p, "fldSimple", instr="PAGE")
    h = doc.add_heading
    p = doc.add_paragraph

    p("Plano de testes do Flaskr", "Title")
    p("Marco 2  •  Versão 1.0  •  19/11/2026  •  Turma B, Grupo 1")
    p(
        "UNISAGRADO, Ciência da Computação, Testes e Qualidade de Software. Objeto de teste "
        "Flaskr 1.0.0, tutorial Pallets na tag Flask 3.1.3, commit 22d9247. As referências "
        "flaskr/ e tests/ são relativas a flaskr-app/. Plano baseado no manual do Projeto "
        "Integrado P2, seções 7, 9.3, 9.4 e 10 e apêndices C e D."
    )
    h("Objetivo", 1)
    p(
        "Verificar se leitores conseguem consultar publicações e se autores conseguem criar "
        "conta, entrar, publicar e administrar os próprios posts, com validação de entradas, "
        "proteção da sessão e persistência. Acompanhar a qualidade com resultados reproduzíveis."
    )
    h("Catálogo do escopo", 1)
    p("Identificadores propostos para detalhamento no Marco 3. Os riscos associados constam na matriz do Marco 2.")
    quadro(doc, ("ID e fluxo", "Comportamento a verificar e referência", "Riscos"), (1.28, 4.77, .85), [
        ("RF-01 Cadastro", "Aceitar cadastro válido e rejeitar campos vazios ou nome duplicado. flaskr/auth.py → register().", "R-02, R-07"),
        ("RF-02 Login", "Iniciar sessão com credenciais válidas e informar entrada inválida. flaskr/auth.py → login().", "R-04"),
        ("RF-03 Logout", "Limpar a sessão e exigir login em rota protegida. flaskr/auth.py → logout(), login_required().", "R-04"),
        ("RF-04 Listagem", "Exibir publicações para leitores, com autoria e ordenação por data decrescente. flaskr/blog.py → index().", "R-11"),
        ("RF-05 Criação", "Gravar post com título e autor da sessão. Rejeitar título vazio. flaskr/blog.py → create().", "R-02, R-03"),
        ("RF-06 Edição", "Persistir alteração válida do autor. Devolver 403 para outro usuário e 404 para post inexistente. flaskr/blog.py → update(), get_post().", "R-01, R-02, R-03"),
        ("RF-07 Exclusão", "Cancelar preserva o post. Confirmar como autor remove apenas o alvo. flaskr/blog.py → delete(), get_post() e flaskr/templates/blog/update.html.", "R-01, R-06"),
        ("RNF-01 Senhas", "Armazenar um hash verificável e manter a senha fora do HTML retornado. flaskr/auth.py → register(), login().", "R-05"),
        ("RNF-02 Confiabilidade", "Manter posts e alterações após reinício com o mesmo SQLite. flaskr/db.py → get_db() e flaskr/blog.py → index().", "R-03"),
        ("RNF-03 Navegação", "Concluir cadastro e criação por teclado. [CONFIRMAR] Foco e acionamento no Safari. Templates auth/register.html e blog/create.html.", "R-08, R-12"),
    ])
    h("Fora do escopo", 2).paragraph_format.page_break_before = True
    p(
        "Produção, dados reais, carga pesada, exploração de segurança, implantação pública, "
        "API REST, serviços externos do produto, recuperação de senha, comentários e moderação. "
        "A evolução funcional fica restrita ao exercício de TDD do Marco 9."
    )

    h("Riscos e estratégia de teste", 1)
    p(
        "A matriz Matriz_de_Riscos_Flaskr.xlsx, em 02_REQUISITOS_ESCOPO_RISCOS, lista 12 riscos "
        "de produto e de processo. Probabilidade e impacto são estimativas qualitativas. A "
        "prioridade adota o maior nível entre ambos. Executar os riscos altos primeiro e "
        "repetir os casos afetados após correções. R-08 a R-10 orientam a preparação do ambiente, "
        "do banco e das dependências."
    )
    quadro(doc, ("Nível", "Abordagem e evidência planejada"), (1.12, 5.78), [
        ("Unitário", "pytest com dependências isoladas para decisões de login_required() e get_post(). Relatório JUnit e rastreio ao requisito ou caso."),
        ("Integração", "Postman por HTTP nas rotas HTML com dados de formulário e sessão por cookie. Conferir status, redirecionamento e mensagens. Usar testes de integração com SQLite temporário quando for preciso conferir o estado gravado."),
        ("Sistema", "Selenium com WebDriverWait em aplicativo local. Validar resultados visíveis de cadastro, login, criação e manutenção de posts. Registrar captura em falha."),
        ("Aceitação", "Representante que não escreveu os testes valida quatro tarefas de leitor e autor. Registrar resultado por cenário como Aceito, Aceito com ressalvas ou Não aceito."),
    ])
    h("Tipos e técnicas", 2)
    p(
        "Cobrir testes funcionais, regressão e verificações não funcionais de segurança básica, "
        "confiabilidade, usabilidade e compatibilidade. Planejar seis verificações não funcionais "
        "em pelo menos três categorias, incluindo hash armazenado, acesso deslogado, persistência "
        "após reinício, navegação por teclado, visibilidade de mensagens e fluxo em navegador alternativo."
    )
    p(
        "Aplicar partições de equivalência para credenciais e títulos, fronteira entre vazio e um "
        "caractere quando a regra exigir preenchimento, tabela de decisão para sessão, autoria e "
        "existência do post e transição de estados para login e logout. Incluir casos positivos, "
        "negativos, alternativos e de exceção. Vincular cada execução ao caso e à evidência."
    )
    h("Ambiente ferramentas e dados", 2)
    p(
        "Linha de base macOS 27.2, Python 3.13.15, Flask 3.1.3, Jinja e SQLite local. Usar "
        "ambiente virtual, pytest e pytest-cov, Postman, Selenium e Safari. Preferir "
        "http://127.0.0.1:5001/ se a porta 5000 conflitar. Registrar versões de navegador, driver "
        "e ferramentas por execução. [CONFIRMAR] Safari WebDriver habilitado e navegador alternativo disponível."
    )
    p(
        "Usar autor e leitor fictícios, posts distintos e SQLite temporário (tests/conftest.py → app()). "
        "Restaurar a massa após testes de escrita e manter o mesmo arquivo no teste de reinício. "
        "Aplicar flaskr/db.py → init_db() somente a bancos descartáveis."
    )
    h("Responsabilidades e critérios", 1).paragraph_format.page_break_before = True
    p(
        "Equipe registrada no AGENTS.md: Yago da Silva Leme, Henrique Motta Canho, Guilherme "
        "Tamelini Bertozzo e Victor Hugo de Deus Machado. A tabela registra os papéis definidos pelo grupo."
    )
    agentes = (RAIZ / "AGENTS.md").read_text(encoding="utf-8")
    tabela_papeis = agentes.split("## 8.", 1)[1].split("## 9.", 1)[0]
    responsaveis = {}
    for linha in tabela_papeis.splitlines():
        if linha.startswith("| "):
            papel, nome, *_ = linha.strip("|").split("|")
            nome = nome.strip()
            responsaveis[papel.strip()] = "[PREENCHER]" if nome.startswith("`[PENDENTE-HUMANO") else nome
    quadro(doc, ("Papel", "Integrante", "Responsabilidade"), (2.12, 1.62, 3.16), [
        ("Coordenação e planejamento", responsaveis["Coordenação e planejamento"], "Manter o escopo, priorizar riscos e acompanhar prazos e bloqueios."),
        ("Análise e execução manual", responsaveis["Análise e execução manual"], "Especificar casos, coordenar execuções e registrar evidências e defeitos confirmados."),
        ("Automação e qualidade", responsaveis["Automação e qualidade"], "Manter testes automatizados, CI/CD, cobertura e análises Sonar."),
        ("Documentação, relatório e apresentação", responsaveis["Documentação, relatório e apresentação"], "Consolidar produtos, rastreabilidade, relatório e apresentação."),
    ])
    h("Entrada", 2)
    p(
        "Para cada ciclo, confirmar a revisão em teste, ambiente e versões registrados, URL com "
        "resposta HTTP 200 e página esperada, banco isolado inicializado, dados disponíveis e casos "
        "revisados com critérios observáveis. Confirmar acessos para as atividades remotas previstas no ciclo."
    )
    h("Saída", 2)
    for item in (
        "Executar 100% dos casos de prioridade Alta e concluir pelo menos 24 casos manuais com 24 execuções registradas. Para o percentual, contar somente casos com resultado conclusivo, aprovado ou reprovado, sobre todos os casos de prioridade Alta planejados.",
        "Demonstrar 100% de rastreabilidade dos requisitos do escopo a risco, caso, execução e evidência, com vínculo a defeito quando aplicável. Cobrir ao menos seis RF e dois RNF.",
        "Registrar execução de ao menos seis testes unitários, cinco de integração, quatro de sistema, quatro cenários de aceitação e seis verificações não funcionais em pelo menos três categorias.",
        "Fechar com zero defeitos bloqueadores em aberto. Retestar 100% dos casos afetados por correções aplicadas e registrar a decisão humana para os quatro cenários de aceitação.",
        "Registrar oito métricas, dois resultados Sonar, uma sequência TDD Red, Green e Refactor em commits separados e evidências de pipeline aprovado, falha controlada e correção aprovada.",
    ):
        p(item, style="List Bullet")
    h("Suspensão e retomada", 2)
    p(
        "Suspender o bloco afetado quando a verificação inicial falhar, houver banco incorreto ou "
        "inconsistente, defeito bloqueador impedir vários casos, ou navegador, driver ou serviço "
        "indispensável estiver indisponível. Registrar horário, revisão, evidência, casos afetados "
        "e responsável. Continuar blocos independentes."
    )
    p(
        "Retomar após restaurar a massa, validar a revisão e repetir com sucesso a verificação "
        "inicial do ambiente. Reexecutar os casos bloqueados e os afetados pela correção. Vincular "
        "as novas execuções às anteriores e registrar a retomada no diário."
    )

    h("Cronograma e produtos", 1).paragraph_format.page_break_before = True
    p("Marcos relativos aos tópicos do manual. [CONFIRMAR] datas no calendário oficial da disciplina.")
    quadro(doc, ("Marco", "Momento", "Produto previsto"), (1.12, 1.66, 4.12), [
        ("0", "Lançamento", "Leitura do manual e levantamento das opções de sistema."),
        ("1", "Após o Tópico 1", "Justificativa do Flaskr e classificação dos níveis de teste."),
        ("2", "Após o Tópico 2", "Escopo, matriz de riscos e plano de testes v1.0."),
        ("3", "Após o Tópico 3", "Catálogo de requisitos e casos e matriz de rastreabilidade."),
        ("4", "Após o Tópico 4", "Execuções manuais, evidências e registro de defeitos confirmados."),
        ("5", "Após o Tópico 5", "README, automação unitária, cobertura e análise de qualidade inicial."),
        ("6", "Após o Tópico 6", "Coleção Postman e testes Selenium com resultados e evidências."),
        ("7", "Após o Tópico 7", "Cenários e decisões de aceitação e verificações não funcionais."),
        ("8", "Após o Tópico 8", "Oito métricas do manual com dados reais, gráficos e interpretação."),
        ("9", "Após o Tópico 9", "Evidências TDD e CI/CD, análise Sonar final e plano de melhoria."),
        ("Entrega final", "Data oficial da P2", "Drive, relatório DOCX e PDF, apresentação PPTX e PDF, diário, demonstração ou vídeo de contingência e backup."),
    ])
    h("Controle de versão e evidências", 2)
    p(
        "Usar branch por etapa e PR para main, revisado por integrante diferente do responsável. "
        "Registrar autor humano e prefixo da etapa no commit. Atualizar a versão do plano quando "
        "houver mudança de escopo, risco ou critério. Registrar data, autor e motivo na revisão. "
        "Manter testes originais e código do Flaskr da linha de base, salvo a alteração prevista em TDD."
    )
    p(
        "Gravar saídas reais em evidencias/etapaN/ com data, comando e versões. Guardar novas "
        "execuções em arquivos distintos. Usar os identificadores RF, RNF, R, CT, EX e BUG para "
        "rastrear requisitos, riscos, casos, execuções e defeitos. Vincular evidências aos registros."
    )
    p(
        "Usar GitHub Issues para defeitos confirmados, GitHub Actions para pipeline, SonarCloud "
        "com cobertura do pytest-cov para qualidade e XLSX para casos, execuções e métricas. "
        "[CONFIRMAR] acessos do grupo aos serviços remotos antes das etapas que dependem deles."
    )

    h("Comunicação", 2)
    p(
        "Revisar riscos, bloqueios e progresso a cada marco. Registrar decisões no Diário de "
        "Participação e mudanças técnicas nos PRs. Registrar defeitos confirmados no GitHub Issues. "
        "Usar os canais indicados pelo professor para aprovações e exceções escritas. O grupo "
        "revisa as evidências e entrega a pasta final no Google Drive na data oficial."
    )

    destino = RAIZ / "entrega/03_PLANO_DE_TESTES/Plano_de_Testes_Flaskr.docx"
    doc.save(destino)
    print(destino)


if __name__ == "__main__":
    gerar()
