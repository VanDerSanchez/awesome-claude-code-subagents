"""Generate LinkedIn company banner for Grupo Piroval — 1128x191 px.
V2: logo real y foto del taller embebidas."""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = "/home/user/awesome-claude-code-subagents/linkedin-piroval"

W, H = 1128, 191
LEFT_W = 420

DARK = (15, 15, 15)
DARK_2 = (26, 26, 26)
WHITE = (255, 255, 255)
OFF_WHITE = (246, 246, 246)
GRAY = (110, 110, 110)
GRAY_LIGHT = (168, 168, 168)
GRAY_DARK = (55, 55, 55)
RED = (200, 16, 46)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def f(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)

font_title_es = f("DejaVuSans-Bold.ttf", 23)
font_title_en = f("DejaVuSans.ttf", 14)
font_sectors = f("DejaVuSans.ttf", 11)
font_url = f("DejaVuSans-Bold.ttf", 13)

img = Image.new("RGB", (W, H), OFF_WHITE)
draw = ImageDraw.Draw(img)

# --- LEFT PANEL (dark with photo background) ---
photo = Image.open(f"{ROOT}/IMG_3900.jpeg").convert("RGB")
# Cover crop to LEFT_W x H
src_ratio = photo.width / photo.height
dst_ratio = LEFT_W / H
if src_ratio > dst_ratio:
    new_w = int(photo.height * dst_ratio)
    off = (photo.width - new_w) // 2
    photo = photo.crop((off, 0, off + new_w, photo.height))
else:
    new_h = int(photo.width / dst_ratio)
    off = (photo.height - new_h) // 2
    photo = photo.crop((0, off, photo.width, off + new_h))
photo = photo.resize((LEFT_W, H), Image.LANCZOS)
# Darken overlay
overlay = Image.new("RGB", (LEFT_W, H), (0, 0, 0))
photo = Image.blend(photo, overlay, 0.60)
img.paste(photo, (0, 0))

# Red vertical divider
draw = ImageDraw.Draw(img)
draw.rectangle([LEFT_W - 3, 0, LEFT_W, H], fill=RED)

# Paste real logo on the left panel
logo = Image.open(f"{ROOT}/logo-piroval.png").convert("RGBA")
# Use the logo at target height 130
target_h = 140
ratio = logo.width / logo.height
target_w = int(target_h * ratio)
logo_resized = logo.resize((target_w, target_h), Image.LANCZOS)
# Center in left panel
lx = (LEFT_W - target_w) // 2
ly = (H - target_h) // 2
# White version: convert red to white for dark background — but the logo is red on transparent,
# which shows well on dark. We paste it directly.
img.paste(logo_resized, (lx, ly), logo_resized)

# --- RIGHT PANEL (light) ---
rx = LEFT_W + 35
draw.text((rx, 48), "Equipos térmicos industriales a medida", font=font_title_es, fill=DARK)
draw.rectangle([rx, 84, rx + 36, 86], fill=RED)
draw.text((rx, 96), "Custom industrial thermal equipment", font=font_title_en, fill=GRAY)
draw.text((rx, 128), "Automoción  ·  Cerámica  ·  Química  ·  Alimentación", font=font_sectors, fill=GRAY_DARK)

url = "hornosysecaderos.com"
bbox = draw.textbbox((0, 0), url, font=font_url)
url_w = bbox[2] - bbox[0]
ux = W - url_w - 28
uy = H - 30
draw.text((ux, uy), url, font=font_url, fill=RED)

OUT = f"{ROOT}/banner-split-light.png"
img.save(OUT, "PNG", optimize=True)
print(f"Saved: {OUT} ({os.path.getsize(OUT)} bytes)  {W}x{H}")
