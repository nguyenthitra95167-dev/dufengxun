"""
Generate PNG images for the Dufengxun website.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import random
import os

random.seed(42)
OUT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(OUT, "images")
os.makedirs(IMG_DIR, exist_ok=True)


# Color palette
BG_DARK = (10, 14, 26)
BG_SURFACE = (22, 27, 44)
ACCENT = (91, 141, 239)
CYAN = (79, 195, 247)
PURPLE = (139, 127, 216)
TEXT = (245, 248, 255)
TEXT_DIM = (168, 181, 207)
TEXT_FAINT = (107, 122, 153)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient_bg(w, h, c1=BG_DARK, c2=(15, 20, 33)):
    img = Image.new("RGB", (w, h), c1)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        c = lerp(c1, c2, t)
        draw.line([(0, y), (w, y)], fill=c)
    return img


def add_glow_orbs(img, orbs):
    base = img.copy()
    for x, y, r, color, alpha in orbs:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(*color, alpha))
        layer = layer.filter(ImageFilter.GaussianBlur(radius=r // 3))
        base = Image.alpha_composite(base.convert("RGBA"), layer)
    return base


def add_grid(img, color=(91, 141, 239), spacing=40, alpha=20):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    for x in range(0, w, spacing):
        draw.line([(x, 0), (x, h)], fill=(*color, alpha))
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=(*color, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def add_scan_lines(img, alpha=12, spacing=3):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=(91, 141, 239, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_phone(draw, x, y, w, h, screen_color, radius=24, border=(91, 141, 239, 200), border_w=2):
    rounded_rect(draw, [x, y, x + w, y + h], radius, fill=(20, 25, 40), outline=border, width=border_w)
    inset = 6
    rounded_rect(draw, [x + inset, y + inset, x + w - inset, y + h - inset],
                 radius - 2, fill=screen_color)
    notch_w = 60
    notch_h = 18
    rounded_rect(draw,
                 [x + (w - notch_w) / 2, y + inset, x + (w + notch_w) / 2, y + inset + notch_h],
                 notch_h // 2, fill=(10, 14, 26))


# Hero illustration
def make_hero_illustration():
    w, h = 1600, 1000
    base = gradient_bg(w, h, c1=BG_DARK, c2=(15, 22, 40))
    img = add_glow_orbs(base, [
        (w * 0.2, h * 0.3, 350, ACCENT, 90),
        (w * 0.8, h * 0.7, 300, CYAN, 70),
        (w * 0.5, h * 0.5, 250, PURPLE, 60),
        (w * 0.9, h * 0.2, 200, ACCENT, 50),
        (w * 0.1, h * 0.8, 220, PURPLE, 50),
    ])
    img = add_grid(img, alpha=18)
    img = add_scan_lines(img, alpha=8)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    cx, cy = w // 2, h // 2
    r = 280
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, outline=(*ACCENT, 100), width=2)
    inner_r = 200
    inner_points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        inner_points.append((cx + inner_r * math.cos(angle), cy + inner_r * math.sin(angle)))
    draw.polygon(inner_points, outline=(*CYAN, 130), width=1)

    for i, r in enumerate([60, 40, 20]):
        alpha = 200 - i * 50
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*ACCENT, alpha))

    card_w, card_h = 200, 130
    positions = [
        (200, 200, ACCENT),
        (w - 400, 250, CYAN),
        (180, h - 350, PURPLE),
        (w - 380, h - 380, ACCENT),
        (w // 2 - card_w // 2, 100, CYAN),
    ]
    for x, y, color in positions:
        rounded_rect(draw, [x, y, x + card_w, y + card_h], 14,
                     fill=(22, 27, 44, 220), outline=(*color, 180), width=1)
        for i, dot_color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
            draw.ellipse([x + 12 + i * 14, y + 12, x + 20 + i * 14, y + 20], fill=dot_color)
        for i in range(4):
            ly = y + 40 + i * 18
            line_w = card_w - 40 - (i * 15)
            rounded_rect(draw, [x + 16, ly, x + 16 + line_w, ly + 8], 4,
                         fill=(*color, 150))

    img = Image.alpha_composite(img, overlay)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    img.convert("RGB").save(os.path.join(IMG_DIR, "hero-illustration.png"), "PNG", optimize=True)
    print("Saved hero-illustration.png")


# App mockup
def make_app_mockup(filename, screen_color, accent_color, title, subtitle, chart_type="radial"):
    w, h = 800, 1200
    base = gradient_bg(w, h, c1=BG_DARK, c2=(15, 20, 35))
    base = add_glow_orbs(base, [
        (w * 0.5, h * 0.3, 250, accent_color, 50),
        (w * 0.3, h * 0.8, 200, accent_color, 40),
    ])
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    phone_w, phone_h = 380, 800
    px = (w - phone_w) // 2
    py = (h - phone_h) // 2
    draw_phone(draw, px, py, phone_w, phone_h, screen_color)

    sx, sy = px + 16, py + 28
    draw.text((sx, sy), "9:41", fill=TEXT)
    draw.text((px + phone_w - 60, sy), "5G", fill=TEXT)

    header_y = py + 80
    draw.text((px + 30, header_y), title, fill=TEXT)
    draw.text((px + 30, header_y + 30), subtitle, fill=TEXT_DIM)

    card_x, card_y = px + 24, header_y + 90
    card_w, card_h = phone_w - 48, 380
    rounded_rect(draw, [card_x, card_y, card_x + card_w, card_y + card_h], 18,
                 fill=(22, 27, 44, 240), outline=(*accent_color, 180), width=1)

    cx = card_x + card_w // 2
    cy = card_y + card_h // 2

    if chart_type == "radial":
        for i, r in enumerate([130, 100, 70]):
            for a in range(0, 360, 6):
                rad = math.radians(a)
                x1 = cx + r * math.cos(rad)
                y1 = cy + r * math.sin(rad)
                x2 = cx + (r + 8) * math.cos(rad)
                y2 = cy + (r + 8) * math.sin(rad)
                alpha = 80 + (a % 60) * 2
                if a > 270 - 60 * (3 - i):
                    color = accent_color
                else:
                    color = (60, 70, 100)
                draw.line([(x1, y1), (x2, y2)], fill=(*color, alpha), width=3)
        draw.text((cx - 40, cy - 12), "82%", fill=TEXT)
        draw.text((cx - 50, cy + 12), "Today", fill=TEXT_DIM)
    elif chart_type == "bars":
        bar_w = 18
        gap = 8
        for i in range(10):
            bh = random.randint(60, 220)
            bx = card_x + 30 + i * (bar_w + gap)
            by = card_y + card_h - 40 - bh
            color = accent_color if i > 5 else (60, 70, 100)
            rounded_rect(draw, [bx, by, bx + bar_w, card_y + card_h - 40], 4, fill=(*color, 220))
    elif chart_type == "wave":
        points = []
        for i in range(60):
            x = card_x + 30 + i * 5
            y = cy + math.sin(i * 0.3) * 80 + random.randint(-10, 10)
            points.append((x, y))
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=(*accent_color, 220), width=3)
        area = points + [(points[-1][0], card_y + card_h - 40), (points[0][0], card_y + card_h - 40)]
        draw.polygon(area, fill=(*accent_color, 60))
    elif chart_type == "grid":
        cell = 18
        gap = 4
        for r in range(7):
            for c in range(12):
                intensity = random.random()
                color = lerp((30, 35, 50), accent_color, intensity)
                bx = card_x + 24 + c * (cell + gap)
                by = card_y + 40 + r * (cell + gap)
                rounded_rect(draw, [bx, by, bx + cell, by + cell], 4, fill=(*color, 200))

    nav_y = py + phone_h - 60
    for i in range(4):
        bx = px + 40 + i * 80
        color = accent_color if i == 0 else TEXT_FAINT
        draw.ellipse([bx, nav_y, bx + 16, nav_y + 16], fill=color)

    img = Image.alpha_composite(base.convert("RGBA"), overlay)
    img.convert("RGB").save(os.path.join(IMG_DIR, filename), "PNG", optimize=True)
    print(f"Saved {filename}")


# Team illustration
def make_team_illustration():
    w, h = 1400, 900
    base = gradient_bg(w, h, c1=(10, 14, 26), c2=(20, 25, 45))
    base = add_glow_orbs(base, [
        (w * 0.15, h * 0.4, 280, ACCENT, 60),
        (w * 0.85, h * 0.6, 280, CYAN, 60),
        (w * 0.5, h * 0.5, 200, PURPLE, 40),
    ])
    base = add_grid(base, alpha=12)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    monitors = [
        (180, 250, 320, 220, ACCENT),
        (560, 180, 320, 220, CYAN),
        (940, 280, 320, 220, PURPLE),
        (350, 520, 320, 220, ACCENT),
        (730, 540, 320, 220, CYAN),
    ]
    for x, y, mw, mh, color in monitors:
        rounded_rect(draw, [x, y, x + mw, y + mh], 12,
                     fill=(20, 25, 40, 230), outline=(*color, 180), width=2)
        rounded_rect(draw, [x + 20, y + 20, x + mw - 20, y + 50], 6, fill=(*color, 100))
        for i in range(3):
            ly = y + 80 + i * 30
            lw = random.randint(120, mw - 80)
            rounded_rect(draw, [x + 20, ly, x + 20 + lw, ly + 8], 4,
                         fill=(*color, 80))
        draw.rectangle([x + mw // 2 - 30, y + mh, x + mw // 2 + 30, y + mh + 20], fill=(*color, 150))
        draw.rectangle([x + mw // 2 - 60, y + mh + 20, x + mw // 2 + 60, y + mh + 30], fill=(*color, 150))

    for _ in range(60):
        x = random.randint(0, w)
        y = random.randint(0, h)
        r = random.randint(2, 5)
        color = random.choice([ACCENT, CYAN, PURPLE, TEXT_DIM])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(*color, 150))

    img = Image.alpha_composite(base.convert("RGBA"), overlay)
    img.convert("RGB").save(os.path.join(IMG_DIR, "team-illustration.png"), "PNG", optimize=True)
    print("Saved team-illustration.png")


# Privacy illustration
def make_privacy_illustration():
    w, h = 1200, 800
    base = gradient_bg(w, h, c1=(10, 14, 26), c2=(15, 20, 40))
    base = add_glow_orbs(base, [
        (w * 0.5, h * 0.5, 300, ACCENT, 80),
        (w * 0.5, h * 0.5, 200, CYAN, 50),
    ])
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    cx, cy = w // 2, h // 2
    shield = [
        (cx, cy - 200),
        (cx + 150, cy - 150),
        (cx + 150, cy + 50),
        (cx, cy + 200),
        (cx - 150, cy + 50),
        (cx - 150, cy - 150),
    ]
    draw.polygon(shield, outline=(*CYAN, 220), width=4)
    inner = [
        (cx, cy - 160),
        (cx + 110, cy - 120),
        (cx + 110, cy + 30),
        (cx, cy + 160),
        (cx - 110, cy + 30),
        (cx - 110, cy - 120),
    ]
    draw.polygon(inner, fill=(20, 25, 40, 200), outline=(*ACCENT, 200), width=2)

    draw.ellipse([cx - 25, cy - 50, cx + 25, cy], fill=(*CYAN, 230))
    draw.rectangle([cx - 8, cy - 10, cx + 8, cy + 50], fill=(*CYAN, 230))

    for r in [240, 290, 340]:
        for a in range(0, 360, 8):
            rad = math.radians(a)
            x1 = cx + r * math.cos(rad)
            y1 = cy + r * math.sin(rad) * 0.7
            x2 = cx + (r + 6) * math.cos(rad)
            y2 = cy + (r + 6) * math.sin(rad) * 0.7
            alpha = 40 + (a % 90)
            color = ACCENT if a % 60 < 30 else CYAN
            draw.line([(x1, y1), (x2, y2)], fill=(*color, alpha), width=2)

    for i, angle in enumerate([0, 60, 120, 180, 240, 300]):
        rad = math.radians(angle)
        bx = cx + 320 * math.cos(rad)
        by = cy + 220 * math.sin(rad)
        color = [ACCENT, CYAN, PURPLE][i % 3]
        rounded_rect(draw, [bx - 30, by - 20, bx + 30, by + 20], 6,
                     fill=(*color, 200))
        for r in range(2):
            for c in range(4):
                px = bx - 24 + c * 12
                py = by - 10 + r * 8
                if random.random() > 0.4:
                    draw.rectangle([px, py, px + 6, py + 4], fill=(255, 255, 255, 230))

    img = Image.alpha_composite(base.convert("RGBA"), overlay)
    img.convert("RGB").save(os.path.join(IMG_DIR, "privacy-illustration.png"), "PNG", optimize=True)
    print("Saved privacy-illustration.png")


# Services illustration
def make_services_illustration():
    w, h = 1400, 900
    base = gradient_bg(w, h, c1=(10, 14, 26), c2=(20, 25, 45))
    base = add_glow_orbs(base, [
        (w * 0.2, h * 0.5, 250, ACCENT, 50),
        (w * 0.8, h * 0.5, 250, CYAN, 50),
    ])
    base = add_grid(base, alpha=14)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    stages = [
        (150, h // 2, "01", ACCENT),
        (370, h // 2, "02", CYAN),
        (590, h // 2, "03", PURPLE),
        (810, h // 2, "04", ACCENT),
        (1030, h // 2, "05", CYAN),
        (1250, h // 2, "06", PURPLE),
    ]
    for i, (x, y, num, color) in enumerate(stages):
        r = 60
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(*color, 200), outline=(255, 255, 255, 100), width=2)
        draw.text((x - 15, y - 12), num, fill=(10, 14, 26))
        draw.text((x - 30, y + 80), ["Discover", "Design", "Engineer", "Verify", "Ship", "Refine"][i],
                  fill=TEXT)
        if i < len(stages) - 1:
            ax1 = x + r + 8
            ax2 = stages[i + 1][0] - r - 8
            draw.line([(ax1, y), (ax2, y)], fill=(*TEXT_DIM, 180), width=2)
            draw.polygon([(ax2, y - 6), (ax2, y + 6), (ax2 + 8, y)], fill=(*TEXT_DIM, 200))

    for _ in range(40):
        x = random.randint(0, w)
        y = random.randint(50, h - 50)
        lw = random.randint(30, 200)
        color = random.choice([ACCENT, CYAN, PURPLE, TEXT_DIM])
        alpha = random.randint(40, 100)
        rounded_rect(draw, [x, y, x + lw, y + 4], 2, fill=(*color, alpha))

    img = Image.alpha_composite(base.convert("RGBA"), overlay)
    img.convert("RGB").save(os.path.join(IMG_DIR, "services-illustration.png"), "PNG", optimize=True)
    print("Saved services-illustration.png")


# Open Graph image
def make_og_image():
    w, h = 1200, 630
    base = gradient_bg(w, h, c1=(10, 14, 26), c2=(20, 25, 45))
    base = add_glow_orbs(base, [
        (200, 200, 250, ACCENT, 100),
        (1000, 400, 250, CYAN, 100),
        (600, 500, 200, PURPLE, 70),
    ])
    base = add_grid(base, alpha=15)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    cx, cy = w // 2, h // 2
    r = 50
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        points.append((cx + r * math.cos(angle), cy - 100 + r * math.sin(angle)))
    draw.polygon(points, outline=(*ACCENT, 220), width=3)
    draw.ellipse([cx - 18, cy - 118, cx + 18, cy - 82], fill=(*ACCENT, 230))

    rounded_rect(draw, [cx - 280, cy - 20, cx + 280, cy + 30], 6, fill=(*TEXT, 240))
    rounded_rect(draw, [cx - 200, cy + 50, cx + 200, cy + 90], 4, fill=(*TEXT_DIM, 200))

    img = Image.alpha_composite(base.convert("RGBA"), overlay)
    img.convert("RGB").save(os.path.join(IMG_DIR, "og-default.png"), "PNG", optimize=True)
    print("Saved og-default.png")


# Pattern
def make_pattern():
    w, h = 800, 800
    img = Image.new("RGB", (w, h), BG_DARK)
    draw = ImageDraw.Draw(img)
    spacing = 30
    for x in range(0, w, spacing):
        for y in range(0, h, spacing):
            d = 2
            dist = math.sqrt((x - w / 2) ** 2 + (y - h / 2) ** 2)
            if dist < 300:
                color = lerp(ACCENT, CYAN, dist / 300)
                draw.ellipse([x - d, y - d, x + d, y + d], fill=color)
    img.save(os.path.join(IMG_DIR, "pattern.png"), "PNG", optimize=True)
    print("Saved pattern.png")


# Download badges illustration
def make_download_illustration():
    w, h = 800, 500
    base = gradient_bg(w, h, c1=(15, 20, 35), c2=(10, 14, 26))
    base = add_glow_orbs(base, [
        (w * 0.3, h * 0.5, 200, ACCENT, 60),
        (w * 0.7, h * 0.5, 200, CYAN, 60),
    ])
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    badges = [
        (80, 200, 260, 110, "App Store", ACCENT),
        (460, 200, 260, 110, "Google Play", CYAN),
    ]
    for x, y, bw, bh, label, color in badges:
        rounded_rect(draw, [x, y, x + bw, y + bh], 16,
                     fill=(20, 25, 40, 240), outline=(*color, 200), width=2)
        rounded_rect(draw, [x + 20, y + 20, x + 90, y + bh - 20], 12,
                     fill=(*color, 200))
        rounded_rect(draw, [x + 110, y + 30, x + 110 + 100, y + 50], 4, fill=(*TEXT_DIM, 200))
        rounded_rect(draw, [x + 110, y + 60, x + 110 + 130, y + 80], 6, fill=(*TEXT, 240))

    img = Image.alpha_composite(base.convert("RGBA"), overlay)
    img.convert("RGB").save(os.path.join(IMG_DIR, "download-illustration.png"), "PNG", optimize=True)
    print("Saved download-illustration.png")


if __name__ == "__main__":
    make_hero_illustration()
    make_app_mockup("app-pulsetrack.png", screen_color=(15, 20, 35), accent_color=ACCENT,
                    title="PulseTrack", subtitle="Today's parameters", chart_type="radial")
    make_app_mockup("app-decidewise.png", screen_color=(15, 20, 35), accent_color=PURPLE,
                    title="DecideWise", subtitle="Decision matrix", chart_type="bars")
    make_app_mockup("app-chronoflow.png", screen_color=(15, 20, 35), accent_color=CYAN,
                    title="ChronoFlow", subtitle="Time visualization", chart_type="wave")
    make_app_mockup("app-moodcanvas.png", screen_color=(15, 20, 35), accent_color=(139, 127, 216),
                    title="MoodCanvas", subtitle="Mood journal", chart_type="grid")
    make_team_illustration()
    make_privacy_illustration()
    make_services_illustration()
    make_og_image()
    make_pattern()
    make_download_illustration()
    print("\nAll images generated successfully.")




