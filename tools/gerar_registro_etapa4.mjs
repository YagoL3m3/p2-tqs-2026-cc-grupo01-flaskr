import assert from "node:assert/strict";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";
import { casos } from "./dados_marco3.mjs";

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Execuções");
sheet.showGridLines = false;

const cabecalho = ["Execução", "Caso", "Data", "Versão", "Executor", "Resultado",
  "Evidência", "Defeito", "Resultado obtido / observações"];
const linhas = casos.map(({ id }) => {
  assert.match(id, /^CT-\d{3}$/);
  return [id.replace("CT-", "EX-"), id, null, null, null, null, null, null, null];
});
assert.equal(new Set(linhas.map(linha => linha[0])).size, linhas.length, "Há IDs de execução repetidos.");

const primeira = 7;
const ultima = primeira + linhas.length - 1;
const enderecoTabela = `A6:I${ultima}`;
const tabela = sheet.tables.add(enderecoTabela, true, "ExecucoesMarco4");
tabela.style = "TableStyleLight9";
tabela.showBandedRows = false;
tabela.showFilterButton = true;
sheet.getRange(enderecoTabela).values = [cabecalho, ...linhas];

const larguras = [113, 110, 112, 160, 179, 153, 262, 115, 391];
for (const [indice, largura] of larguras.entries()) {
  sheet.getCell(0, indice).format.columnWidthPx = largura;
}
sheet.getRange("A1").format.rowHeight = 10;
for (const [linha, texto] of [
  [2, "Registro de execução manual do Flaskr"],
  [3, "UNISAGRADO · Projeto Integrado P2 · Turma B, Grupo 1 · Etapa 4A · Apêndice F"],
  [4, "Após executar cada caso, preencha data, versão, executor, resultado e evidência. Use o campo Defeito quando houver um BUG vinculado."],
]) {
  const faixa = sheet.getRange(`A${linha}:G${linha}`);
  faixa.merge();
  faixa.values = [[texto]];
  faixa.format = {
    verticalAlignment: "center",
    rowHeight: linha === 2 ? 29 : 20,
    font: { name: "Calibri", size: linha === 2 ? 17 : 11, color: "#15314A", bold: linha === 2 },
  };
}
sheet.getRange("A6:I6").format = {
  fill: "#244E6D", verticalAlignment: "center", wrapText: true, rowHeight: 29,
  font: { name: "Calibri", size: 11, bold: true, color: "#FFFFFF" },
  borders: { insideVertical: { style: "thin", color: "#FFFFFF" } },
};
sheet.getRange(`A${primeira}:I${ultima}`).format = {
  verticalAlignment: "center", wrapText: true, rowHeight: 28,
  font: { name: "Calibri", size: 11, color: "#202831" },
  borders: { insideHorizontal: { style: "thin", color: "#E1EAF1" } },
};
sheet.getRange(`A${primeira}:B${ultima}`).format.font.bold = true;
for (let linha = primeira + 1; linha <= ultima; linha += 2) {
  sheet.getRange(`A${linha}:I${linha}`).format.fill = "#F3F7FA";
}
sheet.getRange(`C${primeira}:C${ultima}`).setNumberFormat("dd/mm/yyyy");
sheet.getRange(`D${primeira}:D${ultima}`).setNumberFormat("@");
sheet.getRange(`F${primeira}:F${ultima}`).dataValidation = {
  rule: { type: "list", values: ["Aprovado", "Reprovado", "Bloqueado", "Não executado"] },
};
sheet.freezePanes.freezeRows(6);
workbook.recalculate();
assert.deepEqual(sheet.getRange(`A${ultima}:I${ultima}`).values[0], linhas.at(-1));

if (process.env.MARCO4_PREVIEW) {
  const preview = await workbook.render({ sheetName: sheet.name, range: "A1:I14", format: "png" });
  await writeFile(process.env.MARCO4_PREVIEW, new Uint8Array(await preview.arrayBuffer()));
}
const destino = new URL("../entrega/05_EXECUCAO_MANUAL/Registro_de_Execucao_Manual_Flaskr.xlsx", import.meta.url);
const arquivo = await SpreadsheetFile.exportXlsx(workbook);
await arquivo.save(fileURLToPath(destino));
console.log(`${linhas.length} IDs de execução vinculados ao catálogo da Etapa 3. Campos de resultado e evidência em branco.`);
