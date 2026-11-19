import assert from "node:assert/strict";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";
import { casos, notasCasos, requisitos } from "./dados_marco3.mjs";

const raiz = fileURLToPath(new URL("../", import.meta.url));
const agentes = await readFile(join(raiz, "AGENTS.md"), "utf8");
const responsavel = agentes.match(/^\| Análise e execução manual \| (.+?) \|$/m)?.[1];
assert.ok(responsavel, "O papel de análise e execução manual precisa constar em AGENTS.md.");

const requisitosPorId = new Map(requisitos.map(requisito => [requisito[0], requisito]));
assert.equal(requisitosPorId.size, requisitos.length, "IDs de requisitos repetidos.");
assert.ok(requisitos.filter(requisito => requisito[2] === "Funcional").length >= 6);
assert.ok(requisitos.filter(requisito => requisito[2] === "Não funcional").length >= 2);
assert.ok(casos.length >= 24);

const idsCasos = new Set();
for (const [indice, caso] of casos.entries()) {
  assert.equal(caso.id, `CT-${String(indice + 1).padStart(3, "0")}`);
  assert.ok(!idsCasos.has(caso.id));
  idsCasos.add(caso.id);
  assert.ok(caso.titulo && caso.tipo && caso.tecnica && caso.prioridade);
  assert.ok(caso.pre && caso.dados && caso.esperado && caso.passos.length > 0);
  assert.ok(["Sim", "Não"].includes(caso.candidato) && caso.motivo);
  const requisito = requisitosPorId.get(caso.requisito);
  assert.ok(requisito, `${caso.id} tem requisito desconhecido.`);
  assert.ok(caso.riscos.length > 0 && caso.riscos.every(risco => requisito[5].includes(risco)));
}

const fontes = new Set([
  ...requisitos.flatMap(requisito => requisito[6]),
  ...casos.flatMap(caso => caso.fontes),
]);
for (const referencia of fontes) {
  const match = /^([\w/.-]+)\b(?:\s*·|,)/.exec(referencia);
  assert.ok(match, `Fonte sem arquivo: ${referencia}`);
  const codigo = await readFile(join(raiz, "flaskr-app", match[1]), "utf8");
  for (const funcao of referencia.matchAll(/\b([a-z_]+)\(\)/g)) {
    assert.ok(codigo.includes(`def ${funcao[1]}(`), `Função não encontrada: ${referencia}`);
  }
  for (const linhas of referencia.matchAll(/\b(\d+)(?:–(\d+))?/g)) {
    assert.ok(Number(linhas[2] ?? linhas[1]) <= codigo.split("\n").length, referencia);
  }
}

const rastreabilidade = requisitos.flatMap(([id, , , , , riscos]) =>
  riscos.map(risco => {
    const associados = casos.filter(caso => caso.requisito === id && caso.riscos.includes(risco));
    assert.ok(associados.length, `${id} / ${risco} sem caso planejado.`);
    return [id, risco, associados.map(caso => caso.id).join("; "), null, null, "Planejado", null];
  }),
);

const workbook = Workbook.create();
const tema = {
  titulo: "#15314A", cabecalho: "#244E6D", texto: "#202831",
  nota: "#42576C", linha: "#E1EAF1", alternado: "#F3F7FA", branco: "#FFFFFF",
};

function bloco(sheet, row, ultimo, value, format) {
  sheet.mergeCells(`A${row}:${ultimo}${row}`);
  sheet.getRange(`A${row}`).values = [[value]];
  sheet.getRange(`A${row}:${ultimo}${row}`).format = format;
}

function linhasVisiveis(value, largura) {
  const capacidade = Math.floor((largura - 16) / 7.2);
  return String(value ?? "").split("\n").reduce((total, texto) => {
    let linhas = 1;
    let ocupacao = 0;
    for (const palavra of texto.split(/\s+/)) {
      const acrescentar = palavra.length + (ocupacao > 0 ? 1 : 0);
      if (ocupacao + acrescentar > capacidade) {
        linhas += 1;
        ocupacao = palavra.length;
      } else {
        ocupacao += acrescentar;
      }
    }
    return total + linhas;
  }, 0);
}

function criarAba({ nome, titulo, notas, cabecalhos, larguras, registros, colunasNotas = cabecalhos.length }) {
  const sheet = workbook.worksheets.add(nome);
  sheet.showGridLines = false;
  const ultimo = String.fromCharCode(64 + cabecalhos.length);
  const ultimaColunaNotas = String.fromCharCode(64 + colunasNotas);
  const larguraNotas = larguras.slice(0, colunasNotas).reduce((total, largura) => total + largura, 0);
  const linhaCabecalho = notas.length + 4;
  const ultimaLinha = linhaCabecalho + registros.length;
  const endereco = `A${linhaCabecalho}:${ultimo}${ultimaLinha}`;

  for (const [indice, largura] of larguras.entries()) {
    sheet.getCell(0, indice).format.columnWidthPx = largura;
  }
  sheet.getRange("A1").format.rowHeightPx = 10;
  bloco(sheet, 2, ultimaColunaNotas, titulo, {
    font: { name: "Calibri", size: 17, bold: true, color: tema.titulo },
    verticalAlignment: "center", rowHeightPx: 34,
  });
  for (const [indice, nota] of notas.entries()) {
    bloco(sheet, indice + 3, ultimaColunaNotas, nota, {
      font: { name: "Calibri", size: 11, color: tema.nota },
      wrapText: true, verticalAlignment: "center",
      rowHeightPx: 20 + 16 * Math.max(0, linhasVisiveis(nota, larguraNotas) - 1),
    });
  }
  const cabecalho = sheet.getRange(`A${linhaCabecalho}:${ultimo}${linhaCabecalho}`);
  const tabela = sheet.tables.add(endereco, true, `Marco3${nome.normalize("NFD").replace(/\p{M}/gu, "")}`);
  tabela.style = "TableStyleLight9";
  tabela.showBandedRows = false;
  tabela.showFilterButton = true;
  sheet.getRange(endereco).values = [cabecalhos, ...registros];
  cabecalho.format = {
    fill: tema.cabecalho,
    font: { name: "Calibri", size: 11, bold: true, color: tema.branco },
    verticalAlignment: "center",
    wrapText: true,
    rowHeightPx: 37,
    borders: { insideVertical: { style: "thin", color: tema.branco } },
  };
  const dados = sheet.getRange(`A${linhaCabecalho + 1}:${ultimo}${ultimaLinha}`);
  dados.format = {
    font: { name: "Calibri", size: 11, color: tema.texto },
    wrapText: true,
    verticalAlignment: "center",
    borders: { insideHorizontal: { style: "thin", color: tema.linha } },
  };
  for (const [indice, registro] of registros.entries()) {
    const linha = linhaCabecalho + 1 + indice;
    const faixa = sheet.getRange(`A${linha}:${ultimo}${linha}`);
    const linhas = Math.max(...registro.map((value, col) => linhasVisiveis(value, larguras[col])));
    faixa.format.rowHeightPx = Math.max(33, linhas * 18 + 12);
    faixa.format.fill = indice % 2 === 0 ? tema.branco : tema.alternado;
  }
  sheet.getRange(`A${linhaCabecalho + 1}:A${ultimaLinha}`).format.font.bold = true;
  sheet.freezePanes.freezeRows(linhaCabecalho);
  return { sheet, ultimo, linhaCabecalho, ultimaLinha };
}

const req = criarAba({
  nome: "Requisitos", titulo: "Requisitos verificáveis do Flaskr",
  notas: [
    "UNISAGRADO · Projeto Integrado P2 · Turma B, Grupo 1 · Marco 3 · Flaskr 1.0.0 · Flask 3.1.3 / 22d9247",
    "Apêndice B do manual e Plano de Testes do Marco 2. Caminhos de código relativos a flaskr-app. Critérios de aceitação para verificação nas próximas etapas.",
  ],
  cabecalhos: ["ID", "Descrição verificável", "Tipo", "Prioridade", "Critério de aceitação", "Riscos", "Base no código"],
  larguras: [98, 360, 120, 102, 456, 125, 300],
  registros: requisitos.map(([id, descricao, tipo, prioridade, criterio, riscos, base]) =>
    [id, descricao, tipo, prioridade, criterio, riscos.join("; "), base.join("\n")]),
});

const cat = criarAba({
  nome: "Casos", titulo: "Catálogo de casos manuais",
  notas: notasCasos,
  colunasNotas: 6,
  cabecalhos: ["ID do caso", "Título", "Requisito", "Nível / tipo", "Técnica aplicada", "Prioridade", "Pré-condições",
    "Dados de entrada", "Passos numerados", "Resultado esperado", "Automatizar?", "Justificativa",
    "Responsável", "Observações e base no código", "Riscos"],
  larguras: [111, 238, 109, 168, 210, 103, 315, 260, 480, 390, 122, 265, 169, 320, 123],
  registros: casos.map(caso => [
    caso.id, caso.titulo, caso.requisito, caso.tipo, caso.tecnica, caso.prioridade, caso.pre, caso.dados,
    caso.passos.map((passo, indice) => `${indice + 1}. ${passo}`).join("\n"),
    caso.esperado, caso.candidato, caso.motivo, responsavel,
    [...caso.fontes, caso.observacao].filter(Boolean).join("\n"), caso.riscos.join("; "),
  ]),
});

const rast = criarAba({
  nome: "Rastreabilidade", titulo: "Matriz de rastreabilidade",
  notas: [
    "Apêndice H. Cada linha relaciona um requisito, um risco e os casos associados. As colunas de execução, defeito e evidência serão preenchidas com registros reais.",
    "R-09 e R-10 são riscos do processo. O banco descartável e a disponibilidade do ambiente são verificações de preparação previstas no Marco 2.",
  ],
  cabecalhos: ["Requisito", "Risco", "Caso(s)", "Execução(ões)", "Defeito(s)", "Situação", "Evidência(s)"],
  larguras: [130, 108, 338, 160, 132, 130, 185],
  registros: rastreabilidade,
});

const guia = rast.ultimaLinha + 3;
bloco(rast.sheet, guia, rast.ultimo, "CT-026 · Conferir o hash no banco descartável", {
  font: { name: "Calibri", size: 13, bold: true, color: tema.titulo },
  verticalAlignment: "center", rowHeightPx: 28,
});
bloco(rast.sheet, guia + 1, rast.ultimo,
  "Em flaskr-app, no mesmo ambiente virtual e com a configuração do servidor, execute python -m flask --app flaskr shell. Cole uma linha por vez e informe a senha fictícia da conta A quando solicitada.",
  { font: { name: "Calibri", size: 11, color: tema.nota }, verticalAlignment: "center", wrapText: true, rowHeightPx: 44 });
const consulta = [
  "from pathlib import Path",
  "from getpass import getpass",
  "from sqlite3 import connect",
  "from werkzeug.security import check_password_hash",
  "banco = connect(Path(app.config['DATABASE']).resolve().as_uri() + '?mode=ro', uri=True)",
  "linhas = banco.execute('SELECT password FROM user WHERE username = ?', ('qa_autor_a',)).fetchall()",
  "banco.close()",
  "senha = getpass('Senha fictícia da conta A: ')",
  "unico = len(linhas) == 1",
  "print(unico, unico and linhas[0][0] != senha, unico and check_password_hash(linhas[0][0], senha))",
].join("\n");
bloco(rast.sheet, guia + 2, rast.ultimo, consulta, {
  fill: tema.alternado, font: { name: "Courier New", size: 11, color: tema.texto },
  verticalAlignment: "center", wrapText: true, rowHeightPx: 188,
});
bloco(rast.sheet, guia + 3, rast.ultimo,
  "Registre somente os três indicadores booleanos. Cada um deve ser True. Feche o shell ao terminar.",
  { font: { name: "Calibri", size: 11, color: tema.nota }, verticalAlignment: "center", rowHeightPx: 28 });

workbook.recalculate();
assert.equal(req.sheet.getRange(`A${req.ultimaLinha}`).values[0][0], "RNF-03");
assert.equal(cat.sheet.getRange(`A${cat.ultimaLinha}`).values[0][0], `CT-${String(casos.length).padStart(3, "0")}`);
assert.equal(rast.sheet.getRange(`F${rast.ultimaLinha}`).values[0][0], "Planejado");
if (process.env.MARCO3_PREVIEWS) {
  await mkdir(process.env.MARCO3_PREVIEWS, { recursive: true });
  const intervalos = [
    [req, `A1:G${req.ultimaLinha}`, "requisitos"],
    [cat, "A1:H14", "casos-identificacao"],
    [cat, `I${cat.linhaCabecalho}:O${cat.ultimaLinha}`, "casos-procedimento"],
    [rast, `A1:G${guia + 3}`, "rastreabilidade"],
  ];
  for (const [aba, range, nome] of intervalos) {
    const png = await workbook.render({ sheetName: aba.sheet.name, range, scale: 1, format: "png" });
    await writeFile(join(process.env.MARCO3_PREVIEWS, `${nome}.png`), new Uint8Array(await png.arrayBuffer()));
  }
}

const destino = new URL("../entrega/04_CASOS_E_RASTREABILIDADE/Requisitos_Casos_e_Rastreabilidade_Flaskr.xlsx", import.meta.url);
const arquivo = await SpreadsheetFile.exportXlsx(workbook);
await arquivo.save(fileURLToPath(destino));
console.log(`Etapa 3: ${requisitos.length} requisitos, ${casos.length} casos e ${rastreabilidade.length} relações requisito-risco verificadas.`);
console.log(`Especificação gravada em ${fileURLToPath(destino)}.`);
