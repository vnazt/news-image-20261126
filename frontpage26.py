#!/usr/bin/env python3
"""frontpage26.py — draws the news-image-20261126 entry (v2).

A serif newspaper front page, 1024x1024, summing up Thursday 26 November
2026: 35 dated stories, 9 regions, 13 drawn scenes, a world map, a UTC
timeline and an explicit date check. Content comes only from dossier.md
(35 verified stories + 33 date traps). No external assets.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 233)
INK = (18, 18, 18)
RED = (163, 30, 34)
BLUE = (39, 75, 115)
BLUE_LT = (214, 228, 240)
GOLD = (176, 124, 20)
GREY = (110, 108, 100)
GREEN = (46, 110, 70)

FDIR = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)


def rule(x0, y, x1, w=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


# ---------------------------------------------------------------- masthead
text(W // 2, 14, "THE WORLD IN ONE DAY", SERIF_B(58), anchor="ma")
rule(24, 84, 1000, 3)
text(W // 2, 90, "Thursday 26 November 2026", SERIF_B(25), anchor="ma")
text(W // 2, 118, "35 dated stories  ·  9 regions  ·  13 drawn scenes  ·  map  ·  UTC timeline  ·  date check",
     SANS(12), fill=GREY, anchor="ma")
rule(24, 138, 1000, 1, fill=GREY)

# ---------------------------------------------------------------- scene helpers
def cloud(cx, cy, s, fill=(70, 70, 70)):
    for dx, dy, r in [(-1.1, 0.1, 0.62), (0, -0.35, 0.8), (1.1, 0.1, 0.62), (0, 0.25, 0.7)]:
        d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s,
                   cx + dx * s + r * s, cy + dy * s + r * s], fill=fill)


def rain(x0, y0, x1, y1, n=9, fill=BLUE):
    for i in range(n):
        x = x0 + (x1 - x0) * i / max(n - 1, 1)
        d.line([(x, y0), (x - 4, y1)], fill=fill, width=2)


def tag(x, y, s, fill=INK):
    """Top-left scene label on a clean paper chip."""
    w = d.textlength(s, font=SANS_B(11)) + 10
    d.rectangle([x, y, x + w, y + 17], fill=PAPER)
    text(x + 5, y + 2, s, SANS_B(11), fill=fill)


def scene_macys(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    cloud(x + w * 0.30, y + h * 0.42, 16)
    cloud(x + w * 0.72, y + h * 0.36, 13, fill=(95, 95, 95))
    d.ellipse([x + w * 0.38, y + h * 0.52, x + w * 0.66, y + h * 0.82],
              fill=RED, outline=INK, width=2)
    d.polygon([(x + w * 0.50, y + h * 0.82), (x + w * 0.56, y + h * 0.82),
               (x + w * 0.53, y + h * 0.96)], fill=GOLD)
    rain(x + 8, y + h * 0.55, x + w - 8, y + h * 0.98)
    tag(x + 6, y + 6, "100th PARADE — GROUNDED")


def scene_gulf(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=BLUE_LT)
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(58, 110, 160))
    for i in range(4):
        yy = y + h * 0.66 + i * 8
        d.arc([x + 6 + i * 4, yy, x + w - 6 - i * 4, yy + 12], 0, 180, fill=(255, 255, 255), width=2)
    d.rectangle([x + w * 0.10, y + h * 0.46, x + w * 0.52, y + h * 0.62], fill=INK)
    d.rectangle([x + w * 0.42, y + h * 0.32, x + w * 0.52, y + h * 0.46], fill=INK)
    d.line([(x + w * 0.30, y + h * 0.46), (x + w * 0.30, y + h * 0.26)], fill=INK, width=3)
    for r, c in [(11, GOLD), (7, (230, 120, 30)), (4, RED)]:
        d.ellipse([x + w * 0.20 - r, y + h * 0.46 - r * 1.5,
                   x + w * 0.20 + r, y + h * 0.46], fill=c)
    import math
    mx, my, mr = x + w * 0.78, y + h * 0.74, 8
    for a in range(0, 360, 45):
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        d.line([(mx + dx * mr, my + dy * mr), (mx + dx * (mr + 5), my + dy * (mr + 5))],
               fill=INK, width=2)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=INK)
    tag(x + 6, y + 6, "HORMUZ — MINE CLAIM")


def scene_eu(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 214))
    d.ellipse([x + w * 0.14, y + h * 0.34, x + w * 0.86, y + h * 0.86],
              fill=(150, 120, 70), outline=INK, width=2)
    d.ellipse([x + w * 0.32, y + h * 0.48, x + w * 0.68, y + h * 0.72],
              fill=(210, 190, 150), outline=INK, width=1)
    for i, fx in enumerate([0.18, 0.38, 0.58, 0.78]):
        d.rectangle([x + w * fx, y + h * 0.18, x + w * fx + 14, y + h * 0.32],
                    fill=BLUE if i % 2 == 0 else GOLD, outline=INK, width=1)
    text(x + w // 2, y + h * 0.52, "€45bn", SERIF_B(18), fill=RED, anchor="ma")
    tag(x + 6, y + 6, "EU SUMMIT — NO DEAL")


def scene_ebola(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    d.rectangle([x + 8, y + h * 0.42, x + w - 8, y + h * 0.62], fill=(255, 255, 255), outline=INK, width=2)
    d.ellipse([x + w * 0.18, y + h * 0.28, x + w * 0.30, y + h * 0.44], fill=(200, 160, 120))
    d.rectangle([x + w * 0.30, y + h * 0.36, x + w * 0.85, y + h * 0.48], fill=(120, 160, 190))
    d.rectangle([x + w - 24, y + 6, x + w - 8, y + 22], fill=RED)
    d.text((x + w - 20, y + 7), "+", font=SANS_B(13), fill=(255, 255, 255))


def scene_taj(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 226, 210))
    d.rectangle([x + 12, y + h * 0.52, x + w - 12, y + h * 0.78], fill=(190, 170, 140))
    d.pieslice([x + w * 0.38, y + h * 0.18, x + w * 0.62, y + h * 0.56], 180, 360, fill=(190, 170, 140))
    d.line([(x + w * 0.50, y + h * 0.06), (x + w * 0.50, y + h * 0.20)], fill=INK, width=2)
    d.rectangle([x + w * 0.14, y + h * 0.28, x + w * 0.20, y + h * 0.76], fill=(190, 170, 140))
    d.rectangle([x + w * 0.80, y + h * 0.28, x + w * 0.86, y + h * 0.76], fill=(190, 170, 140))
    for fx in [0.25, 0.35, 0.65, 0.75]:
        d.ellipse([x + w * fx - 3, y + h * 0.82, x + w * fx + 3, y + h * 0.88], fill=RED)


def scene_chess(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    s = min(w, h) // 4
    ox, oy = x + (w - 4 * s) // 2, y + 2
    for r in range(4):
        for c in range(4):
            fill = INK if (r + c) % 2 == 0 else (255, 255, 255)
            d.rectangle([ox + c * s, oy + r * s, ox + (c + 1) * s, oy + (r + 1) * s],
                        fill=fill, outline=INK, width=1)
    d.ellipse([ox + s * 1.2, oy + s * 0.2, ox + s * 1.8, oy + s * 0.8], fill=RED)
    d.ellipse([ox + s * 2.2, oy + s * 2.2, ox + s * 2.8, oy + s * 2.8], fill=BLUE)


def scene_hk(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 230, 238))
    d.rectangle([x + w * 0.28, y + h * 0.12, x + w * 0.72, y + h * 0.68],
                fill=(120, 120, 130), outline=INK, width=2)
    for r in range(3):
        for c in range(4):
            d.rectangle([x + w * (0.33 + c * 0.10), y + h * (0.20 + r * 0.16),
                         x + w * (0.40 + c * 0.10), y + h * (0.30 + r * 0.16)],
                        fill=(240, 220, 120))
    for fx in [0.2, 0.35, 0.5, 0.65, 0.8]:
        d.ellipse([x + w * fx - 4, y + h * 0.76, x + w * fx + 4, y + h * 0.84], fill=RED)
        d.ellipse([x + w * fx - 2, y + h * 0.78, x + w * fx + 2, y + h * 0.82], fill=GOLD)


def scene_bangkok(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    for i, tx in enumerate([0.18, 0.42, 0.66]):
        d.rectangle([x + w * tx, y + h * 0.28, x + w * tx + 15, y + h * 0.72],
                    fill=(150, 150, 150), outline=INK, width=1)
    for r, c in [(12, GOLD), (8, (230, 120, 30)), (4, RED)]:
        d.ellipse([x + w * 0.50 - r, y + h * 0.30 - r, x + w * 0.50 + r, y + h * 0.30 + r], fill=c)
    cloud(x + w * 0.74, y + h * 0.20, 9, fill=(90, 90, 90))


def scene_bogor(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 200))
    d.polygon([(x, y + h * 0.72), (x + w * 0.35, y + h * 0.32), (x + w * 0.65, y + h * 0.58),
               (x + w, y + h * 0.38), (x + w, y + h), (x, y + h)], fill=GREEN)
    d.rectangle([x + w * 0.45, y + h * 0.52, x + w * 0.55, y + h * 0.92], fill=INK)
    d.line([(x + w * 0.50, y + h * 0.28), (x + w * 0.50, y + h * 0.52)], fill=RED, width=3)
    d.ellipse([x + w * 0.46, y + h * 0.22, x + w * 0.54, y + h * 0.30], fill=RED)


def scene_europa(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 90, 50))
    d.rectangle([x + w * 0.10, y + h * 0.14, x + w * 0.90, y + h * 0.80],
                outline=(255, 255, 255), width=2)
    for i in range(1, 5):
        yy = y + h * (0.14 + i * 0.132)
        d.line([(x + w * 0.10, yy), (x + w * 0.90, yy)], fill=(255, 255, 255), width=1)
    for i in range(1, 6):
        xx = x + w * (0.10 + i * 0.16)
        d.line([(xx, y + h * 0.14), (xx, y + h * 0.80)], fill=(255, 255, 255), width=1)
    d.ellipse([x + w * 0.44, y + h * 0.40, x + w * 0.56, y + h * 0.52],
              fill=(255, 255, 255), outline=INK, width=1)


def scene_canary(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=BLUE_LT)
    d.rectangle([x, y + h * 0.58, x + w, y + h], fill=(58, 110, 160))
    d.polygon([(x + w * 0.30, y + h * 0.56), (x + w * 0.70, y + h * 0.56),
               (x + w * 0.62, y + h * 0.70), (x + w * 0.38, y + h * 0.70)], fill=(120, 80, 40))
    d.line([(x + w * 0.50, y + h * 0.56), (x + w * 0.50, y + h * 0.26)], fill=INK, width=2)
    d.polygon([(x + w * 0.50, y + h * 0.26), (x + w * 0.50, y + h * 0.54),
               (x + w * 0.68, y + h * 0.54)], fill=(255, 255, 255))
    for fx in [0.40, 0.50, 0.60]:
        d.ellipse([x + w * fx - 3, y + h * 0.44, x + w * fx + 3, y + h * 0.50], fill=INK)


def scene_court(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    for cx in [0.22, 0.50, 0.78]:
        d.rectangle([x + w * cx - 5, y + h * 0.24, x + w * cx + 5, y + h * 0.68], fill=(200, 190, 170))
    d.polygon([(x + w * 0.08, y + h * 0.24), (x + w * 0.92, y + h * 0.24),
               (x + w * 0.50, y + h * 0.06)], fill=(170, 150, 120))
    d.rectangle([x + w * 0.08, y + h * 0.68, x + w * 0.92, y + h * 0.76], fill=(170, 150, 120))


def scene_korea(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    bars = [0.30, 0.48, 0.40, 0.66]
    for i, bh in enumerate(bars):
        bx = x + w * (0.12 + i * 0.20)
        d.rectangle([bx, y + h * (0.74 - bh), bx + 13, y + h * 0.74],
                    fill=BLUE if i < 3 else RED)
    d.line([(x + 8, y + h * 0.74), (x + w - 8, y + h * 0.74)], fill=INK, width=2)
    text(x + w - 8, y + h * 0.06, "3.25%", SERIF_B(14), fill=RED, anchor="ra")


# ---------------------------------------------------------------- hero row
heroes = [
    ("MACY'S 100TH PARADE POSTPONED",
     "The Thanksgiving nor'easter grounds the centenary parade — a first in 100 years. 750,000+ without power.",
     scene_macys),
    ("THE GULF WAR WIDENS",
     "Hormuz mine claim (unverified) · drones kill 2 Italians in Kuwait · Houthis hit Jazan refinery · Brent $96.57.",
     scene_gulf),
    ("EU SUMMIT FAILS ON BUDGET + €45BN LOAN",
     "No deal on the 2028–34 budget or the Ukraine loan — deferred to 17–18 Dec — as the ECB picks Hernández de Cos.",
     scene_eu),
]
for i, (head, sub, scene) in enumerate(heroes):
    x = 24 + i * 328
    d.rectangle([x, 146, x + 320, 316], outline=INK, width=2)
    scene(x + 2, 148, 316, 88)
    hl = wrap(head, SERIF_B(16), 306)
    for j, ln in enumerate(hl):
        text(x + 8, 240 + j * 19, ln, SERIF_B(16))
    for j, ln in enumerate(wrap(sub, SERIF(10), 306)):
        text(x + 8, 280 + j * 13, ln, SERIF(10), fill=(60, 60, 60))

# ---------------------------------------------------------------- vignette strip
text(24, 326, "DRAWN SCENES", SANS_B(11), fill=RED)
rule(140, 332, 1000, 1, fill=GREY)
vignettes = [
    (scene_ebola, "EBOLA · 12,021"),
    (scene_taj, "26/11 · 18 YRS"),
    (scene_chess, "GUKESH DRAW"),
    (scene_hk, "WANG FUK · 168"),
    (scene_bangkok, "BANGKOK BLAST"),
    (scene_bogor, "BOGOR · 13 DEAD"),
    (scene_europa, "BOURNEMOUTH 5/5"),
    (scene_canary, "CANARIES 16,000+"),
    (scene_court, "DEPARDIEU TRIAL"),
    (scene_korea, "KOREA RATE 3.25%"),
]
for i, (sc, cap) in enumerate(vignettes):
    x = 24 + i * 98
    d.rectangle([x, 340, x + 94, 404], outline=INK, width=1)
    sc(x + 1, 341, 92, 44)
    d.rectangle([x + 1, 385, x + 93, 403], fill=PAPER)
    text(x + 4, 389, cap, SANS_B(8))

# ---------------------------------------------------------------- map + timeline
text(24, 414, "WORLD MAP — 35 STORIES · 9 REGIONS", SANS_B(11), fill=RED)
text(536, 414, "UTC TIMELINE — THURSDAY 26 NOVEMBER", SANS_B(11), fill=RED)
# map box
d.rectangle([24, 430, 524, 524], fill=BLUE_LT, outline=INK, width=2)
d.line([(24, 477), (524, 477)], fill=(180, 200, 215), width=1)
# stylised continents (schematic, separated blobs)
d.polygon([(52, 448), (120, 436), (175, 446), (165, 468), (105, 474), (58, 462)], fill=(226, 214, 180))  # N America
d.polygon([(148, 482), (182, 480), (192, 502), (168, 514), (146, 496)], fill=(226, 214, 180))  # S America
d.polygon([(262, 452), (305, 444), (330, 458), (322, 484), (292, 496), (264, 476)], fill=(226, 214, 180))  # Africa
d.polygon([(312, 440), (360, 434), (392, 440), (380, 452), (330, 452), (312, 446)], fill=(226, 214, 180))  # Europe
d.polygon([(396, 440), (478, 436), (506, 452), (492, 478), (440, 486), (400, 462)], fill=(226, 214, 180))  # Asia
d.ellipse([452, 494, 478, 508], fill=(226, 214, 180))  # Australia
markers = [(110, 452, "NA"), (168, 498, "LAT"), (294, 470, "AF"),
           (348, 444, "EU"), (326, 462, "ME"), (392, 456, "SA"),
           (452, 448, "EA"), (428, 478, "SEA"), (468, 502, "SP")]
for mx, my, lab in markers:
    d.ellipse([mx - 6, my - 6, mx + 6, my + 6], fill=RED, outline=(255, 255, 255), width=1)
    text(mx, my - 15, lab, SANS_B(8), fill=RED, anchor="ma")
# timeline box
d.rectangle([536, 430, 1000, 524], outline=INK, width=2)
d.line([(556, 480), (980, 480)], fill=INK, width=2)
for h in range(0, 25, 3):
    tx = 556 + (980 - 556) * h / 24
    d.line([(tx, 476), (tx, 484)], fill=INK, width=2)
    text(tx, 488, f"{h:02d}", SANS(9), fill=GREY, anchor="ma")
text(556, 438, "UTC", SANS_B(10), fill=GREY)
events = [  # (hour, label, row) row: 1=above far, 2=above near, 3=below
    (0.5, "#8 KYIV", 1), (2, "#9 GAZA", 3), (6, "#13 EBOLA", 1),
    (7.75, "#19 BANGKOK", 3), (9, "#6 EU SUMMIT", 2), (12, "#24 UK 77k", 2),
    (18, "#27 SHEINBAUM", 3), (20, "#35 EUROPA LGE", 1),
]
for hr, lab, row in events:
    tx = 556 + (980 - 556) * hr / 24
    d.ellipse([tx - 4, 476, tx + 4, 484], fill=RED)
    ly = {1: 442, 2: 458, 3: 500}[row]
    text(tx, ly, lab, SANS_B(8), fill=INK, anchor="ma")
text(556, 512, "Times UTC as reported; overnight items placed 00–03.", SANS(8), fill=GREY)

# ---------------------------------------------------------------- story grid
stories = {
    "NORTH AMERICA · 5": [
        ("#1", "MACY'S 100TH PARADE POSTPONED — first delay in a century; moves to Sat 28 Nov"),
        ("#2", "NOR'EASTER PEAKS ON THANKSGIVING — 750,000+ lose power; 844 flights cancelled"),
        ("#3", "NFL HISTORY: THREE THRILLERS — Bears, Eagles, Bills all win on final-minute scores"),
        ("#29", "TARIFF FALLOUT — China and EU reject new US 14-economy tariff plan (reactions 26 Nov)"),
        ("#30", "FEDEX MIAMI DELAYS TOP 3½ HOURS — after Wed-night runway overrun"),
    ],
    "EUROPE · 7": [
        ("#6", "EU SUMMIT FAILS ON BUDGET AND €45BN UKRAINE LOAN — deferred to 17–18 Dec"),
        ("#7", "ECB PICKS HERNÁNDEZ DE COS — first Spaniard to head the bank"),
        ("#8", "KYIV HIT BY BALLISTIC MISSILES — 7 wounded; Zelenskyy warns new strike is coming"),
        ("#24", "UK NET MIGRATION FALLS TO 77,000 — lowest since 1997, ONS says"),
        ("#25", "DEPARDIEU ORDERED TO STAND TRIAL — for alleged 2018 rape; he denies it"),
        ("#26", "CANARY ISLANDS: BUSIEST MONTH ON RECORD — November arrivals pass 16,000"),
        ("#31", "GERMANY ARRESTS TWO OVER ALLEGED COLOGNE SYNAGOGUE PLOT — 17 raids"),
    ],
    "MIDDLE EAST · 5": [
        ("#9", "GAZA STRIKES KILL 9–10 — incl. Hamas minister Abu Nada; third straight night"),
        ("#10", "IRGC CLAIMS TWO TANKERS HIT MINES OFF KHASAB — claim unconfirmed"),
        ("#11", "HOUTHIS HIT SAUDI JAZAN REFINERY — 1 worker killed; operations halted"),
        ("#12", "THOUSANDS PROTEST IN IRBIL — Baghdad seizes Kurdish oil and borders"),
        ("#32", "IRANIAN DRONES KILL TWO ITALIANS IN KUWAIT — Italy, Kuwait blame Iran; Tehran denies"),
    ],
    "AFRICA · 5": [
        ("#13", "EBOLA IN DR CONGO PASSES 12,000 CASES — 5,904 dead; fastest-growing outbreak"),
        ("#14", "CAIRO MOURNS 31 KILLED IN TANKER BLAST — driver arrested; blast itself was 25 Nov"),
        ("#15", "GUINEA-BISSAU JUNTA POSTPONES ELECTIONS TO 2028 — one year after the coup"),
        ("#16", "UN PEACEKEEPERS STEP UP IN ITURI — fighting resumes as Ebola spreads"),
        ("#17", "SENEGAL'S YOUNG RISK THE ATLANTIC — record November crossings to the Canaries"),
    ],
    "SOUTH ASIA · 1": [
        ("#5", "INDIA MARKS 18 YEARS SINCE 26/11 — Mumbai on high alert; tributes at the Taj"),
    ],
    "EAST ASIA · 3": [
        ("#21", "HONG KONG MARKS ONE YEAR SINCE WANG FUK COURT FIRE — 168 dead"),
        ("#22", "KIM CALLS TACTICAL-NUKE DEPLOYMENT 'URGENT' — KCNA reports facility tour"),
        ("#23", "BANK OF KOREA RAISES RATE TO 3.25% — 2027 growth seen at 4.1%"),
    ],
    "SE ASIA & PACIFIC · 3": [
        ("#18", "BOGOR MINE TOLL RISES TO 13 — 13 still trapped; rain halts rescue (flood was 23 Nov)"),
        ("#19", "BANGKOK REFINERY BLAST INJURES 7–9 — plant shut; all units halted"),
        ("#20", "MYANMAR WON'T FULLY COMPLY WITH ICJ ORDERS — president at cabinet meeting"),
    ],
    "LATIN AMERICA · 2": [
        ("#27", "SHEINBAUM BLASTS DEA TIP LINES AS 'INTERFERENCE' — 'cooperation without subordination'"),
        ("#28", "WHO CHIEF PLEDGES $1M FOR HAITI'S LAST MAJOR PUBLIC HOSPITAL"),
    ],
    "SPORT & WORLD · 4": [
        ("#4", "GUKESH–SINDAROV GAME 3: 60-MOVE DRAW — 1.5–1.5 in Geneva"),
        ("#33", "BRENT SETTLES AT $96.57 — strongest close since 6 Nov as Gulf fears spike"),
        ("#34", "UNCTAD: MARITIME TRADE TO STALL AT ZERO GROWTH — four chokepoints"),
        ("#35", "EUROPA LEAGUE: BOURNEMOUTH STAY PERFECT — 5 from 5; Milan, Juve fight back"),
    ],
}
columns = [
    [("NORTH AMERICA · 5", stories["NORTH AMERICA · 5"]),
     ("EUROPE · 7", stories["EUROPE · 7"])],
    [("MIDDLE EAST · 5", stories["MIDDLE EAST · 5"]),
     ("AFRICA · 5", stories["AFRICA · 5"]),
     ("SOUTH ASIA · 1", stories["SOUTH ASIA · 1"])],
    [("EAST ASIA · 3", stories["EAST ASIA · 3"]),
     ("SE ASIA & PACIFIC · 3", stories["SE ASIA & PACIFIC · 3"]),
     ("LATIN AMERICA · 2", stories["LATIN AMERICA · 2"]),
     ("SPORT & WORLD · 4", stories["SPORT & WORLD · 4"])],
]
GRID_TOP = 534
for ci, col in enumerate(columns):
    x = 24 + ci * 328
    y = GRID_TOP
    for region, items in col:
        text(x, y, region, SANS_B(12), fill=RED)
        rule(x, y + 16, x + 318, 1, fill=RED)
        y += 20
        for no, head in items:
            lines = wrap(head, SERIF_B(10), 284)
            text(x, y, no, SANS_B(10), fill=RED)
            for j, ln in enumerate(lines):
                text(x + 30, y + j * 11.5, ln, SERIF_B(10))
            y += len(lines) * 11.5 + 3
        y += 2

# ---------------------------------------------------------------- date check
d.rectangle([24, 942, 1000, 1016], outline=RED, width=2)
text(36, 948, "DATE CHECK — NOT 26 NOVEMBER NEWS (EXCLUDED):", SANS_B(11), fill=RED)
excluded = [
    "25 Nov: US tariff plan on 14 economies",
    "25 Nov: Asian chip rout (Kospi −6.2%)",
    "25 Nov: Shenzhou-24 docks at Tiangong",
    "25 Nov: Cairo tanker blast (31 dead)",
    "23 Nov: Bogor mine flood",
    "23 Nov: COP31 collapse · NATO session · Merkury",
    "25 Nov: Durant 33,000 pts · gold <$3,500",
    "25 Nov: Australia CPI 4.9% · Rams–Packers",
    "24 Nov: Huawei convicted · 19 Nov: ICJ Myanmar ruling",
    "25 Nov: Houthi Ras Tanura claim · Netanyahu judges",
]
for i, item in enumerate(excluded):
    cx = 36 + (i % 2) * 480
    cy = 968 + (i // 2) * 9
    text(cx, cy, "•  " + item, SANS(9), fill=(70, 60, 55))

out = os.environ.get("FRONTPAGE_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"))
img.save(out, "PNG", optimize=True)
print("saved", out, img.size, os.path.getsize(out), "bytes")
