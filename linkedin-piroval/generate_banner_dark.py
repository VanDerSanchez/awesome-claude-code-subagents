"""Generate LinkedIn company banner for Grupo Piroval — dark variant 1128x191 px."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1128, 191

DARK = (15, 15, 15)
DARK_2 = (26, 26, 26)
DARK_3 = (38, 38, 38)
WHITE = (255, 255, 255)
OFF_WHITE = (236, 236, 236)
GRAY = (150, 150, 150)
GRAY_LIGHT = (180, 180, 180)
RED = (200, 16, 46)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def f(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)

font_mono = f("DejaVuSans-Bold.ttf", 30)
font_grupo = f("DejaVuSans.ttf", 15)
font_piroval = f("DejaVuSans-Bold.ttf", 26)
font_tag = f("DejaVuSans-Bold.ttf", 9)
font_title_es = f("DejaVuSans-Bold.ttf", 24)
font_title_en = f("DejaVuSans.ttf", 14)
font_sectors = f("DejaVuSans.ttf", 11)
font_url = f("DejaVuSans-Bold.ttf", 13)

img = Image.new("RGB", (W, H), DARK)
draw = ImageDraw.Draw(img)

# Very subtle blueprint-like grid
for y in range(0, H, 16):
    draw.line([(0, y), (W, y)], fill=DARK_2, width=1)
for x in range(0, W, 16):
    draw.line([(x, 0), (x, H)], fill=DARK_2, width=1)

# Left-side brand lockup area (no visible divider panel, continuous dark)
LEFT_W = 420

# Logo monogram
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

tx = mx + mono_size + 18
draw.text((tx, 62), "GRUPO", font=font_grupo, fill=GRAY_LIGHT)
draw.text((tx, 81), "PIROVAL", font=font_piroval, fill=WHITE)
draw.text((tx, 116), "HORNOS · SECADEROS · INCINERADORES", font=font_tag, fill=RED)

# Thin red vertical accent between brand and content (not full divider, just a mark)
draw.rectangle([LEFT_W - 3, 55, LEFT_W, H - 55], fill=RED)

# Content on right
rx = LEFT_W + 30

draw.text((rx, 48), "Equipos térmicos industriales a medida", font=font_title_es, fill=WHITE)
draw.rectangle([rx, 86, rx + 36, 88], fill=RED)
draw.text((rx, 98), "Custom industrial thermal equipment", font=font_title_en, fill=GRAY_LIGHT)
draw.text((rx, 130), "Automoción  ·  Cerámica  ·  Química  ·  Alimentación", font=font_sectors, fill=GRAY)

url = "hornosysecaderos.com"
bbox = draw.textbbox((0, 0), url, font=font_url)
url_w = bbox[2] - bbox[0]
ux = W - url_w - 28
uy = H - 30
draw.text((ux, uy), url, font=font_url, fill=RED)

OUT = "/home/user/awesome-claude-code-subagents/linkedin-banner-piroval-dark.png"
img.save(OUT, "PNG", optimize=True)
print(f"Saved: {OUT} ({os.path.getsize(OUT)} bytes)  {W}x{H}")
