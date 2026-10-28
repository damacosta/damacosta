"""Gera o GIF de terminal do perfil da Danielle (Dandan) no GitHub.

Feito com a biblioteca gifos (pip install github-readme-terminal).
O GitHub Actions roda este arquivo todo dia e publica o output.gif
na branch "gifos". Para testar no seu computador sem token, rode:
    PREVIEW=1 python main.py
"""

import os
from datetime import datetime
from zoneinfo import ZoneInfo

import gifos

USUARIO = "damacosta"
FUSO = ZoneInfo("America/Sao_Paulo")

# Cores ANSI (a paleta "dandan" está em gifos-colors/ansi_escape_colors.toml)
CORAL, VERDE, AMARELO, LILAS, CIANO, SUAVE = "91", "92", "93", "94", "96", "90"
R = "\x1b[0m"


def cor(codigo, texto):
    return f"\x1b[{codigo}m{texto}{R}"


def titulo(texto):
    # Texto escuro sobre fundo coral, como uma etiqueta
    return f"\x1b[30;101m {texto} {R}"


# O cachorro da Danielle em pixel art: caramelo, orelhas caídas mais escuras,
# peito e patinhas brancas, língua de fora e a coleira roxa com sininho.
# B = pelo caramelo, D = orelhas e rabo, L = focinho, E = olho, W = branco,
# N = nariz, T = língua, R = coleira, Y = sininho, . = fundo
CACHORRO = [
    "......BBBBBB......",
    "....BBBBBBBBBB....",
    "..DDBBBBBBBBBBDD..",
    ".DDDBBBBBBBBBBDDD.",
    ".DDDBEEBBBBEEBDDD.",
    ".DDDBEWBBBBEWBDDD.",
    ".DDDBBBBLLBBBBDDD.",
    "..DDBBBLNNLBBBDD..",
    "..DD.BBLLLLBB.DD..",
    "......BLTTLB......",
    ".......BBBB.......",
    "....RRRRYRRRR.....",
    "....BBBWWWBBB...D.",
    "...BBBWWWWWBBB.DD.",
    "...BBBBWWWBBBBDD..",
    "...BBBBBBBBBBBD...",
    "...BB.BB..BB.BB...",
    "...WW.WW..WW.WW...",
]
CORES_PIXEL = {
    "B": "#C27A3E", "D": "#6B3F22", "L": "#E3A86C", "W": "#FFF8F1",
    "E": "#2A170C", "N": "#120D20", "T": "#FF8FA3", "R": "#7B4FE0",
    "Y": "#FFC83D", ".": "#1C1530",
}
TAMANHO_PIXEL = 12


def gerar_cachorro(arquivo="cachorro.png"):
    """Desenha o cachorro como imagem PNG (pixels sem frestas entre as linhas)."""
    from PIL import Image, ImageDraw

    largura, altura = len(CACHORRO[0]), len(CACHORRO)
    img = Image.new("RGB", (largura * TAMANHO_PIXEL, altura * TAMANHO_PIXEL))
    draw = ImageDraw.Draw(img)
    for y, linha in enumerate(CACHORRO):
        for x, p in enumerate(linha):
            draw.rectangle(
                [x * TAMANHO_PIXEL, y * TAMANHO_PIXEL,
                 (x + 1) * TAMANHO_PIXEL - 1, (y + 1) * TAMANHO_PIXEL - 1],
                fill=CORES_PIXEL[p],
            )
    img.save(arquivo)
    return arquivo


def estatisticas():
    """Busca os números do GitHub. No modo PREVIEW usa valores de exemplo."""
    if os.getenv("PREVIEW"):
        return {
            "repos": "31",
            "commits": "--",
            "prs": "--",
            "linguagens": "TypeScript, PHP, JavaScript",
        }
    dados = gifos.utils.fetch_github_stats(USUARIO)
    linguagens = [lang[0] for lang in dados.languages_sorted][:3]
    return {
        "repos": str(dados.total_repo_contributions),
        "commits": str(dados.total_commits_last_year),
        "prs": str(dados.total_pull_requests_made),
        "linguagens": ", ".join(linguagens),
    }


def main():
    t = gifos.Terminal(width=750, height=500, xpad=15, ypad=15)
    t.set_fps(15)
    t.set_prompt(f"{cor(CORAL, 'dandan')}@{cor(AMARELO, 'he4rt')} {cor(LILAS, '~>')} ")
    ano = datetime.now(FUSO).strftime("%Y")

    # 1. "Liga" o computador
    t.gen_text("", 1, count=15)
    t.toggle_show_cursor(False)
    t.gen_text("DandanOS BIOS v2.0.26", 1)
    t.gen_text(f"Copyright (C) {ano}, {cor(CORAL, '<Danielle::Costa> Inc.')}", 2)
    t.gen_text(cor(LILAS, "Kernel: Criatividade + Funcionalidade"), 4)
    t.gen_text("Processador: Cafe(tm) Quad-Core", 5)
    for i in range(0, 65537, 8192):
        t.delete_row(7)
        t.gen_text(f"Teste de memoria: {i} KB", 7, count=2, contin=True)
    t.delete_row(7)
    t.gen_text(f"Teste de memoria: 64 MB {cor(VERDE, 'OK')}", 7, count=10, contin=True)

    # 2. Logo com efeito de embaralhar letras
    t.clear_frame()
    t.gen_text("Iniciando o sistema ", 1)
    t.gen_typing_text(".....", 1, contin=True)
    logo = "D A N D A N   O S"
    linha_meio = (t.num_rows + 1) // 2
    coluna_meio = (t.num_cols - len(logo) + 1) // 2
    for quadro in gifos.effects.text_scramble_effect_lines(logo, 3, include_special=False):
        t.delete_row(linha_meio)
        t.gen_text(cor(CORAL, quadro), linha_meio, coluna_meio)
    t.gen_text(cor(SUAVE, "sites com personalidade"), linha_meio + 2, coluna_meio - 1, count=15)

    # 3. Login
    t.clear_frame()
    t.gen_text(cor(AMARELO, "DandanOS v2.0.26 (tty1)"), 1, count=5)
    t.gen_text("login: ", 3, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("dandan", 3, contin=True)
    t.toggle_show_cursor(False)
    t.gen_text("senha: ", 4, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("************", 4, contin=True)
    t.toggle_show_cursor(False)
    agora = datetime.now(FUSO).strftime("%d/%m/%Y %H:%M")
    t.gen_text(f"Ultimo login: {agora} no tty1", 6)

    # 4. O "fetch" com o cachorro e as informações
    t.gen_prompt(8, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text(cor(VERDE, "clear"), 8, contin=True)
    t.clear_frame()
    t.gen_prompt(1)
    t.gen_typing_text(cor(VERDE, "fetch.sh") + " -u dandan", 1, contin=True)
    t.toggle_show_cursor(False)

    t.paste_image(gerar_cachorro(), 3, 3)

    s = estatisticas()
    info = f"""{titulo('Danielle Costa @ GitHub')}
{cor(SUAVE, '--------------------------')}
{cor(CIANO, 'Funcao: ')} {cor(AMARELO, 'Desenvolvedora front-end')}
{cor(CIANO, 'Estudo: ')} {cor(AMARELO, 'Eng. da Computacao')} {cor(LILAS, '#UNIVESP')}
{cor(CIANO, 'Comunid:')} {cor(AMARELO, 'He4rt Developers')} {cor(LILAS, '<3')}
{cor(CIANO, 'Stack:  ')} {cor(AMARELO, 'React, Next.js, TS, PHP')}
{cor(CIANO, 'Freela: ')} {cor(VERDE, '[ON]')} {cor(AMARELO, 'sites e landing pages')}
{cor(CIANO, 'Pet:    ')} {cor(AMARELO, 'Scooby')} {cor(LILAS, '(o doguinho ao lado)')}

{titulo('Contato')}
{cor(SUAVE, '--------------------------')}
{cor(CIANO, 'Site:    ')} {cor(AMARELO, 'daniellecosta.dev.br')}
{cor(CIANO, 'LinkedIn:')} {cor(AMARELO, 'daniellecostadev')}

{titulo('GitHub')}
{cor(SUAVE, '--------------------------')}
{cor(CIANO, 'Commits no ano:')} {cor(AMARELO, s['commits'])}
{cor(CIANO, 'Pull requests: ')} {cor(AMARELO, s['prs'])}
{cor(CIANO, 'Linguagens:    ')} {cor(AMARELO, s['linguagens'])}"""
    t.gen_text(info, 3, 32, count=5, contin=True)
    t.gen_prompt(t.curr_row + 2)
    t.save_frame("screenshot.png")
    t.toggle_show_cursor(True)
    t.gen_text("", t.curr_row, count=60, contin=True)

    # 5. Recado final
    t.gen_typing_text(cor(VERDE, "echo") + ' "bora tirar seu site do papel?"', t.curr_row, contin=True)
    t.toggle_show_cursor(False)
    t.gen_text(cor(CORAL, "bora tirar seu site do papel?"), t.curr_row + 1, count=60)

    t.gen_gif()


if __name__ == "__main__":
    main()
