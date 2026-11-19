// Execute com @oai/artifact-tool disponível no runtime Node.
import { writeFile } from "node:fs/promises";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";

const riscos = [
  ["R-01", "Edição ou exclusão por usuário que não é autor", "Médio", "Alto", "Com dois usuários fictícios, verificar 403 na edição e na exclusão por outro usuário e confirmar que o post permanece intacto. flaskr/blog.py: get_post(), update(), delete()."],
  ["R-02", "Formulários aceitam campos obrigatórios vazios", "Médio", "Médio", "Enviar campos vazios e válidos, conferir mensagens e ausência de gravação inválida. flaskr/auth.py: register(). flaskr/blog.py: create(), update()."],
  ["R-03", "Publicação criada ou editada se perde após reinício", "Médio", "Alto", "Criar e editar um post, reiniciar mantendo o arquivo SQLite e conferir os valores na listagem. flaskr/blog.py: create(), update(), index(). flaskr/db.py: get_db()."],
  ["R-04", "Login inválido inicia sessão ou logout deixa operações protegidas acessíveis", "Médio", "Alto", "Testar senha incorreta, login válido e logout. Verificar redirecionamento ao login quando deslogado. flaskr/auth.py: login(), logout(), login_required()."],
  ["R-05", "Senha gravada em texto puro ou exibida na interface", "Baixo", "Alto", "Cadastrar conta fictícia e verificar localmente que o valor armazenado difere da senha e valida com check_password_hash. Conferir ausência da senha na resposta HTML. flaskr/auth.py: register(), login()."],
  ["R-06", "Exclusão pelo autor remove a publicação errada ou ocorre após cancelar", "Médio", "Alto", "Criar dois posts fictícios, cancelar o diálogo e verificar que ambos permanecem. Confirmar a exclusão e verificar que apenas o alvo sumiu. flaskr/blog.py: delete(). flaskr/templates/blog/update.html."],
  ["R-07", "Cadastro duplicado grava duas contas ou falha sem mensagem", "Médio", "Médio", "Repetir o cadastro com o mesmo nome. Conferir mensagem de duplicidade e uma única linha para o usuário. flaskr/auth.py: register(). flaskr/schema.sql: UNIQUE em username."],
  ["R-08", "Porta ocupada ou incompatibilidade entre navegador, driver e ambiente", "Alto", "Alto", "Verificar URL e página Posts antes do ciclo, registrar versões, validar Selenium no Safari e prever IPv4 na porta 5001 caso a 5000 esteja ocupada. [CONFIRMAR] Safari WebDriver habilitado."],
  ["R-09", "Massa compartilhada ou reinicialização apaga dados de outra execução", "Médio", "Alto", "Usar SQLite temporário por teste ou banco descartável por ciclo. Validar o caminho antes de init-db e restaurar massa fictícia. flaskr/db.py: init_db(). tests/conftest.py: app()."],
  ["R-10", "Dependências ou serviços remotos indisponíveis atrasam evidências", "Médio", "Alto", "Preparar dependências e testar acesso a GitHub e SonarCloud com antecedência. Executar testes locais quando possível e registrar bloqueios das etapas remotas."],
  ["R-11", "Ordem da listagem divergente para posts de datas distintas", "Baixo", "Baixo", "Preparar posts com horários de criação distintos e conferir a ordem da tela. flaskr/blog.py: index()."],
  ["R-12", "Navegação por teclado dificulta concluir os fluxos principais", "Médio", "Médio", "Percorrer cadastro e criação com Tab e verificar acesso a campos, foco e acionamento por teclado. flaskr/templates/auth/register.html e flaskr/templates/blog/create.html. [CONFIRMAR] Comportamento no Safari."],
];

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Matriz de riscos");
sheet.showGridLines = false;
const end = riscos.length + 4;
sheet.getRange("A1:F1").merge();
sheet.getRange("A1").values = [["Matriz de riscos do Flaskr"]];
sheet.getRange("A2:F2").merge();
sheet.getRange("A2").values = [["Marco 2  |  Versão 1.0  |  Estimativas de planejamento  |  Manual §9.3 e Apêndice C"]];
sheet.getRange("A3:F3").merge();
sheet.getRange("A3").values = [["Prioridade = maior nível entre probabilidade e impacto. Alto primeiro e após correções, Médio no ciclo principal, Baixo depois."]];
sheet.getRange("A4:F4").values = [["ID", "Risco", "Probabilidade", "Impacto", "Prioridade", "Resposta e teste"]];
for (const [index, [id, risco, prob, impacto, resposta]] of riscos.entries()) {
  const row = index + 5;
  sheet.getRange(`A${row}:D${row}`).values = [[id, risco, prob, impacto]];
  sheet.getRange(`E${row}`).formulas = [[`=IF(OR(C${row}="Alto",D${row}="Alto"),"Alto",IF(OR(C${row}="Médio",D${row}="Médio"),"Médio","Baixo"))`]];
  sheet.getRange(`F${row}`).values = [[resposta]];
}
for (const [index, width] of [76, 315, 112, 82, 91, 555].entries()) {
  const col = "ABCDEF"[index];
  sheet.getRange(`${col}:${col}`).format.columnWidthPx = width;
}
sheet.getRange(`A1:F${end}`).format.font.name = "Calibri";
sheet.getRange(`A4:F${end}`).format.wrapText = true;
sheet.getRange(`A4:F${end}`).format.verticalAlignment = "center";
sheet.getRange(`C5:E${end}`).format.horizontalAlignment = "center";
sheet.getRange("A1:F1").format = { fill: "#15314A", font: { bold: true, color: "#FFFFFF", size: 17 }, rowHeight: 32 };
sheet.getRange("A2:F3").format = { fill: "#E8EFF6", font: { color: "#15314A", size: 11 }, rowHeight: 23 };
sheet.getRange("A4:F4").format = { fill: "#244E6D", font: { bold: true, color: "#FFFFFF" }, rowHeight: 27 };
for (let row = 5; row <= end; row++) {
  sheet.getRange(`A${row}:F${row}`).format.rowHeight = 52;
  if (row % 2 === 0) sheet.getRange(`A${row}:F${row}`).format.fill = "#F1F5F8";
}
sheet.freezePanes.freezeRows(4);
const preview = process.env.MATRIZ_PREVIEW;
if (preview) {
  const png = await workbook.render({ sheetName: sheet.name, range: `A1:F${end}`, format: "png" });
  await writeFile(preview, new Uint8Array(await png.arrayBuffer()));
}
const arquivo = await SpreadsheetFile.exportXlsx(workbook);
await arquivo.save(new URL("../entrega/02_REQUISITOS_ESCOPO_RISCOS/Matriz_de_Riscos_Flaskr.xlsx", import.meta.url).pathname);
