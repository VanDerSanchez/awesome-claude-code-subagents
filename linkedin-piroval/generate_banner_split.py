"""Generate LinkedIn company banner for Grupo Piroval — 1128x191 px."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1128, 191
LEFT_W = 420

DARK = (15, 15, 15)
DARK_2 = (26, 26, 26)
DARK_3 = (34, 34, 34)
WHITE = (255, 255, 255)
OFF_WHITE = (246, 246, 246)
GRAY = (110, 110, 110)
GRAY_LIGHT = (168, 168, 168)
GRAY_DARK = (55, 55, 55)
RED = (200, 16, 46)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def f(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)

font_mono = f("DejaVuSans-Bold.ttf", 30)
font_grupo = f("DejaVuSans.ttf", 15)
font_piroval = f("DejaVuSans-Bold.ttf", 26)
font_tag = f("DejaVuSans-Bold.ttf", 9)
font_title_es = f("DejaVuSans-Bold.ttf", 23)
font_title_en = f("DejaVuSans.ttf", 14)
font_sectors = f("DejaVuSans.ttf", 11)
font_url = f("DejaVuSans-Bold.ttf", 13)

img = Image.new("RGB", (W, H), OFF_WHITE)
draw = ImageDraw.Draw(img)

# --- LEFT PANEL (dark) ---
draw.rectangle([0, 0, LEFT_W, H], fill=DARK)

# Subtle horizontal lines (technical drawing vibe)
for y in range(0, H, 14):
    draw.line([(25, y), (LEFT_W - 25, y)], fill=DARK_2, width=1)

# Red vertical divider
draw.rectangle([LEFT_W - 3, 0, LEFT_W, H], fill=RED)

# Logo monogram: red square with "GP"
mono_size = 62
mx = 45
my = (H - mono_size) // 2
draw.rectangle([mx, my, mx + mono_size, my + mono_size], fill=RED)
gp = "GP"
bbox = draw.textbbox((0, 0), gp, font=font_mono)
gp_w = bbox[2] - bbox[0]
gp_h = bbox[3] - bbox[1]
draw.text(
    (mx + (mono_size - gp_w) // 2 - 1, my + (mono_size - gp_h) // 2 - 6),
    gp, font=font_mono, fill=WHITE,
)

# Wordmark
tx = mx + mono_size + 18
draw.text((tx, 62), "GRUPO", font=font_grupo, fill=GRAY_LIGHT)
draw.text((tx, 81), "PIROVAL", font=font_piroval, fill=WHITE)
draw.text((tx, 116), "HORNOS · SECADEROS · INCINERADORES", font=font_tag, fill=RED)

# --- RIGHT PANEL (light) ---
rx = LEFT_W + 35

# ES headline
draw.text((rx, 48), "Equipos térmicos industriales a medida", font=font_title_es, fill=DARK)

# Thin red underline under ES title (8 px wide accent)
draw.rectangle([rx, 84, rx + 36, 86], fill=RED)

# EN subtitle
draw.text((rx, 96), "Custom industrial thermal equipment", font=font_title_en, fill=GRAY)

# Sector line
draw.text((rx, 128), "Automoción  ·  Cerámica  ·  Química  ·  Alimentación", font=font_sectors, fill=GRAY_DARK)

# URL bottom-right
url = "grupopiroval.com"
bbox = draw.textbbox((0, 0), url, font=font_url)
url_w = bbox[2] - bbox[0]
ux = W - url_w - 28
uy = H - 30
draw.text((ux, uy), url, font=font_url, fill=RED)

# Save
OUT = "/home/user/awesome-claude-code-subagents/linkedin-banner-piroval.png"
img.save(OUT, "PNG", optimize=True)
print(f"Saved: {OUT} ({os.path.getsize(OUT)} bytes)  {W}x{H}")
