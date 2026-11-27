#!/usr/bin/env python3
"""frontpage26_v5.py — news-image-20261126 v5 (TOTAL REBUILD, fresh frame).

Title-first broadsheet, written 100% fresh from v5-spec.md.
Structure: top bar, masthead, stat boxes, 6-number strip, region bar, drawn
UTC timeline, 3 heroes, 10 one-idea scenes, continent map with big red pins,
2-column ALSO list, one-line DATE CHECK, sources footer.
Deterministic: no randomness, no timestamps. Output: entry.png 1024x1024.
One-idea-per-scene rule enforced: one background, one focal shape, at most
one secondary element per picture.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MX = 12  # side margin

NAVY = (14, 42, 71)
NAVY_D = (9, 28, 48)
CREAM = (250, 243, 227)
PAPER = (255, 253, 246)
GOLD = (201, 162, 39)
GOLD_L = (235, 200, 95)
RED = (178, 34, 34)
RED_D = (140, 20, 20)
INK = (22, 22, 22)
GREY = (96, 96, 96)
LINE = (205, 195, 175)
TAN = (222, 205, 170)
TAN_D = (185, 165, 125)
GREEN = (34, 139, 34)
AMBER = (200, 130, 20)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF = "LiberationSerif-Regular.ttf"
SERIF_B = "LiberationSerif-Bold.ttf"
SERIF_I = "LiberationSerif-Italic.ttf"
SANS = "LiberationSans-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS_I = "LiberationSans-Italic.ttf"


def F(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


REGIONS = {
    "NORTH AMERICA": (27, 98, 163),
    "EUROPE": (90, 60, 160),
    "MIDDLE EAST": (178, 34, 34),
    "NORTH AFRICA": (214, 130, 30),
    "SUB-SAHARAN AFRICA": (34, 139, 34),
    "EAST ASIA": (200, 40, 90),
    "SE ASIA & PACIFIC": (0, 150, 150),
    "SOUTH ASIA": (230, 120, 20),
    "LATIN AMERICA & CARIBBEAN": (120, 160, 30),
    "OCEANIA": (180, 60, 120),
    "SPORT & WORLD": (100, 100, 100),
}

CHIP_FILL = {"CONFIRMED": GREEN, "REPORTED": AMBER, "CLAIM": RED, "OFFICIAL": NAVY}


def wrap(d, text, fnt, max_w):
    """Greedy word wrap to max_w px; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        t = (cur + " " + word).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def chip(d, x, y, text, fnt, fill, fg=(255, 255, 255)):
    """Small rounded chip; returns width."""
    pad = 5
    w = int(d.textlength(text, font=fnt)) + 2 * pad
    h = fnt.size + 6
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill)
    d.text((x + pad, y + 2), text, font=fnt, fill=fg)
    return w


def num_badge(d, cx, cy, n, r=12):
    """Numbered circle badge centred at (cx, cy)."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(255, 255, 255), width=2)
    f = F(SANS_B, 13 if n < 10 else 11)
    t = str(n)
    tw = d.textlength(t, font=f)
    d.text((cx - tw / 2, cy - f.size / 2 - 1), t, font=f, fill=(255, 255, 255))


def fit_font(d, text, name, sizes, max_w):
    """Largest font size from `sizes` whose text fits max_w; returns (font, size)."""
    for s in sizes:
        f = F(name, s)
        if d.textlength(text, font=f) <= max_w:
            return f, s
    return F(name, sizes[-1]), sizes[-1]


# ---------------------------------------------------------------- top sections

def draw_top_bar(d, y):
    d.rectangle([0, y, W, y + 28], fill=NAVY)
    f_l = F(SANS_B, 13)
    d.text((MX, y + 7), "THE WORLD IN ONE DAY", font=f_l, fill=(255, 255, 255))
    f_r = F(SANS_B, 10)
    r = "THURSDAY 26 NOVEMBER 2026  ·  42 STORIES  ·  11 REGIONS  ·  14 FIELDS  ·  1 DAY"
    d.text((W - MX - d.textlength(r, font=f_r), y + 9), r, font=f_r, fill=GOLD_L)
    return y + 28


def draw_masthead(d, y):
    # 86px: title 44px serif bold, red date 18px, italic deck 12px
    f_t = F(SERIF_B, 44)
    t = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(t, font=f_t)) / 2, y + 2), t, font=f_t, fill=INK)
    f_d = F(SANS_B, 18)
    dt = "THURSDAY 26 NOVEMBER 2026"
    d.text(((W - d.textlength(dt, font=f_d)) / 2, y + 50), dt, font=f_d, fill=RED)
    f_k = F(SERIF_I, 12)
    deck = ("A storm stops a centenary parade, the Gulf war reaches Kuwait, and India "
            "marks eighteen years since 26/11 — Thursday's world, in one page.")
    d.text(((W - d.textlength(deck, font=f_k)) / 2, y + 71), deck, font=f_k, fill=GREY)
    return y + 86


def draw_stat_boxes(d, y):
    # 3 boxes, 32px tall
    stats = [("42", "STORIES"), ("11", "REGIONS"), ("14", "FIELDS · ~22 SOURCES")]
    bw = (W - 2 * MX - 2 * 8) // 3
    for i, (num, lab) in enumerate(stats):
        x = MX + i * (bw + 8)
        d.rectangle([x, y, x + bw, y + 32], outline=NAVY, width=2, fill=CREAM)
        f_n = F(SANS_B, 17)
        f_l = F(SANS, 10)
        txt = num + "  " + lab
        tw = d.textlength(txt, font=f_n)
        d.text((x + (bw - tw) / 2, y + 7), num, font=f_n, fill=NAVY)
        # label drawn after the number: measure number width
        nw = d.textlength(num + "  ", font=f_n)
        d.text((x + (bw - tw) / 2 + nw, y + 9), lab, font=f_l, fill=INK)
    return y + 32


def draw_number_strip(d, y):
    # navy band, 54px, 6 cells: gold numeral + white label
    cells = [
        ("750,000+", "WITHOUT POWER\nIN US STORM"),
        ("2", "ITALIANS KILLED\nIN KUWAIT"),
        ("€45bn", "UKRAINE LOAN\nBLOCKED"),
        ("12,021", "EBOLA CASES\nIN DRC"),
        ("77,000", "UK NET\nMIGRATION"),
        ("3.25%", "BANK OF KOREA\nRATE"),
    ]
    d.rectangle([0, y, W, y + 54], fill=NAVY)
    cw = (W - 2 * MX) // 6
    f_n = F(SANS_B, 24)
    f_l = F(SANS, 8)
    for i, (num, lab) in enumerate(cells):
        x = MX + i * cw
        if i:
            d.line([x, y + 8, x, y + 46], fill=GOLD, width=1)
        tw = d.textlength(num, font=f_n)
        d.text((x + (cw - tw) / 2, y + 3), num, font=f_n, fill=GOLD_L)
        for j, ln in enumerate(lab.split("\n")):
            lw = d.textlength(ln, font=f_l)
            d.text((x + (cw - lw) / 2, y + 31 + j * 10), ln, font=f_l, fill=(255, 255, 255))
    return y + 54


def draw_region_bar(d, y):
    # one centred line: coloured dot + "NAME count", 20px
    counts = [
        ("NORTH AMERICA", 5), ("EUROPE", 9), ("MIDDLE EAST", 5),
        ("NORTH AFRICA", 2), ("SUB-SAHARAN AFRICA", 5), ("EAST ASIA", 3),
        ("SE ASIA & PACIFIC", 3), ("SOUTH ASIA", 2),
        ("LATIN AMERICA & CARIBBEAN", 2), ("OCEANIA", 1), ("SPORT & WORLD", 5),
    ]
    f = None
    total = 0
    for size in (9, 8):
        f = F(SANS_B, size)
        total = 0
        for name, n in counts:
            seg = name + " " + str(n)
            total += 12 + d.textlength(seg, font=f) + 10
        total -= 10
        if total <= W - 2 * MX:
            break
    x = (W - total) // 2
    for name, n in counts:
        seg = name + " " + str(n)
        d.ellipse([x, y + 6, x + 8, y + 14], fill=REGIONS[name])
        x += 12
        d.text((x, y + 4), seg, font=f, fill=INK)
        x += d.textlength(seg, font=f) + 10
    return y + 20


def draw_timeline(d, y):
    # drawn rule, 6 dots, red bold time above, short label below; 52px
    stops = [
        ("00:41", "Flinders fire: six homes lost"),
        ("01:00", "Bank of Korea lifts rate to 3.25%"),
        ("07:45", "Bangkok refinery blast: 7–9 hurt"),
        ("09:30", "ONS: UK net migration falls to 77,000"),
        ("13:30", "Macy's parade due to step off — postponed"),
        ("EVENING", "EU summit ends: no deal"),
    ]
    f_t = F(SANS_B, 11)
    f_l = F(SANS, 8)
    x0, x1 = 60, W - 60
    d.line([x0, y + 24, x1, y + 24], fill=NAVY, width=2)
    for i, (tm, lab) in enumerate(stops):
        cx = x0 + i * (x1 - x0) // 5
        tw = d.textlength(tm, font=f_t)
        d.text((cx - tw / 2, y + 4), tm, font=f_t, fill=RED)
        d.ellipse([cx - 5, y + 19, cx + 5, y + 29], fill=NAVY, outline=(255, 255, 255), width=2)
        lines = wrap(d, lab, f_l, 150)
        for j, ln in enumerate(lines[:2]):
            lw = d.textlength(ln, font=f_l)
            lx = cx - lw / 2
            lx = max(MX, min(lx, W - MX - lw))
            d.text((lx, y + 32 + j * 10), ln, font=f_l, fill=INK)
    return y + 52


# ---------------------------------------------------------------- hero pictures

def pic_macys(d, x, y, w, h):
    """H1: night skyline, ONE red balloon with a face, rain, POSTPONED banner."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 22, 44))
    # skyline: dark buildings with lit windows (fixed pattern, no randomness)
    bldgs = [(0, 62, 34, 42), (38, 48, 30, 56), (72, 66, 26, 38),
             (102, 54, 32, 50), (138, 70, 28, 34), (170, 58, 30, 46),
             (204, 66, 26, 38), (234, 50, 32, 54), (270, 64, 28, 40),
             (302, 56, 26, 48)]
    for bx, by, bw, bh in bldgs:
        d.rectangle([x + bx, y + by, x + bx + bw, y + h], fill=(24, 36, 62))
        for wy in range(y + by + 6, y + h - 6, 12):
            for wx in range(bx + 5, bx + bw - 4, 10):
                if (wx * 7 + wy * 13) % 3 == 0:
                    d.rectangle([x + wx, wy, x + wx + 4, wy + 5], fill=GOLD_L)
    # rain slashes
    for rx in range(14, w, 26):
        d.line([x + rx, y + 4, x + rx - 8, y + 22], fill=(120, 150, 200), width=1)
        d.line([x + rx + 10, y + 30, x + rx + 2, y + 48], fill=(120, 150, 200), width=1)
    # balloon: big red circle with a face
    cx, cy, r = x + w // 2, y + 46, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 40, 40), outline=(150, 20, 20), width=2)
    d.ellipse([cx - 22, cy - 14, cx - 10, cy - 2], fill=(255, 255, 255))
    d.ellipse([cx + 10, cy - 14, cx + 22, cy - 2], fill=(255, 255, 255))
    d.ellipse([cx - 18, cy - 11, cx - 14, cy - 7], fill=INK)
    d.ellipse([cx + 14, cy - 11, cx + 18, cy - 7], fill=INK)
    d.arc([cx - 16, cy + 2, cx + 16, cy + 22], start=20, end=160, fill=(255, 255, 255), width=3)
    # gold "100" badge on the balloon
    d.ellipse([cx + 18, cy + 18, cx + 46, cy + 46], fill=GOLD, outline=(255, 255, 255), width=2)
    f_b = F(SANS_B, 11)
    d.text((cx + 24, cy + 27), "100", font=f_b, fill=NAVY)
    # white banner across the bottom of the picture
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(255, 255, 255))
    f_bn = F(SANS_B, 11)
    bn = "POSTPONED TO SATURDAY"
    d.text((x + (w - d.textlength(bn, font=f_bn)) / 2, y + h - 16), bn, font=f_bn, fill=NAVY)


def pic_kuwait(d, x, y, w, h):
    """H2: desert at dusk, ONE drone + ONE missile trail, ONE refinery flare."""
    d.rectangle([x, y, x + w, y + h - 30], fill=(74, 52, 44))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(196, 164, 120))
    # sun low on the horizon
    d.ellipse([x + w - 70, y + 18, x + w - 34, y + 54], fill=(232, 150, 60))
    # refinery flare on the horizon (one small structure + flame)
    d.rectangle([x + 34, y + h - 52, x + 44, y + h - 30], fill=(40, 30, 26))
    d.rectangle([x + 48, y + h - 44, x + 58, y + h - 30], fill=(40, 30, 26))
    d.polygon([(x + 30, y + h - 52), (x + 38, y + h - 74), (x + 46, y + h - 52)],
              fill=(240, 120, 20))
    d.polygon([(x + 34, y + h - 52), (x + 38, y + h - 64), (x + 42, y + h - 52)],
              fill=(255, 210, 80))
    # drone silhouette with ONE missile trail
    dx, dy = x + w - 120, y + 26
    d.ellipse([dx - 22, dy - 6, dx + 22, dy + 6], fill=(20, 18, 16))
    d.line([dx - 34, dy - 10, dx - 10, dy - 10], fill=(20, 18, 16), width=2)
    d.line([dx + 10, dy - 10, dx + 34, dy - 10], fill=(20, 18, 16), width=2)
    d.line([dx - 22, dy + 4, dx - 70, dy + 44], fill=(255, 255, 255), width=3)
    d.ellipse([dx - 74, dy + 40, dx - 66, dy + 48], fill=(255, 220, 120))
    # red badge (top-right: the number badge occupies top-left)
    f_b = F(SANS_B, 10)
    badge = "2 ITALIANS KILLED"
    bw = int(d.textlength(badge, font=f_b)) + 12
    d.rounded_rectangle([x + w - bw - 8, y + 8, x + w - 8, y + 26], radius=9, fill=RED)
    d.text((x + w - bw - 2, y + 11), badge, font=f_b, fill=(255, 255, 255))


def pic_mumbai(d, x, y, w, h):
    """H3: India Gate silhouette, row of candles, ONE tricolor flag."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 26, 48))
    # stars
    for sx, sy in [(30, 14), (70, 8), (250, 12), (290, 20), (120, 22), (210, 8)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # India Gate: pale stone, arch opening cut dark
    gx0, gx1 = x + 108, x + 220
    d.rectangle([gx0, y + 22, gx1, y + h - 14], fill=(224, 208, 172))
    d.rectangle([gx0 + 8, y + 14, gx1 - 8, y + 24], fill=(224, 208, 172))
    d.pieslice([gx0 + 38, y + 34, gx1 - 38, y + 78], start=180, end=360, fill=(18, 26, 48))
    d.rectangle([gx0 + 44, y + 56, gx1 - 44, y + h - 14], fill=(18, 26, 48))
    d.rectangle([gx0, y + 14, gx1, y + 18], fill=(200, 180, 140))
    # candles: row of 6 flames at the base
    for i in range(6):
        cx = x + 118 + i * 18
        cy = y + h - 12
        d.rectangle([cx - 2, cy, cx + 2, cy + 8], fill=(240, 230, 200))
        d.ellipse([cx - 3, cy - 8, cx + 3, cy], fill=(255, 200, 60))
    # tricolor flag on a pole, right of the gate
    fx = x + 250
    d.line([fx, y + 30, fx, y + h - 14], fill=(220, 220, 220), width=2)
    d.rectangle([fx, y + 30, fx + 34, y + 38], fill=(255, 153, 51))
    d.rectangle([fx, y + 38, fx + 34, y + 46], fill=(255, 255, 255))
    d.rectangle([fx, y + 46, fx + 34, y + 54], fill=(19, 136, 8))
    # badge (top-right: the number badge occupies top-left)
    f_b = F(SANS_B, 10)
    badge = "18 YEARS"
    bw = int(d.textlength(badge, font=f_b)) + 12
    d.rounded_rectangle([x + w - bw - 8, y + 8, x + w - 8, y + 26], radius=9, fill=RED)
    d.text((x + w - bw - 2, y + 11), badge, font=f_b, fill=(255, 255, 255))


def draw_hero(d, x, y, w, h, num, pic_fn, headline, sub, why, dateline, chip_text, region):
    pic_h = 104
    pic_fn(d, x, y, w, pic_h)
    num_badge(d, x + 16, y + 16, num, r=12)
    # region tick: small coloured bar under the picture
    d.rectangle([x, y + pic_h, x + w, y + pic_h + 3], fill=REGIONS[region])
    f_h = F(SANS_B, 15)
    hy = y + pic_h + 8
    d.text((x, hy), headline, font=f_h, fill=INK)
    f_s = F(SANS, 11)
    lines = wrap(d, sub, f_s, w)[:2]
    sy = hy + 19
    for j, ln in enumerate(lines):
        d.text((x, sy + j * 13), ln, font=f_s, fill=(50, 50, 50))
    f_w = F(SANS_I, 10)
    wy = sy + 13 * len(lines) + 3
    d.text((x, wy), "WHY IT MATTERS: " + why, font=f_w, fill=GREY)
    f_c = F(SANS_B, 9)
    chip(d, x, y + h - 15, chip_text, f_c, CHIP_FILL[chip_text])
    f_dl = F(SANS_B, 9)
    dl = dateline
    d.text((x + w - d.textlength(dl, font=f_dl), y + h - 13), dl, font=f_dl, fill=GREY)


HEROES = [
    (1, pic_macys, "MACY'S 100TH PARADE POSTPONED",
     "Thanksgiving nor'easter grounds the centenary parade — a first in 100 years. 750,000+ without power.",
     "Thanksgiving Day itself had no parade, ever.",
     "NEW YORK", "CONFIRMED", "NORTH AMERICA"),
    (2, pic_kuwait, "THE GULF WAR WIDENS",
     "Iranian drones kill 2 Italians in Kuwait; Houthis hit Jazan refinery; Brent $96.57.",
     "The war reached Kuwait — and oil spiked.",
     "KUWAIT", "CONFIRMED", "MIDDLE EAST"),
    (3, pic_mumbai, "MUMBAI MARKS 26/11",
     "18 years on, 166 killed, tributes at the Taj.",
     "The anniversary falls exactly on 26 November.",
     "MUMBAI", "CONFIRMED", "SOUTH ASIA"),
]


def draw_heroes(d, y):
    hw = (W - 2 * MX - 2 * 8) // 3
    for i, (num, fn, hl, sub, why, dl, ch, rg) in enumerate(HEROES):
        x = MX + i * (hw + 8)
        draw_hero(d, x, y, hw, 188, num, fn, hl, sub, why, dl, ch, rg)
    return y + 188


# ---------------------------------------------------------------- small scenes

def pic_kyiv(d, x, y, w, h):
    """4: night sky, TWO missile trails (the only scene allowed two of anything)."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 20, 40))
    d.line([x + 20, y + 40, x + 90, y + 6], fill=(255, 255, 255), width=3)
    d.line([x + 70, y + 44, x + 150, y + 8], fill=(255, 255, 255), width=3)
    d.ellipse([x + 86, y + 2, x + 94, y + 10], fill=(255, 220, 120))
    d.ellipse([x + 146, y + 4, x + 154, y + 12], fill=(255, 220, 120))
    for bx, bw, bh in [(0, 34, 16), (38, 26, 22), (68, 30, 14), (102, 24, 20),
                       (130, 30, 16), (164, 26, 18)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(24, 34, 58))
        for wy in range(y + h - bh + 4, y + h - 3, 7):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if (wx + wy) % 3 == 0:
                    d.rectangle([x + wx, wy, x + wx + 3, wy + 3], fill=GOLD_L)


def pic_ebola(d, x, y, w, h):
    """5: ONE white tent with red cross, ONE PPE worker at the door."""
    d.rectangle([x, y, x + w, y + h], fill=(236, 226, 198))
    # tent: triangle roof + body, left-of-centre (badge lives top-right)
    tx = x + 18
    d.polygon([(tx, y + 20), (tx + 62, y + 20), (tx + 31, y + 2)], fill=(255, 255, 255),
              outline=(180, 175, 160))
    d.rectangle([tx, y + 20, tx + 62, y + h - 4], fill=(255, 255, 255),
                outline=(180, 175, 160))
    d.rectangle([tx + 26, y + 30, tx + 36, y + 42], fill=RED)
    d.rectangle([tx + 29, y + 33, tx + 33, y + 39], fill=(255, 255, 255))
    # door + PPE worker
    d.rectangle([tx + 44, y + 30, tx + 58, y + h - 4], fill=(120, 120, 120))
    wx = tx + 74
    d.ellipse([wx - 5, y + 16, wx + 5, y + 26], fill=(250, 250, 250), outline=(150, 150, 150))
    d.rectangle([wx - 6, y + 27, wx + 6, y + h - 4], fill=(250, 250, 250),
                outline=(150, 150, 150))
    d.rectangle([wx - 6, y + 30, wx + 6, y + 34], fill=(0, 150, 150))


def pic_gaza(d, x, y, w, h):
    """6: dusk skyline, ONE smoke column, ONE dark building silhouette."""
    d.rectangle([x, y, x + w, y + h], fill=(120, 70, 50))
    d.ellipse([x + 30, y + 6, x + 44, y + 20], fill=(240, 180, 90))
    # smoke column
    for i, (sx, sy, sr) in enumerate([(120, 8, 9), (122, 18, 11), (118, 28, 12), (121, 38, 10)]):
        d.ellipse([x + sx - sr, y + sy, x + sx + sr, y + sy + 2 * sr], fill=(110, 105, 100))
    # building silhouette
    d.rectangle([x + 100, y + 18, x + 150, y + h], fill=(40, 32, 28))
    d.rectangle([x + 152, y + 30, x + 180, y + h], fill=(52, 42, 36))
    d.rectangle([x + 20, y + 32, x + 70, y + h], fill=(48, 38, 32))


def pic_hongkong(d, x, y, w, h):
    """7: dark street, row of 7 candle flames."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 28, 42))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(18, 18, 26))
    for i in range(7):
        cx = x + 24 + i * 24
        cy = y + h - 12
        d.rectangle([cx - 2, cy, cx + 2, cy + 8], fill=(240, 230, 200))
        d.ellipse([cx - 4, cy - 10, cx + 4, cy], fill=(255, 200, 60))
        d.ellipse([cx - 2, cy - 7, cx + 2, cy - 2], fill=(255, 240, 160))
    f_b = F(SANS_B, 10)
    badge = "168"
    bw = int(d.textlength(badge, font=f_b)) + 12
    d.rounded_rectangle([x + w - bw - 6, y + 6, x + w - 6, y + 24], radius=9, fill=RED)
    d.text((x + w - bw, y + 9), badge, font=f_b, fill=(255, 255, 255))


def pic_bangkok(d, x, y, w, h):
    """8: ONE refinery silhouette, ONE flame tongue, ONE smoke column."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 44, 40))
    d.rectangle([x + 20, y + 22, x + 90, y + h], fill=(30, 26, 24))
    d.rectangle([x + 96, y + 30, x + 150, y + h], fill=(36, 30, 28))
    d.rectangle([x + 156, y + 18, x + 164, y + h], fill=(30, 26, 24))
    # one flame tongue
    d.polygon([(x + 118, y + 30), (x + 126, y + 8), (x + 134, y + 30)], fill=(240, 120, 20))
    d.polygon([(x + 121, y + 30), (x + 126, y + 18), (x + 131, y + 30)], fill=(255, 210, 80))
    # one smoke column
    for i, (sx, sy, sr) in enumerate([(160, 2, 7), (162, 10, 8), (158, 18, 7)]):
        d.ellipse([x + sx - sr, y + sy, x + sx + sr, y + sy + 2 * sr], fill=(120, 115, 108))


def pic_cairo(d, x, y, w, h):
    """9: ONE tanker silhouette with a small flame, mourning candles below."""
    d.rectangle([x, y, x + w, y + h], fill=(70, 60, 52))
    # tanker: rounded body + cab
    d.rounded_rectangle([x + 30, y + 14, x + 150, y + 30], radius=8, fill=(40, 36, 32))
    d.rectangle([x + 150, y + 18, x + 168, y + 30], fill=(40, 36, 32))
    d.ellipse([x + 46, y + 30, x + 58, y + 42], fill=(20, 18, 16))
    d.ellipse([x + 128, y + 30, x + 140, y + 42], fill=(20, 18, 16))
    # small flame on the tanker
    d.polygon([(x + 84, y + 14), (x + 90, y + 2), (x + 96, y + 14)], fill=(240, 120, 20))
    # mourning candles below
    for i in range(3):
        cx = x + 66 + i * 26
        cy = y + h - 6
        d.rectangle([cx - 2, cy, cx + 2, cy + 5], fill=(240, 230, 200))
        d.ellipse([cx - 3, cy - 7, cx + 3, cy], fill=(255, 200, 60))


def pic_flinders(d, x, y, w, h):
    """10: TALL flame tongues over a LOW dark hill line, ONE smoke column."""
    d.rectangle([x, y, x + w, y + h], fill=(140, 90, 50))
    # low dark hill
    d.polygon([(x, y + h), (x, y + h - 12), (x + 60, y + h - 20),
               (x + 130, y + h - 10), (x + w, y + h - 16), (x + w, y + h)],
              fill=(40, 30, 22))
    # tall flames
    for fx, fh, fw in [(36, 34, 14), (70, 42, 16), (108, 36, 14), (142, 30, 12)]:
        d.polygon([(x + fx, y + h - 10), (x + fx + fw // 2, y + h - 10 - fh),
                   (x + fx + fw, y + h - 10)], fill=(240, 110, 15))
        d.polygon([(x + fx + 3, y + h - 10), (x + fx + fw // 2, y + h - 10 - fh + 14),
                   (x + fx + fw - 3, y + h - 10)], fill=(255, 210, 80))
    # one smoke column
    for i, (sx, sy, sr) in enumerate([(168, 0, 7), (170, 8, 8), (166, 16, 7)]):
        d.ellipse([x + sx - sr, y + sy, x + sx + sr, y + sy + 2 * sr], fill=(120, 112, 104))


def pic_gukesh(d, x, y, w, h):
    """11: chess board from above, 4 pieces ONLY, two clock faces."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 205, 170))
    bs = 44
    bx, by = x + 12, y + 2
    for r in range(8):
        for c in range(8):
            col = (240, 225, 195) if (r + c) % 2 == 0 else (120, 90, 60)
            s = bs // 8
            d.rectangle([bx + c * s, by + r * s, bx + (c + 1) * s, by + (r + 1) * s], fill=col)
    # 4 pieces only
    for px, py, col in [(bx + 8, by + 8, (255, 255, 255)), (bx + 30, by + 20, (30, 30, 30)),
                        (bx + 14, by + 32, (255, 255, 255)), (bx + 34, by + 8, (30, 30, 30))]:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=col, outline=(150, 130, 100))
    # two clock faces reading 1:32
    for cx in (x + 96, x + 138):
        d.ellipse([cx - 18, y + 6, cx + 18, y + 42], fill=(255, 255, 255),
                  outline=(60, 60, 60), width=2)
        d.line([cx, y + 24, cx + 8, y + 14], fill=INK, width=2)   # hour ~1:30
        d.line([cx, y + 24, cx - 2, y + 40], fill=INK, width=2)   # minute ~32
        d.ellipse([cx - 2, y + 22, cx + 2, y + 26], fill=INK)
    f_c = F(SANS_B, 8)
    d.text((x + 96 - 10, y + 44), "1:32", font=f_c, fill=INK)
    d.text((x + 138 - 10, y + 44), "1:32", font=f_c, fill=INK)


def pic_ecb(d, x, y, w, h):
    """12: EU star-circle emblem + DE COS name plate."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 244))
    cx, cy, r = x + w // 2, y + 20, 16
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 51, 153))
    import math
    for i in range(12):
        a = math.pi * 2 * i / 12 - math.pi / 2
        sx = cx + int(11 * math.cos(a))
        sy = cy + int(11 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    # name plate
    f_p = F(SANS_B, 10)
    plate = "DE COS"
    pw = int(d.textlength(plate, font=f_p)) + 16
    d.rounded_rectangle([cx - pw // 2, y + h - 14, cx + pw // 2, y + h - 2],
                        radius=4, fill=NAVY)
    d.text((cx - pw // 2 + 8, y + h - 12), plate, font=f_p, fill=(255, 255, 255))


def pic_eu(d, x, y, w, h):
    """13: oval table from above (NO delegates), EU star circle, NO DEAL banner."""
    d.rectangle([x, y, x + w, y + h], fill=(228, 222, 205))
    # oval table
    d.ellipse([x + 14, y + 6, x + w - 14, y + h - 6], fill=(150, 105, 60),
              outline=(100, 70, 35), width=2)
    d.ellipse([x + 26, y + 12, x + w - 26, y + h - 12], fill=(176, 128, 76))
    # EU star circle in the centre
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(0, 51, 153))
    import math
    for i in range(12):
        a = math.pi * 2 * i / 12 - math.pi / 2
        sx = cx + int(7 * math.cos(a))
        sy = cy + int(7 * math.sin(a))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 204, 0))
    # NO DEAL banner across
    f_b = F(SANS_B, 10)
    bn = "NO DEAL"
    bw = int(d.textlength(bn, font=f_b)) + 12
    d.rounded_rectangle([cx - bw // 2, cy - 22, cx + bw // 2, cy - 8], radius=6, fill=RED)
    d.text((cx - bw // 2 + 6, cy - 20), bn, font=f_b, fill=(255, 255, 255))
    # €45bn label
    f_l = F(SANS_B, 9)
    lb = "€45bn"
    d.text((cx - d.textlength(lb, font=f_l) / 2, cy + 12), lb, font=f_l, fill=NAVY)


SCENES = [
    (4, pic_kyiv, "MISSILES HIT KYIV",
     "Ballistic missiles wound 7 overnight.", "CONFIRMED", "EUROPE"),
    (5, pic_ebola, "EBOLA PASSES 12,000 CASES",
     None, "CONFIRMED", "SUB-SAHARAN AFRICA"),
    (6, pic_gaza, "GAZA STRIKES KILL 9–10",
     None, "CONFIRMED", "MIDDLE EAST"),
    (7, pic_hongkong, "HONG KONG: ONE YEAR ON",
     "Wang Fuk fire, 168 dead remembered, flowers at Tai Po.", "CONFIRMED", "EAST ASIA"),
    (8, pic_bangkok, "BANGKOK REFINERY BLAST INJURES 7–9",
     None, "CONFIRMED", "SE ASIA & PACIFIC"),
    (9, pic_cairo, "CAIRO MOURNS 31 KILLED",
     None, "CONFIRMED", "NORTH AFRICA"),
    (10, pic_flinders, "FLINDERS FIRE: 14,000 HA",
     None, "CONFIRMED", "OCEANIA"),
    (11, pic_gukesh, "GUKESH–SINDAROV DRAW",
     "Game 3 drawn, match level 1.5–1.5.", "CONFIRMED", "SPORT & WORLD"),
    (12, pic_ecb, "ECB PICKS HERNÁNDEZ DE COS",
     None, "CONFIRMED", "EUROPE"),
    (13, pic_eu, "EU SUMMIT FAILS ON BUDGET",
     "No deal on the 2028–34 budget or the Ukraine loan — deferred to 17–18 Dec.",
     "CONFIRMED", "EUROPE"),
]


def draw_scene(d, x, y, w, h, num, pic_fn, headline, sub, chip_text, region):
    pic_h = 48
    pic_fn(d, x, y, w, pic_h)
    num_badge(d, x + 13, y + 13, num, r=10)
    # Ebola badge: "12,021" top-right of the cell, outside the tent
    if num == 5:
        f_b = F(SANS_B, 10)
        badge = "12,021"
        bw = int(d.textlength(badge, font=f_b)) + 10
        d.rounded_rectangle([x + w - bw - 4, y + 4, x + w - 4, y + 20], radius=7, fill=RED)
        d.text((x + w - bw + 1, y + 7), badge, font=f_b, fill=(255, 255, 255))
    # Flinders plaque: "14,000 HA" below the picture
    ty = y + pic_h + 3
    if num == 10:
        f_p = F(SANS_B, 10)
        plaque = "14,000 HA"
        pw = int(d.textlength(plaque, font=f_p)) + 12
        d.rounded_rectangle([x + (w - pw) // 2, ty, x + (w - pw) // 2 + pw, ty + 14],
                            radius=4, fill=RED)
        d.text((x + (w - pw) // 2 + 6, ty + 2), plaque, font=f_p, fill=(255, 255, 255))
        ty += 17
    f_h = F(SANS_B, 13)
    if d.textlength(headline, font=f_h) > w:
        f_h = F(SANS_B, 12)
        if d.textlength(headline, font=f_h) > w:
            f_h = F(SANS_B, 11)
    lh = f_h.size + 2
    hlines = wrap(d, headline, f_h, w)[:2]
    for j, ln in enumerate(hlines):
        d.text((x, ty + j * lh), ln, font=f_h, fill=INK)
    ty += lh * len(hlines) + 2
    if sub:
        f_s = F(SANS, 10)
        slines = wrap(d, sub, f_s, w)[:2]
        for j, ln in enumerate(slines):
            d.text((x, ty + j * 12), ln, font=f_s, fill=(50, 50, 50))
    f_c = F(SANS_B, 9)
    chip(d, x, y + h - 14, chip_text, f_c, CHIP_FILL[chip_text])


def draw_scenes(d, y):
    cw = (W - 2 * MX - 4 * 8) // 5
    ch = 110
    for i, (num, fn, hl, sub, chp, rg) in enumerate(SCENES):
        row, col = divmod(i, 5)
        x = MX + col * (cw + 8)
        yy = y + row * (ch + 8)
        draw_scene(d, x, yy, cw, ch, num, fn, hl, sub, chp, rg)
    return y + 2 * ch + 8


# ---------------------------------------------------------------- map

CONTINENTS = [
    # North America
    [(40, 18), (90, 6), (150, 4), (210, 10), (250, 20), (245, 32), (220, 38),
     (200, 48), (180, 58), (165, 50), (150, 44), (130, 40), (100, 34), (60, 28),
     (40, 24)],
    # Greenland
    [(268, 2), (292, 2), (296, 10), (276, 12)],
    # South America
    [(235, 52), (270, 46), (295, 54), (290, 70), (270, 80), (250, 72), (238, 62)],
    # Europe
    [(448, 14), (500, 8), (530, 12), (525, 22), (500, 26), (472, 24), (452, 20)],
    # Africa
    [(460, 32), (505, 28), (545, 32), (560, 42), (550, 56), (525, 66),
     (495, 64), (475, 52), (460, 42)],
    # Asia (mainland)
    [(530, 12), (600, 4), (680, 4), (760, 6), (840, 10), (880, 16), (860, 28),
     (800, 36), (740, 40), (680, 38), (620, 34), (570, 28), (545, 20)],
    # India peninsula
    [(638, 38), (662, 50), (650, 58), (632, 44)],
    # SE Asia
    [(720, 40), (750, 42), (745, 52), (725, 50)],
    # Indonesia islands
    [(768, 56), (798, 58), (828, 56)],
    # Australia
    [(820, 56), (870, 52), (895, 58), (885, 70), (845, 72), (822, 64)],
    # UK
    [(446, 10), (454, 8), (456, 14), (448, 16)],
    # Japan
    [(878, 22), (886, 20), (888, 28), (880, 30)],
]

PINS = [
    (1, 205, 24), (2, 600, 30), (3, 648, 44), (4, 532, 20), (5, 505, 50),
    (6, 575, 32), (7, 790, 34), (8, 748, 38), (9, 540, 36), (10, 872, 66),
    (11, 478, 28), (12, 504, 14), (13, 452, 20),
]


def draw_map(d, y):
    # 100px band: title + continent map with BIG red pins
    f_t = F(SANS_B, 11)
    d.text((MX, y + 2), "WHERE IT HAPPENED — pins = picture numbers",
           font=f_t, fill=NAVY)
    my = y + 18
    for poly in CONTINENTS:
        pts = [(MX + px, my + py) for px, py in poly]
        d.polygon(pts, fill=TAN, outline=TAN_D)
    for n, px, py in PINS:
        num_badge(d, MX + px, my + py, n, r=11)
    return y + 100


# ---------------------------------------------------------------- ALSO list

ALSO_COL1 = [
    (14, "NFL — Bears 39–35 Lions, Eagles 39–38 Cowboys, Bills 13–10.", "NORTH AMERICA"),
    (15, "HORMUZ — IRGC claims two oil tankers hit sea mines near Oman's Khasab. [CLAIM]", "MIDDLE EAST"),
    (16, "IRBIL — Thousands protest as Baghdad seizes Kurdish oil and borders.", "MIDDLE EAST"),
    (17, "BISSAU — Junta postpones elections to Nov 2028, a year after the coup.", "SUB-SAHARAN AFRICA"),
    (18, "ITURI — UN peacekeepers step up protection as fighting continues.", "SUB-SAHARAN AFRICA"),
    (19, "SENEGAL — Record November crossings as young risk the Atlantic.", "SUB-SAHARAN AFRICA"),
    (20, "BOGOR — Mine toll rises to 13.", "SE ASIA & PACIFIC"),
    (21, "PYONGYANG — Kim calls tactical-nuke deployment “complete”. [CLAIM]", "EAST ASIA"),
    (22, "SEOUL — Bank of Korea lifts rate to 3.25%; growth seen at 4.1%.", "EAST ASIA"),
    (23, "LONDON — Net migration falls to 77,000, lowest since 1997.", "EUROPE"),
    (24, "PARIS — Depardieu, 77, ordered to stand trial for alleged 2018 rape.", "EUROPE"),
    (25, "CANARY ISLANDS — Pass 16,000 in Nov; busiest month on the Atlantic route.", "EUROPE"),
    (26, "MEXICO CITY — Sheinbaum blames DEA tip lines as interference.", "LATIN AMERICA & CARIBBEAN"),
    (27, "HAITI — WHO pledges $1m for last major public hospital.", "LATIN AMERICA & CARIBBEAN"),
]

ALSO_COL2 = [
    (28, "TARIFFS — China, EU reject new 14-economy US tariff plan.", "NORTH AMERICA"),
    (29, "COLOGNE — Two arrested over alleged synagogue bomb plot.", "EUROPE"),
    (30, "BRENT — $96.57.", "SPORT & WORLD"),
    (31, "SHIPPING — UNCTAD: maritime trade to stall at zero growth in 2026.", "SPORT & WORLD"),
    (32, "EUROPA LEAGUE — Bournemouth stay perfect (5 from 5).", "SPORT & WORLD"),
    (33, "UK–EU — Treaty texts published with 10-year exit clause.", "EUROPE"),
    (34, "STOCKHOLM — Centre backs Kristersson for PM; parliament votes Monday.", "EUROPE"),
    (35, "DHAKA — Fresh garment-wage protests met with tear gas.", "SOUTH ASIA"),
    (36, "WASHINGTON — Trump calls revised GDP data “fake”, demands probe. [HIS CLAIM]", "NORTH AMERICA"),
    (37, "TENNIS — Sinner to miss Australian Open after knee surgery.", "SPORT & WORLD"),
    (38, "KENYA — Court halts US-backed Ebola quarantine site; 50-bed base frozen.", "SUB-SAHARAN AFRICA"),
    (39, "BENGHAZI — Meloni rebukes Kyiv at EU summit; Libya vows retaliation.", "NORTH AFRICA"),
    (40, "NVIDIA — Halts AI server shipments to 4 SE Asian nations.", "SE ASIA & PACIFIC"),
]


def draw_also(d, y):
    # heading + 27 lines in 2 columns; 172px
    f_h = F(SANS_B, 12)
    d.text((MX, y), "ALSO ON 26 NOVEMBER — 27 MORE STORIES", font=f_h, fill=NAVY)
    f_l = F(SANS, 9)
    f_n = F(SANS_B, 9)
    row_h = 10.6
    col_w = (W - 2 * MX - 16) // 2
    for ci, col in enumerate((ALSO_COL1, ALSO_COL2)):
        x = MX + ci * (col_w + 16)
        for i, (n, text, rg) in enumerate(col):
            ly = y + 18 + i * row_h
            d.ellipse([x, ly + 2, x + 7, ly + 9], fill=REGIONS[rg])
            num = str(n) + " "
            d.text((x + 11, ly), num, font=f_n, fill=INK)
            nx = x + 11 + d.textlength(num, font=f_n)
            d.text((nx, ly), text, font=f_l, fill=(40, 40, 40))
    return y + 172


# ---------------------------------------------------------------- DATE CHECK + footer

def draw_datecheck(d, y):
    f_lab = F(SANS_B, 9)
    lab = "DATE CHECK — NOT 26 NOV NEWS: "
    text = ("Eurostar walkout 25/11 · Venezuela debt 24/11 · FCC Starlink 25/11 · "
            "Malaysia Google suits 25/11 · Shenzhou-24 docking 25/11 · Hera crater "
            "images 25/11 · Macy's postponement 25/11 · Giza tanker blast 25/11 "
            "(driver held 26/11).")
    f_txt, _ = fit_font(d, lab + text, SANS, [10, 9, 8.5, 8, 7.5, 7], W - 2 * MX)
    d.text((MX, y + 4), lab, font=f_txt, fill=RED)
    d.text((MX + d.textlength(lab, font=f_txt), y + 4), text, font=f_txt, fill=INK)
    return y + 22


def draw_footer(d, y):
    f1 = F(SANS, 8)
    l1 = ("HOW SURE: OFFICIAL = authority's own word · CONFIRMED = 2+ outlets · "
          "REPORTED = 1 outlet · CLAIM = one side's account, not verified · "
          "ONGOING = still unfolding.")
    d.text((MX, y + 2), l1, font=f1, fill=GREY)
    l2 = ("Sources: AP, Reuters, BBC, AFP, CNN, Guardian, USA Today, Euronews, "
          "Al Jazeera, SCMP, Yonhap, KCNA, UN News, ABC, AAP, TBS, The Hindu, "
          "OkayAfrica, FlightAware, BusinessWorld, FT, Straits Times — every story "
          "happened or was first reported Thu 26 Nov 2026; drawn scenes are "
          "illustrations, not photos.")
    f2, _ = fit_font(d, l2, SANS, [8, 7.5, 7, 6.5], W - 2 * MX)
    d.text((MX, y + 18), l2, font=f2, fill=GREY)
    return y + 36


# ---------------------------------------------------------------- main

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0
    y = draw_top_bar(d, y)          # 28
    y = draw_masthead(d, y)         # 86
    y = draw_stat_boxes(d, y)       # 32
    y = draw_number_strip(d, y)     # 54
    y = draw_region_bar(d, y)       # 20
    y = draw_timeline(d, y)         # 52
    y = draw_heroes(d, y)           # 188
    y = draw_scenes(d, y)           # 228
    y = draw_map(d, y)              # 100
    y = draw_also(d, y)             # 172
    y = draw_datecheck(d, y)        # 22
    y = draw_footer(d, y)           # 36
    print("FINAL Y:", y, "of", H)
    assert y <= H, "layout overflow: FINAL Y %d > %d" % (y, H)
    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
