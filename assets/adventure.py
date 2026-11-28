#!/usr/bin/env python3
"""Generate assets/adventure.svg: an HD-2D style pixel-art adventure loop.

Crisp pixel-art sprites live inside a layered "diorama" with depth of field
(blurred background and foreground), golden-hour lighting, god rays, bloom,
long shadows, floating dust and falling leaves. The hero walks a forest trail,
cuts a bush and opens a chest holding the legendary code.

Everything is original art drawn as SVG with CSS animations, because GitHub
READMEs do not run JavaScript.

Run:  python assets/adventure.py
"""
import math
import random
import unicodedata
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).with_suffix(".svg")
W, H = 800, 320
S = 3                  # size of one sprite pixel in the mid plane
T = 12                 # loop length in seconds
PATH_Y0, PATH_Y1 = 224, 280
FEET = 266
SUN = (716, 22)

# --------------------------------------------------------------------------
# 5x7 pixel font (dialog box)
# --------------------------------------------------------------------------
_FONT_SRC = r"""
A .###. #...# #...# ##### #...# #...# #...#
C .###. #...# #.... #.... #.... #...# .###.
D ####. #...# #...# #...# #...# #...# ####.
E ##### #.... #.... ####. #.... #.... #####
G .###. #...# #.... #.### #...# #...# .####
I .###. ..#.. ..#.. ..#.. ..#.. ..#.. .###.
L #.... #.... #.... #.... #.... #.... #####
N #...# #...# ##..# #.#.# #..## #...# #...#
O .###. #...# #...# #...# #...# #...# .###.
R ####. #...# #...# ####. #.#.. #..#. #...#
T ##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..
U #...# #...# #...# #...# #...# #...# .###.
V #...# #...# #...# #...# #...# .#.#. ..#..
! ..#.. ..#.. ..#.. ..#.. ..#.. ..... ..#..
"""
FONT = {" ": ["....."] * 7}
for _line in _FONT_SRC.strip().splitlines():
    _ch, *_rows = _line.split()
    assert len(_rows) == 7 and all(len(r) == 5 for r in _rows), _line
    FONT[_ch] = _rows

# --------------------------------------------------------------------------
# Hand-drawn sprites ("." is transparent). Light comes from the upper right.
# --------------------------------------------------------------------------
HERO_TOP = [
    "......KKKKK.........",
    ".....KHhhjjK........",
    "....KHHhhhjjK.......",
    "...KHHHHhhhjjK......",
    "...KHHHHHHhSSK......",
    "...KHHHHHSSSEK......",
    "...KHHHHsSSSSK......",
    "....KHHsSSSSK.......",
    "....KKsssssK........",
    "..RRKqqqqqqK........",
    ".RRrKuTTTTTuK.......",
    ".RrrKtTTTTTuSK......",
    "RRrrKtTTTTTuSK......",
    "RrrrKLLLYLLLK.......",
    "Rrrr.KtTTTTuK.......",
    ".rrr.KtTTTTuK.......",
    "..rr.KPPPPPpK.......",
    ".....KPPKKPPK.......",
]
HERO_LEGS = {
    "stand": [".....KPpK.KPpK......", ".....KBBK.KBBK......",
              "....KBBbK.KBBbK.....", "....KKKKK.KKKKK....."],
    "walkA": ["....KPpK...KPpK.....", "...KBBK.....KBBK....",
              "..KBBbK.....KBBbK...", "..KKKKK.....KKKKK..."],
    "walkB": ["......KPPPpK........", "......KBBBBK........",
              ".....KBBBBbK........", ".....KKKKKKK........"],
}
HERO_PAL = {"K": "#1b1424", "H": "#3d2418", "h": "#6b3d24", "j": "#a8653a", "S": "#f0b98d",
            "s": "#c98764", "E": "#1b1424", "R": "#b83a2e", "r": "#7d2520", "q": "#e0674a",
            "T": "#2f6f73", "t": "#1f4c50", "u": "#5aa8a4", "L": "#6b4226", "Y": "#e9b949",
            "P": "#3b3346", "p": "#5a5068", "B": "#5a3a22", "b": "#8a5a32"}

SWORD = [
    "..KKKKKKKKKKK.",
    "YKWWWWWWWWWWWK",
    "..KKKKKKKKKKK.",
]
SWORD_PAL = {"K": "#1b1424", "Y": "#e9b949", "W": "#eef2f7"}

CHEST_CLOSED = [
    "..KKKKKKKKKKKK..",
    ".KbbbbbbbbbbbhK.",
    "KbbBbbbbbbbbBhhK",
    "KBBBBBBBBBBBBBbK",
    "KYYYYYYKKYYYYYyK",
    "KBBBBBKLLKBBBBbK",
    "KbbbbbKLLKbbbbhK",
    "KBBBBBBKKBBBBBbK",
    "KbbbbbbbbbbbbbhK",
    "KBBBBBBBBBBBBBbK",
    "KYYYYYYYYYYYYYyK",
    "KBBBBBBBBBBBBBbK",
    "KKKKKKKKKKKKKKKK",
]
CHEST_OPEN = [
    "..KKKKKKKKKKKK..",
    ".KbbbbbbbbbbbhK.",
    "KBBBBBBBBBBBBBbK",
    "KYYYYYYYYYYYYYyK",
    "KKKKKKKKKKKKKKKK",
    "KDDDDDDDDDDDDDDK",
    "KDGGGGGGGGGGGGDK",
    "KBBBBBBBBBBBBBbK",
    "KbbbbbbbbbbbbbhK",
    "KBBBBBBBBBBBBBbK",
    "KYYYYYYYYYYYYYyK",
    "KBBBBBBBBBBBBBbK",
    "KKKKKKKKKKKKKKKK",
]
CHEST_PAL = {"K": "#2a1a12", "B": "#8e4a26", "b": "#b8693a", "h": "#e39a5c", "Y": "#d9a530",
             "y": "#ffe08a", "L": "#fde047", "D": "#1a0f0a", "G": "#fff1b0"}

CODE_ITEM = [
    "..YYYYYYYYYYYY..",
    ".YddddddddddddY.",
    "YddddddddddddddY",
    "YdddCddddCdCdddY",
    "YddCddddCdddCddY",
    "YdCdddddCddddCdY",
    "YdCddddCdddddCdY",
    "YddCdddCddddCddY",
    "YdddCdCddddCdddY",
    "YddddddddddddddY",
    ".YddddddddddddY.",
    "..YYYYYYYYYYYY..",
]
CODE_PAL = {"Y": "#ffd24a", "d": "#1e1b4b", "C": "#5eead4"}

FLOWER = [".P.", "PYP", ".P."]
SPARK = ["..W..", "..W..", "WWWWW", "..W..", "..W.."]
LEAF = ["..LL", "LLLl", "Ll.."]

# --------------------------------------------------------------------------
# Procedural lit sprites (trees, bushes, rocks)
# --------------------------------------------------------------------------
_L = (0.62, -0.55, 0.56)
_LN = math.sqrt(sum(c * c for c in _L))
LIGHT = tuple(c / _LN for c in _L)


def _noise(x, y, seed):
    n = (x * 374761393 + y * 668265263 + seed * 1442695041) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 0xFFFF - 0.5


def lit_blobs(w, h, blobs, seed, noise=0.28, grain=2):
    """Union of spheres lit from the upper right; levels 1..5, K for shadowed rims."""
    light = [[None] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            px, py = x + 0.5, y + 0.5
            best = None
            for cx, cy, r in blobs:
                d = math.hypot(px - cx, py - cy) / r
                if d <= 1 and (best is None or d < best[0]):
                    best = (d, cx, cy, r)
            if best:
                _, cx, cy, r = best
                nx, ny = (px - cx) / r, (py - cy) / r
                nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
                lam = max(0.0, nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2])
                light[y][x] = 0.12 + 0.88 * lam + noise * _noise(x // grain, y // grain, seed)
    rows = []
    for y in range(h):
        row = ""
        for x in range(w):
            b = light[y][x]
            if b is None:
                row += "."
                continue
            edge = any(not (0 <= x + dx < w and 0 <= y + dy < h) or light[y + dy][x + dx] is None
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge:
                row += "K" if b < 0.62 else "3"
            else:
                row += "12345"[min(4, max(0, int(b * 5)))]
        rows.append(row)
    return rows


def make_tree(seed):
    rnd = random.Random(seed)
    w, ch, th = 36, 30, 14
    blobs = [(18, 16, 12.5)]
    for _ in range(5):
        r = rnd.uniform(6.5, 9.5)
        blobs.append((rnd.uniform(r, w - r), rnd.uniform(r, ch - r - 1), r))
    rows = [list(r) for r in lit_blobs(w, ch, blobs, seed)]
    rows += [list("." * w) for _ in range(th)]
    total = ch + th
    for y in range(ch - 6, total):
        x0, x1 = (14, 21) if y >= total - 2 else (15, 20)
        for x in range(x0, x1 + 1):
            if rows[y][x] != ".":
                continue
            if x in (x0, x1) or y == total - 1:
                rows[y][x] = "K"
            elif x == x1 - 1:
                rows[y][x] = "e"
            elif x == x0 + 1 or _noise(x, y, seed) > 0.3:
                rows[y][x] = "a"
            else:
                rows[y][x] = "c"
    return ["".join(r) for r in rows]


def blend(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(a, b))


LEAF_PAL = {"K": "#14261a", "1": "#1e3b22", "2": "#2c5a2b", "3": "#3f7f35", "4": "#6ea846",
            "5": "#c4dc6e", "a": "#3a2416", "c": "#5e3b22", "e": "#9a6a3a"}
BACK_PAL = {k: blend(v, "#e9c294", 0.5) for k, v in LEAF_PAL.items()}
BUSH = lit_blobs(20, 17, [(10, 9, 8.5), (5.5, 10.5, 5.5), (14.5, 10.5, 5.5)], seed=7, noise=0.24)
BUSH_PAL = {"K": "#1c3a18", "1": "#2d5a24", "2": "#3f7d31", "3": "#5aa03f", "4": "#8cc85c", "5": "#d4ef92"}
ROCK = lit_blobs(14, 10, [(7, 7, 7)], seed=3, noise=0.12)
ROCK_PAL = {"K": "#3a3440", "1": "#4f4856", "2": "#6b6370", "3": "#8d8590", "4": "#b5aca8", "5": "#e6d9c4"}
FOLIAGE = lit_blobs(34, 24, [(12, 10, 11), (24, 8, 9), (8, 18, 7), (22, 17, 8)], seed=11, noise=0.3)
FOLIAGE_PAL = {k: blend(v, "#0b1a10", 0.45) for k, v in LEAF_PAL.items()}


def _check():
    for rows in [HERO_TOP + v for v in HERO_LEGS.values()] + [SWORD, CHEST_CLOSED, CHEST_OPEN, CODE_ITEM]:
        assert all(len(r) == len(rows[0]) for r in rows), rows


_check()

# --------------------------------------------------------------------------
# Drawing helpers
# --------------------------------------------------------------------------


def runs(rows):
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            c = row[x]
            if c == ".":
                x += 1
                continue
            start = x
            while x < len(row) and row[x] == c:
                x += 1
            yield start, y, x - start, c


def sprite(rows, pal, ox, oy, s=S):
    paths = defaultdict(list)
    for x, y, n, c in runs(rows):
        paths[c].append(f"M{ox + x * s} {oy + y * s}h{n * s}v{s}h-{n * s}z")
    return "".join(f'<path fill="{pal[c]}" d="{"".join(d)}"/>' for c, d in paths.items())


class Pixels:
    """Accumulates loose pixels by colour so scattered detail stays one path per colour."""

    def __init__(self):
        self.paths = defaultdict(list)

    def rect(self, x, y, w, h, color):
        self.paths[color].append(f"M{x} {y}h{w}v{h}h-{w}z")

    def svg(self):
        return "".join(f'<path fill="{c}" d="{"".join(d)}"/>' for c, d in self.paths.items())


def text(s, x, y, scale, fill):
    d = []
    for i, ch in enumerate(s):
        for px, py, n, _ in runs(FONT.get(ch, FONT[" "])):
            gx = x + i * 6 * scale
            d.append(f"M{gx + px * scale} {y + py * scale}h{n * scale}v{scale}h-{n * scale}z")
    return f'<path fill="{fill}" d="{"".join(d)}"/>'


def kf(name, *frames):
    return "@keyframes %s{%s}" % (name, "".join("%s{%s}" % f for f in frames))


def at(x, y):
    return f"transform:translate({x}px,{y}px)"


def blur(name, sd, pad=20):
    return (f'<filter id="{name}" x="-{pad}%" y="-{pad}%" width="{100 + 2 * pad}%" height="{100 + 2 * pad}%" '
            f'color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="{sd}"/></filter>')


# --------------------------------------------------------------------------
# Scene
# --------------------------------------------------------------------------


def defs():
    return (
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#e48a52"/><stop offset=".45" stop-color="#f5c27f"/>'
        '<stop offset=".8" stop-color="#fde2ad"/><stop offset="1" stop-color="#fff0cf"/></linearGradient>'
        '<radialGradient id="sun"><stop offset="0" stop-color="#fffbe8"/>'
        '<stop offset=".14" stop-color="#fff1c2" stop-opacity=".95"/>'
        '<stop offset=".45" stop-color="#ffd38a" stop-opacity=".42"/>'
        '<stop offset="1" stop-color="#ffb060" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="haze" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#ffe3b3" stop-opacity="0"/>'
        '<stop offset=".65" stop-color="#ffe3b3" stop-opacity=".6"/>'
        '<stop offset="1" stop-color="#ffe3b3" stop-opacity=".15"/></linearGradient>'
        '<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#c2b56c"/><stop offset=".22" stop-color="#93ab4e"/>'
        '<stop offset=".6" stop-color="#5f9136"/><stop offset="1" stop-color="#3b6a26"/></linearGradient>'
        '<linearGradient id="trail" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#9c7448"/><stop offset=".2" stop-color="#c39762"/>'
        '<stop offset=".6" stop-color="#dcb277"/><stop offset="1" stop-color="#c2955c"/></linearGradient>'
        '<linearGradient id="ray" x1="1" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#fff4d6" stop-opacity=".6"/>'
        '<stop offset="1" stop-color="#fff4d6" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="burst" x1="0" y1="1" x2="0" y2="0">'
        '<stop offset="0" stop-color="#fff6c8" stop-opacity=".85"/>'
        '<stop offset="1" stop-color="#fff6c8" stop-opacity="0"/></linearGradient>'
        '<radialGradient id="glow"><stop offset="0" stop-color="#fff8dc"/>'
        '<stop offset=".4" stop-color="#ffe9a8" stop-opacity=".55"/>'
        '<stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="mote"><stop offset="0" stop-color="#fffbe6"/>'
        '<stop offset=".45" stop-color="#fff0b8" stop-opacity=".7"/>'
        '<stop offset="1" stop-color="#ffe08a" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="bokeh"><stop offset="0" stop-color="#fff5d8" stop-opacity=".55"/>'
        '<stop offset=".75" stop-color="#ffe6b0" stop-opacity=".28"/>'
        '<stop offset="1" stop-color="#ffe6b0" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="shade"><stop offset="0" stop-color="#1b1f33" stop-opacity=".6"/>'
        '<stop offset="1" stop-color="#1b1f33" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="vig" cx=".56" cy=".4" r=".78">'
        '<stop offset=".55" stop-color="#1a0d24" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#1a0d24" stop-opacity=".72"/></radialGradient>'
        '<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#2a2048" stop-opacity=".94"/>'
        '<stop offset="1" stop-color="#151026" stop-opacity=".94"/></linearGradient>'
        + blur("fFar", 2.6) + blur("fBack", 1.1) + blur("fSoft", 3) + blur("fFg", 3.4)
        + blur("fFg2", 6, pad=40) + blur("fBloom", 5, pad=40)
    )


def ridge(rnd, base, lo, hi, step, color):
    y = rnd.uniform(lo, hi)
    pts = [f"0 {base}"]
    for x in range(0, W + step, step):
        y = min(hi, max(lo, y + rnd.uniform(-9, 9)))
        pts.append(f"{x} {round(y)}")
    pts.append(f"{W} {base}")
    return f'<polygon fill="{color}" points="{" ".join(pts)}"/>'


def tufts(rnd, px, n, y0, y1, scale_of, avoid):
    for _ in range(n):
        x, y = rnd.randrange(-6, W), rnd.randrange(y0, y1)
        if any(a0 <= y <= a1 for a0, a1 in avoid):
            continue
        s = scale_of(y)
        dark = rnd.choice(["#2f5a22", "#376828", "#3f7230"])
        lit = rnd.choice(["#8fbf52", "#a9cf62", "#c8dd78"])
        px.rect(x, y, s, s, dark)
        px.rect(x + 2 * s, y, s, s, lit)
        px.rect(x + s, y + s, s, s, dark)


def build():
    rnd = random.Random(2025)
    css = []
    L = []  # layers in paint order

    # sky, sun, distant ridges with atmospheric haze
    L.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    L.append(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="250" fill="url(#sun)"/>')
    L.append('<g filter="url(#fFar)">'
             + ridge(rnd, 170, 84, 112, 16, "#d8a487")
             + ridge(rnd, 170, 104, 134, 12, "#b98a72") + "</g>")
    L.append(f'<rect y="40" width="{W}" height="130" fill="url(#haze)"/>')

    # ground plane
    L.append(f'<rect y="136" width="{W}" height="{H - 136}" fill="url(#ground)"/>')
    far = Pixels()
    tufts(rnd, far, 160, 140, 186, lambda y: 2, [])
    L.append(f'<g filter="url(#fBack)" opacity=".8">{far.svg()}</g>')

    # back tree line (small, hazy, slightly out of focus)
    back = []
    for i, x in enumerate(range(-40, W + 40, 62)):
        base = 160 + rnd.randrange(-6, 8)
        tree = make_tree(100 + i)
        back.append(sprite(tree, BACK_PAL, x + rnd.randrange(-14, 14), base - len(tree) * 2, 2))
    L.append(f'<g filter="url(#fBack)">{"".join(back)}</g>')
    L.append(f'<rect y="70" width="{W}" height="110" fill="url(#haze)" opacity=".45"/>')

    # warm sun patches on the grass
    patches = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#ffe7a0"/>'
                      for cx, cy, rx, ry in ((520, 196, 130, 18), (300, 206, 90, 12), (690, 300, 120, 22),
                                             (420, 298, 90, 14), (150, 200, 70, 10)))
    L.append(f'<g filter="url(#fSoft)" opacity=".45" style="mix-blend-mode:screen">{patches}</g>')

    # mid-ground grass detail (in focus)
    mid = Pixels()
    tufts(rnd, mid, 520, 186, 320, lambda y: 2 if y < 214 else 3,
          [(PATH_Y0 - 8, PATH_Y1 + 2)])
    L.append(f'<g shape-rendering="crispEdges">{mid.svg()}</g>')

    # mid trees with long golden-hour shadows (sun upper right -> shadows fall down-left)
    trees = [(-46, 214, 1), (70, 204, 2), (236, 198, 3), (516, 200, 4), (726, 212, 5)]
    shadows = "".join(f'<polygon points="{x + 40} {b} {x + 70} {b} {x - 70} {b + 30} {x - 120} {b + 22}"/>'
                      for x, b, _ in trees)
    L.append(f'<g fill="#1b2433" opacity=".3" filter="url(#fSoft)">{shadows}</g>')
    for x, b, seed in trees:
        tree = make_tree(seed)
        L.append(f'<ellipse cx="{x + 54}" cy="{b - 2}" rx="34" ry="7" fill="url(#shade)"/>')
        L.append(f'<g shape-rendering="crispEdges">{sprite(tree, LEAF_PAL, x, b - len(tree) * S)}</g>')

    # trail
    L.append(f'<rect y="{PATH_Y0}" width="{W}" height="{PATH_Y1 - PATH_Y0}" fill="url(#trail)"/>')
    trail = Pixels()
    for x in range(-6, W, 12):
        trail.rect(x + rnd.randrange(0, 6, 3), PATH_Y0 - 3, 9, 6, rnd.choice(["#4e8a2f", "#5a9636"]))
        trail.rect(x + rnd.randrange(0, 6, 3), PATH_Y1 - 3, 9, 6, rnd.choice(["#3f7a28", "#4b852d"]))
    for x in range(0, W, 30):
        if rnd.random() < 0.7:
            trail.rect(x, 242, rnd.randrange(12, 24, 3), 3, "#b88a55")
        if rnd.random() < 0.7:
            trail.rect(x + 9, 262, rnd.randrange(12, 24, 3), 3, "#b88a55")
    for _ in range(60):
        x, y = rnd.randrange(0, W, 3), rnd.randrange(PATH_Y0 + 9, PATH_Y1 - 9, 3)
        trail.rect(x, y, 3, 3, "#a77e4c")
        trail.rect(x + 3, y - 3, 3, 3, "#f0d6a4")
    L.append(f'<g shape-rendering="crispEdges">{trail.svg()}</g>')

    # rocks and flowers
    for x, y in ((170, 288), (548, 206), (360, 204)):
        L.append(f'<ellipse cx="{x + 20}" cy="{y + 28}" rx="24" ry="5" fill="url(#shade)"/>')
        L.append(f'<g shape-rendering="crispEdges">{sprite(ROCK, ROCK_PAL, x, y)}</g>')
    flowers = []
    for i in range(26):
        y = rnd.choice([rnd.randrange(188, 216), rnd.randrange(284, 304)])
        x = rnd.randrange(0, W)
        s = 2 if y < 220 else 3
        pal = {"P": rnd.choice(["#f87171", "#fff7ed", "#c084fc", "#fde047", "#fb923c"]),
               "Y": "#facc15" if i % 2 else "#f97316"}
        cls = f' class="sway" style="animation-delay:-{rnd.random() * 1.6:.2f}s"' if i % 3 == 0 else ""
        flowers.append(f"<g{cls}>{sprite(FLOWER, pal, x, y, s)}</g>")
    L.append(f'<g shape-rendering="crispEdges">{"".join(flowers)}</g>')
    css.append(".sway{animation:sway 1.6s steps(1) infinite}" + kf("sway", ("50%", "transform:translateX(2px)")))

    # bush blocking the trail
    bush_x, bush_y = 412, FEET - 2 - len(BUSH) * S
    L.append(f'<g class="bush"><ellipse cx="{bush_x + 30}" cy="{FEET}" rx="34" ry="6" fill="url(#shade)"/>'
             f'<polygon fill="#1b2433" opacity=".3" filter="url(#fSoft)" points="{bush_x + 30} {FEET} '
             f'{bush_x + 60} {FEET} {bush_x - 30} {FEET + 14} {bush_x - 60} {FEET + 10}"/>'
             f'<g shape-rendering="crispEdges">{sprite(BUSH, BUSH_PAL, bush_x, bush_y)}</g></g>')
    css.append(f".bush{{animation:bush {T}s steps(1) infinite}}" +
               kf("bush", ("0%", "opacity:1"), ("32.5%", "opacity:0"), ("100%", "opacity:0")))

    # chest
    cx, cy = 672, FEET - 2 - len(CHEST_CLOSED) * S
    L.append(f'<ellipse cx="{cx + 24}" cy="{FEET}" rx="30" ry="6" fill="url(#shade)"/>'
             f'<polygon fill="#1b2433" opacity=".3" filter="url(#fSoft)" points="{cx + 20} {FEET} {cx + 48} {FEET} '
             f'{cx - 40} {FEET + 14} {cx - 70} {FEET + 10}"/>')
    L.append(f'<g shape-rendering="crispEdges"><g class="chc">{sprite(CHEST_CLOSED, CHEST_PAL, cx, cy)}</g>'
             f'<g class="cho">{sprite(CHEST_OPEN, CHEST_PAL, cx, cy)}</g></g>')
    css.append(f".chc{{animation:chc {T}s steps(1) infinite}}" +
               kf("chc", ("0%", "opacity:1"), ("62%", "opacity:0"), ("100%", "opacity:0")) +
               f".cho{{opacity:0;animation:cho {T}s steps(1) infinite}}" +
               kf("cho", ("0%", "opacity:0"), ("62%", "opacity:1"), ("100%", "opacity:1")))

    # hero
    hero_rows = len(HERO_TOP) + 4
    hy = FEET - hero_rows * S
    frames = {k: sprite(HERO_TOP + v, HERO_PAL, 0, 0) for k, v in HERO_LEGS.items()}
    sword = sprite(SWORD, SWORD_PAL, 54, 33)
    arc_pts = [math.radians(d) for d in range(-75, 76, 10)]
    arc = "".join(f'<rect x="{round(36 + math.cos(a) * 42) - 3}" y="{round(36 + math.sin(a) * 42) - 3}" '
                  f'width="6" height="6"/>' for a in arc_pts)
    foot = hero_rows * S
    hero = (f'<ellipse cx="30" cy="{foot}" rx="24" ry="5" fill="url(#shade)"/>'
            f'<polygon fill="#1b2433" opacity=".3" filter="url(#fSoft)" points="18 {foot} 44 {foot} '
            f'-50 {foot + 14} -80 {foot + 10}"/>'
            '<g shape-rendering="crispEdges">'
            f'<g class="walk"><g class="wa">{frames["walkA"]}</g><g class="wb">{frames["walkB"]}</g></g>'
            f'<g class="stand">{frames["stand"]}</g><g class="atk">{sword}</g></g>'
            f'<g class="arc"><g fill="#fff6d8" filter="url(#fBloom)">{arc}</g>'
            f'<g fill="#ffffff" shape-rendering="crispEdges">{arc}</g></g>')
    L.append(f'<g class="hero">{hero}</g>')
    css.append(f".hero{{animation:hero {T}s linear infinite}}" +
               kf("hero", ("0%,3%", at(-80, hy)), ("30%,35%", at(344, hy)), ("58%,100%", at(606, hy))) +
               f".walk{{animation:walk {T}s steps(1) infinite}}" +
               kf("walk", ("0%", "opacity:0"), ("3%", "opacity:1"), ("30%", "opacity:0"), ("35%", "opacity:1"),
                  ("58%", "opacity:0"), ("100%", "opacity:0")) +
               f".stand{{animation:stand {T}s steps(1) infinite}}" +
               kf("stand", ("0%", "opacity:1"), ("3%", "opacity:0"), ("30%", "opacity:1"), ("35%", "opacity:0"),
                  ("58%", "opacity:1"), ("100%", "opacity:1")) +
               ".wa{animation:wa .4s steps(1) infinite}" + kf("wa", ("50%", "opacity:0")) +
               ".wb{opacity:0;animation:wb .4s steps(1) infinite}" + kf("wb", ("50%", "opacity:1")) +
               f".atk{{opacity:0;animation:atk {T}s steps(1) infinite}}" +
               kf("atk", ("0%", "opacity:0"), ("30.5%", "opacity:1"), ("34%", "opacity:0"), ("100%", "opacity:0")) +
               f".arc{{opacity:0;animation:arc {T}s linear infinite}}" +
               kf("arc", ("0%,31.2%", "opacity:0"), ("31.6%", "opacity:1"), ("33.6%,100%", "opacity:0")))

    # leaves bursting out of the cut bush
    bcx, bcy = bush_x + 30, bush_y + 24
    for i in range(12):
        ang = -math.pi / 2 + (i - 5.5) * 0.28
        dx, peak = round(math.cos(ang) * rnd.uniform(40, 80)), round(rnd.uniform(26, 56))
        land = FEET - rnd.randrange(0, 20)
        color = ["#5aa03f", "#8cc85c", "#3f7d31", "#d4ef92"][i % 4]
        L.append(f'<rect class="lf{i}" x="-3" y="-3" width="6" height="6" fill="{color}"/>')
        css.append(f".lf{i}{{opacity:0;animation:lf{i} {T}s linear infinite}}" +
                   kf(f"lf{i}", ("0%,32.5%", at(bcx, bcy) + ";opacity:0;animation-timing-function:ease-out"),
                      ("33%", "opacity:1"),
                      ("36%", at(bcx + dx * 0.6, bcy - peak) + ";animation-timing-function:ease-in"),
                      ("41%", at(bcx + dx, land) + ";opacity:1"), ("45%,100%", at(bcx + dx, land) + ";opacity:0")))

    # treasure: light burst, bloom, rising item, sparkles
    ccx = cx + 24
    beams = "".join(f'<polygon points="{ccx - 10} {cy + 12} {ccx + 10} {cy + 12} {ccx + dx + w} {cy - 140} '
                    f'{ccx + dx - w} {cy - 140}"/>' for dx, w in ((-60, 16), (-18, 10), (24, 14), (64, 18)))
    L.append(f'<g class="burst" style="mix-blend-mode:screen">'
             f'<circle cx="{ccx}" cy="{cy - 30}" r="120" fill="url(#glow)" class="pulse"/>'
             f'<g fill="url(#burst)" filter="url(#fBloom)">{beams}</g></g>')
    css.append(f".burst{{opacity:0;animation:burst {T}s linear infinite}}" +
               kf("burst", ("0%,62%", "opacity:0"), ("63%", "opacity:1"), ("92%", "opacity:1"),
                  ("97%,100%", "opacity:0")) +
               ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 1.6s ease-in-out infinite alternate}" +
               kf("pulse", ("to", "transform:scale(1.15);opacity:.75")))
    item = sprite(CODE_ITEM, CODE_PAL, 0, 0)
    L.append(f'<g class="item"><g class="float"><circle cx="24" cy="18" r="34" fill="url(#glow)"/>'
             f'<g shape-rendering="crispEdges">{item}</g></g></g>')
    css.append(f".item{{opacity:0;animation:item {T}s ease-out infinite}}" +
               kf("item", ("0%,62%", at(cx, cy + 6) + ";opacity:0"), ("62.5%", "opacity:1"),
                  ("70%,100%", at(cx, cy - 82) + ";opacity:1")) +
               ".float{animation:float 1s ease-in-out infinite alternate}" +
               kf("float", ("to", "transform:translateY(-6px)")))
    sparks = []
    for i, (sx, sy) in enumerate(((cx - 22, cy - 100), (cx + 58, cy - 92), (cx - 12, cy - 46), (cx + 62, cy - 54),
                                  (cx + 22, cy - 116))):
        sparks.append(f'<g class="tw" style="animation-delay:-{i * 0.17:.2f}s">'
                      f'{sprite(SPARK, {"W": "#fffbe6"}, sx, sy, 2)}</g>')
    L.append(f'<g class="sp" shape-rendering="crispEdges">{"".join(sparks)}</g>')
    css.append(f".sp{{opacity:0;animation:sp {T}s steps(1) infinite}}" +
               kf("sp", ("0%", "opacity:0"), ("65%", "opacity:1"), ("100%", "opacity:1")) +
               ".tw{animation:tw .85s steps(1) infinite}" + kf("tw", ("50%", "opacity:0")))
    L.append(f'<rect class="flash" width="{W}" height="{H}" fill="#fff8e0"/>')
    css.append(f".flash{{opacity:0;animation:flash {T}s linear infinite}}" +
               kf("flash", ("0%,62%", "opacity:0"), ("62.6%", "opacity:.55"), ("66%,100%", "opacity:0")))

    # god rays + sun bloom on top of the scene
    rays = []
    for i, (top, spread, width) in enumerate(((640, 520, 46), (700, 470, 30), (760, 600, 60), (820, 420, 40),
                                              (590, 360, 24))):
        x2 = top - spread
        rays.append(f'<polygon class="ray" style="animation-delay:-{i * 1.3:.1f}s" fill="url(#ray)" '
                    f'points="{top} -10 {top + width * 0.4} -10 {x2 + width} {H + 10} {x2} {H + 10}"/>')
    L.append(f'<g style="mix-blend-mode:screen" filter="url(#fSoft)">{"".join(rays)}</g>')
    css.append(".ray{animation:ray 6s ease-in-out infinite alternate}" + kf("ray", ("0%", "opacity:.35"),
                                                                            ("100%", "opacity:.85")))
    L.append(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="150" fill="url(#sun)" opacity=".55" '
             'style="mix-blend-mode:screen"/>')

    # floating dust motes in the light
    motes = []
    for i in range(34):
        x, y = rnd.randrange(260, W), rnd.randrange(10, 300)
        r = rnd.uniform(1.4, 3.2)
        motes.append(f'<g class="m{i % 3}" style="animation-duration:{rnd.uniform(6, 11):.1f}s;'
                     f'animation-delay:-{rnd.uniform(0, 10):.1f}s"><circle cx="{x}" cy="{y}" r="{r:.1f}" '
                     'fill="url(#mote)"/></g>')
    L.append("".join(motes))
    for k, (dx, dy) in enumerate(((14, -18), (-12, -14), (18, 10))):
        css.append(f".m{k}{{animation:m{k} 8s ease-in-out infinite}}" +
                   kf(f"m{k}", ("0%,100%", "transform:translate(0,0);opacity:.25"),
                      ("50%", f"transform:translate({dx}px,{dy}px);opacity:1")))

    # falling leaves
    for i in range(6):
        x0 = rnd.randrange(160, W + 120)
        pal = {"L": rnd.choice(["#e8a33c", "#d9772f", "#9cc65a", "#f2c14e"]), "l": "#8a4b1f"}
        dur = rnd.uniform(8, 12)
        L.append(f'<g class="fall" style="animation-duration:{dur:.1f}s;animation-delay:-{rnd.uniform(0, dur):.1f}s;'
                 f'--x0:{x0}px"><g class="swing" style="animation-delay:-{rnd.uniform(0, 1.8):.1f}s">'
                 f'<g shape-rendering="crispEdges">{sprite(LEAF, pal, 0, 0)}</g></g></g>')
    css.append(".fall{animation:fall 10s linear infinite}" +
               kf("fall", ("0%", "transform:translate(var(--x0),-20px)"),
                  ("100%", "transform:translate(calc(var(--x0) - 220px),340px)")) +
               ".swing{animation:swing 1.8s ease-in-out infinite alternate}" +
               kf("swing", ("0%", "transform:translateX(-12px)"), ("100%", "transform:translateX(12px)")))

    # foreground: out-of-focus grass, bokeh and a branch framing the top-left corner
    blades = []
    for x in range(-24, W + 24, 7):
        edge = x < 140 or x > 660
        h = rnd.randint(26, 92) if edge else rnd.randint(12, 40)
        w = rnd.randint(5, 10)
        lean = rnd.randint(-14, 14)
        color = rnd.choice(["#16301a", "#1f3f1f", "#2a5226", "#3a6b2c"])
        blades.append(f'<path fill="{color}" d="M{x} {H + 4}L{x + lean + w / 2:.0f} {H + 4 - h}L{x + w} {H + 4}Z"/>')
    L.append(f'<g filter="url(#fFg)">{"".join(blades)}</g>')
    bokeh = "".join(f'<circle class="bk" style="animation-delay:-{i * 1.7:.1f}s" cx="{x}" cy="{y}" r="{r}" '
                    f'fill="url(#bokeh)"/>'
                    for i, (x, y, r) in enumerate(((90, 286, 16), (210, 304, 11), (610, 296, 20),
                                                   (740, 270, 13), (520, 312, 9), (40, 120, 22), (330, 18, 14))))
    L.append(f'<g style="mix-blend-mode:screen" filter="url(#fSoft)">{bokeh}</g>')
    css.append(".bk{animation:bk 7s ease-in-out infinite alternate}" +
               kf("bk", ("to", "transform:translate(6px,-5px)")))
    L.append(f'<g filter="url(#fFg2)">{sprite(FOLIAGE, FOLIAGE_PAL, -70, -66, 6)}</g>')

    # colour grade + vignette
    L.append(f'<rect width="{W}" height="{H}" fill="#ff9442" opacity=".32" style="mix-blend-mode:soft-light"/>')
    L.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')

    # dialog panel with typewriter reveal
    msg = "VOCE ENCONTROU O CODIGO LENDARIO!"
    tw = len(msg) * 12 - 2
    bx0, by0, bw, bh = 150, 14, 500, 46
    tx, ty = (W - tw) // 2, by0 + 16
    dialog = (f'<rect x="{bx0}" y="{by0}" width="{bw}" height="{bh}" rx="6" fill="url(#panel)" '
              f'stroke="#e9c46a" stroke-width="2"/>'
              f'<rect x="{bx0 + 5}" y="{by0 + 5}" width="{bw - 10}" height="{bh - 10}" rx="3" fill="none" '
              f'stroke="#e9c46a" stroke-opacity=".35"/>'
              f'<g mask="url(#reveal)" shape-rendering="crispEdges">{text(msg, tx + 2, ty + 2, 2, "#0b0716")}'
              f'{text(msg, tx, ty, 2, "#fff7e6")}</g>'
              f'<path class="arrow" fill="#e9c46a" d="M{bx0 + bw - 22} {by0 + bh - 14}h10l-5 6z"/>')
    L.append(f'<g class="dialog">{dialog}</g>')
    css.append(f".dialog{{opacity:0;animation:dialog {T}s linear infinite}}" +
               kf("dialog", ("0%,67%", "opacity:0"), ("68%,92%", "opacity:1"), ("94%,100%", "opacity:0")) +
               f".reveal{{transform-box:fill-box;transform-origin:left center;animation:reveal {T}s infinite}}" +
               kf("reveal", ("0%,68%", "transform:scaleX(0);animation-timing-function:steps(%d)" % len(msg)),
                  ("80%,100%", "transform:scaleX(1)")) +
               ".arrow{animation:tw .85s steps(1) infinite}")
    mask = (f'<mask id="reveal"><rect class="reveal" x="{tx - 2}" y="{ty - 2}" width="{tw + 6}" '
            f'height="20" fill="#fff"/></mask>')

    # fade between loops
    L.append(f'<rect class="fade" width="{W}" height="{H}" fill="#0b0716"/>')
    css.append(f".fade{{animation:fade {T}s linear infinite}}" +
               kf("fade", ("0%", "opacity:1"), ("3%", "opacity:0"), ("95%", "opacity:0"), ("100%", "opacity:1")))

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        'aria-label="HD-2D style pixel adventure: a hero walks a sunlit forest trail, cuts a bush and opens a '
        'chest with the legendary code">'
        '<title>Pixel adventure</title>'
        f'<style>{"".join(css)}</style><defs>{defs()}{mask}</defs>'
        f'{"".join(L)}'
        '</svg>\n'
    )


if __name__ == "__main__":
    svg = build()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg) // 1024} KB)")
