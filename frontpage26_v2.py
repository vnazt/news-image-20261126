# frontpage26_v2.py — THE WORLD IN ONE DAY, Thursday 26 November 2026
# Fresh rebuild from zero (v2). Written 100% fresh from dossier.md +
# dossier-add.md + v2-spec.md. No previous builder was read.
# Draws a dense illustrated broadsheet front page, 1024x1024, Pillow only.
import math, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
NAVY = (11, 31, 58)
NAVY2 = (16, 45, 84)
RED = (185, 28, 28)
GOLD = (201, 162, 39)
INK = (22, 22, 22)
GREY = (90, 86, 78)
CREAM_LINE = (210, 200, 175)

FDIR = "/usr/share/fonts/truetype/liberation/"
def F(name, size):
    return ImageFont.truetype(FDIR + name, size)
SERIF_B = lambda s: F("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: F("LiberationSerif-Regular.ttf", s)
SERIF_I = lambda s: F("LiberationSerif-Italic.ttf", s)
SERIF_BI = lambda s: F("LiberationSerif-BoldItalic.ttf", s)
SANS = lambda s: F("LiberationSans-Regular.ttf", s)
SANS_B = lambda s: F("LiberationSans-Bold.ttf", s)
SANS_I = lambda s: F("LiberationSans-Italic.ttf", s)

random.seed(20261126)

def wrap(d, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def txt(d, x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def vgrad(d, box, top, bottom):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for i in range(h):
        t = i / h
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)

def glow(base, cx, cy, r, color, alpha=90):
    """Soft radial glow on an RGBA overlay, composited onto base."""
    ov = Image.new("RGBA", base.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    steps = 6
    for i in range(steps, 0, -1):
        a = int(alpha * (1 - i / (steps + 1)) * 0.55)
        rr = r * i / steps
        od.ellipse([cx - rr, cy - rr * 0.75, cx + rr, cy + rr * 0.75],
                   fill=color + (a,))
    base.alpha_composite(ov)

def stars(d, box, n=24, seed=7):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = rnd.uniform(x0 + 4, x1 - 4)
        y = rnd.uniform(y0 + 3, y1 - 6)
        r = rnd.choice([1, 1, 1, 1.5])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 235, 220))

def windows(d, x, y, w, h, cols, rows, lit=(255, 214, 110), dark=(30, 42, 66)):
    cw, ch = w / cols, h / rows
    for r in range(rows):
        for c in range(cols):
            wx = x + c * cw + cw * 0.22
            wy = y + r * ch + ch * 0.22
            ww, wh = cw * 0.56, ch * 0.56
            if (r * 7 + c * 3) % 4 != 0:
                d.rectangle([wx, wy, wx + ww, wy + wh], fill=lit)
            else:
                d.rectangle([wx, wy, wx + ww, wy + wh], fill=dark)

def skyline(d, box, heights, base_y=None, color=(13, 22, 44)):
    x0, y0, x1, y1 = box
    n = len(heights)
    bw = (x1 - x0) / n
    by = base_y if base_y is not None else y1
    for i, hh in enumerate(heights):
        bx = x0 + i * bw + 1
        d.rectangle([bx, by - hh, bx + bw - 2, by], fill=color)
        windows(d, bx + 2, by - hh + 3, bw - 6, hh - 6, 3, max(2, int(hh / 14)))

def rain(d, box, n=26, seed=3):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = rnd.uniform(x0, x1)
        y = rnd.uniform(y0, y1 - 12)
        d.line([(x, y), (x - 3, y + 11)], fill=(190, 205, 225, 170), width=1)

def fire(d, cx, base_y, s=1.0):
    """Layered flame: outer red, mid orange, core yellow."""
    for (col, w, h) in [((220, 60, 20), 34, 34), ((245, 130, 30), 26, 26),
                        ((255, 200, 60), 16, 18)]:
        pts = [(cx - w * s / 2, base_y), (cx - w * s * 0.28, base_y - h * s * 0.7),
               (cx, base_y - h * s), (cx + w * s * 0.28, base_y - h * s * 0.7),
               (cx + w * s / 2, base_y)]
        d.polygon(pts, fill=col)

def smoke(d, cx, cy, s=1.0, n=5):
    for i in range(n):
        r = (10 + i * 5) * s
        x = cx + (i % 2) * 8 * s - 4 * s
        y = cy - i * 9 * s
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7],
                  fill=(120, 118, 112, 150))

def chip(d, x, y, code):
    """HOW-SURE chip. code: OF/CF/RP/CL. Returns width used."""
    conf = {"OF": ("OFFICIAL", NAVY), "CF": ("CONFIRMED", (22, 101, 52)),
            "RP": ("REPORTED", (180, 83, 9)), "CL": ("CLAIM", RED)}
    label, col = conf[code]
    f = SANS_B(8)
    w = int(d.textlength(label, font=f)) + 8
    d.rounded_rectangle([x, y, x + w, y + 11], radius=2, fill=col)
    d.text((x + 4, y + 1), label, font=f, fill=(255, 255, 255))
    return w

def minichip(d, x, y, code):
    """Tiny 2-letter HOW-SURE chip for the dense ALSO list. Returns width."""
    conf = {"OF": NAVY, "CF": (22, 101, 52), "RP": (180, 83, 9), "CL": RED}
    col = conf[code]
    f = SANS_B(7)
    w = int(d.textlength(code, font=f)) + 6
    d.rounded_rectangle([x, y, x + w, y + 9], radius=2, fill=col)
    d.text((x + 3, y), code, font=f, fill=(255, 255, 255))
    return w

def num_badge(d, x, y, n, r=10, fill=RED):
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=(255, 255, 255), width=1)
    d.text((x, y), str(n), font=SANS_B(11), fill=(255, 255, 255), anchor="mm")

def art_frame(d, box):
    d.rectangle(box, outline=INK, width=1)

# ---------------------------------------------------------------- scenes
def scene_macys(d, box):
    """Night skyline, big red balloon, rain. Hero 1."""
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y1), (24, 34, 66), (74, 96, 140))
    stars(d, (x0, y0, x1, y0 + 40), 18, seed=11)
    # clouds
    for (cx, cy, r) in [(x0 + 40, y0 + 22, 16), (x0 + 62, y0 + 18, 12),
                        (x1 - 46, y0 + 26, 15), (x1 - 26, y0 + 20, 11)]:
        d.ellipse([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], fill=(52, 62, 88))
    skyline(d, (x0, y1 - 52, x1, y1), [46, 30, 52, 38, 44, 28, 50, 34], base_y=y1)
    # big red balloon
    bx, by = (x0 + x1) // 2, y0 + 52
    d.ellipse([bx - 52, by - 20, bx + 52, by + 20], fill=(178, 34, 34),
              outline=(120, 18, 18), width=2)
    d.ellipse([bx - 52, by - 20, bx + 52, by - 2], fill=(205, 60, 55))
    d.polygon([(bx - 14, by + 20), (bx + 14, by + 20), (bx, by + 34)], fill=(120, 18, 18))
    d.rectangle([bx - 8, by + 34, bx + 8, by + 42], outline=(60, 30, 10), width=1)
    d.line([(bx - 30, by + 6), (bx - 52, by + 14)], fill=(230, 230, 230), width=1)
    rain(d, (x0, y0, x1, y1), 30, seed=5)

def scene_kuwait(d, box):
    """Desert dusk, radar + antenna, drone, explosion starburst. Hero 2."""
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y1), (64, 40, 66), (196, 120, 58))
    # sun low
    d.ellipse([x1 - 58, y0 + 16, x1 - 26, y0 + 48], fill=(240, 170, 80))
    # dunes
    d.polygon([(x0, y1), (x0, y1 - 26), (x0 + 110, y1 - 40), (x1, y1 - 22), (x1, y1)],
              fill=(146, 96, 52))
    d.polygon([(x0, y1), (x0, y1 - 12), (x0 + 150, y1 - 22), (x1, y1 - 10), (x1, y1)],
              fill=(110, 70, 38))
    # radar mast + dish (left)
    mx, my = x0 + 52, y1 - 18
    d.line([(mx, my), (mx, my - 52)], fill=(40, 32, 28), width=3)
    d.arc([mx - 26, my - 78, mx + 6, my - 46], 200, 340, fill=(230, 225, 210), width=3)
    d.line([(mx, my - 62), (mx + 16, my - 70)], fill=(230, 225, 210), width=2)
    d.ellipse([mx - 3, my - 58, mx + 3, my - 52], fill=(255, 220, 120))
    # antenna (right)
    ax = x1 - 44
    d.line([(ax, y1 - 14), (ax, y1 - 58)], fill=(40, 32, 28), width=2)
    for k in range(3):
        yy = y1 - 50 + k * 7
        d.line([(ax - 10, yy), (ax + 10, yy)], fill=(40, 32, 28), width=1)
    d.ellipse([ax - 3, y1 - 62, ax + 3, y1 - 56], fill=(255, 90, 60))
    # drone (centre-top)
    dx, dy = (x0 + x1) // 2 + 18, y0 + 34
    d.ellipse([dx - 12, dy - 4, dx + 12, dy + 4], fill=(35, 35, 40))
    d.line([(dx - 20, dy - 8), (dx + 20, dy - 8)], fill=(35, 35, 40), width=2)
    d.ellipse([dx - 24, dy - 11, dx - 14, dy - 8], fill=(120, 120, 120))
    d.ellipse([dx + 14, dy - 11, dx + 24, dy - 8], fill=(120, 120, 120))
    # explosion starburst near antenna
    ex, ey = x1 - 66, y1 - 46
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        r = 26 if i % 2 == 0 else 11
        pts.append((ex + r * math.cos(ang), ey + r * math.sin(ang) * 0.8))
    d.polygon(pts, fill=(255, 190, 60))
    pts2 = []
    for i in range(12):
        ang = math.pi * i / 6
        r = 14 if i % 2 == 0 else 6
        pts2.append((ex + r * math.cos(ang), ey + r * math.sin(ang) * 0.8))
    d.polygon(pts2, fill=(255, 90, 30))
    d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 240, 180))

def scene_eu(d, box):
    """Summit room in slight perspective: wall flag + late-hour clock,
    delegates behind a thick oval table, name plates, star centrepiece,
    NO DEAL banner across the table front. Hero 3."""
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y1), (28, 40, 72), (52, 68, 104))
    cx = (x0 + x1) // 2
    # picture rail on the wall
    d.line([(x0, y0 + 36), (x1, y0 + 36)], fill=(120, 100, 60), width=1)
    # big EU flag on the wall, left
    fx0, fy0, fx1, fy1 = x0 + 14, y0 + 7, x0 + 66, y0 + 33
    d.rectangle([fx0, fy0, fx1, fy1], fill=(0, 51, 153), outline=(220, 220, 210))
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        sx = (fx0 + fx1) / 2 + 11 * math.cos(ang)
        sy = (fy0 + fy1) / 2 + 8 * math.sin(ang)
        d.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=(255, 215, 0))
    # wall clock, right — inset from the panel edge, hands near midnight
    ccx, ccy, cr = x1 - 26, y0 + 20, 12
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr],
              fill=(240, 238, 225), outline=(40, 40, 40), width=2)
    for hh in range(12):
        ang = math.pi * hh / 6
        tx = ccx + (cr - 2) * math.sin(ang)
        ty = ccy - (cr - 2) * math.cos(ang)
        d.ellipse([tx - 1, ty - 1, tx + 1, ty + 1], fill=(40, 40, 40))
    d.line([(ccx, ccy), (ccx, ccy - cr + 4)], fill=(40, 40, 40), width=2)
    d.line([(ccx, ccy), (ccx - 5, ccy - 3)], fill=(40, 40, 40), width=2)
    d.ellipse([ccx - 2, ccy - 2, ccx + 2, ccy + 2], fill=(40, 40, 40))
    # far-side delegates: heads + shoulders above the table
    for fx in [cx - 104, cx - 52, cx, cx + 52, cx + 104]:
        d.ellipse([fx - 5, y0 + 40, fx + 5, y0 + 50], fill=(235, 220, 195))
        d.rounded_rectangle([fx - 11, y0 + 50, fx + 11, y0 + 58], radius=3,
                            fill=(28, 28, 36))
    # table: dark side band (thickness) first, then the top surface
    d.ellipse([cx - 130, y0 + 62, cx + 130, y0 + 86], fill=(74, 46, 22))
    d.ellipse([cx - 130, y0 + 56, cx + 130, y0 + 80], fill=(120, 74, 40),
              outline=(70, 42, 20), width=2)
    d.ellipse([cx - 122, y0 + 59, cx + 122, y0 + 77], outline=(160, 104, 58),
              width=1)
    # name plates on the table in front of each delegate
    for fx in [cx - 104, cx - 52, cx, cx + 52, cx + 104]:
        d.rectangle([fx - 9, y0 + 60, fx + 9, y0 + 66], fill=(245, 242, 230),
                    outline=(120, 110, 90))
        d.line([(fx - 6, y0 + 63), (fx + 6, y0 + 63)], fill=(120, 110, 90),
               width=1)
    # star centrepiece + €45bn on the table surface
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        sx = cx - 34 + 10 * math.cos(ang)
        sy = y0 + 68 + 6 * math.sin(ang)
        d.ellipse([sx - 1.8, sy - 1.8, sx + 1.8, sy + 1.8], fill=(255, 215, 0))
    d.text((cx + 6, y0 + 68), "€45bn", font=SERIF_B(14), fill=(255, 255, 255),
           anchor="lm")
    # near-side chair backs in the foreground corners
    for fx in [x0 + 26, x1 - 26]:
        d.rounded_rectangle([fx - 12, y0 + 88, fx + 12, y1 - 2], radius=3,
                            fill=(24, 24, 32))
    # NO DEAL banner across the table front
    d.rectangle([cx - 46, y0 + 84, cx + 46, y0 + 96], fill=(185, 28, 28))
    d.text((cx, y0 + 90), "NO DEAL", font=SANS_B(11), fill=(255, 255, 255),
           anchor="mm")

def scene_kyiv(d, box):
    """Night skyline, missile trails, fire glow. Scene 4."""
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y1), (12, 16, 38), (52, 44, 74))
    stars(d, (x0, y0, x1, y0 + 30), 14, seed=21)
    skyline(d, (x0, y1 - 26, x1, y1), [30, 44, 26, 40, 34, 46, 30], base_y=y1)
    # missile trails (arcs with glow dots)
    for (sx, sy, ex, ey) in [(x0 + 20, y0 + 8, x0 + 70, y0 + 34),
                             (x1 - 30, y0 + 6, x1 - 80, y0 + 30),
                             (x0 + 90, y0 + 4, x0 + 120, y0 + 26)]:
        d.line([(sx, sy), (ex, ey)], fill=(255, 200, 120), width=2)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 220, 150))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 240, 200))
    # fire glow bottom-left
    fire(d, x0 + 34, y1 - 2, 0.8)
    fire(d, x1 - 30, y1 - 2, 0.6)
    smoke(d, x0 + 34, y1 - 34, 0.7, 3)

def scene_ebola(d, box):
    """Treatment tent + health worker + red cross. Scene 5."""
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y1), (214, 196, 168), (168, 142, 110))
    d.rectangle([x0, y1 - 14, x1, y1], fill=(120, 96, 66))
    # tent
    tx, ty = (x0 + x1) // 2 - 14, y1 - 16
    d.polygon([(tx - 58, ty), (tx, ty - 52), (tx + 58, ty)], fill=(238, 232, 214),
              outline=(90, 80, 66))
    d.polygon([(tx - 58, ty), (tx, ty - 52), (tx + 58, ty)], outline=(90, 80, 66))
    d.polygon([(tx - 16, ty), (tx, ty - 22), (tx + 16, ty)], fill=(60, 52, 44))
    # red cross on tent
    d.rectangle([tx - 3, ty - 44, tx + 3, ty - 32], fill=RED)
    d.rectangle([tx - 9, ty - 41, tx + 9, ty - 35], fill=RED)
    # health worker (PPE)
    wx = x1 - 34
    d.ellipse([wx - 7, y1 - 52, wx + 7, y1 - 38], fill=(240, 240, 230))  # hood
    d.rectangle([wx - 9, y1 - 38, wx + 9, y1 - 14], fill=(250, 250, 244))  # gown
    d.rectangle([wx - 9, y1 - 34, wx - 4, y1 - 20], fill=(240, 240, 230))
    d.rectangle([wx + 4, y1 - 34, wx + 9, y1 - 20], fill=(240, 240, 230))
    # fence posts + sign
    d.rectangle([x0 + 8, y1 - 30, x0 + 44, y1 - 18], fill=(250, 248, 240),
                outline=(90, 80, 66))
    d.text((x0 + 26, y1 - 24), "12,021", font=SANS_B(9), fill=RED, anchor="mm")

def scene_ecb(d, box):
    """Euro symbol + Frankfurt tower. Scene 6."""
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y1), (18, 32, 64), (52, 78, 120))
    stars(d, (x0, y0, x1, y0 + 26), 10, seed=31)
    # tower
    tx = x0 + 26
    d.rectangle([tx, y0 + 22, tx + 46, y1], fill=(22, 30, 52))
    windows(d, tx + 4, y0 + 26, 38, y1 - y0 - 30, 3, 6)
    d.polygon([(tx - 4, y0 + 22), (tx + 23, y0 + 6), (tx + 50, y0 + 22)],
              fill=(30, 42, 70))
    # big euro
    d.text((x1 - 52, y0 + 34), "€", font=SERIF_B(52), fill=GOLD, anchor="mm")
    d.text((x1 - 52, y0 + 66), "ECB", font=SANS_B(10), fill=(255, 255, 255), anchor="mm")
    # small skyline
    skyline(d, (x0 + 80, y1 - 18, x1, y1), [18, 26, 16], base_y=y1)

def scene_korea(d, box):
    """Rate bar chart. Scene 7. (Caption below carries the title.)"""
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(238, 234, 222))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=1)
    base = y1 - 16
    vals = [("JUL", 2.50, 16), ("SEP", 2.75, 21), ("OCT", 3.00, 26), ("NOV", 3.25, 31)]
    bw = 26
    gap = (x1 - x0 - 20 - 4 * bw) // 3
    x = x0 + 12
    for (lab, v, h) in vals:
        col = RED if lab == "NOV" else NAVY
        d.rectangle([x, base - h, x + bw, base], fill=col)
        # value label INSIDE the bar (white) so it can't hit the badge
        d.text((x + bw / 2, base - h + 2), f"{v:.2f}%", font=SANS_B(8),
               fill=(255, 255, 255), anchor="ma")
        d.text((x + bw / 2, base + 3), lab, font=SANS(7), fill=GREY, anchor="ma")
        x += bw + gap

def scene_hk(d, box):
    """Candle rows at night, 168. Scene 8."""
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y1), (16, 18, 40), (44, 40, 66))
    stars(d, (x0, y0, x1, y0 + 24), 12, seed=41)
    # building silhouette
    d.rectangle([x0 + 8, y0 + 18, x0 + 52, y1 - 22], fill=(24, 26, 48))
    windows(d, x0 + 12, y0 + 22, 36, y1 - y0 - 48, 3, 5)
    # candle rows (caption below already says 168 dead)
    for r in range(3):
        yy = y1 - 34 + r * 12
        for c in range(9):
            cx = x0 + 66 + c * 14
            d.rectangle([cx - 2, yy, cx + 2, yy + 9], fill=(245, 240, 225))
            d.ellipse([cx - 2.5, yy - 5, cx + 2.5, yy], fill=(255, 190, 60))

def scene_cairo(d, box):
    """Street memorial: candles + flowers for the 31 dead. Scene 9.
    (The blast was 25 Nov; the 26-Nov story is the mourning + arrest.)"""
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y1), (40, 34, 52), (86, 66, 70))
    # wall
    d.rectangle([x0, y0 + 26, x1, y1 - 18], fill=(96, 80, 72))
    d.line([(x0, y0 + 26), (x1, y0 + 26)], fill=(70, 58, 52), width=2)
    # flowers (small coloured dots in rows)
    rnd = random.Random(99)
    for r in range(2):
        yy = y0 + 34 + r * 12
        for c in range(10):
            cx = x0 + 14 + c * 17
            col = rnd.choice([(200, 60, 60), (240, 220, 230), (230, 180, 60),
                              (180, 60, 120)])
            d.ellipse([cx - 3, yy - 3, cx + 3, yy + 3], fill=col)
    # candles row
    for c in range(8):
        cx = x0 + 22 + c * 19
        d.rectangle([cx - 2, y1 - 40, cx + 2, y1 - 28], fill=(245, 240, 225))
        d.ellipse([cx - 2.5, y1 - 45, cx + 2.5, y1 - 40], fill=(255, 190, 60))
    # plaque
    d.rectangle([(x0 + x1) // 2 - 34, y1 - 16, (x0 + x1) // 2 + 34, y1 - 4],
                fill=(40, 34, 40))
    d.text(((x0 + x1) // 2, y1 - 10), "31 LIVES", font=SANS_B(8),
           fill=(240, 230, 200), anchor="mm")

def scene_bangkok(d, box):
    """Refinery towers + fire + smoke. Scene 10."""
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y1), (58, 52, 66), (140, 96, 60))
    # towers
    for (tx, tw, th) in [(x0 + 14, 20, 52), (x0 + 44, 16, 64), (x0 + 66, 24, 44),
                         (x1 - 46, 18, 58), (x1 - 22, 14, 40)]:
        d.rectangle([tx, y1 - 14 - th, tx + tw, y1 - 14], fill=(52, 48, 54))
        d.rectangle([tx + 3, y1 - 14 - th, tx + tw - 3, y1 - 14 - th + 4],
                    fill=(90, 84, 90))
    # pipes
    d.line([(x0 + 34, y1 - 40), (x1 - 30, y1 - 40)], fill=(70, 64, 70), width=3)
    # fire at base of two towers
    fire(d, x0 + 52, y1 - 12, 0.9)
    fire(d, x1 - 36, y1 - 12, 0.7)
    # smoke kept short so it stays inside the art box
    smoke(d, x0 + 52, y1 - 30, 0.7, 3)
    smoke(d, x1 - 36, y1 - 28, 0.6, 3)
    # ground
    d.rectangle([x0, y1 - 14, x1, y1], fill=(40, 36, 40))

def scene_chess(d, box):
    """Chess board + clocks, Gukesh vs Sindarov. Scene 11."""
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(232, 226, 208))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=1)
    # board (46px, fits the strip)
    bx, by, bs = x0 + 8, y0 + 6, 46
    sq = bs / 8
    for r in range(8):
        for c in range(8):
            col = (238, 232, 210) if (r + c) % 2 == 0 else (52, 52, 60)
            d.rectangle([bx + c * sq, by + r * sq, bx + (c + 1) * sq, by + (r + 1) * sq],
                        fill=col)
    for (c, r, col) in [(4, 0, (255, 255, 255)), (3, 0, (255, 255, 255)),
                        (4, 7, (20, 20, 20)), (5, 7, (20, 20, 20)),
                        (2, 3, (255, 255, 255)), (5, 4, (20, 20, 20))]:
        cx, cy = bx + (c + 0.5) * sq, by + (r + 0.5) * sq
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=col,
                  outline=(120, 100, 60), width=1)
    # clocks (right side, clear of the number badge)
    for (cx, label, t) in [(x1 - 80, "GUKESH", "1:32"), (x1 - 50, "SINDAROV", "0:06")]:
        d.rounded_rectangle([cx - 13, by + 2, cx + 13, by + 24], radius=3,
                            fill=(30, 30, 34))
        d.text((cx, by + 9), t, font=SANS_B(9), fill=(255, 220, 120), anchor="mm")
        d.text((cx, by + 19), label, font=SANS(6), fill=(220, 220, 210), anchor="mm")
    # venue tag in the middle gap
    d.text(((bx + bs + x1 - 82) // 2, by + 12), "GENEVA", font=SANS_B(8),
           fill=GREY, anchor="mm")
    d.text(((bx + bs + x1 - 82) // 2, by + 24), "GAME 3", font=SANS(8),
           fill=GREY, anchor="mm")
    # score line
    d.text(((x0 + x1) // 2, y1 - 5), "60 MOVES · 1.5–1.5",
           font=SANS_B(9), fill=NAVY, anchor="mm")

def scene_bogor(d, box):
    """Mine shaft + rescue cage + rain. Scene 12."""
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y1), (52, 62, 52), (110, 104, 78))
    rain(d, (x0, y0, x1, y1), 22, seed=77)
    # hill
    d.polygon([(x0, y1), (x0, y1 - 34), (x0 + 90, y1 - 52), (x1, y1 - 30), (x1, y1)],
              fill=(72, 84, 58))
    # shaft opening
    sx = (x0 + x1) // 2
    d.rectangle([sx - 22, y1 - 44, sx + 22, y1 - 6], fill=(28, 24, 20))
    d.rectangle([sx - 22, y1 - 44, sx + 22, y1 - 40], fill=(120, 100, 70))
    # winch frame + rope + cage
    d.line([(sx - 30, y1 - 44), (sx - 30, y1 - 66)], fill=(60, 52, 44), width=3)
    d.line([(sx + 30, y1 - 44), (sx + 30, y1 - 66)], fill=(60, 52, 44), width=3)
    d.line([(sx - 30, y1 - 66), (sx + 30, y1 - 66)], fill=(60, 52, 44), width=3)
    d.line([(sx, y1 - 66), (sx, y1 - 46)], fill=(220, 210, 180), width=2)
    d.rectangle([sx - 10, y1 - 46, sx + 10, y1 - 28], outline=(220, 210, 180), width=2)
    d.line([(sx - 10, y1 - 37), (sx + 10, y1 - 37)], fill=(220, 210, 180), width=1)
    # rescue workers
    for wx in [x0 + 24, x1 - 26]:
        d.ellipse([wx - 5, y1 - 34, wx + 5, y1 - 24], fill=(255, 200, 60))
        d.rectangle([wx - 6, y1 - 24, wx + 6, y1 - 8], fill=(230, 110, 40))
    # flood water
    d.rectangle([x0, y1 - 8, x1, y1], fill=(70, 96, 120))

def scene_canary(d, box):
    """Boats at sea, El Hierro. Scene 13."""
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y1), (126, 164, 196), (40, 78, 120))
    # sun + clouds
    d.ellipse([x1 - 44, y0 + 8, x1 - 20, y0 + 32], fill=(245, 230, 170))
    for (cx, cy, r) in [(x0 + 34, y0 + 16, 12), (x0 + 52, y0 + 12, 9)]:
        d.ellipse([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5], fill=(235, 238, 242))
    # island
    d.polygon([(x0 + 8, y1 - 30), (x0 + 40, y1 - 52), (x0 + 78, y1 - 30)],
              fill=(86, 96, 66))
    # boats
    for (bx, by, s) in [(x0 + 96, y1 - 40, 1.0), (x1 - 62, y1 - 28, 0.8)]:
        d.polygon([(bx - 22 * s, by), (bx + 22 * s, by), (bx + 14 * s, by + 9 * s),
                   (bx - 14 * s, by + 9 * s)], fill=(120, 60, 40))
        d.polygon([(bx - 2, by - 20 * s), (bx - 2, by), (bx + 12 * s, by)],
                  fill=(245, 242, 230))
        d.line([(bx, by - 20 * s), (bx, by)], fill=(60, 50, 40), width=1)
        for px in range(5):
            d.ellipse([bx - 16 * s + px * 7 * s - 1, by + 3 * s,
                       bx - 16 * s + px * 7 * s + 1, by + 5 * s], fill=(30, 30, 30))
    # waves
    for yy in [y1 - 18, y1 - 10]:
        for xx in range(x0 + 6, x1 - 10, 22):
            d.arc([xx, yy - 3, xx + 16, yy + 3], 180, 360, fill=(220, 235, 245), width=1)

# ---------------------------------------------------------------- map
# Hand-built land bitmap: 24 rows, lat 84..-54 in 6 deg steps; each row is
# a list of (first_col, last_col) land spans, cols = 5 deg lon steps
# (col 0 = -180..-175, col 36 = 0..5, col 71 = 175..180).
LAND_BITMAP = [
    [(4, 7), (11, 19), (25, 30)],                                  # 84
    [(2, 8), (10, 22), (25, 32), (38, 41), (44, 50), (55, 60), (64, 71)],  # 78
    [(2, 8), (10, 22), (25, 31), (44, 71)],                        # 72
    [(2, 8), (9, 25), (37, 41), (42, 71)],                         # 66
    [(3, 8), (9, 25), (35, 36), (37, 42), (42, 71)],               # 60
    [(9, 25), (34, 42), (42, 71)],                                 # 54
    [(11, 25), (34, 42), (42, 64)],                                # 48
    [(11, 22), (34, 42), (42, 47), (47, 63), (62, 64)],            # 42
    [(11, 21), (34, 43), (43, 48), (48, 61)],                      # 36
    [(13, 19), (34, 43), (43, 47), (49, 53), (56, 60)],            # 30
    [(14, 19), (33, 43), (44, 47), (50, 53), (55, 57), (60, 60)],  # 24
    [(15, 19), (33, 43), (51, 52), (55, 57), (60, 60)],            # 18
    [(17, 20), (33, 38), (43, 46), (51, 51), (55, 57), (60, 60)],  # 12
    [(21, 22), (34, 38), (38, 42), (55, 60)],                      # 6
    [(20, 29), (38, 44), (55, 64), (64, 66)],                      # 0
    [(20, 29), (38, 44), (57, 64), (64, 66)],                      # -6
    [(21, 28), (38, 43), (44, 46), (62, 66)],                      # -12
    [(22, 28), (39, 43), (45, 46), (60, 66)],                      # -18
    [(22, 28), (39, 42), (59, 66)],                                # -24
    [(22, 26), (39, 42), (59, 66), (69, 71)],                      # -30
    [(22, 24), (64, 66), (69, 70)],                                # -36
    [(21, 23)],                                                     # -42
    [(21, 23)],                                                     # -48
    [(22, 23)],                                                     # -54
]
REGION_COL = {
    "NA": (31, 78, 121), "EU": (46, 107, 52), "ME": (139, 69, 19),
    "AF": (122, 62, 157), "EA": (185, 28, 28), "SEA": (14, 116, 144),
    "SA": (194, 65, 12), "LAT": (77, 124, 15), "SP": (51, 65, 85),
}
PINS = [  # (lon, lat, num, region, dx, dy) — dx/dy = display offset for legibility
    (-74, 40.7, 1, "NA", 0, 0), (47.5, 29.3, 2, "ME", 0, 0),
    (4.35, 50.85, 3, "EU", -8, -9), (30.5, 50.45, 4, "EU", 0, 0),
    (25, 0, 5, "AF", 0, 0), (8.68, 50.11, 6, "EU", 16, -5),
    (127, 37.5, 7, "EA", 0, 0), (114.2, 22.3, 8, "EA", 0, 0),
    (31.2, 30.05, 9, "AF", 12, 7), (100.5, 13.75, 10, "SEA", 0, 0),
    (6.14, 46.2, 11, "EU", -10, 9), (106.8, -6.6, 12, "SEA", 0, 0),
    (-18, 28.3, 13, "EU", 0, 0),
]

def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(238, 234, 220), outline=INK, width=1)
    mw, mh = x1 - x0, y1 - y0
    # dense uniform dot grid (7px); each dot's lon/lat is tested against
    # the hand-built land bitmap (nearest cell) so the continents read.
    step, dot_r = 7, 2.2
    for gy in range(int(mh // step)):
        py = y0 + step / 2 + gy * step
        lat = 83 - (py - y0) / mh * 138
        row = max(0, min(23, int(round((84 - lat) / 6))))
        spans = LAND_BITMAP[row]
        for gx in range(int(mw // step)):
            px = x0 + step / 2 + gx * step
            lon = -180 + (px - x0) / mw * 360
            col = max(0, min(71, int(round((lon + 180) / 5))))
            if any(a <= col <= b for (a, b) in spans):
                d.ellipse([px - dot_r, py - dot_r, px + dot_r, py + dot_r],
                          fill=(70, 88, 118))
    for (lon, lat, n, reg, dx, dy) in PINS:
        px = x0 + (lon + 180) / 360 * mw
        py = y0 + (83 - lat) / 138 * mh
        qx, qy = px + dx, py + dy
        if dx or dy:
            d.line([(px, py), (qx, qy)], fill=(90, 86, 78), width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(90, 86, 78))
        r = 8
        d.ellipse([qx - r, qy - r, qx + r, qy + r], fill=REGION_COL[reg],
                  outline=(255, 255, 255), width=1)
        d.text((qx, qy), str(n), font=SANS_B(9), fill=(255, 255, 255), anchor="mm")

# ---------------------------------------------------------------- data
HEROES = [
    dict(num=1, art=scene_macys, date="NEW YORK — 26 NOV", chip="CF",
         head="MACY'S 100TH PARADE POSTPONED",
         sub="Thanksgiving nor'easter grounds the centenary parade — a first in 100 years. 750,000+ without power.",
         why="WHY IT MATTERS — Thanksgiving Day itself had no parade, ever.",
         src="Sources: CNN, USA Today, FlightAware"),
    dict(num=2, art=scene_kuwait, date="KUWAIT / HORMUZ — 26 NOV", chip="CF",
         head="THE GULF WAR WIDENS",
         sub="Iranian drones kill 2 Italians in Kuwait; Houthis hit Jazan refinery; Brent $96.57.",
         why="WHY IT MATTERS — The war reached Kuwait — and oil spiked.",
         src="Sources: Reuters, CNN — attribution disputed: Tehran denies"),
    dict(num=3, art=scene_eu, date="BRUSSELS — 26 NOV", chip="CF",
         head="EU SUMMIT FAILS ON BUDGET + €45BN LOAN",
         sub="No deal on the 2028–34 budget or the Ukraine loan — deferred to 17–18 Dec — as the ECB picks Hernández de Cos.",
         why="WHY IT MATTERS — Ukraine's money now waits on December.",
         src="Sources: Reuters, Agence Europe"),
]
SCENES = [
    dict(num=4, art=scene_kyiv, date="KYIV — 26 NOV", chip="CF",
         head="MISSILES HIT KYIV",
         sub="Ballistic missiles wound 7; Zelenskyy warns of a mass strike"),
    dict(num=5, art=scene_ebola, date="DRC — 26 NOV", chip="OF",
         head="EBOLA PASSES 12,000 CASES",
         sub="5,904 dead; fastest-growing outbreak on record"),
    dict(num=6, art=scene_ecb, date="FRANKFURT — 26 NOV", chip="CF",
         head="ECB PICKS HERNÁNDEZ DE COS",
         sub="First Spaniard to head the bank; Lagarde out 7 Feb"),
    dict(num=7, art=scene_korea, date="SEOUL — 26 NOV", chip="OF",
         head="KOREA LIFTS RATE TO 3.25%",
         sub="Third hike since July; 2027 growth seen at 4.1%"),
    dict(num=8, art=scene_hk, date="HONG KONG — 26 NOV", chip="CF",
         head="ONE YEAR AFTER WANG FUK FIRE",
         sub="168 dead remembered; flowers at Tai Po"),
    dict(num=9, art=scene_cairo, date="CAIRO — 26 NOV", chip="CF",
         head="CAIRO MOURNS 31 KILLED",
         sub="Driver arrested after tanker blast; anger grows"),
    dict(num=10, art=scene_bangkok, date="BANGKOK — 26 NOV", chip="CF",
         head="REFINERY BLAST INJURES 7–9",
         sub="Bangchak shuts all units; cause unknown"),
    dict(num=11, art=scene_chess, date="GENEVA — 26 NOV", chip="CF",
         head="GUKESH–SINDAROV: 60-MOVE DRAW",
         sub="Game 3 drawn; match level at 1.5–1.5"),
    dict(num=12, art=scene_bogor, date="BOGOR — 26 NOV", chip="CF",
         head="MINE TOLL RISES TO 13",
         sub="13 still trapped; rain halts the rescue"),
    dict(num=13, art=scene_canary, date="EL HIERRO — 26 NOV", chip="CF",
         head="CANARIES PASS 16,000 IN NOV",
         sub="Busiest month on the Atlantic route"),
]
ALSO = [
    (3, "CF", "NFL — Bears 39–35 Lions, Eagles 39–38 Cowboys, Bills 13–10 Chiefs: three final-minute thrillers"),
    (5, "CF", "MUMBAI — 18 years since 26/11; city on high alert, tributes at the Taj"),
    (9, "CF", "GAZA — Israeli strikes kill 9–10, incl. Hamas minister Abu Nada"),
    (12, "CF", "IRBIL — Thousands protest as Baghdad seizes Kurdish oil and borders"),
    (15, "CF", "BISSAU — Junta postpones elections to Nov 2028, a year after the coup"),
    (16, "CF", "ITURI — UN peacekeepers step up protection as fighting displaces thousands"),
    (17, "CF", "SENEGAL — Record November crossings as young risk the Atlantic"),
    (20, "CF", "MYANMAR — Won't fully comply with ICJ genocide orders"),
    (22, "CF", "PYONGYANG — Kim calls tactical-nuke deployment 'urgent' (KCNA)"),
    (24, "OF", "LONDON — Net migration falls to 77,000, lowest since 1997"),
    (25, "CF", "PARIS — Depardieu ordered to stand trial for alleged 2018 rape"),
    (27, "CF", "MEXICO CITY — Sheinbaum blasts DEA tip lines as 'interference'"),
    (28, "OF", "HAITI — WHO chief pledges $1m for last major public hospital"),
    (29, "CF", "TARIFFS — China, EU reject new 14-economy US tariff plan (reactions)"),
    (30, "CF", "MIAMI — FedEx delays top 3½ hours after jet overruns runway"),
    (31, "CF", "COLOGNE — Two arrested over alleged synagogue bomb plot"),
    (34, "OF", "SHIPPING — UNCTAD: maritime trade to stall at zero growth in 2026"),
    (35, "CF", "EUROPA LEAGUE — Bournemouth stay perfect; Milan, Juve fight back"),
    (36, "OF", "LONDON — UK–EU treaty texts published with 10-year exit clause"),
    (37, "CF", "IBIZA — Diesel tanker capsizes; one crew member dies"),
    (38, "CF", "STOCKHOLM — Centre backs Kristersson for PM in major shift"),
    (42, "CF", "DHAKA — Fresh garment-wage protests met with tear gas"),
    (43, "CF", "WASHINGTON — Trump calls revised GDP data 'fake', demands probe"),
    (44, "CF", "TENNIS — Sinner to miss Australian Open after knee surgery"),
]
DATECHECK = [
    "25 Nov — US tariff plan on 14 economies",
    "25 Nov — Asian chip rout (Kospi −6.2%)",
    "25 Nov — Shenzhou-24 docks at Tiangong",
    "25 Nov — Cairo tanker blast (31 dead)",
    "25 Nov — Houthi Ras Tanura refinery claim",
    "25 Nov — $621.9m F-16 package for Ukraine",
    "25 Nov — EU €50bn tech fund proposed",
    "24 Nov — Huawei convicted (10 of 12 counts)",
    "23 Nov — Bogor mine flood",
    "23 Nov — COP31 collapse · NATO session · Merkury sunk",
]
NUMBERS = [
    ("750,000+", "WITHOUT POWER IN US STORM"),
    ("2", "ITALIANS KILLED IN KUWAIT"),
    ("€45bn", "UKRAINE LOAN BLOCKED"),
    ("12,021", "EBOLA CASES IN DRC"),
    ("77,000", "UK NET MIGRATION"),
    ("3.25%", "BANK OF KOREA RATE"),
]
REGIONS = [
    ("N. AMERICA", 6, (31, 78, 121)), ("EUROPE", 10, (46, 107, 52)),
    ("M. EAST", 5, (139, 69, 19)), ("AFRICA", 5, (122, 62, 157)),
    ("E. ASIA", 3, (185, 28, 28)), ("SE ASIA", 3, (14, 116, 144)),
    ("S. ASIA", 2, (194, 65, 12)), ("LATAM", 2, (77, 124, 15)),
    ("SPORT", 5, (51, 65, 85)),
]
UTC_EVENTS = [
    ("EARLY", "Ibiza tanker capsizes; 1 dies"),
    ("MORNING", "Nor'easter peaks; 750,000+ dark"),
    ("07:45 UTC", "Bangkok refinery blast; 7–9 hurt"),
    ("26 NOV", "Ebola passes 12,000 in DRC"),
    ("EVENING", "Europa League: Bournemouth 5 from 5"),
    ("26 NOV", "EU summit ends: no deal"),
]

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0
    # --- top bar
    d.rectangle([0, y, W, y + 28], fill=NAVY)
    d.text((10, y + 14), "THE WORLD IN ONE DAY", font=SANS_B(13),
           fill=(255, 255, 255), anchor="lm")
    rt = "41 STORIES · NINE REGIONS · ALL FROM THURSDAY 26 NOVEMBER 2026"
    d.text((W - 10, y + 14), rt, font=SANS_B(10), fill=GOLD, anchor="rm")
    y += 28
    # --- masthead (centred two-tone date)
    _w1 = d.textlength("Thursday ", font=SERIF_B(42))
    _w2 = d.textlength("26 November 2026", font=SERIF_B(42))
    _sx = (W - _w1 - _w2) / 2
    d.text((_sx, y + 2), "Thursday ", font=SERIF_B(42), fill=INK, anchor="la")
    d.text((_sx + _w1, y + 2), "26 November 2026", font=SERIF_B(42), fill=RED,
           anchor="la")
    sub = ("A storm stops a centenary parade, the Gulf war reaches Kuwait, and "
           "Europe's budget talks fail — Thursday's world, in one page.")
    d.text((W // 2, y + 48), sub, font=SERIF_I(13), fill=RED, anchor="ma")
    d.line([(8, y + 66), (W - 8, y + 66)], fill=INK, width=2)
    y += 68
    # --- big-number strip
    cw = (W - 16 - 5 * 2) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        x = 8 + i * (cw + 2)
        d.rectangle([x, y, x + cw, y + 48], fill=NAVY)
        d.text((x + cw / 2, y + 12), num, font=SANS_B(20), fill=GOLD, anchor="mm")
        for j, ln in enumerate(wrap(d, lab, SANS_B(8), cw - 8)):
            d.text((x + cw / 2, y + 30 + j * 9), ln, font=SANS_B(8),
                   fill=(255, 255, 255), anchor="ma")
    y += 48
    # --- region bar
    rw = (W - 16 - 8 * 2) / 9
    for i, (name, n, col) in enumerate(REGIONS):
        x = 8 + i * (rw + 2)
        d.rectangle([x, y, x + rw, y + 22], fill=col)
        d.text((x + rw / 2, y + 11), f"{name} · {n}", font=SANS_B(9),
               fill=(255, 255, 255), anchor="mm")
    y += 22
    # --- UTC strip (header row + timeline row)
    d.text((8, y + 1), "THE DAY IN UTC", font=SANS_B(10), fill=NAVY, anchor="la")
    d.line([(8, y + 24), (W - 8, y + 24)], fill=CREAM_LINE, width=1)
    ew = (W - 16) / 6
    for i, (t, ev) in enumerate(UTC_EVENTS):
        cx = 8 + ew * i + ew / 2
        d.ellipse([cx - 3, y + 21, cx + 3, y + 27], fill=RED)
        d.text((cx, y + 14), t, font=SANS_B(8), fill=RED, anchor="ma")
        for j, ln in enumerate(wrap(d, ev, SANS(8), ew - 12)[:2]):
            d.text((cx, y + 30 + j * 9), ln, font=SANS(8), fill=INK, anchor="ma")
    y += 50
    # --- heroes
    hw = (W - 16 - 2 * 8) / 3
    hy = y
    for i, h in enumerate(HEROES):
        x = 8 + i * (hw + 8)
        d.rectangle([x, hy, x + hw, hy + 198], fill=(255, 255, 255),
                    outline=INK, width=1)
        h["art"](d, (x + 1, hy + 1, x + hw - 1, hy + 101))
        art_frame(d, (x + 1, hy + 1, x + hw - 1, hy + 101))
        num_badge(d, x + 14, hy + 15, h["num"])
        ty = hy + 105
        d.text((x + 6, ty), h["date"], font=SANS_B(8), fill=GREY, anchor="la")
        chip(d, x + hw - 66, ty - 1, h["chip"])
        ty += 13
        for ln in wrap(d, h["head"], SERIF_B(15), hw - 12)[:2]:
            d.text((x + 6, ty), ln, font=SERIF_B(15), fill=INK, anchor="la")
            ty += 17
        for ln in wrap(d, h["sub"], SANS(9), hw - 12)[:2]:
            d.text((x + 6, ty), ln, font=SANS(9), fill=(50, 50, 50), anchor="la")
            ty += 11
        ty += 1
        for ln in wrap(d, h["why"], SERIF_I(9), hw - 12)[:1]:
            d.text((x + 6, ty), ln, font=SERIF_I(9), fill=RED, anchor="la")
            ty += 11
        d.text((x + 6, hy + 198 - 9), h["src"], font=SANS(7), fill=GREY, anchor="la")
    y = hy + 198 + 4
    # --- scenes grid 5x2
    sw, sh = 196, 108
    for idx, s in enumerate(SCENES):
        r, c = divmod(idx, 5)
        x = 8 + c * (sw + 7)
        sy = y + r * (sh + 4)
        d.rectangle([x, sy, x + sw, sy + sh], fill=(255, 255, 255),
                    outline=INK, width=1)
        s["art"](d, (x + 1, sy + 1, x + sw - 1, sy + 63))
        art_frame(d, (x + 1, sy + 1, x + sw - 1, sy + 63))
        chip(d, x + 4, sy + 4, s["chip"])
        num_badge(d, x + sw - 13, sy + 14, s["num"], r=9)
        ty = sy + 67
        d.text((x + 4, ty), s["date"], font=SANS_B(7), fill=GREY, anchor="la")
        ty += 9
        for ln in wrap(d, s["head"], SERIF_B(10), sw - 8)[:1]:
            d.text((x + 4, ty), ln, font=SERIF_B(10), fill=INK, anchor="la")
            ty += 11
        for ln in wrap(d, s["sub"], SANS(8), sw - 8)[:2]:
            d.text((x + 4, ty), ln, font=SANS(8), fill=(50, 50, 50), anchor="la")
            ty += 10
    y = y + 2 * sh + 4 + 4
    # --- map
    d.text((8, y), "WHERE IT HAPPENED — pins = picture numbers, coloured by region",
           font=SANS_B(10), fill=NAVY, anchor="la")
    y += 14
    draw_map(d, (8, y, W - 8, y + 88))
    y += 88 + 4
    # --- ALSO list
    d.text((8, y), "ALSO ON 26 NOVEMBER — 24 MORE STORIES",
           font=SANS_B(12), fill=NAVY, anchor="la")
    d.text((W - 8, y), "17 pictured above + 24 below = 41 stories",
           font=SANS_I(9), fill=GREY, anchor="ra")
    y += 15
    colw = (W - 16 - 2 * 10) / 3
    for i, (n, code, text) in enumerate(ALSO):
        col, row = divmod(i, 8)
        x = 8 + col * (colw + 10)
        ry = y + row * 22
        d.text((x, ry), str(n), font=SANS_B(10), fill=RED, anchor="la")
        mw = minichip(d, x + 20, ry + 1, code)
        tx = x + 20 + mw + 4
        lines = wrap(d, text, SANS(10), colw - (tx - x) - 2)[:2]
        for j, ln in enumerate(lines):
            d.text((tx, ry + j * 11), ln, font=SANS(10), fill=INK, anchor="la")
    y += 8 * 22 + 2
    # --- date check
    d.rectangle([8, y, W - 8, y + 58], outline=RED, width=2)
    d.text((14, y + 5), "DATE CHECK — NOT 26 NOVEMBER NEWS (EXCLUDED):",
           font=SANS_B(10), fill=RED, anchor="la")
    for i, item in enumerate(DATECHECK):
        col, row = divmod(i, 5)
        x = 14 + col * ((W - 28) / 2)
        d.text((x, y + 19 + row * 7), "• " + item, font=SANS(8), fill=INK, anchor="la")
    y += 58 + 3
    # --- footer
    d.text((8, y), "HOW SURE:  OFFICIAL = authority's own word  ·  CONFIRMED = 2+ outlets  ·  REPORTED = 1 outlet  ·  CLAIM = one side's account, not verified  (ALSO list: OF/CF/RP/CL = same scale)",
           font=SANS(8), fill=GREY, anchor="la")
    y += 10
    d.text((8, y), "Every story happened or was first reported on Thursday 26 November 2026. Drawn scenes are illustrations, not photos.",
           font=SANS_I(8), fill=GREY, anchor="la")
    y += 10
    print("FINAL Y:", y, "H:", H)
    return img

if __name__ == "__main__":
    im = build()
    im.save("entry.png", optimize=True)
    print("saved entry.png")
