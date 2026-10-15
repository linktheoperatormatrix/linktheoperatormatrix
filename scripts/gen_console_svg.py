#!/usr/bin/env python3
"""Генерирует assets/console.svg — операторская «Навуходоносора»:
анимированный цифровой дождь (CSS внутри SVG) + терминал оператора."""
import random
from pathlib import Path

random.seed(2110)  # Марк III, № 11 — детерминированный дождь
W, H = 846, 230
GLYPHS = "アイウエオカキクケコサシスセソタチツテト0123456789AB"
COLS = 26
COL_W = W // COLS

rain = []
for c in range(COLS):
    x = c * COL_W + 7
    n = 26
    dur = round(random.uniform(2.2, 4.8), 2)
    delay = round(random.uniform(-4.8, 0), 2)
    op = round(random.uniform(0.16, 0.38), 2)
    fs = random.choice((12, 13, 14))
    step = fs + 3
    tspans = "".join(
        f'<tspan x="{x}" dy="{step}">{random.choice(GLYPHS)}</tspan>'
        for _ in range(n)
    )
    rain.append(
        f'<text class="rain" style="animation-duration:{dur}s;'
        f'animation-delay:{delay}s;opacity:{op};font-size:{fs}px" '
        f'x="{x}" y="{-n * step}">{tspans}</text>'
    )

TERMINAL = [
    ("link@nebuchadnezzar:~$", " ./operator --connect", "#C9D1D9"),
    ("&gt; судно:", " Nebuchadnezzar — Mark III, № 11", "#00FF41"),
    ("&gt; uplink:", " Zion · связь устойчива", "#00FF41"),
    ("&gt; the matrix has you", "", "#00FF41"),
    ("&gt; следуй за белым кроликом 🐇", "", "#00FF41"),
]
term_lines = []
for i, (left, right, color) in enumerate(TERMINAL):
    if i == 0:
        body = f'<tspan fill="#00FF41">{left}</tspan><tspan fill="{color}">{right}</tspan>'
    else:
        body = f'<tspan fill="{color}">{left}{right}</tspan>'
    if i == len(TERMINAL) - 1:
        body += '<tspan class="cur" fill="#00FF41"> ▌</tspan>'
    term_lines.append(f'<text class="term" x="44" y="{62 + i * 29}">{body}</text>')

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Операторская: цифровой дождь и терминал Zion">
<style>
  .rain {{ animation-name: fall; animation-timing-function: linear; animation-iteration-count: infinite; fill: #00FF41; font-family: Menlo, Consolas, monospace; }}
  @keyframes fall {{ from {{ transform: translateY(0); }} to {{ transform: translateY({26 * 17 + 230 + 40}px); }} }}
  .term {{ fill: #00FF41; font-family: Menlo, Consolas, monospace; font-size: 15px; letter-spacing: 0.5px; }}
  .cur {{ animation: blink 1.1s steps(1) infinite; }}
  @keyframes blink {{ 0%, 55% {{ opacity: 1; }} 56%, 100% {{ opacity: 0; }} }}
</style>
<rect width="{W}" height="{H}" fill="#000000"/>
{''.join(rain)}
<rect x="16" y="16" width="{W - 32}" height="{H - 32}" rx="10" fill="#000000" opacity="0.82" stroke="#00FF41" stroke-opacity="0.45" stroke-width="1.5"/>
<circle cx="36" cy="36" r="5" fill="#00FF41" opacity="0.9"/>
{''.join(term_lines)}
</svg>
"""

out = Path(__file__).resolve().parent.parent / "assets" / "console.svg"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(svg, encoding="utf-8")
print(f"written {out} ({out.stat().st_size} bytes)")
