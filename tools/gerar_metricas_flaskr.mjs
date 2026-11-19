import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const [dados, saida, preview] = process.argv.slice(2);
const d = JSON.parse(await readFile(dados, "utf8"));
const workbook = Workbook.create();
const painel = workbook.worksheets.add("Indicadores");
const casos = workbook.worksheets.add("Casos");
const requisitos = workbook.worksheets.add("Requisitos");
const defeitos = workbook.worksheets.add("Defeitos");

const inicia = (sheet, titulo, referencia, larguras) => {
  sheet.showGridLines = false;
  for (const [idx, width] of larguras.entries()) sheet.getCell(0, idx).format.columnWidthPx = width;
  const fim = String.fromCharCode(64 + larguras.length);
  for (const [linha, texto] of [[2, titulo], [3, referencia]]) {
    const faixa = sheet.getRange(`A${linha}:${fim}${linha}`);
    faixa.merge();
    faixa.values = [[texto]];
    faixa.format = {
      verticalAlignment: "center",
      rowHeight: linha === 2 ? 36 : 26,
      font: { name: "Calibri", size: linha === 2 ? 18 : 11, bold: linha === 2, color: "#193C52" },
    };
  }
  sheet.freezePanes.freezeRows(5);
};

const tabela = (sheet, range, headers, values) => {
  const i = sheet.getRange(range);
  i.values = [headers, ...values];
  i.format = {
    rowHeight: 24, verticalAlignment: "center", wrapText: true,
    font: { name: "Calibri", size: 11, color: "#172C36" },
    borders: { insideHorizontal: { color: "#D8E4E9", style: "thin" } },
  };
  i.getRow(0).format = {
    rowHeight: 26, verticalAlignment: "center", fill: "#244A61",
    font: { name: "Calibri", size: 11, color: "#FFFFFF", bold: true },
  };
};

inicia(painel, "Métricas do Flaskr", "Projeto Integrado P2 · Turma B · Grupo 1 · rodada de 19/11/2026", [215, 105, 105, 105, 560]);
inicia(casos, "Base de casos e execução", "Fonte: planilhas de requisitos, casos, rastreabilidade e execução manual das pastas 04 e 05. AUT remete aos guias das pastas 07 a 09.", [90, 95, 390, 100, 115, 105, 100, 238]);
inicia(requisitos, "Requisitos no escopo", "Fonte: aba Requisitos da planilha da pasta 04. A cobertura exige uma execução manual conclusiva.", [95, 115, 115, 410]);
inicia(defeitos, "Base de defeitos", "Fonte: Registro_de_Defeitos_Flaskr.csv e consulta ao GitHub Issues de 19/11/2026. Sem registros nesta rodada.", [100, 150, 165, 115, 115, 450]);

const lc = 5 + d.casos.length;
const lr = 5 + d.requisitos.length;
tabela(casos, `A5:H${lc}`, ["Caso", "Requisito", "Título", "Última execução", "Resultado", "Planejado p/ autom.", "Automação", "Casos automatizados"], d.casos);
tabela(requisitos, `A5:D${lr}`, ["Requisito", "Tipo", "Executado?", "Critério"], d.requisitos.map(row => [...row, null, "Ao menos um caso aprovado ou reprovado"]));
requisitos.getRange(`C6:C${lr}`).formulas = d.requisitos.map((_, i) => [
  `=IF(COUNTIFS(Casos!B6:B${lc},A${i + 6},Casos!E6:E${lc},"Aprovado")+COUNTIFS(Casos!B6:B${lc},A${i + 6},Casos!E6:E${lc},"Reprovado")>0,"Sim","Não")`,
]);
tabela(defeitos, "A5:F5", ["ID", "Severidade", "Status", "Retestado?", "Reaberto?", "Referência"], []);

tabela(painel, "A5:E13", ["Indicador", "Resultado", "Numerador", "Denominador", "Interpretação"], [
  ["Percentual de execução", null, null, null, "Os 28 casos planejados têm execução conclusiva no resultado mais recente."],
  ["Taxa de aprovação", null, null, null, "Todos os casos com resultado conclusivo passaram."],
  ["Taxa de reprovação", null, null, null, "Nenhum caso foi reprovado. A primeira tentativa de CT-028 ficou bloqueada."],
  ["Cobertura de requisitos", null, null, null, "Cada requisito do escopo possui pelo menos um caso com execução conclusiva."],
  ["Taxa de automação", null, null, null, "Conta apenas a automação integral dos critérios dos casos marcados Sim no catálogo."],
  ["Defeitos por severidade", null, null, null, "Não houve defeitos registrados. As contagens por severidade estão abaixo."],
  ["Defeitos por status", null, null, null, "Não houve defeitos registrados. As contagens por estado estão abaixo."],
  ["Taxa de reabertura", null, null, null, "Não aplicável porque nenhum defeito foi retestado."],
]);
painel.getRange("A6:E13").format.rowHeight = 32;
painel.getRange("B6:D13").formulas = [
  ['=IF(D6=0,"N/A",C6/D6)', "=C7+C8", `=COUNTA(Casos!A6:A${lc})`],
  ['=IF(D7=0,"N/A",C7/D7)', `=COUNTIF(Casos!E6:E${lc},"Aprovado")`, "=C6"],
  ['=IF(D8=0,"N/A",C8/D8)', `=COUNTIF(Casos!E6:E${lc},"Reprovado")`, "=C6"],
  ['=IF(D9=0,"N/A",C9/D9)', `=COUNTIF(Requisitos!C6:C${lr},"Sim")`, `=COUNTA(Requisitos!A6:A${lr})`],
  ['=IF(D10=0,"N/A",C10/D10)', `=COUNTIFS(Casos!F6:F${lc},"Sim",Casos!G6:G${lc},"Integral")`, `=COUNTIF(Casos!F6:F${lc},"Sim")`],
  ["=SUM(B16:B19)", null, null],
  ["=SUM(B22:B27)", null, null],
  ['=IF(D13=0,"N/A",C13/D13)', '=COUNTIF(Defeitos!E6:E505,"Sim")', '=COUNTIF(Defeitos!D6:D505,"Sim")'],
];
painel.getRange("B6:B10").setNumberFormat("0.0%");
painel.getRange("B13").setNumberFormat("0.0%");
painel.getRange("B6:B13").format.font.bold = true;

const severidades = ["Crítica", "Alta", "Média", "Baixa"];
const etapas = ["Novo", "Em análise", "Em correção", "Pronto para reteste", "Encerrado", "Reaberto"];
tabela(painel, "A15:B19", ["Severidade", "Defeitos"], severidades.map(x => [x, null]));
tabela(painel, "A21:B27", ["Status", "Defeitos"], etapas.map(x => [x, null]));
painel.getRange("B16:B19").formulas = severidades.map((_, i) => [`=COUNTIF(Defeitos!B6:B505,A${16 + i})`]);
painel.getRange("B22:B27").formulas = etapas.map((_, i) => [`=COUNTIF(Defeitos!C6:C505,A${22 + i})`]);

const chart = painel.charts.add("bar", painel.getRange("A5:B10"));
chart.title = "Execução, cobertura e automação";
chart.setPosition("D15", "E28");
chart.hasLegend = false;
chart.series.items[0].fill = "#25777A";
chart.yAxis = { numberFormatCode: "0%", numberFormatSourceLinked: false, minimumScale: 0, maximumScale: 1 };

workbook.recalculate();
assert.deepEqual(painel.getRange("B6:B13").values.flat(), [
  1, d.aprovados / d.executados, d.reprovados / d.executados,
  d.cobertura / d.requisitos.length, d.automatizados / d.candidatos, 0, 0, "N/A",
]);
if (preview) {
  const png = await workbook.render({ sheetName: "Indicadores", range: "A1:E29", format: "png" });
  await writeFile(preview, new Uint8Array(await png.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(workbook)).save(saida);
