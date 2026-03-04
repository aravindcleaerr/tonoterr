#!/usr/bin/env python3
"""Generate a one-page A4 company brochure PDF for toN0tErr / CleaErr Tech Solutions."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

WIDTH, HEIGHT = A4  # 595 x 842 pt

# Brand colors
PRIMARY = HexColor("#1B4F72")
ACCENT = HexColor("#E74C3C")
SECONDARY = HexColor("#2E86C1")
SUCCESS = HexColor("#27AE60")
DARK_TEXT = HexColor("#1a1a2e")
BODY_TEXT = HexColor("#4a4a5a")
LIGHT_BG = HexColor("#F8F9FA")
DIVIDER = HexColor("#D8D8D8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "assets", "cleaerr-logo.png")
OUTPUT = os.path.join(SCRIPT_DIR, "assets", "company-brochure.pdf")

LEFT = 30
RIGHT = WIDTH - 30
CW = RIGHT - LEFT  # content width
MID = WIDTH / 2
COL_GAP = 20
COL_W = (CW - COL_GAP) / 2
FOOTER_H = 38


def word_wrap(c, text, font, size, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = f"{cur} {w}" if cur else w
        if c.stringWidth(test, font, size) < max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_header(c):
    """Header bar with branding."""
    h = 72
    top = HEIGHT
    c.setFillColor(PRIMARY)
    c.rect(0, top - h, WIDTH, h, fill=1, stroke=0)

    # Logo
    try:
        logo = ImageReader(LOGO_PATH)
        c.drawImage(logo, 22, top - 58, width=26, height=34, mask="auto")
    except Exception:
        pass

    # Company name
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(54, top - 36, "toN0tErr")
    nw = c.stringWidth("toN0tErr", "Helvetica-Bold", 15)
    c.setFillColor(HexColor("#88AACC"))
    c.setFont("Helvetica", 10)
    c.drawString(54 + nw + 8, top - 35, "|")
    c.setFillColor(HexColor("#C8DDF0"))
    c.setFont("Helvetica", 9)
    c.drawString(54 + nw + 18, top - 35, "CleaErr Tech Solutions")

    # Label
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(RIGHT, top - 32, "COMPANY BROCHURE")

    # Tagline
    c.setFillColor(HexColor("#88AACC"))
    c.setFont("Helvetica", 8)
    c.drawString(54, top - 52, "Tools to Nought Error \u2014 Engineering precision into every system")

    # Accent top stripe
    c.setFillColor(ACCENT)
    c.rect(0, top - 3, WIDTH, 3, fill=1, stroke=0)

    return top - h


def draw_mission(c, y):
    """Mission statement section."""
    y -= 22
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(LEFT, y, "Engineering Zero Errors")
    y -= 6
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2.5)
    c.line(LEFT, y, LEFT + 190, y)
    y -= 18

    mission = (
        "We build products, devices, processes, and applications that systematically "
        "reduce and eliminate errors \u2014 human, machine, and system. From embedded "
        "hardware consulting to AI-powered software tools, every solution drives "
        "error rates toward zero."
    )
    c.setFillColor(BODY_TEXT)
    c.setFont("Helvetica", 10)
    for line in word_wrap(c, mission, "Helvetica", 10, CW):
        c.drawString(LEFT, y, line)
        y -= 14

    return y - 6


def draw_pillars(c, y):
    """Two-column pillars: Consulting + Tools."""
    col1_x = LEFT
    col2_x = LEFT + COL_W + COL_GAP

    # Divider line above
    c.setStrokeColor(DIVIDER)
    c.setLineWidth(0.5)
    c.line(LEFT, y, RIGHT, y)
    y -= 18

    start_y = y

    # ── Left column: Consulting ──
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(col1_x, y, "Hardware & Embedded Consulting")
    y_left = y - 5
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    sw = c.stringWidth("Hardware & Embedded Consulting", "Helvetica-Bold", 12)
    c.line(col1_x, y_left, col1_x + sw, y_left)
    y_left -= 16

    desc1 = (
        "Concept to production. Defence to HealthTech to EV. "
        "We deliver Technical Consulting, Design Consulting, and "
        "Embedded Engineering \u2014 integrated into your team, not assigned as a vendor."
    )
    c.setFillColor(BODY_TEXT)
    c.setFont("Helvetica", 9.5)
    for line in word_wrap(c, desc1, "Helvetica", 9.5, COL_W):
        c.drawString(col1_x, y_left, line)
        y_left -= 13
    y_left -= 8

    # Engagements label
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(col1_x, y_left, "Engagements:")
    y_left -= 14

    engagements = [
        ("I-Max", "Solenoid coil test automation"),
        ("Amberroot", "EV motor drive & IoT telemetry"),
        ("SupraEnergy", "Connected lighting systems"),
        ("Freshot Robotics", "Automated food robot (Idli ATM)"),
        ("Tenxer", "Semiconductor IC evaluation"),
    ]
    for name, desc in engagements:
        c.setFillColor(ACCENT)
        c.circle(col1_x + 5, y_left + 3, 2, fill=1, stroke=0)
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(col1_x + 13, y_left, name)
        nw = c.stringWidth(name, "Helvetica-Bold", 9)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(BODY_TEXT)
        c.drawString(col1_x + 13 + nw + 4, y_left, f"\u2014 {desc}")
        y_left -= 14

    # ── Right column: Tools ──
    y_right = start_y
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(col2_x, y_right, "AI-Powered Software Tools")
    y_right -= 5
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    sw = c.stringWidth("AI-Powered Software Tools", "Helvetica-Bold", 12)
    c.line(col2_x, y_right, col2_x + sw, y_right)
    y_right -= 16

    desc2 = (
        "Intelligent tools built to catch what humans miss. Manufacturing QC, "
        "energy compliance, part inspection, PCB analysis, and production "
        "test management."
    )
    c.setFillColor(BODY_TEXT)
    c.setFont("Helvetica", 9.5)
    for line in word_wrap(c, desc2, "Helvetica", 9.5, COL_W):
        c.drawString(col2_x, y_right, line)
        y_right -= 13
    y_right -= 8

    # Tools label
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(col2_x, y_right, "Our Tools:")
    y_right -= 18

    tools = [
        ("ProdSync", "Manufacturing QC Scanner"),
        ("VoltSpark", "Energy Compliance Platform"),
        ("PartOK", "Mechanical Part Inspection"),
        ("PCBok", "AI-Powered PCB Inspector"),
        ("ZeroTest", "Production Test Management"),
    ]
    for name, desc in tools:
        c.setFillColor(ACCENT)
        c.circle(col2_x + 5, y_right + 3, 2, fill=1, stroke=0)
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(col2_x + 13, y_right, name)
        nw = c.stringWidth(name, "Helvetica-Bold", 9)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(BODY_TEXT)
        c.drawString(col2_x + 13 + nw + 4, y_right, f"\u2014 {desc}")
        y_right -= 14

    # Vertical divider between columns
    mid_x = LEFT + COL_W + COL_GAP / 2
    c.setStrokeColor(DIVIDER)
    c.setLineWidth(0.5)
    c.line(mid_x, start_y + 5, mid_x, min(y_left, y_right) + 5)

    return min(y_left, y_right) - 6


def draw_stats_bar(c, y):
    """Stats bar with accent background."""
    bar_h = 42
    c.setFillColor(PRIMARY)
    c.rect(0, y - bar_h, WIDTH, bar_h, fill=1, stroke=0)

    # Accent line at top
    c.setFillColor(ACCENT)
    c.rect(0, y, WIDTH, 2, fill=1, stroke=0)

    stats = [
        ("25+", "Years Experience"),
        ("10+", "Industries"),
        ("5", "Engagements"),
        ("5", "Software Tools"),
    ]
    slot_w = WIDTH / len(stats)
    mid_y = y - bar_h / 2

    for i, (num, label) in enumerate(stats):
        cx = slot_w * i + slot_w / 2
        # Number
        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(cx, mid_y + 2, num)
        # Label
        c.setFillColor(HexColor("#C8DDF0"))
        c.setFont("Helvetica", 8)
        c.drawCentredString(cx, mid_y - 14, label)

    return y - bar_h


def draw_industries(c, y):
    """Industries served as pill tags."""
    y -= 18
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(LEFT, y, "Industries Served")
    y -= 5
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    c.line(LEFT, y, LEFT + 120, y)
    y -= 20

    industries = [
        "HealthTech", "Defence", "Medical Devices", "EV & Automotive",
        "IoT & Wearables", "Food Robotics", "Industrial Automation",
        "Semiconductor", "Connected Lighting", "Test & Measurement",
    ]

    x = LEFT
    for ind in industries:
        font, sz = "Helvetica", 8.5
        tw = c.stringWidth(ind, font, sz) + 16
        pill_h = 18
        if x + tw > RIGHT:
            x = LEFT
            y -= 24
        # Background
        c.setFillColor(HexColor("#EBF5FB"))
        c.roundRect(x, y - 3, tw, pill_h, 4, fill=1, stroke=0)
        # Border
        c.setStrokeColor(SECONDARY)
        c.setLineWidth(0.6)
        c.roundRect(x, y - 3, tw, pill_h, 4, fill=0, stroke=1)
        # Text
        c.setFillColor(PRIMARY)
        c.setFont(font, sz)
        c.drawString(x + 8, y + 2, ind)
        x += tw + 8

    return y - 24


def draw_approach(c, y):
    """Our Approach — Identify → Engineer → Eliminate."""
    c.setStrokeColor(DIVIDER)
    c.setLineWidth(0.5)
    c.line(LEFT, y, RIGHT, y)
    y -= 16

    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(LEFT, y, "Our Approach")
    y -= 5
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    c.line(LEFT, y, LEFT + 95, y)
    y -= 22

    # Three steps side by side
    steps = [
        ("1. Identify", "Pinpoint the root cause of errors \u2014 human, machine, or system-originated."),
        ("2. Engineer", "Build tools, devices, processes, and applications that address root causes."),
        ("3. Eliminate", "Drive error rates toward zero through deployment, monitoring, and refinement."),
    ]
    step_w = (CW - 30) / 3

    for i, (title, desc) in enumerate(steps):
        sx = LEFT + i * (step_w + 15)

        # Step number circle
        c.setFillColor(ACCENT if i == 0 else PRIMARY if i == 1 else SUCCESS)
        c.circle(sx + 10, y + 3, 8, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(sx + 10, y - 1, str(i + 1))

        # Title
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold", 10)
        # Extract just the name part (after "N. ")
        step_name = title.split(". ", 1)[1]
        c.drawString(sx + 24, y, step_name)

        # Description
        c.setFillColor(BODY_TEXT)
        c.setFont("Helvetica", 8)
        for j, line in enumerate(word_wrap(c, desc, "Helvetica", 8, step_w - 24)):
            c.drawString(sx + 24, y - 14 - j * 11, line)

    # Arrow connectors between steps
    c.setFillColor(BODY_TEXT)
    c.setFont("Helvetica-Bold", 14)
    for i in range(2):
        ax = LEFT + (i + 1) * (step_w + 15) - 10
        c.drawCentredString(ax, y - 2, "\u2192")

    y -= 50
    return y


def draw_founder_bar(c, y):
    """Founder credential bar."""
    c.setStrokeColor(DIVIDER)
    c.setLineWidth(0.5)
    c.line(LEFT, y, RIGHT, y)
    y -= 16

    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(LEFT, y, "Founded By")
    y -= 5
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    c.line(LEFT, y, LEFT + 85, y)
    y -= 18

    # Name and title
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(LEFT, y, "Aravind V Bayari")
    nw = c.stringWidth("Aravind V Bayari", "Helvetica-Bold", 11)
    c.setFillColor(ACCENT)
    c.setFont("Helvetica", 9)
    c.drawString(LEFT + nw + 10, y + 1, "Founder & CTO")
    y -= 16

    # Credentials
    creds = (
        "25+ years of embedded systems expertise. Led R&D of the SCAD 508 "
        "(Technology Development Board Award from the President of India). "
        "Products span defence avionics, EV motor drives, radar-based AI health "
        "monitoring, and viral food robots."
    )
    c.setFillColor(BODY_TEXT)
    c.setFont("Helvetica", 9)
    for line in word_wrap(c, creds, "Helvetica", 9, CW):
        c.drawString(LEFT, y, line)
        y -= 13

    return y - 6


def draw_contact(c, y):
    """Contact information section."""
    c.setStrokeColor(DIVIDER)
    c.setLineWidth(0.5)
    c.line(LEFT, y, RIGHT, y)
    y -= 16

    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(LEFT, y, "Get In Touch")
    y -= 5
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    c.line(LEFT, y, LEFT + 90, y)
    y -= 18

    # Two columns of contact details
    col1_x = LEFT
    col2_x = MID + 10

    contacts_left = [
        ("Phone:", "+91 83173 08558"),
        ("Email:", "aravind.cleaerr@gmail.com"),
    ]
    contacts_right = [
        ("Web:", "tonoterr.vercel.app"),
        ("LinkedIn:", "in/aravind-bayari-66496732"),
    ]

    for i, (label, value) in enumerate(contacts_left):
        cy = y - i * 16
        c.setFillColor(BODY_TEXT)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(col1_x, cy, label)
        lw = c.stringWidth(label, "Helvetica-Bold", 9)
        c.setFont("Helvetica", 9)
        c.setFillColor(DARK_TEXT)
        c.drawString(col1_x + lw + 6, cy, value)

    for i, (label, value) in enumerate(contacts_right):
        cy = y - i * 16
        c.setFillColor(BODY_TEXT)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(col2_x, cy, label)
        lw = c.stringWidth(label, "Helvetica-Bold", 9)
        c.setFont("Helvetica", 9)
        c.setFillColor(DARK_TEXT)
        c.drawString(col2_x + lw + 6, cy, value)

    return y - 35


def draw_footer(c):
    """Footer bar."""
    c.setFillColor(PRIMARY)
    c.rect(0, 0, WIDTH, FOOTER_H, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(0, FOOTER_H, WIDTH, 2, fill=1, stroke=0)

    c.setFillColor(HexColor("#C8DDF0"))
    c.setFont("Helvetica", 8)
    c.drawString(LEFT, 15, "\u00a9 2017\u20132026 toN0tErr / CleaErr Tech Solutions  |  Bangalore, India")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(RIGHT, 15, "tonoterr.vercel.app")


def generate_brochure():
    c = canvas.Canvas(OUTPUT, pagesize=A4)
    c.setTitle("toN0tErr \u2014 Company Brochure")
    c.setAuthor("CleaErr Tech Solutions")
    c.setSubject("Company Overview")

    y = draw_header(c)
    y = draw_mission(c, y)
    y = draw_pillars(c, y)
    y = draw_stats_bar(c, y)
    y = draw_industries(c, y)
    y = draw_approach(c, y)
    y = draw_founder_bar(c, y)
    y = draw_contact(c, y)
    draw_footer(c)

    c.save()
    print(f"Company brochure saved: {OUTPUT}")


if __name__ == "__main__":
    generate_brochure()
