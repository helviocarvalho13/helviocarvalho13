#!/usr/bin/env python3
"""Community boss battle played through GitHub Issues.

Each button in the README opens a pre-filled issue titled ``boss|<move>``.
The "Boss Battle" workflow runs ``engine.py play``, which applies the move,
re-renders the art and the README section, and writes the bot reply.

Usage:
  python3 game/engine.py init     # start a fresh battle and render everything
  python3 game/engine.py render   # re-render art + README from game/state.json
  python3 game/engine.py play     # env: ISSUE_TITLE, ISSUE_NUMBER, PLAYER, REPLY_FILE
"""
import html
import json
import os
import random
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import art  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GAME = ROOT / "game"
STATE_FILE = GAME / "state.json"
README = ROOT / "README.md"
REPO = os.environ.get("GITHUB_REPOSITORY", "helviocarvalho13/helviocarvalho13")
OWNER = REPO.split("/")[0]
RAW = f"https://raw.githubusercontent.com/{REPO}/main/game"
PROFILE = f"https://github.com/{OWNER}"
START, END = "<!-- BOSS:START -->", "<!-- BOSS:END -->"

HERO_MAX = 100
BOSSES = [
    {"name": "MECHA-BYTE", "hp": 100},
    {"name": "NULL POINTER", "hp": 150},
    {"name": "STACK OVERFLOW", "hp": 220},
    {"name": "KERNEL PANIC", "hp": 300},
]
MOVES = {
    "atirar": {"label": "Atirar", "emoji": "🔫"},
    "carregar": {"label": "Tiro carregado", "emoji": "⚡"},
    "defender": {"label": "Defender", "emoji": "🛡️"},
}
LOGIN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})")


# --------------------------------------------------------------------------
# State
# --------------------------------------------------------------------------
def boss_max(state):
    return round(BOSSES[state["boss_index"]]["hp"] * (1 + 0.5 * (state["round"] - 1)))


def new_state():
    state = {"turn": 0, "round": 1, "boss_index": 0, "hero_hp": HERO_MAX,
             "players": {}, "log": [], "hall": [], "last": None}
    state["boss_hp"] = boss_max(state)
    return state


def load():
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def write(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


# --------------------------------------------------------------------------
# Rules
# --------------------------------------------------------------------------
def describe(last):
    move, d = last["move"], last["damage"]
    if move == "atirar":
        s = f"atirou: -{d}"
    elif move == "carregar":
        s = f"tiro carregado CRÍTICO: -{d}" if last["hit"] else "tiro carregado errou"
    else:
        s = f"defendeu: +{last['heal']} de energia"
    if last["counter"]:
        s += f" | contra-ataque -{last['counter']}"
    if last["event"] == "boss_defeated":
        s += f" | {last['defeated']} derrotado!"
    elif last["event"] == "hero_down":
        s += " | GAME OVER? Never!"
    return s


def play_move(state, player, move, seed):
    rng = random.Random(seed)
    boss = BOSSES[state["boss_index"]]
    last = {"move": move, "player": player, "hit": False, "damage": 0,
            "counter": 0, "heal": 0, "event": None}

    if move == "atirar":
        last["hit"], last["damage"] = True, rng.randint(8, 12)
    elif move == "carregar":
        last["hit"] = rng.random() < 0.45
        last["damage"] = rng.randint(26, 34) if last["hit"] else 0
    else:
        last["heal"] = min(15, HERO_MAX - state["hero_hp"])
        state["hero_hp"] += last["heal"]

    stats = state["players"].setdefault(player, {"damage": 0, "moves": 0, "kills": 0})
    stats["moves"] += 1
    dealt = min(last["damage"], state["boss_hp"])
    last["damage"] = dealt
    stats["damage"] += dealt
    state["boss_hp"] -= dealt
    state["turn"] += 1

    if state["boss_hp"] <= 0:
        last["event"], last["defeated"] = "boss_defeated", boss["name"]
        stats["kills"] += 1
        state["hall"].insert(0, {"boss": boss["name"], "round": state["round"],
                                 "by": player, "turn": state["turn"]})
        del state["hall"][10:]
        state["boss_index"] += 1
        if state["boss_index"] >= len(BOSSES):
            state["boss_index"], state["round"] = 0, state["round"] + 1
        state["boss_hp"] = boss_max(state)
    elif move != "defender":
        last["counter"] = rng.randint(6, 10)
        state["hero_hp"] -= last["counter"]
        if state["hero_hp"] <= 0:
            last["event"] = "hero_down"
            state["hero_hp"] = HERO_MAX
            state["boss_hp"] = min(boss_max(state), state["boss_hp"] + boss_max(state) // 4)

    last["text"] = describe(last)
    state["last"] = last
    state["log"].insert(0, {"turn": state["turn"], "player": player, "move": move, "text": last["text"]})
    del state["log"][8:]
    return last


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
def view(state):
    last = state["last"]
    if last:
        message = f"@{last['player']} {last['text']}"
    else:
        message = "ESCOLHA UMA ACAO ABAIXO PARA LUTAR"
    return {
        "hero_hp": state["hero_hp"], "hero_max": HERO_MAX,
        "boss_name": BOSSES[state["boss_index"]]["name"], "boss_palette": state["boss_index"],
        "boss_hp": state["boss_hp"], "boss_max": boss_max(state),
        "boss_num": state["boss_index"] + 1, "boss_total": len(BOSSES),
        "round": state["round"], "turn": state["turn"], "last": last, "message": message,
    }


def issue_link(move):
    spec = MOVES[move]
    body = (f"![Carregando]({RAW}/loading.svg)\n\n"
            f"**{spec['emoji']} {spec['label']}!** Clique em **Create** (ou *Submit new issue*) "
            f"para enviar sua jogada. Não precisa escrever nada.\n\n"
            f"Em cerca de 1 minuto o robô responde aqui e o [perfil]({PROFILE}) é atualizado.")
    query = urllib.parse.urlencode({"title": f"boss|{move}", "body": body}, quote_via=urllib.parse.quote)
    return f"https://github.com/{REPO}/issues/new?{query}"


def readme_section(state):
    v = view(state)
    buttons = "\n".join(
        f'  <a href="{html.escape(issue_link(m))}"><img src="./game/btn-{m}.svg" '
        f'alt="{spec["emoji"]} {spec["label"]}" /></a>'
        for m, spec in MOVES.items())

    ranking = sorted(state["players"].items(), key=lambda kv: (-kv[1]["damage"], -kv[1]["kills"], kv[0]))[:5]
    medals = ["🥇", "🥈", "🥉", "4º", "5º"]
    if ranking:
        rows = "\n".join(f"| {medals[i]} | [@{p}](https://github.com/{p}) | {s['damage']} | {s['moves']} | {s['kills']} |"
                         for i, (p, s) in enumerate(ranking))
        table = ("| # | Jogador | Dano | Jogadas | Chefes derrotados |\n"
                 "|:-:|:--|--:|--:|--:|\n" + rows)
    else:
        table = "_Ninguém lutou ainda. Seja o primeiro!_"

    log = "\n".join(f"- **#{e['turn']}** [@{e['player']}](https://github.com/{e['player']}) {e['text']}"
                    for e in state["log"][:5]) or "- _Nenhuma jogada ainda._"
    hall = "\n".join(f"- 💀 **{h['boss']}** (round {h['round']}) derrotado por "
                     f"[@{h['by']}](https://github.com/{h['by']}) na jogada #{h['turn']}"
                     for h in state["hall"][:5]) or "- _Nenhum chefe derrotado ainda._"

    return f"""{START}
<h2 align="center">⚔️ Boss Battle</h2>

<p align="center">
  <img src="{RAW}/scene.svg?v={state['turn']}" width="800" alt="Batalha contra {v['boss_name']}: chefe com {v['boss_hp']}/{v['boss_max']} de vida, herói com {v['hero_hp']}/{v['hero_max']}" />
</p>

<p align="center">
{buttons}
</p>

<p align="center"><sub>Clique numa ação, confirme a Issue e volte aqui em cerca de 1 minuto. Todo mundo luta junto contra o mesmo chefe!</sub></p>

<details>
<summary><b>🏆 Ranking, últimas jogadas e chefes derrotados</b></summary>
<br>

{table}

**Últimas jogadas**

{log}

**Chefes derrotados**

{hall}

</details>
{END}"""


def update_readme(state):
    text = README.read_text(encoding="utf-8")
    start, end = text.find(START), text.find(END)
    if start < 0 or end < start:
        sys.exit(f"README.md is missing the {START} / {END} markers")
    write(README, text[:start] + readme_section(state) + text[end + len(END):])


def render_all(state):
    write(GAME / "scene.svg", art.scene(view(state)))
    write(GAME / "loading.svg", art.loading())
    for move in MOVES:
        write(GAME / f"btn-{move}.svg", art.button(move))
    update_readme(state)
    write(STATE_FILE, json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def reply_text(state, last):
    v = view(state)
    spec = MOVES[last["move"]]
    return (f"### {spec['emoji']} Jogada registrada!\n\n"
            f"@{last['player']} {last['text']}\n\n"
            f"| ❤️ Herói | 💀 {v['boss_name']} |\n|:-:|:-:|\n"
            f"| {v['hero_hp']}/{v['hero_max']} | {v['boss_hp']}/{v['boss_max']} |\n\n"
            f'<img src="{RAW}/scene.svg?v={state["turn"]}" width="600" alt="Cena da batalha" />\n\n'
            f"[🎮 Voltar ao perfil e jogar de novo]({PROFILE})\n")


def set_output(**values):
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            for k, val in values.items():
                f.write(f"{k}={val}\n")


def cmd_play():
    title = os.environ.get("ISSUE_TITLE", "").strip()
    player = os.environ.get("PLAYER", "").strip()
    number = os.environ.get("ISSUE_NUMBER", "0").strip()
    reply_file = os.environ.get("REPLY_FILE")
    move = title.split("|", 1)[1].strip().lower() if "|" in title else ""

    if move not in MOVES or not LOGIN.fullmatch(player):
        reply = (f"Essa jogada não existe 🤔. Use um dos botões da batalha no [perfil]({PROFILE}): "
                 + ", ".join(f"`boss|{m}`" for m in MOVES) + ".\n")
        set_output(result="invalid", move=move or "none")
    else:
        state = load()
        last = play_move(state, player, move, seed=f"{number}-{state['turn']}")
        render_all(state)
        reply = reply_text(state, last)
        set_output(result="ok", move=move)
        print(f"#{state['turn']} @{player} {last['text']}")

    if reply_file:
        write(reply_file, reply)
    else:
        print(reply)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "render"
    if cmd == "init":
        render_all(new_state())
    elif cmd == "render":
        render_all(load())
    elif cmd == "play":
        cmd_play()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
