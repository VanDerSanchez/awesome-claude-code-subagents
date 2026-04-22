"""
LinkedIn carrusel PDF for Grupo Piroval — 9 slides, 1080x1350 each.
V2: logo real y fotos del taller embebidas.
Output: linkedin-piroval/carrusel-caso-automocion.pdf
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = "/home/user/awesome-claude-code-subagents/linkedin-piroval"

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


# Load logo once (RGBA to preserve transparency)
LOGO = Image.open(f"{ROOT}/logo-piroval.png").convert("RGBA")

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


def paste_logo(img, x, y, height, invert_for_dark=False):
    """Paste the real Piroval logo at a target height, keeping aspect ratio."""
    ratio = LOGO.width / LOGO.height
    target_w = int(height * ratio)
    logo_resized = LOGO.resize((target_w, height), Image.LANCZOS)
    img.paste(logo_resized, (x, y), logo_resized)


def draw_footer(img, draw, idx, total, on_dark=False):
    fg = GRAY_LIGHT if on_dark else GRAY
    y_logo = H - 92
    # Paste real logo (scaled small)
    logo_h = 60
    paste_logo(img, 60, y_logo, logo_h)
    # Slide indicator
    idx_txt = f"{idx} / {total}"
    tw = text_w(draw, idx_txt, F("b", 18))
    draw.text((W - 60 - tw, y_logo + 22), idx_txt, font=F("b", 18), fill=fg)


def new_slide(bg=OFF_WHITE):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)


def red_accent(draw, x, y, w=80, h=6):
    draw.rectangle([x, y, x + w, y + h], fill=RED)


def load_photo(name, target_w, target_h, darken=0.0):
    """Load a photo, cover-crop to target dimensions, optionally darken."""
    p = Image.open(f"{ROOT}/{name}").convert("RGB")
    # Cover crop
    src_ratio = p.width / p.height
    dst_ratio = target_w / target_h
    if src_ratio > dst_ratio:
        # Source wider: crop width
        new_w = int(p.height * dst_ratio)
        off = (p.width - new_w) // 2
        p = p.crop((off, 0, off + new_w, p.height))
    else:
        new_h = int(p.width / dst_ratio)
        off = (p.height - new_h) // 2
        p = p.crop((0, off, p.width, off + new_h))
    p = p.resize((target_w, target_h), Image.LANCZOS)
    if darken > 0:
        overlay = Image.new("RGB", (target_w, target_h), (0, 0, 0))
        p = Image.blend(p, overlay, darken)
    return p


# -------------------------------------------------------------
# SLIDE 1 — Portada (hook) con foto de fondo
# -------------------------------------------------------------
def slide_1():
    img, d = new_slide(DARK)

    # Background photo darkened
    photo = load_photo("IMG_3900.jpeg", W, H, darken=0.70)
    img.paste(photo, (0, 0))
    d = ImageDraw.Draw(img)

    # Top tag
    d.text((80, 110), "CASO DE ÉXITO  ·  AUTOMOCIÓN", font=F("b", 22), fill=RED)

    # Hero numbers — stacked vertically with red dash between
    hero_font = F("b", 180)
    w10 = text_w(d, "10°C", hero_font)
    w80 = text_w(d, "80°C", hero_font)
    d.text(((W - w10) // 2, 200), "10°C", font=hero_font, fill=WHITE)
    d.rectangle([(W - 120) // 2, 400, (W + 120) // 2, 410], fill=RED)
    d.text(((W - w80) // 2, 425), "80°C", font=hero_font, fill=WHITE)

    # Sub hero
    y = 670
    d.text((80, y), "Temperatura constante.", font=F("b", 52), fill=WHITE)
    d.text((80, y + 68), "Llueva o haga 35° fuera.", font=F("b", 52), fill=GRAY_LIGHT)

    red_accent(d, 80, 840, w=100, h=6)

    body = (
        "Cómo diseñamos un equipo térmico a medida "
        "para el curado de un adhesivo estructural "
        "en un proveedor de automoción."
    )
    draw_wrapped(d, (80, 880), body, F("r", 32), GRAY_LIGHT, max_w=W - 160)

    d.text((80, 1130), "Desliza  →", font=F("b", 34), fill=RED)

    draw_footer(img, d, 1, 9, on_dark=True)
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

    draw_footer(img, d, 2, 9, on_dark=False)
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

    d.text((80, 1020), "❄  Frío", font=F("b", 44), fill=GRAY_LIGHT)
    d.text((560, 1020), "☼  Calor", font=F("b", 44), fill=RED)

    draw_footer(img, d, 3, 9, on_dark=True)
    return img


# -------------------------------------------------------------
# SLIDE 4 — La solución (con foto del equipo entero)
# -------------------------------------------------------------
def slide_4():
    img, d = new_slide(RED)
    d.rectangle([0, 0, W, 180], fill=RED_DARK)
    d.text((80, 110), "03  ·  LA SOLUCIÓN", font=F("b", 22), fill=WHITE)

    d.text((80, 230), "Túnel térmico", font=F("b", 80), fill=WHITE)
    d.text((80, 320), "bidireccional.", font=F("b", 80), fill=(255, 220, 220))

    # Photo of the solution
    photo_h = 380
    photo_w = W - 120
    photo = load_photo("IMG_3901.jpeg", photo_w, photo_h)
    img.paste(photo, (60, 450))

    # Spec card bottom
    card_y = 870
    card_h = 300
    d = ImageDraw.Draw(img)
    d.rectangle([60, card_y, W - 60, card_y + card_h], fill=WHITE)
    d.rectangle([60, card_y, 72, card_y + card_h], fill=DARK)

    sy = card_y + 30
    # Two columns
    d.text((100, sy), "RANGO", font=F("b", 18), fill=GRAY)
    d.text((100, sy + 26), "10°C – 80°C", font=F("b", 36), fill=DARK)
    d.text((560, sy), "APORTE", font=F("b", 18), fill=GRAY)
    d.text((560, sy + 26), "Frío o calor", font=F("b", 36), fill=DARK)

    sy += 140
    d.text((100, sy), "TRANSPORTE", font=F("b", 18), fill=GRAY)
    d.text((100, sy + 26), "Cinta + separadores", font=F("b", 30), fill=DARK)
    d.text((560, sy), "PROCESO", font=F("b", 18), fill=GRAY)
    d.text((560, sy + 26), "En continuo", font=F("b", 30), fill=DARK)

    draw_footer(img, d, 4, 9, on_dark=True)
    return img


# -------------------------------------------------------------
# SLIDE 5 — Diseñado para la pieza (con foto cenital)
# -------------------------------------------------------------
def slide_5():
    img, d = new_slide(OFF_WHITE)
    d.text((80, 110), "04  ·  DISEÑO A MEDIDA", font=F("b", 22), fill=RED)

    d.text((80, 180), "Diseñado", font=F("b", 80), fill=DARK)
    d.text((80, 270), "para la pieza.", font=F("b", 80), fill=DARK)
    d.text((80, 360), "No al revés.", font=F("b", 64), fill=RED)

    # Photo showing the custom separators
    photo_h = 460
    photo_w = W - 120
    photo = load_photo("IMG_5495.jpeg", photo_w, photo_h)
    img.paste(photo, (60, 490))

    d = ImageDraw.Draw(img)
    d.text((80, 990), "Separadores a medida. Sin manipulación entre etapas.", font=F("b", 26), fill=DARK)

    draw_footer(img, d, 5, 9, on_dark=False)
    return img


# -------------------------------------------------------------
# SLIDE 6 — Zoom técnico (con foto del cuadro HIGH VOLTAGE)
# -------------------------------------------------------------
def slide_6():
    img, d = new_slide(DARK)

    # Photo darkened as side element
    photo_w = W
    photo_h = 500
    photo = load_photo("IMG_3902.jpeg", photo_w, photo_h, darken=0.35)
    img.paste(photo, (0, 0))

    d = ImageDraw.Draw(img)
    d.text((80, 110), "05  ·  ZOOM TÉCNICO", font=F("b", 22), fill=WHITE)
    d.text((80, 380), "Control térmico,", font=F("b", 60), fill=WHITE)
    d.text((80, 445), "no solo calor.", font=F("b", 60), fill=GRAY_LIGHT)

    red_accent(d, 80, 540, w=100, h=6)

    items = [
        ("Aporte frío / calor", "Sistema bidireccional con consigna ajustable."),
        ("Cuadro eléctrico dedicado", "Control, protecciones y señalización."),
        ("Extracción forzada", "Ventilación y conducción industrial."),
        ("Trazabilidad", "Registro compatible con exigencias OEM."),
    ]
    y = 610
    for title, sub in items:
        d.rectangle([80, y + 14, 100, y + 24], fill=RED)
        d.text((120, y), title, font=F("b", 30), fill=WHITE)
        d.text((120, y + 42), sub, font=F("r", 22), fill=GRAY_LIGHT)
        y += 120

    draw_footer(img, d, 6, 9, on_dark=True)
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
        ("Cero rechazos", "por ventana térmica perdida."),
        ("Producción estable", "en verano y en invierno."),
        ("Equipo móvil", "sobre ruedas, reubicable en la línea."),
        ("Un único interlocutor", "diseño, fabricación, puesta en marcha y SAT."),
    ]
    y = 470
    for title, sub in benefits:
        d.rectangle([80, y, 120, y + 40], fill=RED)
        d.line([(90, y + 22), (102, y + 32)], fill=WHITE, width=4)
        d.line([(102, y + 32), (114, y + 14)], fill=WHITE, width=4)
        d.text((150, y - 4), title, font=F("b", 34), fill=DARK)
        d.text((150, y + 40), sub, font=F("r", 26), fill=GRAY_DARK)
        y += 130

    draw_footer(img, d, 7, 9, on_dark=False)
    return img


# -------------------------------------------------------------
# SLIDE 8 — Quiénes somos (con logo real grande)
# -------------------------------------------------------------
def slide_8():
    img, d = new_slide(DARK)

    # Big logo as watermark on the right
    paste_logo(img, 680, 200, 340)

    d = ImageDraw.Draw(img)
    d.text((80, 110), "07  ·  QUIÉNES SOMOS", font=F("b", 22), fill=RED)

    d.text((80, 240), "Grupo", font=F("b", 88), fill=WHITE)
    d.text((80, 340), "Piroval.", font=F("b", 88), fill=WHITE)

    red_accent(d, 80, 480, w=100, h=6)

    d.text((80, 530), "Hornos, secaderos e incineradores", font=F("b", 34), fill=WHITE)
    d.text((80, 580), "para la industria.", font=F("b", 34), fill=RED)

    body = (
        "Diseñamos y fabricamos equipos térmicos "
        "industriales a medida. Cada equipo se "
        "diseña alrededor de tu proceso — no al "
        "contrario."
    )
    y = draw_wrapped(d, (80, 680), body, F("r", 28), GRAY_LIGHT, max_w=W - 160, line_spacing=1.35)

    d.text((80, y + 50), "SECTORES", font=F("b", 20), fill=RED)
    sectors = "Automoción   ·   Cerámica   ·   Química   ·   Alimentación"
    d.text((80, y + 82), sectors, font=F("b", 22), fill=WHITE)

    draw_footer(img, d, 8, 9, on_dark=True)
    return img


# -------------------------------------------------------------
# SLIDE 9 — CTA
# -------------------------------------------------------------
def slide_9():
    img, d = new_slide(RED)
    d.rectangle([0, 0, W, 180], fill=RED_DARK)
    d.text((80, 110), "08  ·  HABLEMOS", font=F("b", 22), fill=WHITE)

    d.text((80, 230), "¿Tu proceso", font=F("b", 84), fill=WHITE)
    d.text((80, 325), "tiene una ventana", font=F("b", 84), fill=WHITE)
    d.text((80, 420), "térmica crítica?", font=F("b", 84), fill=(255, 220, 220))

    card_y = 600
    card_h = 540
    d.rectangle([60, card_y, W - 60, card_y + card_h], fill=WHITE)
    d.rectangle([60, card_y, 72, card_y + card_h], fill=DARK)

    d.text((110, card_y + 50), "Cuéntanos tu caso.", font=F("b", 44), fill=DARK)
    body = (
        "Evaluamos si un equipo térmico a medida "
        "encaja y te damos presupuesto sin "
        "compromiso, con ingeniería incluida."
    )
    y = draw_wrapped(d, (110, card_y + 130), body, F("r", 28), GRAY_DARK, max_w=W - 240, line_spacing=1.35)

    d.text((110, y + 40), "WEB", font=F("b", 18), fill=GRAY)
    d.text((110, y + 66), "hornosysecaderos.com", font=F("b", 30), fill=RED)

    d.text((110, y + 130), "CONTACTO", font=F("b", 18), fill=GRAY)
    d.text((110, y + 156), "grupopiroval@grupopiroval.com", font=F("b", 26), fill=DARK)

    draw_footer(img, d, 9, 9, on_dark=True)
    return img


# -------------------------------------------------------------
# Build PDF
# -------------------------------------------------------------
slides = [
    slide_1(), slide_2(), slide_3(), slide_4(), slide_5(),
    slide_6(), slide_7(), slide_8(), slide_9(),
]

pdf_path = f"{ROOT}/carrusel-caso-automocion.pdf"
slides[0].save(
    pdf_path, "PDF", resolution=150.0, save_all=True, append_images=slides[1:]
)
print(f"PDF: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")

for i, s in enumerate(slides, 1):
    s.save(f"{ROOT}/slide-{i:02d}.png", "PNG", optimize=True)
print("Slide PNG previews written.")
