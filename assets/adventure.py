#!/usr/bin/env python3
"""Generate assets/adventure.svg: a looping top-down pixel-art adventure scene.

A hero walks along a forest trail, cuts a bush that blocks the way and opens
a chest holding the "legendary code". Everything is original pixel art drawn
as SVG paths with CSS animations (GitHub READMEs do not run JavaScript).

Run:  python assets/adventure.py
"""
import math
import random
import unicodedata
from pathlib import Path

OUT = Path(__file__).with_suffix(".svg")
W, H = 800, 264
S = 3            # size of one sprite pixel
T = 12           # loop length in seconds
PATH_Y0, PATH_Y1 = 140, 212

# --------------------------------------------------------------------------
# 5x7 pixel font (dialog box)
# --------------------------------------------------------------------------
_FONT_SRC = r"""
A .###. #...# #...# ##### #...# #...# #...#
B ####. #...# #...# ####. #...# #...# ####.
C .###. #...# #.... #.... #.... #...# .###.
D ####. #...# #...# #...# #...# #...# ####.
E ##### #.... #.... ####. #.... #.... #####
F ##### #.... #.... ####. #.... #.... #....
G .###. #...# #.... #.### #...# #...# .####
H #...# #...# #...# ##### #...# #...# #...#
I .###. ..#.. ..#.. ..#.. ..#.. ..#.. .###.
J ..### ...#. ...#. ...#. #..#. #..#. .##..
K #...# #..#. #.#.. ##... #.#.. #..#. #...#
L #.... #.... #.... #.... #.... #.... #####
M #...# ##.## #.#.# #.#.# #...# #...# #...#
N #...# #...# ##..# #.#.# #..## #...# #...#
O .###. #...# #...# #...# #...# #...# .###.
P ####. #...# #...# ####. #.... #.... #....
Q .###. #...# #...# #...# #.#.# #..#. .##.#
R ####. #...# #...# ####. #.#.. #..#. #...#
S .#### #.... #.... .###. ....# ....# ####.
T ##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..
U #...# #...# #...# #...# #...# #...# .###.
V #...# #...# #...# #...# #...# .#.#. ..#..
W #...# #...# #...# #.#.# #.#.# #.#.# .#.#.
X #...# #...# .#.#. ..#.. .#.#. #...# #...#
Y #...# #...# .#.#. ..#.. ..#.. ..#.. ..#..
Z ##### ....# ...#. ..#.. .#... #.... #####
0 .###. #...# #..## #.#.# ##..# #...# .###.
1 ..#.. .##.. ..#.. ..#.. ..#.. ..#.. .###.
+ ..... ..#.. ..#.. ##### ..#.. ..#.. .....
! ..#.. ..#.. ..#.. ..#.. ..#.. ..... ..#..
< ...#. ..#.. .#... #.... .#... ..#.. ...#.
> .#... ..#.. ...#. ....# ...#. ..#.. .#...
/ ....# ...#. ...#. ..#.. .#... .#... #....
. ..... ..... ..... ..... ..... .##.. .##..
"""
FONT = {" ": ["....."] * 7}
for _line in _FONT_SRC.strip().splitlines():
    _ch, *_rows = _line.split()
    assert len(_rows) == 7 and all(len(r) == 5 for r in _rows), _line
    FONT[_ch] = _rows

# --------------------------------------------------------------------------
# Hand-drawn sprites ("." is transparent)
# --------------------------------------------------------------------------
HERO_TOP = [
    ".....KKKKK......",
    "....KHHHHHK.....",
    "...KHhhHHHHK....",
    "...KHHHHHHSK....",
    "...KHHHHSSEK....",
    "...KHHHSSSSK....",
    "....KHSSSsK.....",
    "...RKRRRRRRK....",
    "..RRKTTTTTTK....",
    "....KTTTTTSK....",
    "....KtTTTTSK....",
    "....KttttttK....",
]
HERO_LEGS = {
    "stand": ["....KBBKKBBK....", "....KBK..KBK....", "...KBBK..KBBK...", "...KKKK..KKKK..."],
    "walkA": ["....KBBKKBBK....", "...KBK....KBK...", "..KBBK....KBBK..", "..KKKK....KKKK.."],
    "walkB": ["....KBBKKBBK....", ".....KBBBBK.....", ".....KBBBBK.....", ".....KKKKKK....."],
}
HERO_PAL = {"K": "#1a1c2c", "H": "#4a2c1d", "h": "#7a4a2e", "S": "#f2c095", "s": "#d48a62",
            "E": "#1a1c2c", "R": "#e8613c", "T": "#2c7a7b", "t": "#1d5556", "B": "#5a3a22"}

SWORD = [
    "..KKKKKKK.",
    "YKWWWWWWWK",
    "..KKKKKKK.",
]
SWORD_PAL = {"K": "#1a1c2c", "Y": "#facc15", "W": "#e5e7eb"}

CHEST_CLOSED = [
    "..KKKKKKKKKKKK..",
    ".KbbbbbbbbbbbbK.",
    "KbbBbbbbbbbbBbbK",
    "KBBBBBBBBBBBBBBK",
    "KYYYYYYKKYYYYYYK",
    "KBBBBBKLLKBBBBBK",
    "KbbbbbKLLKbbbbbK",
    "KBBBBBBKKBBBBBBK",
    "KbbbbbbbbbbbbbbK",
    "KBBBBBBBBBBBBBBK",
    "KYYYYYYYYYYYYYYK",
    "KBBBBBBBBBBBBBBK",
    "KKKKKKKKKKKKKKKK",
]
CHEST_OPEN = [
    "..KKKKKKKKKKKK..",
    ".KbbbbbbbbbbbbK.",
    "KBBBBBBBBBBBBBBK",
    "KYYYYYYYYYYYYYYK",
    "KKKKKKKKKKKKKKKK",
    "KDDDDDDDDDDDDDDK",
    "KDGGGGGGGGGGGGDK",
    "KBBBBBBBBBBBBBBK",
    "KbbbbbbbbbbbbbbK",
    "KBBBBBBBBBBBBBBK",
    "KYYYYYYYYYYYYYYK",
    "KBBBBBBBBBBBBBBK",
    "KKKKKKKKKKKKKKKK",
]
CHEST_PAL = {"K": "#2a1a12", "B": "#a0522d", "b": "#c97a40", "Y": "#facc15", "L": "#fde047",
             "D": "#1a0f0a", "G": "#fde68a"}

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
CODE_PAL = {"Y": "#facc15", "d": "#1e1b4b", "C": "#22d3ee"}

FLOWER = [".P.", "PYP", ".P."]
SPARK = [".W.", "WWW", ".W."]
BFLY_OPEN = ["P.P", "PKP", ".K."]
BFLY_SHUT = [".P.", ".K.", ".K."]


def disc(size, cx, cy, r, hl, dark_cut, texture=11):
    """Round top-down canopy/bush: outline K, highlight L, shade D, body G."""
    rows = []
    for y in range(size[1]):
        row = ""
        for x in range(size[0]):
            px, py = x + 0.5, y + 0.5
            d = math.hypot(px - cx, py - cy)
            if d > r:
                row += "."
            elif d > r - 1.2:
                row += "K"
            elif math.hypot(px - hl[0], py - hl[1]) < hl[2]:
                row += "L"
            elif (px - cx) + (py - cy) > dark_cut or (x * 7 + y * 13) % texture == 0:
                row += "D"
            else:
                row += "G"
        rows.append(row)
    return rows


def tree():
    rows = [list(r) for r in disc((24, 24), 12, 10, 10.5, (8.5, 6.5, 3.8), 6)]
    for y in range(19, 24):
        for x in range(10, 14):
            if rows[y][x] == ".":
                rows[y][x] = "K" if x in (10, 13) or y == 23 else "W"
    return ["".join(r) for r in rows]


TREE = tree()
TREE_PAL = {"K": "#12301a", "G": "#2f7d32", "D": "#1f5a24", "L": "#4caf50", "W": "#6b4423"}
BUSH = disc((16, 16), 8, 8, 7.5, (5.8, 5.2, 2.4), 4, texture=7)
BUSH_PAL = {"K": "#24501c", "G": "#6abf4b", "D": "#4a9a35", "L": "#9be07a"}
ROCK = disc((12, 10), 6, 5.2, 5, (4.2, 3.4, 1.8), 2.5, texture=97)
ROCK_PAL = {"K": "#374151", "G": "#9ca3af", "D": "#6b7280", "L": "#d1d5db"}


def _check():
    sprites = [HERO_TOP + v for v in HERO_LEGS.values()] + [SWORD, CHEST_CLOSED, CHEST_OPEN, CODE_ITEM]
    for rows in sprites:
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
    paths = {}
    for x, y, n, c in runs(rows):
        paths.setdefault(c, []).append(f"M{ox + x * s} {oy + y * s}h{n * s}v{s}h-{n * s}z")
    return "".join(f'<path fill="{pal[c]}" d="{"".join(d)}"/>' for c, d in paths.items())


def text(s, x, y, scale, fill):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).upper()
    d = []
    for i, ch in enumerate(s):
        for px, py, n, _ in runs(FONT.get(ch, FONT[" "])):
            gx = x + i * 6 * scale
            d.append(f"M{gx + px * scale} {y + py * scale}h{n * scale}v{scale}h-{n * scale}z")
    return f'<path fill="{fill}" d="{"".join(d)}"/>'


def text_width(s, scale):
    return len(s) * 6 * scale - scale


def kf(name, *frames):
    return "@keyframes %s{%s}" % (name, "".join("%s{%s}" % f for f in frames))


def at(x, y):
    return f"transform:translate({x}px,{y}px)"


# --------------------------------------------------------------------------
# Scene
# --------------------------------------------------------------------------


def build():
    rnd = random.Random(2024)
    css, bg, mid, fx = [], [], [], []

    # grass with a faint tile checker
    bg.append(f'<rect width="{W}" height="{H}" fill="#5cab43"/>')
    for ty in range(0, H, 48):
        for tx in range(0, W, 48):
            if (tx // 48 + ty // 48) % 2:
                bg.append(f'<rect x="{tx}" y="{ty}" width="48" height="48" fill="#62b249"/>')

    # pond
    px0, py0, px1, py1 = 300, 18, 528, 114
    for inset, color in ((0, "#e6d3a3"), (6, "#3b82c4"), (18, "#2f6aa5")):
        x0, y0, x1, y1 = px0 + inset, py0 + inset, px1 - inset, py1 - inset
        bg.append(f'<rect x="{x0 + 9}" y="{y0}" width="{x1 - x0 - 18}" height="{y1 - y0}" fill="{color}"/>')
        bg.append(f'<rect x="{x0 + 3}" y="{y0 + 3}" width="{x1 - x0 - 6}" height="{y1 - y0 - 6}" fill="{color}"/>')
        bg.append(f'<rect x="{x0}" y="{y0 + 9}" width="{x1 - x0}" height="{y1 - y0 - 18}" fill="{color}"/>')
    for i, (rx, ry) in enumerate([(330, 44), (420, 36), (470, 70), (352, 84), (440, 92), (390, 62)]):
        bg.append(f'<rect class="rip" style="animation-delay:-{i * 0.4:.1f}s" x="{rx}" y="{ry}" '
                  f'width="18" height="3" fill="#a5d8ff"/>')
    css.append(".rip{animation:rip 1.2s steps(1) infinite}" + kf("rip", ("50%", "transform:translateX(6px)")))
    for lx, ly in ((488, 46), (342, 60)):
        bg.append(f'<rect x="{lx}" y="{ly}" width="15" height="9" fill="#3f8a2c"/>'
                  f'<rect x="{lx + 3}" y="{ly - 3}" width="9" height="15" fill="#3f8a2c"/>'
                  f'<rect x="{lx + 6}" y="{ly + 3}" width="3" height="3" fill="#f9a8d4"/>')

    # trail
    bg.append(f'<rect x="0" y="{PATH_Y0}" width="{W}" height="{PATH_Y1 - PATH_Y0}" fill="#d3ac72"/>')
    bg.append(f'<rect x="0" y="{PATH_Y0}" width="{W}" height="6" fill="#b48a52"/>')
    bg.append(f'<rect x="0" y="{PATH_Y1 - 3}" width="{W}" height="3" fill="#e2c08c"/>')
    for x in range(0, W, 24):
        bg.append(f'<rect x="{x + rnd.randrange(0, 9, 3)}" y="{PATH_Y0 - 3}" width="9" height="6" fill="#5cab43"/>')
        bg.append(f'<rect x="{x + rnd.randrange(0, 9, 3)}" y="{PATH_Y1 - 3}" width="9" height="6" fill="#5cab43"/>')
    for _ in range(40):
        x, y = rnd.randrange(0, W, 3), rnd.randrange(PATH_Y0 + 12, PATH_Y1 - 9, 3)
        bg.append(f'<rect x="{x}" y="{y}" width="3" height="3" fill="#a88454"/>')

    def free(x, y, w, h):
        if not (y + h < PATH_Y0 - 6 or y > PATH_Y1 + 3):
            return False
        return not (x + w > px0 - 6 and x < px1 + 6 and y < py1 + 6)

    # grass tufts
    for _ in range(140):
        x, y = rnd.randrange(0, W, 3), rnd.randrange(0, H, 3)
        if free(x, y, 9, 6):
            bg.append(f'<path fill="#3f8a2c" d="M{x} {y}h3v3h-3zM{x + 6} {y}h3v3h-3zM{x + 3} {y + 3}h3v3h-3z"/>')

    # flowers (some sway)
    colors = ["#f87171", "#ffffff", "#c084fc", "#fde047"]
    placed = 0
    while placed < 22:
        x, y = rnd.randrange(0, W, 3), rnd.randrange(0, H, 3)
        if not free(x, y, 9, 9):
            continue
        pal = {"P": rnd.choice(colors), "Y": "#facc15" if placed % 2 else "#fb923c"}
        cls = f' class="sway" style="animation-delay:-{rnd.random() * 1.4:.2f}s"' if placed % 3 == 0 else ""
        mid.append(f"<g{cls}>{sprite(FLOWER, pal, x, y)}</g>")
        placed += 1
    css.append(".sway{animation:sway 1.4s steps(1) infinite}" + kf("sway", ("50%", "transform:translateX(3px)")))

    # rocks
    for x, y in ((200, 222), (560, 118), (36, 120), (742, 226)):
        mid.append(f'<rect x="{x + 3}" y="{y + 24}" width="30" height="6" fill="#000" opacity=".18"/>')
        mid.append(sprite(ROCK, ROCK_PAL, x, y))

    # trees (top and bottom edges, drawn last so they sit on top)
    for x, y in ((-18, -30), (48, -12), (120, -36), (196, -14), (250, 40), (560, -26), (628, -8),
                 (700, -32), (760, 10), (-10, 52), (680, 54), (-24, 214), (50, 226), (608, 222),
                 (690, 210), (760, 230), (128, 236)):
        mid.append(f'<rect x="{x + 12}" y="{y + 66}" width="48" height="8" fill="#000" opacity=".2"/>')
        mid.append(sprite(TREE, TREE_PAL, x, y))

    # bush blocking the trail (cut by the hero)
    bush_x, bush_y = 402, 150
    mid.append(f'<g class="bush">{sprite(BUSH, BUSH_PAL, bush_x, bush_y)}</g>')
    css.append(".bush{animation:bush %ds steps(1) infinite}" % T +
               kf("bush", ("0%", "opacity:1"), ("32.5%", "opacity:0"), ("100%", "opacity:0")))
    bcx, bcy = bush_x + 24, bush_y + 24
    for i in range(8):
        ang = i * math.pi / 4 + 0.3
        ex, ey = round(bcx + math.cos(ang) * 46), round(bcy + math.sin(ang) * 34)
        color = ["#6abf4b", "#9be07a", "#4a9a35"][i % 3]
        fx.append(f'<rect class="lf{i}" x="-3" y="-3" width="6" height="6" fill="{color}"/>')
        css.append(f".lf{i}{{opacity:0;animation:lf{i} {T}s linear infinite}}" +
                   kf(f"lf{i}", ("0%,32.5%", at(bcx, bcy) + ";opacity:0"), ("33%", "opacity:1"),
                      ("40%", at(ex, ey) + ";opacity:1"), ("41%,100%", at(ex, ey) + ";opacity:0")))

    # chest + treasure
    cx, cy = 660, 158
    mid.append(f'<rect x="{cx + 3}" y="{cy + 36}" width="42" height="6" fill="#000" opacity=".2"/>')
    mid.append(f'<g class="chc">{sprite(CHEST_CLOSED, CHEST_PAL, cx, cy)}</g>')
    mid.append(f'<g class="cho">{sprite(CHEST_OPEN, CHEST_PAL, cx, cy)}</g>')
    css.append(f".chc{{animation:chc {T}s steps(1) infinite}}" +
               kf("chc", ("0%", "opacity:1"), ("62%", "opacity:0"), ("100%", "opacity:0")) +
               f".cho{{opacity:0;animation:cho {T}s steps(1) infinite}}" +
               kf("cho", ("0%", "opacity:0"), ("62%", "opacity:1"), ("100%", "opacity:1")))

    ix = cx
    rays = "".join(f'<path fill="#fde68a" opacity=".35" d="M{ix + 18 + dx} {cy + 18}l-{w} -96h{2 * w + 6}l-{w} 96z"/>'
                   for dx, w in ((-12, 12), (6, 6), (18, 15)))
    fx.append(f'<g class="rays"><g class="pulse">{rays}</g></g>')
    css.append(f".rays{{opacity:0;animation:rays {T}s steps(1) infinite}}" +
               kf("rays", ("0%", "opacity:0"), ("62.5%", "opacity:1"), ("100%", "opacity:1")) +
               ".pulse{animation:pulse .5s steps(1) infinite}" + kf("pulse", ("50%", "opacity:.45")))
    fx.append(f'<g class="item"><g class="float">{sprite(CODE_ITEM, CODE_PAL, 0, 0)}</g></g>')
    css.append(f".item{{opacity:0;animation:item {T}s ease-out infinite}}" +
               kf("item", ("0%,62%", at(ix, cy + 6) + ";opacity:0"), ("62.5%", "opacity:1"),
                  ("70%,100%", at(ix, cy - 66) + ";opacity:1")) +
               ".float{animation:float .9s ease-in-out infinite alternate}" +
               kf("float", ("to", "transform:translateY(-5px)")))
    for i, (sx, sy) in enumerate(((ix - 18, cy - 78), (ix + 54, cy - 72), (ix - 9, cy - 30), (ix + 51, cy - 36))):
        fx.append(f'<g class="sp"><g class="tw" style="animation-delay:-{i * 0.2:.1f}s">'
                  f'{sprite(SPARK, {"W": "#ffffff"}, sx, sy)}</g></g>')
    css.append(f".sp{{opacity:0;animation:sp {T}s steps(1) infinite}}" +
               kf("sp", ("0%", "opacity:0"), ("66%", "opacity:1"), ("100%", "opacity:1")) +
               ".tw{animation:tw .8s steps(1) infinite}" + kf("tw", ("50%", "opacity:0")))

    # hero
    legs_y = len(HERO_TOP) * S
    stand = sprite(HERO_TOP + HERO_LEGS["stand"], HERO_PAL, 0, 0)
    wa = sprite(HERO_TOP + HERO_LEGS["walkA"], HERO_PAL, 0, 0)
    wb = sprite(HERO_TOP + HERO_LEGS["walkB"], HERO_PAL, 0, 0)
    sword = sprite(SWORD, SWORD_PAL, 30, 24)
    arc = "".join(f'<rect x="{round(18 + math.cos(a) * 33) - 3}" y="{round(24 + math.sin(a) * 33) - 3}" '
                  f'width="6" height="6" fill="#ffffff"/>'
                  for a in [math.radians(d) for d in range(-70, 71, 14)])
    hero = (f'<rect x="9" y="{legs_y + 9}" width="30" height="6" fill="#000" opacity=".22"/>'
            f'<g class="walk"><g class="wa">{wa}</g><g class="wb">{wb}</g></g>'
            f'<g class="stand">{stand}</g>'
            f'<g class="atk">{sword}</g><g class="arc" opacity=".85">{arc}</g>')
    mid.append(f'<g class="hero">{hero}</g>')
    hy = 150
    css.append(f".hero{{animation:hero {T}s linear infinite}}" +
               kf("hero", ("0%,3%", at(-48, hy)), ("30%,35%", at(352, hy)), ("58%,100%", at(612, hy))) +
               f".walk{{animation:walk {T}s steps(1) infinite}}" +
               kf("walk", ("0%", "opacity:0"), ("3%", "opacity:1"), ("30%", "opacity:0"), ("35%", "opacity:1"),
                  ("58%", "opacity:0"), ("100%", "opacity:0")) +
               f".stand{{animation:stand {T}s steps(1) infinite}}" +
               kf("stand", ("0%", "opacity:1"), ("3%", "opacity:0"), ("30%", "opacity:1"), ("35%", "opacity:0"),
                  ("58%", "opacity:1"), ("100%", "opacity:1")) +
               ".wa{animation:wa .36s steps(1) infinite}" + kf("wa", ("50%", "opacity:0")) +
               ".wb{opacity:0;animation:wb .36s steps(1) infinite}" + kf("wb", ("50%", "opacity:1")) +
               f".atk{{opacity:0;animation:atk {T}s steps(1) infinite}}" +
               kf("atk", ("0%", "opacity:0"), ("30.5%", "opacity:1"), ("34%", "opacity:0"), ("100%", "opacity:0")) +
               f".arc{{visibility:hidden;animation:arc {T}s steps(1) infinite}}" +
               kf("arc", ("0%", "visibility:hidden"), ("31.5%", "visibility:visible"),
                  ("33.5%", "visibility:hidden"), ("100%", "visibility:hidden")))

    # butterfly
    fx.append(f'<g class="bf"><g class="bo">{sprite(BFLY_OPEN, {"P": "#f9a8d4", "K": "#1a1c2c"}, 0, 0)}</g>'
              f'<g class="bs">{sprite(BFLY_SHUT, {"P": "#f9a8d4", "K": "#1a1c2c"}, 0, 0)}</g></g>')
    css.append(f".bf{{animation:bf {T}s linear infinite}}" +
               kf("bf", ("0%", at(-20, 96)), ("20%", at(160, 60)), ("40%", at(290, 120)), ("60%", at(560, 70)),
                  ("80%", at(720, 110)), ("100%", at(830, 60))) +
               ".bo{animation:wa .3s steps(1) infinite}.bs{opacity:0;animation:wb .3s steps(1) infinite}")

    # dialog box with typewriter reveal
    msg = "VOCE ENCONTROU O CODIGO LENDARIO!"
    tw = text_width(msg, 2)
    bx0, by0, bw, bh = 140, 214, 520, 44
    tx, ty = (W - tw) // 2, by0 + 15
    dialog = (f'<rect x="{bx0 - 3}" y="{by0 - 3}" width="{bw + 6}" height="{bh + 6}" fill="#0b1220"/>'
              f'<rect x="{bx0}" y="{by0}" width="{bw}" height="{bh}" fill="#f8fafc"/>'
              f'<rect x="{bx0 + 3}" y="{by0 + 3}" width="{bw - 6}" height="{bh - 6}" fill="#1e1b4b"/>'
              f'<g mask="url(#reveal)">{text(msg, tx, ty, 2, "#f8fafc")}</g>'
              f'<path class="arrow" fill="#facc15" d="M{bx0 + bw - 21} {by0 + bh - 12}h9v3h-3v3h-3v-3h-3z"/>')
    fx.append(f'<g class="dialog">{dialog}</g>')
    css.append(f".dialog{{opacity:0;animation:dialog {T}s steps(1) infinite}}" +
               kf("dialog", ("0%", "opacity:0"), ("68%", "opacity:1"), ("100%", "opacity:1")) +
               f".reveal{{transform-box:fill-box;transform-origin:left center;animation:reveal {T}s infinite}}" +
               kf("reveal", ("0%,68%", "transform:scaleX(0);animation-timing-function:steps(%d)" % len(msg)),
                  ("80%,100%", "transform:scaleX(1)")) +
               ".arrow{animation:tw .8s steps(1) infinite}")
    defs = (f'<mask id="reveal"><rect class="reveal" x="{tx - 2}" y="{ty - 2}" width="{tw + 4}" '
            f'height="20" fill="#fff"/></mask>')

    # fade in / out between loops
    fx.append(f'<rect class="fade" width="{W}" height="{H}" fill="#000"/>')
    css.append(f".fade{{animation:fade {T}s linear infinite}}" +
               kf("fade", ("0%", "opacity:1"), ("3%", "opacity:0"), ("94%", "opacity:0"), ("100%", "opacity:1")))

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        'shape-rendering="crispEdges" role="img" '
        'aria-label="A pixel-art hero walks a forest trail, cuts a bush and opens a chest with the legendary code">'
        '<title>Pixel adventure</title>'
        f'<style>{"".join(css)}</style><defs>{defs}</defs>'
        f'{"".join(bg)}{"".join(mid)}{"".join(fx)}'
        '</svg>\n'
    )


if __name__ == "__main__":
    svg = build()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg)} bytes)")
