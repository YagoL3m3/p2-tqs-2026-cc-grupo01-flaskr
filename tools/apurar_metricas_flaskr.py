"""Extrai os dados das planilhas e dos relatórios da rodada de referência."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
ENTREGA = ROOT / "entrega"
EVIDENCIAS = ROOT / "evidencias"
MAPEAMENTO = {
    "CT-001": ("Integral", "AUT-I-01, AUT-S-01"),
    "CT-004": ("Integral", "AUT-I-02, AUT-U-02"),
    "CT-005": ("Parcial", "AUT-U-01"),
    "CT-006": ("Integral", "AUT-I-03, AUT-U-03"),
    "CT-008": ("Integral", "AUT-I-04, AUT-S-02"),
    "CT-009": ("Integral", "AUT-I-11, AUT-U-04"),
    "CT-011": ("Parcial", "AUT-U-05"),
    "CT-014": ("Integral", "AUT-I-05, AUT-S-03, AUT-U-06"),
    "CT-016": ("Parcial", "AUT-U-06"),
    "CT-017": ("Integral", "AUT-S-04, AUT-I-06"),
    "CT-018": ("Integral", "AUT-I-07, AUT-S-05"),
    "CT-019": ("Parcial", "AUT-I-08, AUT-U-07"),
    "CT-022": ("Integral", "AUT-S-06"),
    "CT-023": ("Integral", "AUT-S-07, AUT-I-09, AUT-U-08"),
    "CT-024": ("Parcial", "AUT-I-10"),
    "CT-026": ("Parcial", "AUT-U-01"),
}


def workbook(relative_path):
    return load_workbook(ENTREGA / relative_path, read_only=True, data_only=True)


def passed(path):
    suites = ET.parse(path).getroot()
    testcase = suites.findall(".//testcase")
    assert testcase and all(
        item.find(label) is None
        for item in testcase
        for label in ("error", "failure", "skipped")
    )
    return len(testcase)


def apurar():
    catalogo = workbook("04_CASOS_E_RASTREABILIDADE/Requisitos_Casos_e_Rastreabilidade_Flaskr.xlsx")
    registro = workbook("05_EXECUCAO_MANUAL/Registro_de_Execucao_Manual_Flaskr.xlsx")
    execucoes = [(r[0], r[1], r[5]) for r in registro["Execuções"].values if r and str(r[0]).startswith("EX-")]
    ultimas = {ct: (ex, status) for ex, ct, status in sorted(execucoes)}
    casos = []
    for linha in catalogo["Casos"].values:
        if not linha:
            continue
        ct, titulo, req = linha[:3]
        if str(ct).startswith("CT-"):
            ex, status = ultimas.get(ct, ("", "Não executado"))
            cobertura, testes = MAPEAMENTO.get(ct, ("Sem vínculo", ""))
            casos.append([ct, req, titulo, ex, status, linha[10], cobertura, testes])
    requisitos = [
        [r[0], r[2]] for r in catalogo["Requisitos"].values
        if r and str(r[0]).startswith(("RF-", "RNF-"))
    ]
    notas_risco = workbook("02_REQUISITOS_ESCOPO_RISCOS/Matriz_de_Riscos_Flaskr.xlsx")
    riscos = [[r[0], r[1], r[4]] for r in notas_risco.active.values if r and str(r[0]).startswith("R-")]
    with (ENTREGA / "06_DEFEITOS/Registro_de_Defeitos_Flaskr.csv").open(encoding="utf-8") as f:
        defeitos = list(csv.DictReader(f))
    status = Counter(r[4] for r in casos)
    conclusivos = {"Aprovado", "Reprovado"}
    cobertura = sum(any(r[1] == req and r[4] in conclusivos for r in casos) for req, _ in requisitos)
    candidatos = sum(r[5] == "Sim" for r in casos)
    automatizados = sum(r[5:7] == ["Sim", "Integral"] for r in casos)
    parciais = sum(r[5:7] == ["Sim", "Parcial"] for r in casos)
    e5 = json.loads((EVIDENCIAS / "etapa5/2026-11-19_resumo.json").read_text())
    e6 = EVIDENCIAS / "etapa6"
    relatorio_newman = json.loads((e6 / "2026-11-19_newman.json").read_text())
    newman = relatorio_newman["run"]
    assert not newman["failures"]
    assert len(ultimas) == len(casos)
    assert status["Aprovado"] + status["Reprovado"] == len(casos)
    assert not defeitos, "Atualize as contagens por categoria e os eventos de reteste."
    return {
        "casos": casos, "requisitos": requisitos, "riscos": riscos, "defeitos": defeitos,
        "historico_manual": len(execucoes), "historico_bloqueado": sum(r[2] == "Bloqueado" for r in execucoes),
        "executados": status["Aprovado"] + status["Reprovado"],
        "aprovados": status["Aprovado"], "reprovados": status["Reprovado"], "cobertura": cobertura,
        "candidatos": candidatos, "automatizados": automatizados, "parciais": parciais,
        "retestados": 0, "reabertos": 0, "unitarios": e5,
        "integracao": {
            "cenarios": len(relatorio_newman["collection"]["item"]),
            "requisicoes": newman["stats"]["requests"]["total"],
            "assercoes": newman["stats"]["assertions"]["total"],
        },
        "interface": passed(e6 / "2026-11-19_selenium.xml"),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("saida", type=Path)
    args = parser.parse_args()
    args.saida.write_text(json.dumps(apurar(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
