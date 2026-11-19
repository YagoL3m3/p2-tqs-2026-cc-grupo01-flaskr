"""Cria uma demonstração curta com evidências reais e narração sintética."""
import argparse
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EVIDENCIA = ROOT / "evidencias"
DESTINO = ROOT / "entrega/14_APRESENTACAO_E_VIDEO_CONTINGENCIA/Video_de_Contingencia_Flaskr.mp4"
FUNDO, TEXTO, DESTAQUE = "#153444", "#FFFFFF", "#A3D5D9"
LARGURA, ALTURA = 1280, 720


def fonte(size):
    return ImageFont.load_default(size=size)


def captura(nome, caixa):
    with Image.open(EVIDENCIA / "etapa4b/capturas" / nome) as img:
        return img.crop(caixa)


def linhas(nome, marcas):
    arquivo = (EVIDENCIA / "etapa9" / nome).read_text()
    saida = []
    for marca in marcas:
        raw = next(linha for linha in arquivo.splitlines() if marca in linha)
        saida.append(raw.split("Z ", 1)[-1].strip().strip("=").strip())
    return saida


def quadro(destino, titulo, subtitulo, referencia, conteudo):
    img = Image.new("RGB", (LARGURA, ALTURA), FUNDO)
    draw = ImageDraw.Draw(img)
    draw.text((67, 48), "UNISAGRADO / Projeto Integrado P2 / Turma B · Grupo 1", font=fonte(21), fill=DESTAQUE)
    draw.text((67, 120), titulo, font=fonte(47), fill=TEXTO)
    draw.text((69, 194), subtitulo, font=fonte(27), fill=DESTAQUE)
    if isinstance(conteudo, Image.Image):
        conteudo.thumbnail((1120, 335), Image.Resampling.LANCZOS)
        img.paste(conteudo, (69 + (1120 - conteudo.width) // 2, 270))
    else:
        for idx, row in enumerate(conteudo):
            draw.text((70, 298 + idx * 57), row, font=fonte(31), fill=TEXTO)
    draw.text((68, 652), referencia, font=fonte(19), fill=DESTAQUE)
    img.save(destino)


def comando(*args):
    subprocess.run(args, check=True)


def render():
    cenas = [
        (
            "Publicação na interface",
            "CT-014 / EX-014 · Cadastro da publicação com uma conta fictícia",
            "Captura da rodada manual · Conteúdo e autoria na lista de publicações",
            captura("CT-014_2026-11-19.jpg", (464, 0, 1456, 248)),
            "No caso quatorze, a conta de teste criou uma publicação. O Flaskr exibiu o título, o texto e o autor na lista. Este é o registro real da execução manual.",
        ),
        (
            "Navegação por teclado",
            "CT-028 / EX-029 · Publicação concluída no Safari",
            "Captura no Safari · A preferência de navegação por Tab voltou à configuração original",
            captura("CT-028_2026-11-19_EX-029_02_post_publicado.jpg", (350, 145, 2298, 582)),
            "A primeira tentativa ficou bloqueada na configuração do navegador. No reteste, a navegação com Tab permitiu concluir o cadastro, o login e a publicação no Safari.",
        ),
        (
            "Falha controlada do TDD",
            "Os novos casos verificam criação e edição com título só de espaços",
            "Trecho do log local RED · GitHub Actions 44590229007",
            linhas("2026-11-19_tdd_red.txt", ["E       assert 302 == 200", "2 failed in", "Código de saída pytest"]),
            "Na fase Red, os dois testes falharam pelo motivo esperado. As rotas aceitaram o título de espaços e responderam com redirecionamento, quando deveriam manter o formulário aberto.",
        ),
        (
            "Regressão após a correção",
            "Criação e edição passam a compartilhar a validação de título",
            "Trecho do console do GitHub Actions · Execução 44590346309",
            linhas("2026-11-19_actions_refactor.txt", ["34 passed in", "7 passed in", "Códigos de saída: pytest"]),
            "Na execução final do GitHub Actions, passaram trinta e quatro testes Python, onze cenários no Newman e sete fluxos no Selenium. As três suítes terminaram com código zero.",
        ),
    ]

    with tempfile.TemporaryDirectory(prefix="p2-flaskr-video-") as tmp:
        pasta = Path(tmp)
        clipes = []
        for idx, (titulo, subtitulo, referencia, conteudo, fala) in enumerate(cenas):
            imagem, audio, clip = [pasta / f"{idx}.{ext}" for ext in ("png", "aiff", "mp4")]
            quadro(imagem, titulo, subtitulo, referencia, conteudo)
            comando("say", "-v", "Luciana", "-r", "157", "-o", str(audio), fala)
            comando(
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-loop", "1", "-framerate", "25", "-i", str(imagem), "-i", str(audio),
                "-af", "apad=pad_dur=0.8", "-shortest",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "22",
                "-c:a", "aac", "-b:a", "80k", "-ar", "44100", str(clip),
            )
            clipes.append(f"file '{clip.name}'")
        lista = pasta / "lista.txt"
        lista.write_text("\n".join(clipes) + "\n", encoding="utf-8")
        comando(
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
            "-i", str(lista), "-c", "copy", "-movflags", "+faststart", str(DESTINO),
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    render()
