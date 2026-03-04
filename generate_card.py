#!/usr/bin/env python3
"""Generate a WhatsApp-friendly digital visiting card image."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(SCRIPT_DIR, "assets", "visiting-card.png")
LOGO_PATH = os.path.join(SCRIPT_DIR, "assets", "cleaerr-logo.png")

# Card dimensions — landscape, WhatsApp-friendly (16:9-ish)
W, H = 1200, 675

# Brand colors
PRIMARY = (27, 79, 114)       # #1B4F72
ACCENT = (231, 76, 60)        # #E74C3C
WHITE = (255, 255, 255)
LIGHT_BG = (248, 249, 250)    # #F8F9FA
DARK_TEXT = (26, 26, 46)      # #1a1a2e
BODY_TEXT = (74, 74, 90)      # #4a4a5a
LIGHT_TEXT = (200, 210, 225)
DIVIDER = (55, 100, 140)


def load_font(name, size):
    """Try to load a system font, fallback to default."""
    paths = [
        f"/usr/share/fonts/truetype/dejavu/DejaVu{name}.ttf",
        f"/usr/share/fonts/truetype/liberation/Liberation{name}.ttf",
        f"/usr/share/fonts/truetype/noto/Noto{name}.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    # Try generic names
    try:
        return ImageFont.truetype(name, size)
    except (IOError, OSError):
        return ImageFont.load_default()


# Load fonts
font_name = load_font("Sans-Bold", 36)
font_title = load_font("Sans", 18)
font_company = load_font("Sans-Bold", 22)
font_tagline = load_font("SansCondensed-Italic", 15) if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Oblique.ttf") else load_font("Sans", 14)
try:
    font_tagline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Oblique.ttf", 15)
except (IOError, OSError):
    font_tagline = load_font("Sans", 14)
font_detail_label = load_font("Sans-Bold", 14)
font_detail = load_font("Sans", 15)
font_brand_large = load_font("Sans-Bold", 28)
font_website = load_font("Sans", 13)


def create_card():
    card = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(card)

    # ── Left panel (dark blue) ──
    left_w = 420
    draw.rectangle([0, 0, left_w, H], fill=PRIMARY)

    # Accent stripe at top of left panel
    draw.rectangle([0, 0, left_w, 6], fill=ACCENT)

    # Logo
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo_h = 90
        logo_w = int(logo.width * logo_h / logo.height)
        logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
        logo_x = (left_w - logo_w) // 2
        card.paste(logo, (logo_x, 50), logo)
    except Exception:
        pass

    # Company name
    draw.text((left_w // 2, 160), "toN0tErr", fill=WHITE, font=font_brand_large, anchor="mt")

    # Divider line
    div_y = 195
    draw.line([(left_w // 2 - 60, div_y), (left_w // 2 + 60, div_y)], fill=ACCENT, width=2)

    # Company full name
    draw.text((left_w // 2, 210), "CleaErr Tech Solutions", fill=LIGHT_TEXT, font=font_title, anchor="mt")

    # Tagline
    draw.text((left_w // 2, 245), "Tools to Nought Error", fill=(150, 170, 195), font=font_tagline, anchor="mt")

    # ── Left panel — contact details ──
    details_y = 300
    details = [
        ("\uf095", "+91 83173 08558"),
        ("\uf0e0", "aravind.cleaerr@gmail.com"),
        ("\uf0ac", "tonoterr.vercel.app"),
        ("\uf08c", "in/aravind-bayari-66496732"),
        ("\uf09b", "aravindcleaerr"),
        ("\uf3c5", "Bangalore, India"),
    ]

    # Use text labels instead of icons
    labels = [
        ("Phone", "+91 83173 08558"),
        ("Email", "aravind.cleaerr@gmail.com"),
        ("Web", "tonoterr.vercel.app"),
        ("LinkedIn", "in/aravind-bayari-66496732"),
        ("GitHub", "aravindcleaerr"),
        ("Location", "Bangalore, India"),
    ]

    for i, (label, value) in enumerate(labels):
        y = details_y + i * 38
        # Label
        draw.text((30, y), label, fill=(130, 160, 190), font=font_detail_label)
        # Value
        draw.text((115, y), value, fill=WHITE, font=font_detail)

    # Footer on left
    draw.text((left_w // 2, H - 25), "\u00a9 2017\u20132026", fill=(80, 110, 145), font=font_website, anchor="mt")

    # ── Right panel (white) ──
    right_x = left_w + 50

    # Name
    draw.text((right_x, 80), "Aravind V Bayari", fill=DARK_TEXT, font=font_name)

    # Title
    draw.text((right_x, 128), "Founder & CTO", fill=ACCENT, font=font_company)

    # Accent underline
    draw.line([(right_x, 162), (right_x + 180, 162)], fill=ACCENT, width=3)

    # Bio / expertise
    bio_y = 185
    bio_lines = [
        "25+ years of embedded systems expertise",
        "spanning 10+ companies, 20+ products,",
        "and 10+ industries.",
    ]
    for line in bio_lines:
        draw.text((right_x, bio_y), line, fill=BODY_TEXT, font=font_detail)
        bio_y += 24

    # ── Services / What we do ──
    services_y = 285
    draw.text((right_x, services_y), "What We Do", fill=PRIMARY, font=font_detail_label)
    draw.line([(right_x, services_y + 18), (right_x + 85, services_y + 18)], fill=ACCENT, width=2)

    services = [
        "Embedded Systems Consulting",
        "Hardware Design & Firmware",
        "AI-Powered Software Tools",
        "Test Automation & Compliance",
    ]
    for i, svc in enumerate(services):
        y = services_y + 32 + i * 28
        # Bullet
        draw.ellipse([right_x + 4, y + 5, right_x + 10, y + 11], fill=ACCENT)
        draw.text((right_x + 18, y), svc, fill=DARK_TEXT, font=font_detail)

    # ── Tools showcase ──
    tools_y = 440
    draw.text((right_x, tools_y), "Our Tools", fill=PRIMARY, font=font_detail_label)
    draw.line([(right_x, tools_y + 18), (right_x + 70, tools_y + 18)], fill=ACCENT, width=2)

    tools = ["ProdSync", "VoltSpark", "PartOK", "PCBok", "ZeroTest"]
    tx = right_x
    for tool in tools:
        bbox = draw.textbbox((0, 0), tool, font=font_detail_label)
        tw = bbox[2] - bbox[0] + 20
        pill_y = tools_y + 30
        # Pill background
        draw.rounded_rectangle(
            [(tx, pill_y), (tx + tw, pill_y + 28)],
            radius=6,
            fill=(214, 234, 248),
            outline=PRIMARY,
            width=1,
        )
        draw.text((tx + 10, pill_y + 5), tool, fill=PRIMARY, font=font_detail_label)
        tx += tw + 10

    # ── Bottom accent stripe on right ──
    draw.rectangle([left_w, H - 6, W, H], fill=ACCENT)

    # Website at bottom right
    draw.text((W - 30, H - 30), "tonoterr.vercel.app", fill=(180, 180, 190), font=font_website, anchor="rt")

    card.save(OUTPUT, "PNG", quality=95)
    print(f"Visiting card saved: {OUTPUT}")
    print(f"Size: {W}x{H}px")


if __name__ == "__main__":
    create_card()
