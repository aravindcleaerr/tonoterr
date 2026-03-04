#!/usr/bin/env python3
"""Generate one-page product brief PDFs for each toN0tErr tool."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

WIDTH, HEIGHT = A4  # 595 x 842 pt

# Brand colors
BRAND_PRIMARY = HexColor("#1B4F72")
BRAND_ACCENT = HexColor("#E74C3C")
BRAND_DARK_TEXT = HexColor("#1a1a2e")
BRAND_BODY_TEXT = HexColor("#4a4a5a")
BRAND_SUCCESS = HexColor("#27AE60")
BRAND_SECONDARY = HexColor("#2E86C1")
DIVIDER_COLOR = HexColor("#D8D8D8")

LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "cleaerr-logo.png")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "assets", "briefs")

LEFT = 30
RIGHT = WIDTH - 30
CONTENT_W = RIGHT - LEFT
HEADER_H = 75
FOOTER_H = 40


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


def draw_header(c, tool_name, badge_text):
    top = HEIGHT
    c.setFillColor(BRAND_PRIMARY)
    c.rect(0, top - HEADER_H, WIDTH, HEADER_H, fill=1, stroke=0)

    # Logo
    try:
        logo = ImageReader(LOGO_PATH)
        c.drawImage(logo, 22, top - 60, width=28, height=36, mask="auto")
    except Exception:
        pass

    # Company name
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(56, top - 40, "toN0tErr")
    nw = c.stringWidth("toN0tErr", "Helvetica-Bold", 15)

    c.setFillColor(HexColor("#88AACC"))
    c.setFont("Helvetica", 10)
    c.drawString(56 + nw + 8, top - 39, "|")

    c.setFillColor(HexColor("#C8DDF0"))
    c.setFont("Helvetica", 9)
    c.drawString(56 + nw + 20, top - 39, "CleaErr Tech Solutions")

    c.setFillColor(HexColor("#88AACC"))
    c.setFont("Helvetica", 8)
    c.drawString(56, top - 55, "PRODUCT BRIEF")

    # Tool name right
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    tw = c.stringWidth(tool_name, "Helvetica-Bold", 24)
    c.drawString(RIGHT - tw, top - 36, tool_name)

    # Badge pill
    c.setFont("Helvetica-Bold", 8)
    bw = c.stringWidth(badge_text, "Helvetica-Bold", 8) + 14
    c.setFillColor(BRAND_ACCENT)
    c.roundRect(RIGHT - bw, top - 56, bw, 15, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.drawString(RIGHT - bw + 7, top - 52, badge_text)

    return top - HEADER_H


def draw_section_heading(c, y, title):
    c.setFillColor(BRAND_PRIMARY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(LEFT, y, title)
    y -= 5
    c.setStrokeColor(BRAND_ACCENT)
    c.setLineWidth(2)
    sw = c.stringWidth(title, "Helvetica-Bold", 12)
    c.line(LEFT, y, LEFT + sw + 5, y)
    return y - 16


def draw_divider(c, y):
    y -= 8
    c.setStrokeColor(DIVIDER_COLOR)
    c.setLineWidth(0.5)
    c.line(LEFT, y, RIGHT, y)
    return y - 14


def generate_tool_pdf(tool):
    filename = f"{tool['id']}-brief.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)
    c = canvas.Canvas(filepath, pagesize=A4)
    c.setTitle(f"{tool['name']} \u2014 Product Brief | toN0tErr")
    c.setAuthor("CleaErr Tech Solutions")
    c.setSubject(f"{tool['name']} Product Brief")

    # ── Header ──
    y = draw_header(c, tool["name"], tool["badge"])

    # ── Subtitle + Description ──
    y -= 24
    c.setFillColor(BRAND_PRIMARY)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(LEFT, y, tool["subtitle"])
    y -= 8
    c.setStrokeColor(BRAND_ACCENT)
    c.setLineWidth(2)
    sw = c.stringWidth(tool["subtitle"], "Helvetica-Bold", 15)
    c.line(LEFT, y, LEFT + sw, y)
    y -= 20

    c.setFillColor(BRAND_BODY_TEXT)
    c.setFont("Helvetica", 10.5)
    for line in word_wrap(c, tool["description"], "Helvetica", 10.5, CONTENT_W):
        c.drawString(LEFT, y, line)
        y -= 16

    # ── Divider ──
    y = draw_divider(c, y)

    # ── Key Features ──
    y = draw_section_heading(c, y, "Key Features")

    max_w = CONTENT_W - 22
    for feature in tool["features"]:
        # Bullet
        c.setFillColor(BRAND_ACCENT)
        c.circle(LEFT + 6, y + 3, 2.5, fill=1, stroke=0)

        if " \u2014 " in feature:
            label, rest = feature.split(" \u2014 ", 1)
            c.setFillColor(BRAND_DARK_TEXT)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(LEFT + 16, y, label)
            lw = c.stringWidth(label, "Helvetica-Bold", 10)
            c.setFont("Helvetica", 10)
            dash_rest = f" \u2014 {rest}"
            if c.stringWidth(dash_rest, "Helvetica", 10) <= max_w - lw:
                c.drawString(LEFT + 16 + lw, y, dash_rest)
                y -= 18
            else:
                full_lines = word_wrap(c, feature, "Helvetica", 10, max_w)
                # First line: bold label portion
                c.setFont("Helvetica-Bold", 10)
                c.drawString(LEFT + 16, y, label)
                after = full_lines[0][len(label):]
                c.setFont("Helvetica", 10)
                c.drawString(LEFT + 16 + lw, y, after)
                y -= 15
                for ln in full_lines[1:]:
                    c.drawString(LEFT + 16, y, ln)
                    y -= 15
                y -= 3
        else:
            c.setFillColor(BRAND_DARK_TEXT)
            c.setFont("Helvetica", 10)
            lines = word_wrap(c, feature, "Helvetica", 10, max_w)
            for ln in lines:
                c.drawString(LEFT + 16, y, ln)
                y -= 15
            y -= 3

    # ── Divider ──
    y = draw_divider(c, y)

    # ── Technology Stack ──
    y = draw_section_heading(c, y, "Technology Stack")

    x = LEFT
    for tag in tool["tags"]:
        font, sz = "Helvetica-Bold", 10
        tw = c.stringWidth(tag, font, sz) + 22
        pill_h = 24
        # Background
        c.setFillColor(HexColor("#D6EAF8"))
        c.roundRect(x, y - 5, tw, pill_h, 5, fill=1, stroke=0)
        # Border
        c.setStrokeColor(BRAND_PRIMARY)
        c.setLineWidth(1)
        c.roundRect(x, y - 5, tw, pill_h, 5, fill=0, stroke=1)
        # Text
        c.setFillColor(BRAND_PRIMARY)
        c.setFont(font, sz)
        c.drawString(x + 11, y + 2, tag)
        x += tw + 10
        if x > RIGHT - 60:
            x = LEFT
            y -= 30

    y -= 34

    # ── Divider ──
    y = draw_divider(c, y)

    # ── Error Elimination Badge ──
    # Draw downward from y: box top = y, box bottom = y - box_h
    box_h = 52
    box_top = y
    box_bot = box_top - box_h
    c.setFillColor(HexColor("#EAFAEA"))
    c.roundRect(LEFT, box_bot, CONTENT_W, box_h, 6, fill=1, stroke=0)
    c.setStrokeColor(BRAND_SUCCESS)
    c.setLineWidth(1.2)
    c.roundRect(LEFT, box_bot, CONTENT_W, box_h, 6, fill=0, stroke=1)

    # Checkmark circle
    cx = LEFT + 24
    cy = box_bot + box_h / 2
    c.setFillColor(BRAND_SUCCESS)
    c.circle(cx, cy, 10, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(cx, cy - 4, "\u2713")

    text_x = LEFT + 44
    # Strikethrough
    c.setFillColor(HexColor("#888888"))
    c.setFont("Helvetica", 10)
    c.drawString(text_x, cy + 6, tool["error_from"])
    fw = c.stringWidth(tool["error_from"], "Helvetica", 10)
    c.setStrokeColor(HexColor("#888888"))
    c.setLineWidth(0.8)
    c.line(text_x, cy + 10, text_x + fw, cy + 10)
    # Arrow
    c.setFillColor(BRAND_SUCCESS)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(text_x + fw + 8, cy + 4, "\u2192")
    # Result
    c.setFillColor(BRAND_SUCCESS)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(text_x, cy - 14, tool["error_to"])

    y = box_bot - 18

    # ── Live Demo / Status ──
    url = tool.get("url")
    if url:
        c.setFillColor(BRAND_PRIMARY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(LEFT, y, "Live Demo:")
        c.setFillColor(BRAND_ACCENT)
        c.setFont("Helvetica", 10)
        c.drawString(LEFT + 72, y, url)
        uw = c.stringWidth(url, "Helvetica", 10)
        c.setStrokeColor(BRAND_ACCENT)
        c.setLineWidth(0.5)
        c.line(LEFT + 72, y - 2, LEFT + 72 + uw, y - 2)
    else:
        c.setFillColor(HexColor("#777777"))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(LEFT, y, "Status:")
        c.setFillColor(BRAND_ACCENT)
        c.drawString(LEFT + 50, y, "In Development")

    # ── Tagline at bottom of content area ──
    tagline_y = FOOTER_H + 22
    c.setFillColor(HexColor("#BBBBBB"))
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(WIDTH / 2, tagline_y, "Tools to Nought Error \u2014 Engineering precision into every system.")

    # ── Footer ──
    c.setFillColor(BRAND_PRIMARY)
    c.rect(0, 0, WIDTH, FOOTER_H, fill=1, stroke=0)
    c.setStrokeColor(BRAND_ACCENT)
    c.setLineWidth(2)
    c.line(0, FOOTER_H, WIDTH, FOOTER_H)

    c.setFillColor(HexColor("#C8DDF0"))
    c.setFont("Helvetica", 8)
    c.drawString(LEFT, 16, "\u00a9 2017\u20132026 toN0tErr / CleaErr Tech Solutions  |  Bangalore, India")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(RIGHT, 16, "aravindcleaerr.github.io/tonoterr")

    c.save()
    print(f"  Created: {filepath}")


# ── Tool Data ──
TOOLS = [
    {
        "id": "prodsync",
        "name": "ProdSync",
        "subtitle": "Production Scanner App",
        "badge": "Manufacturing QC",
        "description": (
            "AI-powered manufacturing quality control and production tracking. Three role-based modes "
            "for different levels of quality assurance. Designed for shop-floor teams to scan, log, and "
            "verify production output with AI-driven defect detection."
        ),
        "features": [
            "Barcode/QR scanning with quality status logging (Pass/Reject)",
            "AI-powered defect analysis via Google Gemini Vision API",
            "Photo documentation of defects with automated shift reports",
            "Dual-process support: outward production + inward field returns",
            "Offline capability with Google Sheets cloud sync",
        ],
        "tags": ["Gemini AI", "Barcode Scanner", "Google Sheets", "PWA"],
        "error_from": "Manufacturing defects reaching customers",
        "error_to": "AI-caught at the line",
        "url": "https://aravindcleaerr.github.io/ps-app/",
    },
    {
        "id": "voltspark",
        "name": "VoltSpark",
        "subtitle": "Industrial Energy Compliance Platform",
        "badge": "Energy Management",
        "description": (
            "All-in-one energy management and compliance platform for India's industrial sector \u2014 "
            "built for energy consultants, ESCOs, and manufacturing units. Covers ZED certification, "
            "ISO 50001 compliance, utility bill analysis, and ROI documentation."
        ),
        "features": [
            "30+ compliance modules covering ZED, ISO 50001, and electrical safety",
            "Utility bill analysis with auto-detection of penalties and anomalies",
            "Pre-built ROI calculators and savings documentation",
            "Compliance calendar with audit and certification deadline tracking",
            "Multi-tenant SaaS with role-based access for consultants and clients",
        ],
        "tags": ["ZED Compliance", "ISO 50001", "Next.js", "SaaS"],
        "error_from": "Energy compliance violations and missed penalties",
        "error_to": "Automated tracking and documentation",
        "url": "https://volt-spark.vercel.app/",
    },
    {
        "id": "partok",
        "name": "PartOK",
        "subtitle": "Mechanical Part Inspection Platform",
        "badge": "Part Inspection",
        "description": (
            "AI-powered mechanical part inspection and quality management platform for manufacturing "
            "and engineering teams. Upload CAD files, run AI visual defect detection, perform dimensional "
            "inspections, and generate traceable PDF reports."
        ),
        "features": [
            "CAD file upload and parsing (STL, STEP, DXF) with 3D viewer",
            "AI visual defect detection using YOLOv8 with photo evidence",
            "Dimensional inspection with tolerance tracking per feature",
            "PDF inspection report generation with pass/fail traceability",
            "Real-time collaboration with multi-user WebSocket editing",
        ],
        "tags": ["YOLOv8 AI", "CAD Parser", "FastAPI", "React"],
        "error_from": "Undetected mechanical defects reaching assembly",
        "error_to": "AI-inspected with full dimensional traceability",
        "url": "https://part-ok.vercel.app",
    },
    {
        "id": "pcbok",
        "name": "PCBok",
        "subtitle": "AI-Powered PCB Inspector",
        "badge": "PCB Inspection",
        "description": (
            "Comprehensive PCB inspection and management platform with AI analysis, design rule checking, "
            "and component lifecycle tracking. Supports Gerber, KiCad, Altium, and Eagle formats with "
            "interactive layer viewing and BOM cost estimation."
        ),
        "features": [
            "Gerber, KiCad, Altium, Eagle file parsing with interactive layer viewer",
            "Design Rule Check (DRC) for trace width, clearance, and via rules",
            "Component library with lifecycle tracking (active / NRND / EOL)",
            "BOM cost estimation with supplier pricing integration",
            "Board revision diff \u2014 side-by-side comparison of added/removed components",
        ],
        "tags": ["Gerber Parser", "DRC Engine", "FastAPI", "React + TypeScript"],
        "error_from": "PCB design errors and component obsolescence escaping review",
        "error_to": "AI-checked before production",
        "url": "https://pcbok.vercel.app",
    },
    {
        "id": "zerotest",
        "name": "ZeroTest",
        "subtitle": "Production Test Management Platform",
        "badge": "Functional Test Automation",
        "description": (
            "Zero-Defect | Zero-Config | Zero-to-Production \u2014 a complete production test management "
            "platform for hardware teams. Tracks DUTs, runs tests, and drives yield toward 100%. "
            "Covers electronics, power systems, automotive, and industrial domains."
        ),
        "features": [
            "DUT Registry \u2014 multi-industry device tracking across electronics, power, automotive, and industrial domains",
            "Test Profiles \u2014 reusable templates with ordered steps, limits, and equipment requirements",
            "Live Test Runner \u2014 real-time WebSocket streaming of measurements with pass/fail decisions",
            "Equipment Manager \u2014 instrument tracking with calibration schedules",
            "Standards Library \u2014 IPC, IEEE, IEC compliance linked to test profiles",
        ],
        "tags": ["FastAPI", "React + TypeScript", "WebSockets", "PostgreSQL"],
        "error_from": "Production escapes from untested or under-tested devices",
        "error_to": "Every DUT tested, measured, and yield-verified",
        "url": None,
    },
]


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating product brief PDFs...")
    for tool in TOOLS:
        generate_tool_pdf(tool)
    print(f"\nDone! {len(TOOLS)} PDFs generated in {OUTPUT_DIR}/")
