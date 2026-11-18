#!/usr/bin/env python3
"""Render the front page for Tuesday 17 November 2026 (1024x1024 PNG).

A newspaper-style single image summing up the day's world news: 13 featured
stories with flat vector-style illustrations, a world map with numbered pins,
30 one-line briefs, and a source footer. All 43 stories are real news from
17 November 2026, transcribed from the day's reporting and verified against
wire coverage (Reuters, AP, AFP, BBC, Al Jazeera, WHO, PAHO, UN).

Run: python3 compose.py   -> writes entry.png next to this file.
Deterministic: same fonts, same data, same bytes every run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
PAPER = (247, 241, 227)
INK = (26, 26, 26)
SOFT = (90, 84, 72)
RED = (200, 16, 46)
HAIR = (190, 180, 158)
SEA = (201, 222, 236)
LAND = (216, 201, 163)
LAND_LINE = (170, 152, 110)

FDIR = "/usr/share/fonts/truetype"
SERIF_DISPLAY = f"{FDIR}/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = f"{FDIR}/dejavu/DejaVuSerif-Bold.ttf"
SANS = f"{FDIR}/noto/NotoSans-Regular.ttf"
SANS_BOLD = f"{FDIR}/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- data
# cat: display category; sub: second part of the category bar; col: colour.
FEATURED = [
    dict(n=1, cat="EUROPE", sub="UKRAINE WAR", col=(43, 94, 167),
         head="Ukraine says a Crimean Bridge road span fell into the sea",
         deck="Second strike in two days; Zelensky hails it \u2018unprecedented\u2019. The Kremlin vows to rebuild.",
         illo="bridge", lon=36.5, lat=45.3),
    dict(n=2, cat="MIDDLE EAST", sub="IRAN WAR", col=(198, 90, 18),
         head="Iran sends drones at a US radar in Bahrain; US hits back",
         deck="Bahrain and the US say all downed; US jets hit Qeshm. Iran says tankers hit mines in Hormuz.",
         illo="gulf", lon=50.5, lat=26.2),
    dict(n=3, cat="ASIA", sub="DIPLOMACY", col=(106, 63, 160),
         head="Trump holds his first Quad summit, in Manila",
         deck="The four unveil critical-minerals deals; Putin flies to Shenzhen for talks with Trump and Xi.",
         illo="quad", lon=121.0, lat=14.6),
    dict(n=4, cat="AFRICA", sub="HEALTH", col=(46, 125, 50),
         head="Ebola cases in DR Congo top 11,000, WHO says",
         deck="Cases doubled in three months; about 5,400 have died.",
         illo="clinic", lon=23.0, lat=-2.5),
    dict(n=5, cat="GLOBAL", sub="CLIMATE", col=(0, 131, 143),
         head="COP31 divided over a fossil-fuel phase-out",
         deck="Nations weigh the first draft; talks end Friday.",
         illo="globe", lon=30.7, lat=36.9),
    dict(n=6, cat="AMERICAS", sub="HEALTH", col=(183, 28, 28),
         head="US, Mexico and Bolivia lose measles-free status",
         deck="PAHO cites a year of spread; US cases top 5,700 in 2026.",
         illo="flags", lon=-98.0, lat=39.0),
    dict(n=7, cat="US", sub="BUSINESS", col=(31, 56, 100),
         head="Nvidia\u2019s quarterly sales double to $115.8bn",
         deck="Reported after the close; the Dow fell 849 points (\u22121.6%).",
         illo="chart", lon=-122.0, lat=37.4),
    dict(n=8, cat="MIDDLE EAST", sub="GAZA", col=(198, 90, 18),
         head="Gaza truce at risk of collapse, UN is told",
         deck="Board of Peace report; 1.4m face acute hunger, UN says.",
         illo="tents", lon=34.5, lat=31.5),
    dict(n=9, cat="ASIA", sub="POLITICS", col=(106, 63, 160),
         head="Mongolia\u2019s president says he will resign",
         deck="Kh\u00fcrels\u00fckh denies a $25m bribe claim; MPs must accept.",
         illo="palace", lon=106.9, lat=47.9),
    dict(n=10, cat="EUROPE", sub="POLITICS", col=(43, 94, 167),
         head="Serbia\u2019s student majority takes its seats",
         deck="Student List holds 140 of 250; Vu\u010di\u0107\u2019s party in opposition.",
         illo="seats", lon=20.5, lat=44.8),
    dict(n=11, cat="ASIA", sub="LABOUR", col=(106, 63, 160),
         head="Bangladesh police tear-gas garment workers",
         deck="Want Tk 30,000 a month, up from 12,500; 37 factories shut.",
         illo="factory", lon=90.4, lat=23.8),
    dict(n=12, cat="RUSSIA", sub="AIR CRASH", col=(97, 97, 97),
         head="Russian An-12 crash in Siberia kills all 19",
         deck="Air force plane down near Kemerovo; a fault is suspected.",
         illo="crash", lon=86.0, lat=55.4),
    dict(n=13, cat="AFRICA", sub="JUSTICE", col=(46, 125, 50),
         head="Mozambique puts opposition leader on trial",
         deck="Mondlane faces 5 charges over deadly 2024 protests.",
         illo="trial", lon=32.6, lat=-25.9),
]

# (number, one-line text, lon, lat, region colour)
REGION = {
    "americas": (192, 57, 43), "europe": (43, 94, 167),
    "mideast": (198, 90, 18), "asia": (106, 63, 160),
    "africa": (46, 125, 50), "oceania": (0, 131, 143),
    "global": (117, 117, 117),
}
BRIEFS = [
    (14, "Russia: record 1,441 drones downed overnight.", 37.6, 55.7, "europe"),
    (15, "Kyiv: missiles hit the two Dnipro bridges.", 30.5, 50.4, "europe"),
    (16, "UN: Ukraine civilian deaths top all of 2025.", 31.0, 49.0, "europe"),
    (17, "Prague: two trains collide; 46 people injured.", 14.4, 50.1, "europe"),
    (18, "France: public-sector strike; 146,000 march.", 2.35, 48.85, "europe"),
    (19, "Poland: Tusk government survives confidence vote.", 21.0, 52.2, "europe"),
    (20, "Germany: Deutsche Bank shares fall on data leak.", 13.4, 52.5, "europe"),
    (21, "Moldova: shuts airspace as drone nears Chi\u015fin\u0103u.", 28.8, 47.0, "europe"),
    (22, "Turkey: police seize opposition TV channel S\u00f6zc\u00fc.", 32.9, 39.9, "mideast"),
    (23, "Football: Norway win 3\u20132 in Denmark; Haaland x2.", 12.6, 55.7, "europe"),
    (24, "Vatican: Pope Leo XIV back from South America tour.", 12.45, 41.9, "europe"),
    (25, "UK: sanctions 8 settlement firms and Tzav 9.", -0.1, 51.5, "europe"),
    (26, "Israel: Matan Kahana elected speaker, 66\u201352.", 35.2, 31.8, "mideast"),
    (27, "West Bank: settlers kill woman, 72, near Jericho.", 35.5, 31.85, "mideast"),
    (28, "Oman: Iran\u2019s Araghchi holds shipping-safety talks.", 58.4, 23.6, "mideast"),
    (29, "India: Cyclone Akvan nears; Odisha evacuates.", 85.8, 20.3, "asia"),
    (30, "India: bus falls into Uttarakhand gorge, 8 dead.", 79.5, 30.3, "asia"),
    (31, "Japan: protests Russian airspace breach.", 130.4, 33.6, "asia"),
    (32, "China\u2013Canada: tariff cuts after Carney\u2013Xi talks.", 116.4, 39.9, "asia"),
    (33, "Malaysia: Macron visit seals strategic partnership.", 101.7, 3.1, "asia"),
    (34, "Thailand: pledges to scrap tariffs on US goods.", 100.5, 13.75, "asia"),
    (35, "S. Korea: IMF lifts 2026 growth forecast to 3.9%.", 127.0, 37.5, "asia"),
    (36, "Football: India beat Pakistan 2\u20131 in SAFF final.", 77.2, 28.6, "asia"),
    (37, "Kenya: WFP aids 30,000 who fled Ethiopia clashes.", 36.8, -1.3, "africa"),
    (38, "Cricket: Sri Lanka bowled out for 98.", 79.9, 6.9, "asia"),
    (39, "Haiti: Aristide\u2019s party will field no candidates.", -72.3, 18.5, "americas"),
    (40, "US Senate: Van Hollen challenges Schumer.", -77.0, 38.9, "americas"),
    (41, "Australia: eases planned backpacker visa curbs.", 149.1, -35.3, "oceania"),
    (42, "Darwin: M6.6 quake off Indonesia felt; no tsunami.", 130.8, -12.5, "oceania"),
    (43, "Apple: Pay, iCloud, App Store outage; not a hack.", -122.0, 37.3, "global"),
]

LEGEND = [("Americas", "americas"), ("Europe", "europe"),
          ("Middle East", "mideast"), ("Asia", "asia"),
          ("Africa", "africa"), ("Oceania", "oceania"),
          ("Global & space", "global")]


# ---------------------------------------------------------------- helpers
def wrap(text, fnt, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def tint(rgb, f):
    """Mix a colour toward white by factor f (0..1) for pastel backgrounds."""
    return tuple(int(c + (255 - c) * f) for c in rgb)


def rrect(d, box, rad, **kw):
    d.rounded_rectangle(box, radius=rad, **kw)


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(120, 120, 120))
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7], fill=(178, 34, 52))
    d.rectangle([x, y, x + w * 0.42, y + h * 0.55], fill=(30, 60, 120))


def flag_pole(d, x, y, h):
    d.line([x, y, x, y + h], fill=(70, 60, 50), width=2)
    d.ellipse([x - 2, y - 3, x + 2, y + 1], fill=(200, 170, 60))

# ------------------------------------------------------- illustrations
# Each draws a flat vector-style scene inside box (x, y, w, h).
# No text inside any illustration.

def illo_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 233, 242))
    d.rectangle([x, y + h * 0.58, x + w, y + h], fill=(176, 208, 231))
    # bridge deck, broken in the middle
    dy = y + h * 0.55
    d.rectangle([x + 2, dy, x + w * 0.42, dy + 7], fill=(70, 74, 80))
    d.rectangle([x + w * 0.58, dy, x + w - 2, dy + 7], fill=(70, 74, 80))
    d.polygon([(x + w * 0.42, dy), (x + w * 0.50, dy + 16), (x + w * 0.46, dy + 18),
               (x + w * 0.40, dy + 7)], fill=(90, 94, 100))
    d.polygon([(x + w * 0.58, dy), (x + w * 0.52, dy + 12), (x + w * 0.56, dy + 16),
               (x + w * 0.60, dy + 7)], fill=(90, 94, 100))
    # towers + cables
    for tx in (x + w * 0.22, x + w * 0.78):
        d.rectangle([tx - 3, dy - h * 0.42, tx + 3, dy], fill=(70, 74, 80))
        d.line([tx, dy - h * 0.42, x + 4, dy], fill=(120, 126, 132), width=1)
        d.line([tx, dy - h * 0.42, x + w * 0.42, dy], fill=(120, 126, 132), width=1)
        d.line([tx, dy - h * 0.42, x + w * 0.58, dy], fill=(120, 126, 132), width=1)
        d.line([tx, dy - h * 0.42, x + w - 4, dy], fill=(120, 126, 132), width=1)
    # smoke + flame over the break
    cx, cy = x + w * 0.5, dy - h * 0.16
    for ox, oy, r, c in ((-14, 4, 9, (150, 150, 150)), (0, -4, 11, (130, 130, 130)),
                        (13, 3, 8, (160, 160, 160))):
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=c)
    d.polygon([(cx - 6, dy - 2), (cx, dy - 16), (cx + 6, dy - 2)], fill=(230, 120, 40))
    # jets
    for jx, jy in ((x + w * 0.12, y + h * 0.16), (x + w * 0.86, y + h * 0.10)):
        d.polygon([(jx, jy), (jx - 12, jy + 4), (jx - 4, jy + 6), (jx + 2, jy + 3)],
                  fill=(60, 60, 66))


def illo_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(239, 230, 207))
    # sea: the Gulf, diagonal band
    d.polygon([(x + w * 0.28, y + h), (x + w * 0.55, y), (x + w * 0.95, y),
               (x + w * 0.72, y + h)], fill=(150, 196, 224))
    d.polygon([(x + w * 0.28, y + h), (x + w * 0.55, y), (x + w * 0.95, y),
               (x + w * 0.72, y + h)], outline=(110, 160, 195))
    # land masses
    d.polygon([(x, y), (x + w * 0.55, y), (x + w * 0.28, y + h), (x, y + h)],
              fill=(226, 205, 160))
    d.polygon([(x + w * 0.95, y), (x + w, y), (x + w, y + h), (x + w * 0.72, y + h)],
              fill=(226, 205, 160))
    # strait pinch + dots
    for px, py in ((0.50, 0.30), (0.58, 0.52), (0.46, 0.62)):
        d.ellipse([x + w * px - 4, y + h * py - 4, x + w * px + 4, y + h * py + 4],
                  fill=(200, 16, 46))
    # drones: small dark crosses
    for px, py in ((0.40, 0.22), (0.66, 0.68)):
        cx, cy = x + w * px, y + h * py
        d.line([cx - 6, cy, cx + 6, cy], fill=(50, 50, 55), width=2)
        d.line([cx, cy - 6, cx, cy + 6], fill=(50, 50, 55), width=2)
    # strike arrow
    d.line([x + w * 0.70, y + h * 0.18, x + w * 0.60, y + h * 0.42],
           fill=(200, 90, 30), width=3)
    d.polygon([(x + w * 0.60, y + h * 0.42), (x + w * 0.66, y + h * 0.40),
               (x + w * 0.62, y + h * 0.48)], fill=(200, 90, 30))


def illo_quad(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(243, 230, 200))
    # flags on poles
    specs = [("us", 0.10), ("in", 0.32), ("jp", 0.54), ("au", 0.76)]
    for kind, fx in specs:
        px, py = x + w * fx, y + h * 0.10
        fw, fh = w * 0.20, h * 0.26
        flag_pole(d, px, py, h * 0.42)
        if kind == "us":
            flag_us(d, px + 2, py + 2, fw, fh)
        elif kind == "in":
            d.rectangle([px + 2, py + 2, px + 2 + fw, py + 2 + fh], fill=(255, 255, 255),
                        outline=(120, 120, 120))
            d.rectangle([px + 2, py + 2, px + 2 + fw, py + 2 + fh / 3], fill=(255, 153, 51))
            d.rectangle([px + 2, py + 2 + 2 * fh / 3, px + 2 + fw, py + 2 + fh],
                        fill=(19, 136, 8))
            d.ellipse([px + 2 + fw / 2 - 3, py + 2 + fh / 2 - 3, px + 2 + fw / 2 + 3,
                       py + 2 + fh / 2 + 3], outline=(0, 0, 128))
        elif kind == "jp":
            d.rectangle([px + 2, py + 2, px + 2 + fw, py + 2 + fh], fill=(255, 255, 255),
                        outline=(120, 120, 120))
            d.ellipse([px + 2 + fw / 2 - 5, py + 2 + fh / 2 - 5, px + 2 + fw / 2 + 5,
                       py + 2 + fh / 2 + 5], fill=(188, 0, 45))
        else:
            d.rectangle([px + 2, py + 2, px + 2 + fw, py + 2 + fh], fill=(0, 40, 120),
                        outline=(120, 120, 120))
            for sx, sy in ((0.3, 0.3), (0.6, 0.25), (0.5, 0.6), (0.75, 0.65)):
                d.ellipse([px + 2 + fw * sx - 2, py + 2 + fh * sy - 2,
                           px + 2 + fw * sx + 2, py + 2 + fh * sy + 2], fill=(255, 255, 255))
    # table + four seated figures
    d.rectangle([x + w * 0.06, y + h * 0.66, x + w * 0.94, y + h * 0.92],
                fill=(146, 94, 52))
    d.rectangle([x + w * 0.06, y + h * 0.66, x + w * 0.94, y + h * 0.72],
                fill=(120, 74, 40))
    for i, c in enumerate(((52, 84, 150), (180, 90, 40), (60, 120, 70), (130, 70, 140))):
        cx = x + w * (0.18 + i * 0.21)
        d.ellipse([cx - 8, y + h * 0.44, cx + 8, y + h * 0.44 + 16], fill=(232, 190, 150))
        d.polygon([(cx - 14, y + h * 0.66), (cx + 14, y + h * 0.66),
                   (cx + 9, y + h * 0.54), (cx - 9, y + h * 0.54)], fill=c)


def illo_clinic(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 239, 224))
    # clinic building
    bx, by, bw, bh = x + w * 0.08, y + h * 0.34, w * 0.62, h * 0.58
    d.rectangle([bx, by, bx + bw, by + bh], fill=(255, 255, 255), outline=(150, 150, 150))
    d.rectangle([bx, by, bx + bw, by + h * 0.10], fill=(200, 60, 60))
    d.rectangle([bx + bw * 0.42, by + bh * 0.55, bx + bw * 0.58, by + bh],
                fill=(90, 110, 130))
    for wx in (0.14, 0.68):
        d.rectangle([bx + bw * wx, by + bh * 0.30, bx + bw * (wx + 0.16),
                     by + bh * 0.55], fill=(170, 210, 230), outline=(150, 150, 150))
    # red cross sign
    cx, cy = bx + bw / 2, y + h * 0.17
    d.rectangle([cx - 4, cy - 10, cx + 4, cy + 10], fill=(200, 30, 40))
    d.rectangle([cx - 10, cy - 4, cx + 10, cy + 4], fill=(200, 30, 40))
    # virus: spiky circles
    for vx, vy, r, c in ((0.82, 0.28, 10, (150, 60, 60)), (0.88, 0.62, 8, (90, 120, 60))):
        cx, cy = x + w * vx, y + h * vy
        for k in range(8):
            ang = k * 3.14159 / 4
            d.line([cx + r * 0.8 * _cos(ang), cy + r * 0.8 * _sin(ang),
                    cx + r * 1.35 * _cos(ang), cy + r * 1.35 * _sin(ang)],
                   fill=c, width=2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
        d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.2, cy + r * 0.2],
                  fill=(255, 255, 255))


def _cos(a):
    import math
    return math.cos(a)


def _sin(a):
    import math
    return math.sin(a)


def illo_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(221, 238, 234))
    # sun
    sx, sy = x + w * 0.16, y + h * 0.18
    d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=(240, 190, 60))
    for k in range(8):
        ang = k * 3.14159 / 4
        d.line([sx + 11 * _cos(ang), sy + 11 * _sin(ang),
                sx + 17 * _cos(ang), sy + 17 * _sin(ang)], fill=(240, 190, 60), width=2)
    # globe
    cx, cy, r = x + w * 0.42, y + h * 0.55, h * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 210),
              outline=(60, 120, 170), width=2)
    for lx, ly, lr in ((-0.4, -0.25, 0.30), (0.35, 0.15, 0.34), (-0.1, 0.45, 0.26),
                       (0.45, -0.35, 0.18)):
        d.ellipse([cx + lx * r - lr * r, cy + ly * r - lr * r * 0.7,
                   cx + lx * r + lr * r, cy + ly * r + lr * r * 0.7], fill=(110, 190, 110))
    d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340, fill=(255, 255, 255), width=3)
    # thermometer
    tx = x + w * 0.82
    d.rounded_rectangle([tx - 5, y + h * 0.18, tx + 5, y + h * 0.72], radius=5,
                        fill=(255, 255, 255), outline=(120, 120, 120))
    d.rectangle([tx - 3, y + h * 0.42, tx + 3, y + h * 0.70], fill=(220, 60, 50))
    d.ellipse([tx - 10, y + h * 0.68, tx + 10, y + h * 0.88], fill=(220, 60, 50),
              outline=(120, 120, 120))


def illo_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(246, 227, 224))
    # three flags: US, Mexico, Bolivia
    for i, kind in enumerate(("us", "mx", "bo")):
        px = x + w * (0.10 + i * 0.30)
        py = y + h * 0.08
        fw, fh = w * 0.24, h * 0.30
        flag_pole(d, px, py, h * 0.62)
        if kind == "us":
            flag_us(d, px + 2, py + 2, fw, fh)
        elif kind == "mx":
            d.rectangle([px + 2, py + 2, px + 2 + fw, py + 2 + fh], fill=(255, 255, 255),
                        outline=(120, 120, 120))
            d.rectangle([px + 2, py + 2, px + 2 + fw / 3, py + 2 + fh], fill=(0, 104, 71))
            d.rectangle([px + 2 + 2 * fw / 3, py + 2, px + 2 + fw, py + 2 + fh],
                        fill=(206, 17, 38))
            d.ellipse([px + 2 + fw / 2 - 3, py + 2 + fh / 2 - 3, px + 2 + fw / 2 + 3,
                       py + 2 + fh / 2 + 3], fill=(160, 120, 40))
        else:
            d.rectangle([px + 2, py + 2, px + 2 + fw, py + 2 + fh], fill=(255, 255, 255),
                        outline=(120, 120, 120))
            d.rectangle([px + 2, py + 2, px + 2 + fw, py + 2 + fh / 3], fill=(214, 0, 28))
            d.rectangle([px + 2, py + 2 + fh / 3, px + 2 + fw, py + 2 + 2 * fh / 3],
                        fill=(247, 209, 0))
            d.rectangle([px + 2, py + 2 + 2 * fh / 3, px + 2 + fw, py + 2 + fh],
                        fill=(0, 122, 61))
    # virus icons
    for vx, vy, r, c in ((0.24, 0.74, 9, (170, 70, 90)), (0.55, 0.80, 11, (120, 70, 150)),
                         (0.84, 0.72, 8, (170, 70, 90))):
        cx, cy = x + w * vx, y + h * vy
        for k in range(8):
            ang = k * 3.14159 / 4
            d.line([cx + r * 0.8 * _cos(ang), cy + r * 0.8 * _sin(ang),
                    cx + r * 1.35 * _cos(ang), cy + r * 1.35 * _sin(ang)],
                   fill=c, width=2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)


def illo_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 240, 226))
    ox, oy = x + w * 0.10, y + h * 0.86
    d.line([ox, y + h * 0.10, ox, oy], fill=(80, 80, 80), width=2)
    d.line([ox, oy, x + w * 0.92, oy], fill=(80, 80, 80), width=2)
    bars = [0.22, 0.38, 0.55, 0.78]
    bw = w * 0.14
    for i, bh in enumerate(bars):
        bx = ox + 6 + i * (bw + 6)
        top = oy - bh * h * 0.85
        col = (34, 139, 34) if i < 3 else (20, 90, 40)
        d.rectangle([bx, top, bx + bw, oy - 2], fill=col)
    # rising line over the bars
    pts = []
    for i, bh in enumerate(bars):
        pts.append((ox + 6 + i * (bw + 6) + bw / 2, oy - bh * h * 0.85 - 6))
    d.line(pts, fill=(200, 16, 46), width=3, joint="curve")
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(200, 16, 46))
    # chip icon
    cx, cy, s = x + w * 0.80, y + h * 0.20, 14
    d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], fill=(30, 40, 60))
    d.rectangle([cx - s / 4, cy - s / 4, cx + s / 4, cy + s / 4], fill=(90, 200, 120))
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        d.line([cx + dx * s / 2, cy + dy * s / 2, cx + dx * (s / 2 + 5),
                cy + dy * (s / 2 + 5)], fill=(30, 40, 60), width=2)


def illo_tents(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 231, 210))
    gy = y + h * 0.78
    d.rectangle([x, gy, x + w, y + h], fill=(214, 196, 150))
    # tents
    for tx, tw, c in ((0.06, 0.30, (196, 178, 140)), (0.38, 0.26, (150, 170, 190)),
                      (0.64, 0.28, (190, 160, 120))):
        bx = x + w * tx
        d.polygon([(bx, gy), (bx + tw * w / 2, gy - h * 0.42), (bx + tw * w, gy)],
                  fill=c, outline=(120, 110, 90))
        d.polygon([(bx + tw * w * 0.42, gy), (bx + tw * w / 2, gy - h * 0.16),
                   (bx + tw * w * 0.58, gy)], fill=(90, 80, 60))
    # aid truck
    tx, ty = x + w * 0.60, gy - h * 0.30
    d.rectangle([tx, ty, tx + w * 0.30, ty + h * 0.22], fill=(255, 255, 255),
                outline=(140, 140, 140))
    d.rectangle([tx + w * 0.30, ty + h * 0.06, tx + w * 0.38, ty + h * 0.22],
                fill=(200, 60, 60))
    for wx in (0.05, 0.24, 0.34):
        d.ellipse([tx + w * wx - 4, ty + h * 0.20 - 4, tx + w * wx + 4,
                   ty + h * 0.20 + 4], fill=(40, 40, 40))
    d.rectangle([tx + w * 0.11, ty + h * 0.05, tx + w * 0.15, ty + h * 0.17],
                fill=(200, 30, 40))
    d.rectangle([tx + w * 0.08, ty + h * 0.08, tx + w * 0.18, ty + h * 0.14],
                fill=(200, 30, 40))
    # pale sun
    d.ellipse([x + w * 0.84, y + h * 0.06, x + w * 0.84 + 16, y + h * 0.06 + 16],
              fill=(240, 200, 90))


def illo_palace(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(227, 232, 238))
    # government building
    bx, by, bw, bh = x + w * 0.10, y + h * 0.34, w * 0.80, h * 0.52
    d.rectangle([bx, by, bx + bw, by + bh], fill=(245, 240, 225), outline=(140, 130, 110))
    d.polygon([(bx - 4, by), (bx + bw / 2, by - h * 0.16), (bx + bw + 4, by)],
              fill=(120, 110, 95))
    d.ellipse([bx + bw / 2 - 8, by - h * 0.16 - 8, bx + bw / 2 + 8, by - h * 0.16 + 8],
              fill=(90, 120, 150))
    for i in range(4):
        cx = bx + bw * (0.16 + i * 0.23)
        d.rectangle([cx - 5, by + 4, cx + 5, by + bh - 8], fill=(255, 255, 255),
                    outline=(160, 150, 130))
    d.rectangle([bx + bw * 0.42, by + bh * 0.55, bx + bw * 0.58, by + bh - 8],
                fill=(90, 80, 60))
    d.rectangle([bx - 6, by + bh, bx + bw + 6, by + bh + 6], fill=(120, 110, 95))
    # flag: red-blue-red vertical
    fx = x + w * 0.86
    flag_pole(d, fx, y + h * 0.10, h * 0.30)
    d.rectangle([fx + 2, y + h * 0.10, fx + 2 + w * 0.09, y + h * 0.10 + h * 0.22],
                fill=(206, 17, 38))
    d.rectangle([fx + 2 + w * 0.03, y + h * 0.10, fx + 2 + w * 0.06,
                 y + h * 0.10 + h * 0.22], fill=(0, 57, 166))


def illo_seats(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 228, 240))
    cx, cy = x + w * 0.5, y + h * 0.92
    # three arcs of seats: teal = Student List 140, grey = SNS 103, amber = rest
    import math
    total = 0
    for arc_i, (r, n) in enumerate(((0.30, 9), (0.48, 13), (0.66, 17))):
        rr = r * h
        for k in range(n):
            ang = math.pi * (0.12 + 0.76 * k / max(n - 1, 1))
            px = cx - rr * math.cos(ang)
            py = cy - rr * math.sin(ang) * 0.82
            col = (0, 130, 120) if total < 22 else ((120, 120, 120) if total < 35 else (220, 160, 40))
            d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=col)
            total += 1
    # podium
    d.rectangle([cx - 12, cy - 14, cx + 12, cy - 2], fill=(120, 90, 60))
    d.rectangle([cx - 16, cy - 2, cx + 16, cy + 2], fill=(90, 70, 50))


def illo_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 235, 210))
    # factory with sawtooth roof
    bx, by, bw, bh = x + w * 0.06, y + h * 0.42, w * 0.56, h * 0.44
    d.rectangle([bx, by, bx + bw, by + bh], fill=(180, 175, 165), outline=(120, 115, 105))
    d.polygon([(bx, by), (bx + bw * 0.25, by - h * 0.16), (bx + bw * 0.25, by),
               (bx + bw * 0.5, by - h * 0.16), (bx + bw * 0.5, by),
               (bx + bw * 0.75, by - h * 0.16), (bx + bw * 0.75, by),
               (bx + bw, by - h * 0.16), (bx + bw, by)], fill=(140, 135, 125))
    d.rectangle([bx + bw * 0.78, by - h * 0.34, bx + bw * 0.86, by], fill=(150, 90, 70))
    for ox, oy, r in ((0.84, 0.10, 7), (0.88, 0.16, 9)):
        d.ellipse([x + w * ox - r, y + h * oy - r, x + w * ox + r, y + h * oy + r],
                  fill=(200, 200, 200))
    for wx in (0.12, 0.38, 0.64):
        d.rectangle([bx + bw * wx, by + bh * 0.25, bx + bw * (wx + 0.16),
                     by + bh * 0.55], fill=(120, 180, 210), outline=(110, 110, 110))
    # workers: small figures
    for i, wx in enumerate((0.68, 0.78, 0.88)):
        cx = x + w * wx
        cy = y + h * 0.72
        d.ellipse([cx - 5, cy - 16, cx + 5, cy - 6], fill=(232, 190, 150))
        d.polygon([(cx - 7, cy + 12), (cx + 7, cy + 12), (cx + 4, cy - 6),
                   (cx - 4, cy - 6)], fill=((52, 84, 150), (180, 90, 40), (60, 120, 70))[i])
    # tear-gas puffs
    for ox, oy, r, c in ((0.70, 0.30, 10, (210, 210, 205)), (0.80, 0.22, 12, (225, 225, 220)),
                         (0.90, 0.32, 9, (210, 210, 205))):
        d.ellipse([x + w * ox - r, y + h * oy - r, x + w * ox + r, y + h * oy + r], fill=c)


def illo_crash(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(223, 234, 242))
    gy = y + h * 0.72
    # mountains
    d.polygon([(x, gy), (x + w * 0.25, y + h * 0.18), (x + w * 0.50, gy)], fill=(190, 200, 210))
    d.polygon([(x + w * 0.20, gy), (x + w * 0.25, y + h * 0.18), (x + w * 0.30, gy)],
              fill=(255, 255, 255))
    d.polygon([(x + w * 0.42, gy), (x + w * 0.68, y + h * 0.30), (x + w * 0.94, gy)],
              fill=(170, 182, 194))
    d.polygon([(x + w * 0.62, gy), (x + w * 0.68, y + h * 0.30), (x + w * 0.74, gy)],
              fill=(255, 255, 255))
    d.rectangle([x, gy, x + w, y + h], fill=(240, 244, 248))
    # plane, nose-down
    cx, cy = x + w * 0.52, y + h * 0.52
    d.polygon([(cx - 26, cy - 4), (cx + 22, cy - 14), (cx + 30, cy - 8),
               (cx - 18, cy + 8)], fill=(60, 64, 70))
    d.polygon([(cx - 6, cy - 4), (cx + 2, cy - 22), (cx + 10, cy - 20), (cx + 4, cy - 2)],
              fill=(80, 84, 90))
    d.polygon([(cx - 14, cy + 4), (cx - 8, cy + 18), (cx - 2, cy + 16), (cx - 6, cy + 2)],
              fill=(80, 84, 90))
    # smoke + flame
    for ox, oy, r in ((-30, -18, 7), (-36, -28, 9), (-42, -38, 7)):
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=(140, 140, 140))
    d.polygon([(cx + 24, cy - 10), (cx + 30, cy - 20), (cx + 34, cy - 8)],
              fill=(230, 120, 40))


def illo_trial(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(237, 230, 218))
    # columns
    for cx in (x + w * 0.16, x + w * 0.84):
        d.rectangle([cx - 7, y + h * 0.22, cx + 7, y + h * 0.78], fill=(250, 248, 240),
                    outline=(170, 160, 140))
        d.rectangle([cx - 10, y + h * 0.18, cx + 10, y + h * 0.22], fill=(200, 190, 170))
        d.rectangle([cx - 10, y + h * 0.78, cx + 10, y + h * 0.82], fill=(200, 190, 170))
    # scales
    cx, cy = x + w * 0.5, y + h * 0.30
    d.line([cx, cy, cx, cy + h * 0.34], fill=(120, 100, 60), width=3)
    d.line([cx - w * 0.18, cy + h * 0.06, cx + w * 0.18, cy + h * 0.06],
           fill=(120, 100, 60), width=3)
    for ex in (-w * 0.18, w * 0.18):
        d.line([cx + ex, cy + h * 0.06, cx + ex, cy + h * 0.16], fill=(120, 100, 60), width=2)
        d.polygon([(cx + ex - 10, cy + h * 0.16), (cx + ex + 10, cy + h * 0.16),
                   (cx + ex, cy + h * 0.26)], fill=(180, 150, 90))
    d.ellipse([cx - 4, cy - 6, cx + 4, cy + 2], fill=(180, 150, 90))
    # gavel
    gx, gy = x + w * 0.5, y + h * 0.74
    d.rectangle([gx - 16, gy - 5, gx + 16, gy + 5], fill=(120, 80, 40))
    d.line([gx + 12, gy, gx + 30, gy - 12], fill=(100, 65, 30), width=4)
    d.rectangle([gx - 18, gy + 8, gx + 18, gy + 12], fill=(150, 120, 80))


ILLOS = {
    "bridge": illo_bridge, "gulf": illo_gulf, "quad": illo_quad,
    "clinic": illo_clinic, "globe": illo_globe, "flags": illo_flags,
    "chart": illo_chart, "tents": illo_tents, "palace": illo_palace,
    "seats": illo_seats, "factory": illo_factory, "crash": illo_crash,
    "trial": illo_trial,
}

# ------------------------------------------------------------- world map
# Simplified continent outlines in (lon, lat); equirectangular projection.
CONTINENTS = [
    # North America
    [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-135, 57), (-130, 54),
     (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20),
     (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9), (-80, 8),
     (-77, 7), (-75, 10), (-72, 11), (-68, 11), (-64, 10), (-61, 9),
     (-59, 8), (-55, 6), (-52, 5), (-54, 2), (-57, 6), (-60, 8),
     (-62, 11), (-65, 11), (-68, 12), (-70, 12), (-72, 11), (-75, 10),
     (-77, 8), (-80, 9), (-83, 10), (-86, 13), (-88, 15), (-90, 16),
     (-92, 16), (-95, 19), (-97, 22), (-97, 26), (-93, 30), (-90, 30),
     (-86, 30), (-84, 30), (-81, 25), (-80, 27), (-81, 31), (-76, 35),
     (-75, 38), (-74, 40), (-70, 42), (-68, 44), (-66, 45), (-60, 46),
     (-55, 47), (-53, 48), (-55, 52), (-60, 55), (-65, 58), (-68, 58),
     (-72, 62), (-78, 62), (-85, 66), (-90, 69), (-95, 69), (-110, 68),
     (-125, 70), (-140, 70), (-155, 71), (-165, 68)],
    # Greenland
    [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-25, 70),
     (-30, 74), (-40, 76), (-55, 76), (-60, 74), (-58, 70), (-55, 66)],
    # South America
    [(-77, 7), (-80, 3), (-81, -3), (-80, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
     (-66, -55), (-65, -50), (-62, -42), (-58, -35), (-52, -32), (-48, -27),
     (-42, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
     (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12),
     (-75, 11)],
    # Africa
    [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-5, 35), (0, 36),
     (10, 37), (11, 34), (20, 32), (25, 32), (30, 31), (32, 31),
     (35, 28), (37, 22), (39, 18), (43, 12), (48, 11), (51, 12),
     (48, 5), (44, 0), (40, -5), (40, -10), (36, -18), (33, -26),
     (28, -33), (20, -35), (16, -29), (14, -22), (12, -15), (9, -2),
     (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12)],
    # Eurasia
    [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50), (2, 51),
     (5, 53), (8, 55), (8, 57), (10, 59), (6, 60), (5, 62), (10, 64),
     (12, 66), (18, 69), (25, 71), (30, 70), (35, 68), (40, 68),
     (45, 68), (50, 69), (55, 70), (60, 70), (65, 71), (70, 72),
     (75, 73), (80, 73), (85, 74), (90, 75), (95, 76), (100, 77),
     (105, 77), (110, 74), (115, 73), (120, 73), (125, 72), (130, 71),
     (135, 71), (140, 72), (145, 72), (150, 70), (155, 69), (160, 68),
     (162, 66), (170, 66), (178, 65), (178, 62), (170, 60), (162, 58),
     (158, 52), (156, 50), (152, 55), (150, 59), (145, 59), (142, 54),
     (140, 50), (138, 46), (135, 43), (132, 43), (130, 42), (127, 40),
     (126, 38), (122, 38), (120, 35), (120, 31), (121, 28), (118, 25),
     (113, 22), (110, 20), (108, 18), (106, 10), (104, 9), (103, 7),
     (100, 7), (99, 10), (98, 14), (96, 16), (94, 18), (92, 21),
     (90, 22), (88, 22), (86, 20), (84, 18), (82, 16), (80, 13),
     (78, 8), (76, 10), (74, 15), (72, 20), (70, 21), (68, 23),
     (66, 25), (61, 25), (57, 26), (54, 26), (52, 27), (50, 29),
     (48, 30), (50, 26), (52, 25), (54, 24), (56, 26), (58, 24),
     (59, 22), (58, 20), (55, 17), (52, 15), (48, 14), (44, 13),
     (43, 12), (41, 15), (39, 20), (38, 24), (37, 27), (35, 29),
     (34, 31), (36, 36), (33, 36), (30, 36), (27, 37), (26, 39),
     (23, 36), (22, 37), (20, 39), (19, 42), (16, 40), (15, 44),
     (13, 45), (12, 44), (10, 44), (8, 44), (6, 43), (3, 43),
     (0, 39), (-1, 37), (-2, 37), (-6, 36)],
    # UK
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-3, 50)],
    # Japan
    [(129, 31), (131, 33), (133, 34), (136, 35), (139, 35), (140, 38),
     (141, 41), (143, 43), (145, 44), (142, 42), (140, 38), (137, 36),
     (134, 34), (131, 32)],
    # Borneo / Sumatra / New Guinea / Java / Philippines / NZ / Madagascar
    [(109, 1), (113, 4), (117, 2), (118, -2), (116, -4), (112, -3), (110, 0)],
    [(95, 5), (100, 0), (104, -3), (106, -5), (103, -4), (99, 1), (96, 4)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (147, -8), (141, -8),
     (136, -6), (132, -4)],
    [(105, -6), (110, -7), (114, -7), (114, -8), (108, -8), (105, -7)],
    [(120, 18), (122, 17), (122, 14), (121, 11), (120, 10), (121, 13),
     (120, 16)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (174, -41),
     (171, -43), (168, -46)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (46, -24), (44, -25),
     (43, -21), (44, -17)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
]


def draw_map(d, mx, my, mw, mh):
    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA)
    def px(lon):
        return mx + (lon + 180) / 360.0 * mw
    def py(lat):
        return my + (85 - lat) / 145.0 * mh
    for poly in CONTINENTS:
        pts = [(px(lon), py(lat)) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    # dots for briefs first, pins on top
    for n, _t, lon, lat, reg in BRIEFS:
        cx, cy = px(lon), py(lat)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=REGION[reg],
                  outline=(255, 255, 255))
    pin_font = font(SANS_BOLD, 10)
    # Small display nudges so the crowded Europe / Middle East pins do not
    # sit on top of each other (true locations unchanged in the data).
    NUDGE = {1: (9, -9), 2: (7, 7), 5: (-11, 5), 8: (4, 9), 10: (-9, -9)}
    for s in FEATURED:
        cx, cy = px(s["lon"]), py(s["lat"])
        dx, dy = NUDGE.get(s["n"], (0, 0))
        cx, cy = cx + dx, cy + dy
        r = 8.5
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=s["col"],
                  outline=(255, 255, 255), width=1)
        num = str(s["n"])
        tw = pin_font.getlength(num)
        d.text((cx - tw / 2, cy - 7), num, font=pin_font, fill=(255, 255, 255))
    d.rectangle([mx, my, mx + mw, my + mh], outline=(150, 140, 120))


# ---------------------------------------------------------------- layout
def draw_card(d, x, y, w, h, s, big):
    illo_h = 84 if big else 82
    ILLOS[s["illo"]](d, x, y, w, illo_h)
    d.rectangle([x, y, x + w, y + illo_h], outline=(200, 190, 170))
    cy = y + illo_h + 5
    cf = font(SANS_BOLD, 12 if big else 11)
    num = str(s["n"])
    d.text((x, cy), num, font=cf, fill=RED)
    d.text((x + cf.getlength(num + " "), cy),
           f"{s['cat']} \u00b7 {s['sub']}", font=cf, fill=s["col"])
    cy += 16 if big else 15
    hf = font(SERIF_BOLD, 22 if big else 17)
    lh = 25 if big else 20
    lines = wrap(s["head"], hf, w)[:3]
    cy = draw_lines(d, x, cy + 2, lines, hf, INK, lh)
    df = font(SANS, 13 if big else 12)
    dlh = 16 if big else 14
    dlines = wrap(s["deck"], df, w)[:2]
    draw_lines(d, x, cy + 3, dlines, df, SOFT, dlh)


def check_layout():
    """Print wrap counts so overflow is caught before publishing."""
    ok = True
    for s in FEATURED:
        big = s["n"] <= 3
        hf = font(SERIF_BOLD, 22 if big else 17)
        df = font(SANS, 13 if big else 12)
        w = 317 if big else 187
        hl = len(wrap(s["head"], hf, w))
        dl = len(wrap(s["deck"], df, w))
        flag = "" if hl <= 3 and dl <= 2 else "  <-- OVERFLOW"
        if flag:
            ok = False
        print(f"  #{s['n']:>2} head {hl} lines, deck {dl} lines{flag}")
    bf = font(SANS, 11)
    bfb = font(SANS_BOLD, 11)
    worst = 0
    for n, t, _lo, _la, _r in BRIEFS:
        wd = bfb.getlength(str(n) + " ") + bf.getlength(t)
        worst = max(worst, wd)
    print(f"  widest brief: {worst:.0f}px (column 292px)")
    return ok


def render(d):
    # ---- kicker
    kf = font(SANS_BOLD, 13)
    d.text((24, 14), "THE WORLD\u2019S NEWS IN ONE PICTURE", font=kf, fill=RED)
    kr = font(SANS_BOLD, 12)
    rt = "43 STORIES \u00b7 6 CONTINENTS \u00b7 ALL FROM TUESDAY"
    d.text((1000 - kr.getlength(rt), 15), rt, font=kr, fill=INK)
    d.rectangle([24, 38, 1000, 40], fill=INK)
    # ---- masthead
    mf = font(SERIF_DISPLAY, 56)
    d.text((24, 38), "Tuesday 17 November 2026", font=mf, fill=INK)
    d.rectangle([24, 112, 1000, 114], fill=INK)
    d.rectangle([24, 116, 1000, 117], fill=INK)
    # ---- featured rows
    row1_y, row1_h = 122, 222
    row2_y, row2_h = 352, 208
    row3_y, row3_h = 568, 208
    for i, s in enumerate(FEATURED[:3]):
        x = round(24 + i * (317.33 + 12))
        draw_card(d, x, row1_y, 317, row1_h, s, big=True)
    for row_y, group in ((row2_y, FEATURED[3:8]), (row3_y, FEATURED[8:13])):
        for i, s in enumerate(group):
            x = round(24 + i * (187.2 + 10))
            draw_card(d, x, row_y, 187, row2_h, s, big=False)
    for hy in (348, 564, 780):
        d.line([24, hy, 1000, hy], fill=HAIR, width=1)
    # ---- bottom band headers
    hf = font(SANS_BOLD, 13)
    d.text((24, 786), "WHERE IT HAPPENED", font=hf, fill=INK)
    d.text((404, 786), "ALSO ON TUESDAY 17 NOVEMBER", font=hf, fill=INK)
    d.line([24, 804, 392, 804], fill=INK, width=1)
    d.line([404, 804, 1000, 804], fill=INK, width=1)
    # ---- map + legend
    draw_map(d, 24, 810, 368, 164)
    lf = font(SANS, 10)
    lx, ly = 24, 978
    for name, reg in LEGEND:
        d.rectangle([lx, ly + 1, lx + 8, ly + 9], fill=REGION[reg])
        lx += 12
        d.text((lx, ly), name, font=lf, fill=SOFT)
        lx += lf.getlength(name) + 12
        if name == "Asia":
            lx, ly = 24, ly + 12
    # ---- briefs, two columns; shrink font if any line is too wide
    size = 11
    while size > 9:
        bf, bfb = font(SANS, size), font(SANS_BOLD, size)
        if all(bfb.getlength(str(n) + " ") + bf.getlength(t) <= 292
               for n, t, _lo, _la, _r in BRIEFS):
            break
        size -= 1
    bf, bfb = font(SANS, size), font(SANS_BOLD, size)
    lh = size + 2
    for col, group in enumerate((BRIEFS[:15], BRIEFS[15:])):
        bx = 404 + col * 304
        for i, (n, t, _lo, _la, _r) in enumerate(group):
            by = 810 + i * lh
            d.text((bx, by), str(n), font=bfb, fill=RED)
            d.text((bx + bfb.getlength(str(n) + " "), by), t, font=bf, fill=INK)
    # ---- footer
    ff = font(SANS, 10)
    ft = ("Every story here happened or was first reported on Tuesday 17 November 2026. "
          "Contested claims are marked as claims.   Sources: Reuters, AP, AFP, BBC, "
          "Al Jazeera, WHO, UN. Original drawings.")
    d.text(((1024 - ff.getlength(ft)) / 2, 1006), ft, font=ff, fill=SOFT)


def main():
    print("layout check:")
    check_layout()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    render(d)
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    size = os.path.getsize(out)
    print(f"entry.png: {size} bytes (limit 1048576)")
    if size > 1048576:
        img.convert("RGB").save(out, "JPEG", quality=85)
        print(f"over limit; re-saved as JPEG: {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
