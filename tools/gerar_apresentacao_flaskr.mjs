import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const [repo, skill, runtimePython, figureDir] = process.argv.slice(2);
const build = path.join(repo, ".codex-finalizer");
const output = path.join(repo, "entrega/14_APRESENTACAO_E_VIDEO_CONTINGENCIA");
const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const ink = "#142E3E";
const accent = "#176C72";
const muted = "#415D69";
const paper = "#F5F8F8";
const font = "Arial";
const remote = "https://github.com/YagoL3m3/p2-tqs-2026-cc-grupo01-flaskr";

const text = (slide, value, x, y, w, h, size, opts = {}) => {
  const shape = slide.shapes.add({
    name: opts.name ?? value.slice(0, 44),
    geometry: "textbox",
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { fill: "none", width: 0 },
  });
  shape.text = value;
  shape.text.style = {
    typeface: font, fontSize: `${size}pt`,
    color: opts.color ?? ink, bold: opts.bold ?? false,
    verticalAlignment: "middle", wrap: "square",
    insets: { left: 0, right: 0, top: 0, bottom: 0 },
  };
  return shape;
};

const slide = (title, notes) => {
  const s = deck.slides.add();
  s.background.fill = paper;
  text(s, title, 72, 53, 1136, 77, 36, { bold: true });
  text(s, "UNISAGRADO  /  Projeto Integrado P2  /  Turma B · Grupo 1", 72, 650, 1136, 31, 12, { color: muted });
  s.speakerNotes.text = notes;
  return s;
};

const line = (s, label, detail, y) => {
  text(s, label, 76, y, 374, 57, 23, { color: accent, bold: true });
  text(s, detail, 455, y, 738, 57, 21);
};

const metric = (s, value, label, x, y, w = 350) => {
  text(s, value, x, y, w, 85, 47, { color: accent, bold: true });
  text(s, label, x, y + 82, w, 62, 19);
};

const addImage = async (s, file, alt, position) => {
  s.images.add({ blob: new Uint8Array(await fs.readFile(file)), contentType: "image/png", alt, fit: "contain", position });
};

{
  const s = deck.slides.add();
  s.background.fill = "#153444";
  text(s, "UNISAGRADO  /  Ciência da Computação", 72, 53, 1136, 42, 17, { color: "#C4DBE2" });
  text(s, "Testes e qualidade do Flaskr", 72, 177, 1136, 94, 52, { color: "#FFFFFF", bold: true });
  text(s, "Projeto Integrado P2 · Turma B · Grupo 1", 74, 286, 1132, 61, 25, { color: "#C4DBE2" });
  text(s, "Henrique Motta Canho\nYago da Silva Leme\nGuilherme Tamelini Bertozzo\nVictor Hugo de Deus Machado", 74, 406, 840, 152, 19, { color: "#FFFFFF" });
  text(s, "Prof. Dr. Elvio Gilberto da Silva  /  2026", 74, 636, 920, 36, 16, { color: "#C4DBE2" });
  s.speakerNotes.text = ["Victor · 0:00 a 0:40. Apresente o grupo, a disciplina e o objetivo de avaliar o Flaskr com evidências.", "Manual do Projeto Integrado P2, UNISAGRADO, 2026."];
}
{
  const s = slide("Sistema e escopo", [
    "Victor · 0:40 a 1:50. Indique as duas perspectivas, visitante e autor. Descreva o percurso navegador, Flask, Jinja e SQLite.",
    "A tag 3.1.3 foi verificada e a revisão upstream é 22d9247.",
    "Fonte: https://github.com/pallets/flask/releases/tag/3.1.3 e catálogo da pasta 04.",
  ]);
  line(s, "Flaskr 1.0.0", "Blog didático do exemplo oficial do Flask 3.1.3.", 158);
  line(s, "Fluxos", "Cadastro, sessão, listagem, criação, edição e exclusão.", 255);
  line(s, "Tecnologias", "Python, Flask, Jinja, HTML e SQLite.", 352);
  line(s, "Escopo", "7 requisitos funcionais e 3 não funcionais.", 449);
}
{
  const s = slide("Riscos e estratégia de testes", [
    "Victor · 1:50 a 3:05. Associe cada risco ao requisito, ao caso e à evidência. Mostre a matriz na pasta 04.",
    "Fonte: Matriz_de_Riscos_Flaskr.xlsx e Plano_de_Testes_Flaskr.docx.",
  ]);
  line(s, "Autoria", "CT-020 e CT-025 verificam restrições entre duas contas fictícias.", 159);
  line(s, "Sessão", "CT-006 a CT-009 verificam credenciais e encerramento de sessão.", 253);
  line(s, "Persistência", "CT-027 verifica o conteúdo após reiniciar com o mesmo SQLite.", 347);
  text(s, "Cada caso tem preparação da massa, resultado esperado e evidência vinculada.", 76, 499, 1110, 72, 24, { bold: true });
}
{
  const s = slide("Execução manual e evidências", [
    "Henrique · 3:05 a 4:35. Cite requisito RF-05, execução EX-014 e a verificação de título, corpo e autoria.",
    "Mostre o histórico de CT-028. EX-028 ficou bloqueada na configuração do Safari. EX-029 passou com a configuração temporária de Tab, depois restaurada.",
    "Fonte: evidencias/etapa4b/2026-11-19_indice_execucoes_atualizado.md e captura CT-014_2026-11-19.jpg.",
  ]);
  await addImage(s, path.join(figureDir, "ct014_recorte.png"), "Captura de CT-014 com o post Rotina QA publicado no Flaskr.", { left: 76, top: 155, width: 1120, height: 252 });
  text(s, "CT-014 · EX-014 · A listagem exibe a publicação com a autoria da sessão.", 77, 414, 1120, 54, 18, { color: muted });
  text(s, "28 aprovados no último resultado. Um bloqueio inicial foi preservado e retestado.", 77, 499, 1120, 80, 25, { bold: true });
}
{
  const s = slide("Verificações de qualidade em três níveis", [
    "Henrique · 4:35 a 6:40. Demonstre primeiro pytest e depois Newman, com o comando e a saída ao vivo ou nos logs.",
    "Explique que 24 testes vêm do Flask e 10 vêm do grupo, já incluídos os dois de TDD.",
    "Fonte: evidencias/etapa5, evidencias/etapa6 e " + remote + "/actions/runs/44590346309.",
  ]);
  metric(s, "34", "Testes aprovados em pytest\n24 originais e 10 do grupo", 74, 192);
  metric(s, "11", "Cenários de integração\n168 asserções no Newman", 460, 192);
  metric(s, "7", "Fluxos ponta a ponta\nSelenium com Chrome", 846, 192);
  text(s, "Bases SQLite descartáveis e dados fictícios em cada suíte.", 75, 481, 1120, 73, 25, { bold: true });
}
{
  const s = slide("Aceitação e verificações não funcionais", [
    "Guilherme · 6:40 a 8:10. Mostre a ficha de aceitação e os critérios. A decisão cabe ao representante independente.",
    "Explique p95 e amostra. Limites definidos antes: 200 ms para listagem e 750 ms para login em ambiente local.",
    "Fonte: entrega/10_ACEITACAO_NAO_FUNCIONAIS e evidencias/etapa7/2026-11-19_testes_nao_funcionais_reexecucao.txt.",
  ]);
  line(s, "Aceitação", "4 cenários preparados. Execução e decisão independentes pendentes.", 156);
  line(s, "Não funcionais", "7 verificações conformes em 5 categorias.", 250);
  line(s, "Listagem local", "p95 de 2,159 ms com 50 posts, em 30 medições.", 345);
  line(s, "Login local", "p95 de 86,199 ms, em 15 medições.", 440);
}
{
  const s = slide("Indicadores da rodada", [
    "Guilherme · 8:10 a 9:35. Divida casos aprovados por casos conclusivos e explique que o histórico preserva 29 tentativas.",
    "Para automação, 9 candidatos com critérios cobertos integralmente, 5 com cobertura parcial e 9 sem vínculo. Zero defeitos registrados. Reabertura não aplicável.",
    "Fonte: entrega/11_METRICAS_E_QUALIDADE/Metricas_do_Flaskr.xlsx.",
  ]);
  metric(s, "100%", "Execução e aprovação\n28 de 28 casos", 74, 177);
  metric(s, "100%", "Cobertura de requisitos\n10 de 10 no escopo", 460, 177);
  metric(s, "39,1%", "Automação integral\n9 de 23 candidatos", 846, 177);
  text(s, "0 reprovações e 0 defeitos registrados. Taxa de reabertura sem denominador.", 75, 478, 1120, 82, 23, { bold: true });
}
{
  const s = slide("Evolução da validação do título", [
    "Yago · 9:35 a 11:10. Abra o teste e os commits. RED registra o motivo de falha esperado. GREEN aplica a regra. REFACTOR extrai uma função.",
    "Demonstre uma publicação com texto e a rejeição de um título formado por espaços. O banco permanece consistente.",
    "Fonte: entrega/12_TDD_CICD_MELHORIA/Ciclo_TDD_e_Pipeline_Flaskr.md.",
  ]);
  line(s, "RED · 7a63c30", "Dois testes falham na criação e na edição com título só de espaços.", 158);
  line(s, "GREEN · 1c5577c", "A regra recusa esses títulos e a suíte passa.", 258);
  line(s, "REFACTOR · d7c225c", "Criação e edição passam a usar a mesma validação.", 358);
  text(s, "34 testes Python aprovados após a refatoração.", 76, 502, 1120, 64, 26, { bold: true });
}
{
  const s = slide("Pipeline e análise estática", [
    "Yago · 11:10 a 12:25. Mostre os artefatos de JUnit e cobertura nas duas execuções do Actions. O RED falhou só no pytest.",
    "O SonarQube Community Build e o SonarQube Cloud têm registros separados. Mostre a comparação das duas revisões e explique o escopo da cobertura.",
    remote + "/actions/runs/44590229007", remote + "/actions/runs/44590346309",
  ]);
  line(s, "GitHub Actions", "RED 44590229007 falhou como previsto. Correção 44590346309 aprovada.", 162);
  line(s, "SonarQube", "A linha de base e a refatoração usam a cobertura importada dos testes Python.", 277);
  line(s, "Achado estático", "Uma ocorrência de segurança sobre proteção de formulários segue em revisão.", 392);
}
{
  const s = slide("Conclusão e próximas verificações", [
    "Yago · 12:25 a 13:15. Explique a prontidão para demonstração acadêmica local e as limitações. Passe a palavra aos quatro integrantes para perguntas.",
    "Assistência de IA e pendências registradas no relatório. Diário e declarações precisam de revisão e assinatura.",
  ]);
  text(s, "Os fluxos verificados sustentam a demonstração acadêmica em ambiente local.", 75, 166, 1120, 116, 33, { bold: true });
  line(s, "Aceitação", "Executar os quatro cenários com representante independente.", 321);
  line(s, "Qualidade", "Acompanhar o achado sobre proteção dos formulários nas próximas análises.", 425);
}

await fs.mkdir(build, { recursive: true });
await fs.mkdir(output, { recursive: true });
const candidatePath = path.join(build, "Flaskr_Candidato.pptx");
const finalPath = path.join(output, "Apresentacao_Flaskr.pptx");
await (await PresentationFile.exportPptx(deck)).save(candidatePath);
const { finalizePresentation } = await import(pathToFileURL(
  path.join(skill, "container_tools/artifact_tool_utils.mjs")
).href);
await finalizePresentation({
  workspaceDir: repo, candidatePath, finalPath, pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skill, "container_tools/inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skill, "container_tools/inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "12192000,6858000", "--validate-heading-fit"],
  explicitTotalSlideCount: 10, fontPolicy: { basis: "design", families: [font] },
  verifyArtifactToolImport: true, receiptPath: path.join(build, "apresentacao-validacao.json"),
});
