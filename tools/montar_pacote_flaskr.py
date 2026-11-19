"""Empacota as pastas da entrega e um backup do checkout versionado."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
NOME = "P2_TQS_2026_CC_GRUPO01_FLASKR"
BACKUP = Path("16_BACKUP_ENTREGA")
PASTAS_EVIDENCIA = {
    "etapa3": "04_CASOS_E_RASTREABILIDADE",
    "etapa4a": "05_EXECUCAO_MANUAL",
    "etapa4b": "05_EXECUCAO_MANUAL",
    "etapa5": "07_AUTOMACAO_UNITARIA",
    "etapa6": "08_INTEGRACAO_API",
    "etapa7": "10_ACEITACAO_NAO_FUNCIONAIS",
    "etapa8": "11_METRICAS_E_QUALIDADE",
    "etapa9": "12_TDD_CICD_MELHORIA",
}


def arquivo_em_evidencias(caminho):
    _, etapa, *partes = caminho.parts
    pasta = PASTAS_EVIDENCIA.get(etapa)
    if not pasta:
        return BACKUP / "Evidencias" / Path(etapa, *partes)
    if etapa == "etapa6" and partes and "selenium" in partes[0]:
        pasta = "09_SISTEMA_INTERFACE"
    if etapa == "etapa9" and partes and "sonar_" in partes[0]:
        pasta = "11_METRICAS_E_QUALIDADE"
    return Path(pasta, "Evidencias", etapa, *partes)


def local_no_pacote(relativo):
    parte = relativo.parts[0]
    if parte == "entrega":
        return Path(*relativo.parts[1:])
    if parte == "evidencias":
        return arquivo_em_evidencias(relativo) if len(relativo.parts) > 1 else Path(".")
    return BACKUP / "Codigo_e_Testes" / relativo


def ajustar_markdown(original, pasta, caminho, destino, pacote):
    def novo_endereco(match):
        link = match.group(1)
        if re.match(r"(?:[a-zA-Z]+:|#)", link):
            return match.group(0)
        local, _, ancora = link.partition("#")
        resolvido = (caminho.parent / local).resolve()
        if not resolvido.is_relative_to(pasta) or not resolvido.exists():
            return match.group(0)
        relativo = resolvido.relative_to(pasta)
        if not relativo.parts:
            return match.group(0)
        mapeado = pacote / local_no_pacote(relativo)
        if mapeado.exists():
            ret = os.path.relpath(mapeado, destino.parent)
            return f"]({ret}{'#' + ancora if ancora else ''})"
        return match.group(0)

    conteudo = re.sub(r"\]\(([^)]+)\)", novo_endereco, original)
    destino.write_text(conteudo, encoding="utf-8")


def montar(saida):
    if saida.exists():
        raise FileExistsError(f"O arquivo de destino já existe: {saida}")
    revisao = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    with tempfile.TemporaryDirectory(prefix="p2-flaskr-pacote-") as temp:
        raiz = Path(temp)
        repositorio = raiz / "repositorio"
        repositorio.mkdir()
        pacote = raiz / NOME
        pacote.mkdir()
        arquivo_git = raiz / "Backup_Tecnico_Flaskr.zip"
        subprocess.run(
            ["git", "archive", "--format=zip", "-o", str(arquivo_git), revisao],
            check=True, cwd=ROOT,
        )
        with ZipFile(arquivo_git) as zip_git:
            assert zip_git.testzip() is None
            zip_git.extractall(repositorio)
        markdown = []
        for arquivo in sorted(repositorio.rglob("*")):
            if not arquivo.is_file() or arquivo.name == ".gitkeep":
                continue
            relativo = arquivo.relative_to(repositorio)
            alvo = pacote / local_no_pacote(relativo)
            alvo.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(arquivo, alvo)
            if arquivo.suffix == ".md":
                markdown.append((arquivo, alvo))

        for arquivo, alvo in markdown:
            ajustar_markdown(arquivo.read_text(encoding="utf-8"), repositorio, arquivo, alvo, pacote)

        backup = pacote / BACKUP
        shutil.copyfile(arquivo_git, backup / arquivo_git.name)
        guia = backup / "Estrutura_e_Backup.md"
        guia.write_text(
            guia.read_text(encoding="utf-8")
            + "\nA pasta Codigo_e_Testes contém os arquivos-fonte. Para executar os testes com todos os caminhos originais, "
            "extraia Backup_Tecnico_Flaskr.zip e siga o README desse checkout. Os logs e as capturas também estão nas "
            "pastas numeradas que descrevem cada resultado.\n",
            encoding="utf-8",
        )
        arquivos = sorted(p for p in pacote.rglob("*") if p.is_file())
        (backup / "REVISAO_E_MANIFESTO.json").write_text(
            json.dumps(
                {
                    "revisao_git": revisao,
                    "arquivos": {
                        p.relative_to(pacote).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in arquivos
                    },
                },
                indent=2, ensure_ascii=False,
            ) + "\n",
            encoding="utf-8",
        )
        pastas = sorted(p.name[:2] for p in pacote.iterdir() if p.is_dir())
        assert pastas == [f"{i:02}" for i in range(17)], pastas
        with ZipFile(saida, "x", compression=ZIP_DEFLATED, compresslevel=6) as z:
            for arquivo in sorted(pacote.rglob("*")):
                if arquivo.is_file():
                    z.write(arquivo, arquivo.relative_to(raiz))
    with ZipFile(saida) as z:
        assert z.testzip() is None
        print(f"{len(z.namelist())} arquivos íntegros · revisão {revisao}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("saida", type=Path)
    montar(parser.parse_args().saida.resolve())
