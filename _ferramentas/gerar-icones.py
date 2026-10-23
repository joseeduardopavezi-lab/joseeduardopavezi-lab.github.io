# Gera todos os ícones do site a partir do mesmo desenho (o símbolo do avatar.svg do kit da marca),
# para que o ícone do app no TikTok, o favicon e a logo do site sejam idênticos.
# Uso: python _ferramentas/gerar-icones.py  (precisa de Pillow; a pasta _ferramentas não é publicada)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SITE = Path(__file__).resolve().parent.parent
FONTS = Path(__file__).resolve().parents[2] / 'Codex' / 'Projetos' / 'Fio-do-Corte' / 'fontes'
GRAFITE, LARANJA, PAPEL, CINZA = '#101114', '#FF5B35', '#F5F0E8', '#B1B0AE'

# Coordenadas do avatar.svg (quadro de 1080).
RECTS = [(270, 270, 205.2, 64.8), (270, 270, 64.8, 356.4), (604.8, 745.2, 205.2, 64.8), (745.2, 453.6, 64.8, 356.4)]
CUT = [(405, 756), (518.4, 756), (680.4, 324), (567, 324)]


def symbol(draw, scale, dx=0, dy=0, color=LARANJA):
    for x, y, w, h in RECTS:
        draw.rectangle([dx + x * scale, dy + y * scale, dx + (x + w) * scale - 1, dy + (y + h) * scale - 1], fill=color)
    draw.polygon([(dx + x * scale, dy + y * scale) for x, y in CUT], fill=color)


def icon(size):
    big = 4096
    img = Image.new('RGB', (big, big), GRAFITE)
    symbol(ImageDraw.Draw(img), big / 1080)
    return img.resize((size, size), Image.LANCZOS)


master = icon(1024)
master.save(SITE / 'icon-1024.png', optimize=True)
for size, name in [(512, 'icon-512.png'), (192, 'icon-192.png'), (180, 'apple-touch-icon.png')]:
    icon(size).save(SITE / name, optimize=True)
icon(256).save(SITE / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])

svg = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>' for x, y, w, h in RECTS)
(SITE / 'icon.svg').write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080"><title>Fio do Corte Studio</title>'
    f'<rect width="1080" height="1080" fill="{GRAFITE}"/><g fill="{LARANJA}">{svg}'
    f'<polygon points="{" ".join(f"{x},{y}" for x, y in CUT)}"/></g></svg>\n', encoding='utf-8')

# Imagem de compartilhamento (1200 x 630): o mesmo ícone ao lado do nome.
og = Image.new('RGB', (2400, 1260), GRAFITE)
og.paste(icon(720), (180, 270))
d = ImageDraw.Draw(og)
title = ImageFont.truetype(str(FONTS / 'BarlowCondensed-ExtraBold.ttf'), 210)
body = ImageFont.truetype(str(FONTS / 'Inter.ttf'), 58)
body.set_variation_by_axes([24, 500])
d.text((1020, 330), 'FIO DO CORTE', font=title, fill=PAPEL)
d.text((1020, 530), 'STUDIO', font=title, fill=LARANJA)
d.multiline_text((1024, 800), 'Clips from long conversations,\napproved by the creator before every post.', font=body, fill=CINZA, spacing=22)
og.resize((1200, 630), Image.LANCZOS).save(SITE / 'og.png', optimize=True)
print('ok')
