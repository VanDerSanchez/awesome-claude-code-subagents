"""
LinkedIn carrusel PDF for Grupo Piroval — 9 slides, 1080x1350 each.
Output: linkedin-piroval/carrusel-caso-automocion.pdf
"""
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

W, H = 1080, 1350

# Palette
DARK = (15, 15, 15)
DARK_2 = (26, 26, 26)
DARK_3 = (44, 44, 44)
WHITE = (255, 255, 255)
OFF_WHITE = (246, 246, 246)
GRAY = (120, 120, 120)
GRAY_LIGHT = (180, 180, 180)
GRAY_DARK = (60, 60, 60)
GRAY_ULTRA_LIGHT = (220, 220, 220)
RED = (200, 16, 46)
RED_DARK = (150, 12, 34)
RED_SOFT = (232, 90, 110)

FD = "/usr/share/fonts/truetype/dejavu"
def F(style, size):
    fn = {
        "b": "DejaVuSans-Bold.ttf",
        "r": "DejaVuSans.ttf",
        "o": "DejaVuSans-Oblique.ttf",
    }[style]
    return ImageFont.truetype(f"{FD}/{fn}", size)


def text_w(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def text_h(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


def wrap_text(draw, text, font, max_w):
    """Word-wrap text to fit within max_w pixels."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, font, fill, max_w, line_spacing=1.25):
    x, y = xy
    lines = wrap_text(draw, text, font, max_w)
    th = text_h(draw, "Mg", font)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += int(th * line_spacing)
    return y


def draw_logo_monogram(draw, x, y, size=72, red=RED, white=WHITE):
    draw.rectangle([x, y, x + size, y + size], fill=red)
    font = F("b", int(size * 0.55))
    bbox = draw.textbbox((0, 0), "GP", font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x + (size - tw) // 2 - 1, y + (size - th) // 2 - 6), "GP", font=font, fill=white)


def draw_footer(draw, idx, total, on_dark=False):
    fg = GRAY_LIGHT if on_dark else GRAY
    # Logo mini + wordmark
    y_logo = H - 82
    draw_logo_monogram(draw, 60, y_logo, size=40)
    brand_color = WHITE if on_dark else DARK
    draw.text((60 + 40 + 14, y_logo + 2), "GRUPO", font=F("r", 12), fill=GRAY_LIGHT if on_dark else GRAY)
    draw.text((60 + 40 + 14, y_logo + 17), "PIROVAL", font=F("b", 18), fill=brand_color)
    # Slide indicator
    idx_txt = f"{idx} / {total}"
    tw = text_w(draw, idx_txt, F("b", 18))
    draw.text((W - 60 - tw, y_logo + 18), idx_txt, font=F("b", 18), fill=fg)


def new_slide(bg=OFF_WHITE):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)


def red_accent(draw, x, y, w=80, h=6):
    draw.rectangle([x, y, x + w, y + h], fill=RED)


# -------------------------------------------------------------
# SLIDE 1 — Portada (hook)
# -------------------------------------------------------------
def slide_1():
    img, d = new_slide(DARK)
    # Subtle blueprint grid
    for yy in range(0, H, 22):
        d.line([(0, yy), (W, yy)], fill=DARK_2, width=1)
    for xx in range(0, W, 22):
        d.line([(xx, 0), (xx, H)], fill=DARK_2, width=1)

    # Top tag
    d.text((80, 110), "CASO DE ÉXITO  ·  AUTOMOCIÓN", font=F("b", 22), fill=RED)

    # Hero numbers — stacked vertically with red dash between
    hero_font = F("b", 190)
    w10 = text_w(d, "10°C", hero_font)
    w80 = text_w(d, "80°C", hero_font)
    d.text(((W - w10) // 2, 195), "10°C", font=hero_font, fill=WHITE)
    # Red dash divider
    d.rectangle([(W - 120) // 2, 410, (W + 120) // 2, 420], fill=RED)
    d.text(((W - w80) // 2, 435), "80°C", font=hero_font, fill=WHITE)

    # Sub hero
    y = 690
    d.text((80, y), "Temperatura constante.", font=F("b", 52), fill=WHITE)
    d.text((80, y + 68), "Llueva o haga 35° fuera.", font=F("b", 52), fill=GRAY_LIGHT)

    # Divider
    red_accent(d, 80, 860, w=100, h=6)

    # Body
    body = (
        "Cómo diseñamos un equipo térmico a medida "
        "para el curado de un adhesivo estructural "
        "en un proveedor de automoción."
    )
    draw_wrapped(d, (80, 900), body, F("r", 32), GRAY_LIGHT, max_w=W - 160)

    # CTA
    d.text((80, 1150), "Desliza  →", font=F("b", 34), fill=RED)

    draw_footer(d, 1, 9, on_dark=True)
    return img


# -------------------------------------------------------------
# SLIDE 2 — El reto
# -------------------------------------------------------------
def slide_2():
    img, d = new_slide(OFF_WHITE)
    d.text((80, 110), "01  ·  EL RETO", font=F("b", 22), fill=RED)

    d.text((80, 170), "El problema", font=F("b", 84), fill=DARK)
    d.text((80, 260), "del cliente", font=F("b", 84), fill=GRAY)

    red_accent(d, 80, 390, w=100, h=6)

    body = (
        "Un fabricante de componentes de "
        "automoción necesitaba curar un "
        "adhesivo estructural en una ventana "
        "térmica muy estrecha."
    )
    y = draw_wrapped(d, (80, 440), body, F("r", 38), DARK, max_w=W - 160, line_spacing=1.35)

    d.text((80, y + 40), "Fuera de esa ventana:", font=F("b", 34), fill=DARK)

    bullets = [
        "Uniones débiles",
        "Piezas rechazadas",
        "Retrabajo y paradas de línea",
    ]
    by = y + 100
    for b in bullets:
        d.rectangle([80, by + 20, 100, by + 28], fill=RED)
        d.text((120, by), b, font=F("b", 34), fill=DARK)
        by += 62

    draw_footer(d, 2, 9, on_dark=False)
    return img


# -------------------------------------------------------------
# SLIDE 3 — Por qué un horno estándar no servía
# -------------------------------------------------------------
def slide_3():
    img, d = new_slide(DARK)
    for yy in range(0, H, 22):
        d.line([(0, yy), (W, yy)], fill=DARK_2, width=1)

    d.text((80, 110), "02  ·  POR QUÉ NO VALÍA UN HORNO DE CATÁLOGO", font=F("b", 22), fill=RED)

    d.text((80, 180), "Un horno estándar", font=F("b", 72), fill=WHITE)
    d.text((80, 260), "solo aporta", font=F("b", 72), fill=WHITE)
    d.text((80, 340), "CALOR.", font=F("b", 96), fill=RED)

    red_accent(d, 80, 490, w=100, h=6)

    body = (
        "La temperatura ambiente de una nave "
        "industrial varía más de 20°C entre "
        "invierno y verano."
    )
    y = draw_wrapped(d, (80, 540), body, F("r", 38), GRAY_LIGHT, max_w=W - 160, line_spacing=1.35)

    body2 = (
        "Necesitábamos un equipo capaz de "
        "aportar FRÍO o CALOR según el día."
    )
    draw_wrapped(d, (80, y + 30), body2, F("b", 40), WHITE, max_w=W - 160, line_spacing=1.3)

    # Icon cues: cold / hot
    d.text((80, 1020), "❄  Frío", font=F("b", 44), fill=GRAY_LIGHT)
    d.text((560, 1020), "☼  Calor", font=F("b", 44), fill=RED)

    draw_footer(d, 3, 9, on_dark=True)
    return img


# -------------------------------------------------------------
# SLIDE 4 — La solución
# -------------------------------------------------------------
def slide_4():
    img, d = new_slide(RED)
    # decorative red deeper band
    d.rectangle([0, 0, W, 180], fill=RED_DARK)
    d.text((80, 110), "03  ·  LA SOLUCIÓN", font=F("b", 22), fill=WHITE)

    d.text((80, 240), "Túnel térmico", font=F("b", 88), fill=WHITE)
    d.text((80, 340), "bidireccional", font=F("b", 88), fill=WHITE)
    d.text((80, 440), "a medida.", font=F("b", 88), fill=(255, 220, 220))

    # big specs card
    card_y = 620
    card_h = 560
    d.rectangle([60, card_y, W - 60, card_y + card_h], fill=WHITE)
    d.rectangle([60, card_y, 72, card_y + card_h], fill=DARK)

    specs = [
        ("RANGO OPERATIVO", "10°C – 80°C"),
        ("APORTE TÉRMICO", "Frío  o  calor"),
        ("TRANSPORTE", "Cinta con separadores a medida"),
        ("PROCESO", "En continuo, integrable en línea"),
    ]
    sy = card_y + 40
    for label, val in specs:
        d.text((110, sy), label, font=F("b", 20), fill=GRAY)
        d.text((110, sy + 28), val, font=F("b", 42), fill=DARK)
        sy += 130

    draw_footer(d, 4, 9, on_dark=True)
    return img


# -------------------------------------------------------------
# SLIDE 5 — Diseñado para la pieza
# -------------------------------------------------------------
def slide_5():
    img, d = new_slide(OFF_WHITE)
    d.text((80, 110), "04  ·  DISEÑO A MEDIDA", font=F("b", 22), fill=RED)

    d.text((80, 180), "Diseñado", font=F("b", 88), fill=DARK)
    d.text((80, 280), "para la pieza.", font=F("b", 88), fill=DARK)
    d.text((80, 380), "No al revés.", font=F("b", 72), fill=RED)

    red_accent(d, 80, 520, w=100, h=6)

    body = (
        "Separadores fabricados a medida de "
        "cada componente. La pieza entra, "
        "transita por el túnel a temperatura "
        "controlada y sale lista para la "
        "siguiente estación."
    )
    y = draw_wrapped(d, (80, 570), body, F("r", 36), DARK, max_w=W - 160, line_spacing=1.35)

    d.text((80, y + 40), "Sin manipulación manual entre etapas.", font=F("b", 34), fill=RED)

    # Decorative conveyor-like dashes
    cy = 1120
    for i in range(12):
        cx = 80 + i * 78
        d.rectangle([cx, cy, cx + 48, cy + 10], fill=DARK)

    draw_footer(d, 5, 9, on_dark=False)
    return img


# -------------------------------------------------------------
# SLIDE 6 — Zoom técnico
# -------------------------------------------------------------
def slide_6():
    img, d = new_slide(DARK)
    for yy in range(0, H, 22):
        d.line([(0, yy), (W, yy)], fill=DARK_2, width=1)

    d.text((80, 110), "05  ·  ZOOM TÉCNICO", font=F("b", 22), fill=RED)

    d.text((80, 180), "Control térmico,", font=F("b", 80), fill=WHITE)
    d.text((80, 280), "no solo calor.", font=F("b", 80), fill=GRAY_LIGHT)

    red_accent(d, 80, 420, w=100, h=6)

    items = [
        ("Aporte frío / calor", "Sistema bidireccional con consigna ajustable."),
        ("Cuadro eléctrico dedicado", "Control, protecciones y señalización."),
        ("Extracción forzada", "Ventilación y conducción industrial."),
        ("Trazabilidad", "Registro de temperatura compatible con exigencias OEM."),
    ]
    y = 490
    for title, sub in items:
        d.rectangle([80, y + 14, 100, y + 24], fill=RED)
        d.text((120, y), title, font=F("b", 34), fill=WHITE)
        d.text((120, y + 46), sub, font=F("r", 24), fill=GRAY_LIGHT)
        y += 130

    draw_footer(d, 6, 9, on_dark=True)
    return img


# -------------------------------------------------------------
# SLIDE 7 — Qué significa para ti
# -------------------------------------------------------------
def slide_7():
    img, d = new_slide(OFF_WHITE)
    d.text((80, 110), "06  ·  VALOR PARA TU LÍNEA", font=F("b", 22), fill=RED)

    d.text((80, 180), "Qué significa", font=F("b", 80), fill=DARK)
    d.text((80, 270), "para tu producción.", font=F("b", 64), fill=GRAY_DARK)

    red_accent(d, 80, 400, w=100, h=6)

    benefits = [
        ("Cero rechazos",
         "por ventana térmica perdida."),
        ("Producción estable",
         "en verano y en invierno."),
        ("Equipo móvil",
         "sobre ruedas, reubicable en la línea."),
        ("Un único interlocutor",
         "diseño, fabricación, puesta en marcha y SAT."),
    ]
    y = 470
    for title, sub in benefits:
        # Checkmark in red square
        d.rectangle([80, y, 120, y + 40], fill=RED)
        d.line([(90, y + 22), (102, y + 32)], fill=WHITE, width=4)
        d.line([(102, y + 32), (114, y + 14)], fill=WHITE, width=4)
        d.text((150, y - 4), title, font=F("b", 34), fill=DARK)
        d.text((150, y + 40), sub, font=F("r", 26), fill=GRAY_DARK)
        y += 130

    draw_footer(d, 7, 9, on_dark=False)
    return img


# -------------------------------------------------------------
# SLIDE 8 — Quiénes somos
# -------------------------------------------------------------
def slide_8():
    img, d = new_slide(DARK)
    # Big monogram watermark
    draw_logo_monogram(d, 740, 180, size=260)
    d.text((80, 110), "07  ·  QUIÉNES SOMOS", font=F("b", 22), fill=RED)

    d.text((80, 220), "Grupo", font=F("b", 96), fill=WHITE)
    d.text((80, 325), "Piroval.", font=F("b", 96), fill=WHITE)

    red_accent(d, 80, 475, w=100, h=6)

    d.text((80, 520), "Hornos, secaderos e incineradores", font=F("b", 36), fill=WHITE)
    d.text((80, 570), "para la industria.", font=F("b", 36), fill=RED)

    body = (
        "Diseñamos y fabricamos equipos térmicos "
        "industriales a medida. Cada equipo se "
        "diseña alrededor de tu proceso — no al "
        "contrario."
    )
    y = draw_wrapped(d, (80, 670), body, F("r", 30), GRAY_LIGHT, max_w=W - 160, line_spacing=1.35)

    d.text((80, y + 50), "SECTORES", font=F("b", 20), fill=RED)
    sectors = "Automoción   ·   Cerámica   ·   Química   ·   Alimentación"
    d.text((80, y + 82), sectors, font=F("b", 24), fill=WHITE)

    draw_footer(d, 8, 9, on_dark=True)
    return img


# -------------------------------------------------------------
# SLIDE 9 — CTA
# -------------------------------------------------------------
def slide_9():
    img, d = new_slide(RED)
    d.rectangle([0, 0, W, 180], fill=RED_DARK)
    d.text((80, 110), "08  ·  HABLEMOS", font=F("b", 22), fill=WHITE)

    d.text((80, 240), "¿Tu proceso", font=F("b", 88), fill=WHITE)
    d.text((80, 340), "tiene una ventana", font=F("b", 88), fill=WHITE)
    d.text((80, 440), "térmica crítica?", font=F("b", 88), fill=(255, 220, 220))

    # White card
    card_y = 640
    card_h = 480
    d.rectangle([60, card_y, W - 60, card_y + card_h], fill=WHITE)
    d.rectangle([60, card_y, 72, card_y + card_h], fill=DARK)

    d.text((110, card_y + 50), "Cuéntanos tu caso.", font=F("b", 44), fill=DARK)
    body = (
        "Evaluamos si un equipo térmico a medida "
        "encaja y te damos presupuesto sin "
        "compromiso, con ingeniería incluida."
    )
    y = draw_wrapped(d, (110, card_y + 130), body, F("r", 28), GRAY_DARK, max_w=W - 240, line_spacing=1.35)

    # Contact block
    d.text((110, y + 40), "WEB", font=F("b", 18), fill=GRAY)
    d.text((110, y + 66), "grupopiroval.com", font=F("b", 32), fill=RED)

    d.text((560, y + 40), "CONTACTO", font=F("b", 18), fill=GRAY)
    d.text((560, y + 66), "info@grupopiroval.com", font=F("b", 28), fill=DARK)

    draw_footer(d, 9, 9, on_dark=True)
    return img


# -------------------------------------------------------------
# Build PDF
# -------------------------------------------------------------
slides = [
    slide_1(), slide_2(), slide_3(), slide_4(), slide_5(),
    slide_6(), slide_7(), slide_8(), slide_9(),
]

out_dir = "/home/user/awesome-claude-code-subagents/linkedin-piroval"
os.makedirs(out_dir, exist_ok=True)

pdf_path = f"{out_dir}/carrusel-caso-automocion.pdf"
slides[0].save(
    pdf_path, "PDF", resolution=150.0, save_all=True, append_images=slides[1:]
)
print(f"PDF: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")

# Also save individual PNG previews (handy)
for i, s in enumerate(slides, 1):
    s.save(f"{out_dir}/slide-{i:02d}.png", "PNG", optimize=True)
print("Slide PNG previews written.")
