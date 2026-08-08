import io
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
FONT_BOLD = os.path.join(ASSETS_DIR, "Poppins-Bold.ttf")
FONT_REGULAR = os.path.join(ASSETS_DIR, "Poppins-Regular.ttf")

WIDTH, HEIGHT = 1024, 576

# Colores de marca (paleta oscura cripto: negro/morado con acento dorado)
BG_TOP = (13, 10, 24)
BG_BOTTOM = (30, 16, 48)
ACCENT_GOLD = (240, 185, 80)
ACCENT_PURPLE = (130, 70, 220)
TEXT_WHITE = (245, 245, 250)


def _vertical_gradient(draw, width, height, top_color, bottom_color):
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))


def _wrap_headline(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def generate_news_image(headline, tag="CRIPTO"):
    """
    Genera una imagen de plantilla 1024x576 con el titular de la noticia,
    marca Alphax News y una etiqueta de categoría. Devuelve bytes PNG.
    """
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    _vertical_gradient(draw, WIDTH, HEIGHT, BG_TOP, BG_BOTTOM)

    # Franja de acento diagonal simple (rectángulo fino dorado arriba)
    draw.rectangle([(0, 0), (WIDTH, 8)], fill=ACCENT_GOLD)

    # Etiqueta de categoría
    tag_font = ImageFont.truetype(FONT_BOLD, 28)
    draw.text((60, 60), tag.upper(), font=tag_font, fill=ACCENT_GOLD)

    # Titular, centrado verticalmente, envuelto en varias líneas
    headline_font = ImageFont.truetype(FONT_BOLD, 54)
    max_text_width = WIDTH - 120
    lines = _wrap_headline(draw, headline, headline_font, max_text_width)[:5]

    line_height = 66
    total_height = len(lines) * line_height
    start_y = (HEIGHT - total_height) // 2

    for i, line in enumerate(lines):
        draw.text((60, start_y + i * line_height), line, font=headline_font, fill=TEXT_WHITE)

    # Marca en la esquina inferior
    brand_font = ImageFont.truetype(FONT_REGULAR, 26)
    draw.text((60, HEIGHT - 70), "ALPHAX NEWS", font=brand_font, fill=ACCENT_PURPLE)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()
