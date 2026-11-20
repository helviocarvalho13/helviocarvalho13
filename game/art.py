"""Pixel art for the README boss battle: battle scene, loading screen and buttons.

Everything is drawn as plain SVG paths with CSS animations: GitHub strips
JavaScript from READMEs, but it still animates SVG images.
"""
import random
import unicodedata

# --------------------------------------------------------------------------
# 5x7 pixel font
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
2 .###. #...# ....# ...#. ..#.. .#... #####
3 ####. ....# ....# .###. ....# ....# ####.
4 ...#. ..##. .#.#. #..#. ##### ...#. ...#.
5 ##### #.... ####. ....# ....# #...# .###.
6 .###. #.... #.... ####. #...# #...# .###.
7 ##### ....# ...#. ..#.. .#... .#... .#...
8 .###. #...# #...# .###. #...# #...# .###.
9 .###. #...# #...# .#### ....# ....# .###.
- ..... ..... ..... ##### ..... ..... .....
+ ..... ..#.. ..#.. ##### ..#.. ..#.. .....
/ ....# ...#. ...#. ..#.. .#... .#... #....
: ..... ..#.. ..#.. ..... ..#.. ..#.. .....
! ..#.. ..#.. ..#.. ..#.. ..#.. ..... ..#..
? .###. #...# ....# ...#. ..#.. ..... ..#..
. ..... ..... ..... ..... ..... .##.. .##..
@ .###. #...# #.### #.#.# #.### #.... .####
_ ..... ..... ..... ..... ..... ..... #####
| ..#.. ..#.. ..#.. ..#.. ..#.. ..#.. ..#..
"""

FONT = {" ": ["....."] * 7}
for _line in _FONT_SRC.strip().splitlines():
    _ch, *_rows = _line.split()
    assert len(_rows) == 7 and all(len(r) == 5 for r in _rows), _line
    FONT[_ch] = _rows


def clean(s, limit=None):
    """Uppercase, strip accents and drop characters the pixel font lacks."""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c)).upper()
    s = "".join(c if c in FONT else " " for c in s)
    if limit and len(s) > limit:
        s = s[: limit - 3].rstrip() + "..."
    return s


def text_width(s, scale):
    return max(0, len(s) * 6 * scale - scale)


# --------------------------------------------------------------------------
# Sprites (one char per pixel, "." is transparent)
# --------------------------------------------------------------------------
HERO_TOP = [
    "..........KK............",
    ".........KYYK...........",
    ".......KKKKKKKK.........",
    "......KHHLLLLLLK........",
    ".....KHLLGGGGGGGK.......",
    "....KHLGGGGGGGGGGK......",
    "....KLGGGKKKKKKKKKK.....",
    "....KLGGKEEEEEEEHEK.....",
    "....KGGGKEEEEEEEEEK.....",
    "....KGGGGKKKKKKKKKK.....",
    "....KDGGGGGGGGGGGDK.....",
    ".....KDDGGGGGGGDDK......",
    "...KKKKKKWWWWWWKKKKKK...",
    "..KHLLGKWWWWWWWKsssssKK.",
    "..KLGGGKwWWWWWWKSsssssSK",
    "..KGGGDKwWWYYWWKSSSSSSEK",
    "...KDDKKwwWYYWwKSSSSSSEK",
    "....KK..KwwwwwwKKKKKKK..",
]

HERO_LEGS = {
    "stand": [
        "........KDDDKDDDK.......",
        ".......KGGGK.KGGGK......",
        ".......KLGGK.KLGGK......",
        ".......KGGDK.KGGDK......",
        "......KWWWWK.KWWWWK.....",
        ".....KWWWWWK.KWWWWWK....",
        ".....KwwwwwK.KwwwwwK....",
        ".....KKKKKKK.KKKKKKK....",
    ],
    "runA": [
        "........KDDDKDDDK.......",
        "......KGGGK..KGGGK......",
        ".....KLGGK....KLGGK.....",
        "....KGGDK......KGGDK....",
        "...KWWWWK......KWWWWK...",
        "..KWWWWWK......KWWWWWK..",
        "..KwwwwwK......KwwwwwK..",
        "..KKKKKKK......KKKKKKK..",
    ],
    "runB": [
        "........KDDDKDDDK.......",
        ".........KGGGGGK........",
        ".........KLGGGGK........",
        "..........KGGDK.........",
        ".........KWWWWWK........",
        "........KWWWWWWK........",
        "........KwwwwwwK........",
        "........KKKKKKKK........",
    ],
}

HERO_PAL = {
    "K": "#0b1220", "H": "#dcfce7", "L": "#4ade80", "G": "#16a34a",
    "D": "#14532d", "E": "#22d3ee", "Y": "#facc15", "W": "#f8fafc",
    "w": "#cbd5e1", "S": "#475569", "s": "#e2e8f0",
}

BOSS = [
    "....KK................KK....",
    "...KQK................KQK...",
    "...KPK.....KKKKKK.....KPK...",
    "...KPPK..KKQQQQQQKK..KPPK...",
    "....KPPKKQQPPPPPPPPKKPPK....",
    ".....KKQPPPPPPPPPPPPPKK.....",
    "....KQPPKKKKKKPPPPPPPPpK....",
    "....KQPKRRRRRRKPPPPPPPpK....",
    "....KPPKRWWRRRKPPPPPPPpK....",
    "....KPPKRWWRRRKPPPPPPPpK....",
    "....KPPKRRRRRRKPPPPPPPpK....",
    "....KPPPKKKKKKPPPPPPPPpK....",
    ".....KpPPPPPPPPPPPPPPppK....",
    "......KKppppppppppppppKK....",
    "..KKK..KMMMMMMMMMMMMMMK..KKK",
    ".KQPK.KMmmmmmmmmmmmmMK.KPQK.",
    ".KPPK.KMMMMMMMMMMMMMMK.KPPK.",
    ".KPPK.KMmmmmmmmmmmmmMK.KPPK.",
    "KPKKPKKMMMMMMMMMMMMMMKKPKKPK",
    "KPK.KPKKMMMMMMMMMMMMKKPK.KPK",
    "KK...KK.KKKKKKKKKKKK.KK...KK",
    "..........KmmmmmmK..........",
    "...........KmmmmK...........",
    "...........FFFFFF...........",
    "............FffF............",
    ".............ff.............",
]

_BOSS_COMMON = {"K": "#0b0b12", "W": "#ffffff", "M": "#9ca3af", "m": "#4b5563",
                "F": "#fb923c", "f": "#fde047"}
BOSS_PALETTES = [
    {**_BOSS_COMMON, "P": "#a855f7", "p": "#6b21a8", "Q": "#e9d5ff", "R": "#ef4444"},
    {**_BOSS_COMMON, "P": "#f97316", "p": "#9a3412", "Q": "#fed7aa", "R": "#22d3ee"},
    {**_BOSS_COMMON, "P": "#94a3b8", "p": "#475569", "Q": "#f1f5f9", "R": "#f43f5e"},
    {**_BOSS_COMMON, "P": "#dc2626", "p": "#7f1d1d", "Q": "#fecaca", "R": "#facc15"},
]

SHOT = [
    "..YYYY..",
    ".YHWWHY.",
    "YHWWWWHY",
    ".YHWWHY.",
    "..YYYY..",
]
SHOT_PAL = {"Y": "#facc15", "H": "#fef08a", "W": "#ffffff"}

BIG_SHOT = [
    "....YYYY....",
    "..YYHHHHYY..",
    ".YHHWWWWHHY.",
    "YHWWWWWWWWHY",
    "YHWWWWWWWWHY",
    ".YHHWWWWHHY.",
    "..YYHHHHYY..",
    "....YYYY....",
]
BIG_SHOT_PAL = {"Y": "#06b6d4", "H": "#67e8f9", "W": "#ffffff"}

GLOW = [
    "....CC....",
    "....CC....",
    "...CWWC...",
    ".CCWWWWCC.",
    "CCWWWWWWCC",
    "CCWWWWWWCC",
    ".CCWWWWCC.",
    "...CWWC...",
    "....CC....",
    "....CC....",
]
GLOW_PAL = {"C": "#22d3ee", "W": "#ecfeff"}

ORB = [
    "..XXXX..",
    ".XRRRRX.",
    "XRRWWRRX",
    "XRWWWWRX",
    "XRWWWWRX",
    "XRRWWRRX",
    ".XRRRRX.",
    "..XXXX..",
]

COIN = [
    "..KKKK..",
    ".KYYYYK.",
    "KYWYYyyK",
    "KYWYYyyK",
    "KYWYYyyK",
    "KYYYYyyK",
    ".KyyyyK.",
    "..KKKK..",
]
COIN_PAL = {"K": "#78350f", "Y": "#facc15", "y": "#ca8a04", "W": "#fef9c3"}

ICONS = {
    "atirar": ([
        "........",
        "...YY...",
        "..YWWY..",
        "YYWWWWY.",
        "YYWWWWY.",
        "..YWWY..",
        "...YY...",
        "........",
    ], {"Y": "#fde047", "W": "#ffffff"}),
    "carregar": ([
        "....YY..",
        "...YY...",
        "..YY....",
        ".YYYYY..",
        "...YY...",
        "..YY....",
        ".YY.....",
        "Y.......",
    ], {"Y": "#fde047"}),
    "defender": ([
        ".WWWWWW.",
        "WCCCCCCW",
        "WCHHCCCW",
        "WCHCCCCW",
        ".WCCCCW.",
        ".WCCCCW.",
        "..WCCW..",
        "...WW...",
    ], {"W": "#ffffff", "C": "#0891b2", "H": "#a5f3fc"}),
}

BUTTONS = {
    "atirar": ("ATIRAR", "#ca8a04", "#fde047", "#713f12"),
    "carregar": ("TIRO CARREGADO", "#7c3aed", "#c4b5fd", "#3b0764"),
    "defender": ("DEFENDER", "#0e7490", "#67e8f9", "#164e63"),
}


def _check():
    for rows, w in [(HERO_TOP, 24), (BOSS, 28), (SHOT, 8), (BIG_SHOT, 12), (GLOW, 10),
                    (ORB, 8), (COIN, 8)] + [(v, 24) for v in HERO_LEGS.values()] + \
                   [(v[0], 8) for v in ICONS.values()]:
        for i, r in enumerate(rows):
            assert len(r) == w, f"sprite row {i} is {len(r)} wide, expected {w}: {r!r}"


_check()


# --------------------------------------------------------------------------
# Drawing helpers
# --------------------------------------------------------------------------
def _runs(rows):
    """Yield (x, y, length, char) for each horizontal run of opaque pixels."""
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


def _num(n):
    return ("%.2f" % n).rstrip("0").rstrip(".")


def sprite(rows, palette, ox, oy, scale, classes=None):
    """One <path> per colour, so sprites stay small."""
    paths = {}
    for x, y, n, c in _runs(rows):
        paths.setdefault(c, []).append(
            f"M{_num(ox + x * scale)} {_num(oy + y * scale)}h{n * scale}v{scale}h-{n * scale}z")
    out = []
    for c, d in paths.items():
        cls = f' class="{classes[c]}"' if classes and c in classes else ""
        out.append(f'<path{cls} fill="{palette[c]}" d="{"".join(d)}"/>')
    return "".join(out)


def text(s, x, y, scale=2, fill="#ffffff", anchor="start"):
    w = text_width(s, scale)
    if anchor == "middle":
        x -= w // 2
    elif anchor == "end":
        x -= w
    d = []
    for i, ch in enumerate(s):
        gx = x + i * 6 * scale
        for px, py, n, _ in _runs(FONT.get(ch, FONT[" "])):
            d.append(f"M{gx + px * scale} {y + py * scale}h{n * scale}v{scale}h-{n * scale}z")
    return f'<path fill="{fill}" d="{"".join(d)}"/>' if d else ""


def stext(s, x, y, scale=2, fill="#ffffff", anchor="start", shadow="#000000"):
    """Pixel text with a hard drop shadow, readable on any background."""
    s = clean(s)
    return (f'<g opacity=".7">{text(s, x + scale, y + scale, scale, shadow, anchor)}</g>'
            + text(s, x, y, scale, fill, anchor))


def kf(name, *frames):
    return "@keyframes %s{%s}" % (name, "".join("%s{%s}" % f for f in frames))


def pc(x):
    return _num(x) + "%"


def _stars(rnd, width, y0, y1, count, size_max=4):
    out = []
    for i in range(count):
        x, y = rnd.randrange(0, width, 2), rnd.randrange(y0, y1, 2)
        s = rnd.choice([2, 2, 2, 4][: size_max // 2 + 2])
        color = rnd.choice(["#ffffff", "#e9d5ff", "#c4b5fd"])
        if i % 5 == 0:
            out.append(f'<rect class="tw" style="animation-delay:-{rnd.random() * 1.6:.2f}s" '
                       f'x="{x}" y="{y}" width="{s}" height="{s}" fill="{color}"/>')
        else:
            out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{color}" opacity=".75"/>')
    return "".join(out)


def _skyline(rnd, width, base):
    out, x = [], 0
    while x < width:
        w, h = rnd.randint(36, 72), rnd.randint(40, 120)
        out.append(f'<rect x="{x}" y="{base - h}" width="{w - 4}" height="{h}" fill="#140b33"/>')
        for wy in range(base - h + 8, base - 10, 12):
            for wx in range(x + 6, x + w - 12, 10):
                if rnd.random() < 0.16:
                    out.append(f'<rect x="{wx}" y="{wy}" width="4" height="6" fill="#fde68a" opacity=".5"/>')
        x += w
    return "".join(out)


def _ground(width, top, bottom):
    out = [f'<rect x="0" y="{top}" width="{width}" height="{bottom - top}" fill="#1e293b"/>',
           f'<rect x="0" y="{top}" width="{width}" height="4" fill="#64748b"/>',
           f'<rect x="0" y="{top + 24}" width="{width}" height="2" fill="#0f172a"/>']
    for x in range(0, width, 32):
        out.append(f'<rect x="{x}" y="{top + 4}" width="2" height="20" fill="#0f172a"/>')
        out.append(f'<rect x="{x + 16}" y="{top + 26}" width="2" height="{bottom - top - 26}" fill="#0f172a"/>')
    return "".join(out)


def _bar(x, y, w, h, frac, color):
    frac = max(0.0, min(1.0, frac))
    fill = round(w * frac)
    out = [f'<rect x="{x - 4}" y="{y - 4}" width="{w + 8}" height="{h + 8}" fill="#0b1220"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#334155"/>']
    if fill:
        out.append(f'<rect x="{x}" y="{y}" width="{fill}" height="{h}" fill="{color}"/>')
        out.append(f'<rect x="{x}" y="{y}" width="{fill}" height="4" fill="#ffffff" opacity=".35"/>')
    return "".join(out)


def _hp_color(frac):
    return "#22c55e" if frac > 0.5 else "#eab308" if frac > 0.25 else "#ef4444"


# --------------------------------------------------------------------------
# Battle scene
# --------------------------------------------------------------------------
W, H, GROUND = 800, 320, 270
HS, BS = 4, 5
HX, HY = 96, GROUND - len(HERO_TOP + HERO_LEGS["stand"]) * HS
BX, BY = 560, 96
MUZZLE = (HX + 24 * HS + 4, HY + 15 * HS + 4)
HERO_C = (HX + 12 * HS, HY + 13 * HS)
BOSS_HIT = (BX + 8 * BS, BY + 12 * BS)
BOSS_EYE = (BX + 8 * BS, BY + 9 * BS)
POP_X = BX - 50      # damage numbers float left of the boss
BANNER_X = 330       # banners are centred left of the boss so they never cover it

BASE_CSS = (
    ".tw{animation:tw 1.6s steps(1) infinite}" + kf("tw", ("50%", "opacity:.15")) +
    ".flame{animation:flame .2s steps(1) infinite}" + kf("flame", ("50%", "opacity:.3")) +
    ".hover{animation:hover 1.2s ease-in-out infinite alternate}" +
    kf("hover", ("to", "transform:translateY(-10px)")) +
    ".bob{animation:bob .9s steps(1) infinite}" + kf("bob", ("50%", "transform:translateY(4px)"))
)


def _pop(name, start, body, rise=20, hold=18):
    """Text that appears at `start`% of the 4 s loop, floats up and fades."""
    css = (f".{name}{{opacity:0;animation:{name} 4s linear infinite}}" +
           kf(name, ("0%", "opacity:0;transform:translateY(0)"),
              (pc(start), "opacity:0;transform:translateY(0)"),
              (pc(start + 0.5), "opacity:1"),
              (pc(start + hold), f"opacity:1;transform:translateY(-{rise}px)"),
              (pc(min(100, start + hold + 6)) + ",100%", f"opacity:0;transform:translateY(-{rise}px)")))
    return f'<g class="{name}">{body}</g>', css


def _banner(name, start, body, blink=False):
    """Text that appears at `start`% and stays until the loop restarts."""
    css = (f".{name}{{opacity:0;animation:{name} 4s steps(1) infinite}}" +
           kf(name, ("0%", "opacity:0"), (pc(start), "opacity:1"), ("100%", "opacity:1")))
    if blink:
        body = f'<g class="blink">{body}</g>'
        css += ".blink{animation:blink .6s steps(1) infinite}" + kf("blink", ("50%", "opacity:.25"))
    return f'<g class="{name}">{body}</g>', css


def _travel(name, start, end, p0, p1, fade_in=0.5):
    """Projectile moving from p0 to p1 between start% and end%."""
    a = f"transform:translate({p0[0]}px,{p0[1]}px)"
    b = f"transform:translate({p1[0]}px,{p1[1]}px)"
    return (f".{name}{{opacity:0;animation:{name} 4s linear infinite}}" +
            kf(name, ("0%", a + ";opacity:0"), (pc(start), a + ";opacity:0"),
               (pc(start + fade_in), "opacity:1"), (pc(end), b + ";opacity:1"),
               (pc(end + 0.5) + ",100%", b + ";opacity:0")))


def _flash(name, start, blinks=2):
    frames = [("0%", "opacity:1")]
    t = start
    for _ in range(blinks):
        frames += [(pc(t), "opacity:.15"), (pc(t + 2), "opacity:1")]
        t += 4
    frames.append(("100%", "opacity:1"))
    return f".{name}{{animation:{name} 4s steps(1) infinite}}" + kf(name, *frames)


def scene(v):
    """Render the battle. `v` is the view built by engine.py."""
    rnd = random.Random(42)
    css = [BASE_CSS]
    world, fx = [], []
    last = v.get("last") or {}
    move, event = last.get("move"), last.get("event")
    bpal = BOSS_PALETTES[v["boss_palette"]]

    world.append('<rect width="800" height="320" fill="url(#sky)"/>')
    world.append(_stars(rnd, W, 84, 200, 46))
    world.append(_skyline(rnd, W, GROUND))
    world.append(_ground(W, GROUND, H))

    # hero
    legs = sprite(HERO_LEGS["stand"], HERO_PAL, HX, HY + len(HERO_TOP) * HS, HS)
    top = sprite(HERO_TOP, HERO_PAL, HX, HY, HS)
    world.append(f'<rect x="{HX + 16}" y="{GROUND}" width="64" height="6" fill="#000" opacity=".35"/>')
    world.append(f'<g class="herofx">{legs}<g class="bob">{top}</g></g>')

    # boss
    boss = sprite(BOSS, bpal, BX, BY, BS, classes={"F": "flame", "f": "flame"})
    world.append(f'<rect x="{BX + 30}" y="{GROUND + 2}" width="80" height="6" fill="#000" opacity=".35"/>')
    world.append(f'<g class="bossin"><g class="hover"><g class="bosshit">{boss}</g></g></g>')

    hit_at = None
    if move == "atirar":
        fx.append(f'<g class="shot">{sprite(SHOT, SHOT_PAL, -8, -5, 2)}</g>')
        css.append(_travel("shot", 2, 20, MUZZLE, BOSS_HIT))
        hit_at = 20
    elif move == "carregar":
        fx.append(f'<g transform="translate({MUZZLE[0]} {MUZZLE[1]})"><g class="glow">'
                  f'{sprite(GLOW, GLOW_PAL, -15, -15, 3)}</g></g>')
        css.append(".glow{opacity:0;transform-box:fill-box;transform-origin:center;"
                   "animation:glow 4s linear infinite}" +
                   kf("glow", ("0%", "opacity:0;transform:scale(.2)"), ("1%", "opacity:1"),
                      ("16%", "opacity:1;transform:scale(1.3)"), ("17%,100%", "opacity:0;transform:scale(1.3)")))
        target = BOSS_HIT if last.get("hit") else (W + 60, 40)
        fx.append(f'<g class="big">{sprite(BIG_SHOT, BIG_SHOT_PAL, -18, -12, 3)}</g>')
        css.append(_travel("big", 17, 32, MUZZLE, target))
        if last.get("hit"):
            hit_at = 32
            css.append(".world{animation:shake 4s steps(1) infinite}" +
                       kf("shake", ("0%", "transform:translate(0,0)"), ("32%", "transform:translate(8px,-2px)"),
                          ("33%", "transform:translate(-8px,2px)"), ("34%", "transform:translate(6px,0)"),
                          ("35%", "transform:translate(-4px,2px)"), ("36%,100%", "transform:translate(0,0)")))
        else:
            el, c = _pop("miss", 30, stext("ERROU!", POP_X, BY + 30, 3, "#e2e8f0", "middle"))
            fx.append(el)
            css.append(c)
    elif move == "defender":
        fx.append(f'<rect class="shield" x="{HX - 14}" y="{HY - 14}" width="124" height="{GROUND - HY + 18}" '
                  f'fill="#22d3ee" fill-opacity=".12" stroke="#67e8f9" stroke-width="4" stroke-dasharray="12 6"/>')
        css.append(".shield{opacity:0;animation:shield 4s linear infinite,dash .6s linear infinite}" +
                   kf("shield", ("0%", "opacity:0"), ("4%", "opacity:1"), ("78%", "opacity:1"),
                      ("84%,100%", "opacity:0")) +
                   kf("dash", ("to", "stroke-dashoffset:-18")))
        el, c = _pop("heal", 8, stext(f"+{last.get('heal', 0)}", HERO_C[0], HY - 34, 3, "#4ade80", "middle"))
        fx.append(el)
        css.append(c)

    if hit_at is not None:
        if event != "boss_defeated":
            css.append(_flash("bosshit", hit_at))
        el, c = _pop("dmg", hit_at, stext(f"-{last.get('damage', 0)}", POP_X, BY + 30, 3, "#f87171", "middle"))
        fx.append(el)
        css.append(c)
        if move == "carregar":
            el, c = _pop("crit", hit_at, stext("CRITICO!", POP_X, BY + 60, 2, "#facc15", "middle"))
            fx.append(el)
            css.append(c)

    counter = last.get("counter", 0)
    if counter:
        x_pal = {"X": bpal["p"], "R": bpal["R"], "W": "#ffffff"}
        fx.append(f'<g class="orb">{sprite(ORB, x_pal, -8, -8, 2)}</g>')
        css.append(_travel("orb", 48, 62, BOSS_EYE, HERO_C))
        css.append(_flash("herofx", 62, blinks=4 if event == "hero_down" else 2))
        el, c = _pop("hurt", 62, stext(f"-{counter}", HERO_C[0], HY - 34, 3, "#f87171", "middle"))
        fx.append(el)
        css.append(c)

    if event == "boss_defeated":
        cx, cy = BOSS_HIT[0] + 30, BOSS_HIT[1] - 10
        for i in range(12):
            ang = i * 30
            dx, dy = [(1, 0), (.87, .5), (.5, .87), (0, 1), (-.5, .87), (-.87, .5),
                      (-1, 0), (-.87, -.5), (-.5, -.87), (0, -1), (.5, -.87), (.87, -.5)][i]
            dist = 70 if i % 2 else 50
            color = ["#facc15", "#fb923c", "#ffffff"][i % 3]
            fx.append(f'<rect class="ex{ang}" x="-6" y="-6" width="12" height="12" fill="{color}"/>')
            css.append(_travel(f"ex{ang}", hit_at, hit_at + 16, (cx, cy),
                               (round(cx + dx * dist), round(cy + dy * dist))))
        css.append(".bossin{animation:bossin 4s steps(1) infinite}" +
                   kf("bossin", ("0%", "opacity:0"), ("56%", "opacity:1"), ("58%", "opacity:.2"),
                      ("60%", "opacity:1"), ("62%", "opacity:.2"), ("64%,100%", "opacity:1")))
        el, c = _banner("ban1", hit_at + 26, stext("CHEFE DERROTADO!", BANNER_X, 100, 3, "#facc15", "middle"))
        fx.append(el)
        css.append(c)
        msg = f"{last.get('defeated', '')} CAIU! AGORA: {v['boss_name']}"
        el, c = _banner("ban2", 56, stext(msg, BANNER_X, 136, 2, "#f8fafc", "middle"))
        fx.append(el)
        css.append(c)
    elif event == "hero_down":
        el, c = _banner("ban1", 72, stext("GAME OVER? NEVER!", BANNER_X, 104, 3, "#facc15", "middle"), blink=True)
        fx.append(el)
        css.append(c)
    elif not move:
        el, c = _banner("ban1", 0, stext("UM CHEFE APARECEU!", BANNER_X, 104, 3, "#facc15", "middle"), blink=True)
        fx.append(el)
        css.append(c)

    # HUD (outside the shaking world)
    hero_frac = v["hero_hp"] / v["hero_max"]
    boss_frac = v["boss_hp"] / v["boss_max"]
    hud = [
        '<rect width="800" height="80" fill="#000" opacity=".35"/>',
        stext("HEROI", 24, 12, 2, "#f8fafc"),
        _bar(24, 36, 240, 14, hero_frac, _hp_color(hero_frac)),
        stext(f"{v['hero_hp']}/{v['hero_max']}", 24, 58, 2, "#cbd5e1"),
        stext(v["boss_name"], 776, 12, 2, "#f8fafc", "end"),
        _bar(536, 36, 240, 14, boss_frac, "#f43f5e"),
        stext(f"{v['boss_hp']}/{v['boss_max']}", 776, 58, 2, "#cbd5e1", "end"),
        stext(f"CHEFE {v['boss_num']}/{v['boss_total']}", 400, 12, 2, "#facc15", "middle"),
        stext(f"ROUND {v['round']}", 400, 34, 2, "#c4b5fd", "middle"),
        stext(f"JOGADA {v['turn']}", 400, 56, 2, "#94a3b8", "middle"),
        '<rect y="288" width="800" height="32" fill="#000" opacity=".55"/>',
        stext(clean(v.get("message", ""), limit=64), 400, 297, 2, "#f8fafc", "middle"),
    ]

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="320" viewBox="0 0 800 320" '
        'shape-rendering="crispEdges" role="img" aria-label="Boss battle">'
        '<title>Boss battle</title>'
        f'<style>{"".join(css)}</style>'
        '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#070b1a"/><stop offset="1" stop-color="#2e1065"/>'
        '</linearGradient></defs>'
        f'<g class="world">{"".join(world)}{"".join(fx)}</g>'
        f'{"".join(hud)}'
        '</svg>\n'
    )


# --------------------------------------------------------------------------
# Loading screen (shown on the issue page while the move is processed)
# --------------------------------------------------------------------------
def loading():
    w, h = 640, 240
    rnd = random.Random(7)
    hs = 2
    bar_x, bar_y, bar_w = 120, 182, 400
    hero_h = len(HERO_TOP + HERO_LEGS["stand"]) * hs
    hy = bar_y - hero_h

    label = "CARREGANDO"
    lw = text_width(label, 4)
    total = lw + 8 + 40
    lx = (w - total) // 2

    hero = (f'<g class="r1">{sprite(HERO_TOP + HERO_LEGS["runA"], HERO_PAL, 0, hy, hs)}</g>'
            f'<g class="r2">{sprite(HERO_TOP + HERO_LEGS["runB"], HERO_PAL, 0, hy, hs)}</g>')

    dots = "".join(f'<rect class="d{i}" x="{lx + lw + 8 + i * 16}" y="56" width="8" height="8" fill="#facc15"/>'
                   for i in range(3))
    coins = "".join(f'<g class="coin">{sprite(COIN, COIN_PAL, x, 24, 4)}</g>' for x in (lx - 56, lx + total + 24))

    css = (
        ".iris{transform-box:fill-box;transform-origin:center;animation:iris 3.2s ease-in-out infinite}" +
        kf("iris", ("0%", "transform:scale(0)"), ("12%,86%", "transform:scale(1)"), ("100%", "transform:scale(0)")) +
        ".run{animation:run 3.2s linear infinite}" +
        kf("run", ("0%,12%", f"transform:translateX({bar_x - 24}px)"),
           ("86%,100%", f"transform:translateX({bar_x + bar_w - 24}px)")) +
        ".fill{transform-box:fill-box;transform-origin:left center;animation:fill 3.2s linear infinite}" +
        kf("fill", ("0%,12%", "transform:scaleX(0)"), ("86%,100%", "transform:scaleX(1)")) +
        ".r1{animation:r1 .3s steps(1) infinite}" + kf("r1", ("50%", "opacity:0")) +
        ".r2{opacity:0;animation:r2 .3s steps(1) infinite}" + kf("r2", ("50%", "opacity:1")) +
        ".coin{transform-box:fill-box;transform-origin:center;animation:coin .8s steps(4) infinite}" +
        kf("coin", ("0%", "transform:scaleX(1)"), ("50%", "transform:scaleX(.15)"), ("100%", "transform:scaleX(1)")) +
        "".join(f".d{i}{{opacity:0;animation:d{i} 1.2s steps(1) infinite}}" +
                kf(f"d{i}", ("0%", "opacity:0"), (pc((i + 1) * 25), "opacity:1"), ("100%", "opacity:1"))
                for i in range(3)) +
        ".tw{animation:tw 1.6s steps(1) infinite}" + kf("tw", ("50%", "opacity:.15"))
    )

    body = (
        '<rect width="640" height="240" fill="url(#lsky)"/>' +
        _stars(rnd, w, 0, 170, 36) +
        _ground(w, 202, h) +
        stext(label, lx, 36, 4, "#f8fafc") + dots + coins +
        stext("PROCESSANDO SUA JOGADA", w // 2, 90, 2, "#c4b5fd", "middle") +
        stext("VOLTE AO PERFIL EM 1 MINUTO", w // 2, 114, 2, "#e9d5ff", "middle") +
        f'<rect x="{bar_x - 4}" y="{bar_y - 4}" width="{bar_w + 8}" height="20" fill="#0b1220"/>'
        f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="12" fill="#334155"/>'
        f'<rect class="fill" x="{bar_x}" y="{bar_y}" width="{bar_w}" height="12" fill="#facc15"/>'
        f'<g class="run">{hero}</g>'
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        'shape-rendering="crispEdges" role="img" aria-label="Carregando">'
        '<title>Carregando</title>'
        f'<style>{css}</style>'
        '<defs><linearGradient id="lsky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#1e1b4b"/><stop offset="1" stop-color="#4c1d95"/></linearGradient>'
        f'<mask id="m"><rect width="{w}" height="{h}" fill="#000"/>'
        f'<circle class="iris" cx="{w // 2}" cy="{h // 2}" r="360" fill="#fff"/></mask></defs>'
        f'<rect width="{w}" height="{h}" fill="#000"/>'
        f'<g mask="url(#m)">{body}</g>'
        '</svg>\n'
    )


# --------------------------------------------------------------------------
# Action buttons
# --------------------------------------------------------------------------
def button(move):
    label, bg, light, dark = BUTTONS[move]
    icon, pal = ICONS[move]
    w, h = 248, 56
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'shape-rendering="crispEdges" role="img" aria-label="{label.title()}">'
        f'<title>{label.title()}</title>'
        f'<rect x="4" y="0" width="{w - 8}" height="{h}" fill="#0b1220"/>'
        f'<rect x="0" y="4" width="{w}" height="{h - 8}" fill="#0b1220"/>'
        f'<rect x="4" y="4" width="{w - 8}" height="{h - 8}" fill="{bg}"/>'
        f'<rect x="4" y="4" width="{w - 8}" height="4" fill="{light}"/>'
        f'<rect x="4" y="4" width="4" height="{h - 8}" fill="{light}"/>'
        f'<rect x="4" y="{h - 8}" width="{w - 8}" height="4" fill="{dark}"/>'
        f'<rect x="{w - 8}" y="4" width="4" height="{h - 8}" fill="{dark}"/>'
        + sprite(icon, pal, 18, 16, 3)
        + stext(label, 54, 21, 2, "#ffffff")
        + '</svg>\n'
    )
