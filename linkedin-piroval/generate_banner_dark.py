"""Generate LinkedIn company banner for Grupo Piroval — dark variant 1128x191 px.
V2: logo real."""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = "/home/user/awesome-claude-code-subagents/linkedin-piroval"

W, H = 1128, 191

DARK = (15, 15, 15)
DARK_2 = (26, 26, 26)
WHITE = (255, 255, 255)
OFF_WHITE = (236, 236, 236)
GRAY = (150, 150, 150)
GRAY_LIGHT = (180, 180, 180)
RED = (200, 16, 46)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def f(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)

font_title_es = f("DejaVuSans-Bold.ttf", 24)
font_title_en = f("DejaVuSans.ttf", 14)
font_sectors = f("DejaVuSans.ttf", 11)
font_url = f("DejaVuSans-Bold.ttf", 13)

img = Image.new("RGB", (W, H), DARK)
draw = ImageDraw.Draw(img)

# Blueprint grid
for y in range(0, H, 16):
    draw.line([(0, y), (W, y)], fill=DARK_2, width=1)
for x in range(0, W, 16):
    draw.line([(x, 0), (x, H)], fill=DARK_2, width=1)

LEFT_W = 420

# Paste real logo on left
logo = Image.open(f"{ROOT}/logo-piroval.png").convert("RGBA")
target_h = 150
ratio = logo.width / logo.height
target_w = int(target_h * ratio)
logo_resized = logo.resize((target_w, target_h), Image.LANCZOS)
lx = (LEFT_W - target_w) // 2
ly = (H - target_h) // 2
img.paste(logo_resized, (lx, ly), logo_resized)

draw = ImageDraw.Draw(img)

# Red accent between logo and content
draw.rectangle([LEFT_W - 3, 55, LEFT_W, H - 55], fill=RED)

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

OUT = f"{ROOT}/banner-full-dark.png"
img.save(OUT, "PNG", optimize=True)
print(f"Saved: {OUT} ({os.path.getsize(OUT)} bytes)  {W}x{H}")
