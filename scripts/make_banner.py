"""Generate the animated README banner (dark + light SVG).

Left: a synthetic pitch with moving players and vision "detections" (no real
footage). Right: the real stage-2 caption and stage-3 narration from samples/
typing out, then the TTS waveform playing. Standard library only.

    python scripts/make_banner.py
"""
import csv
import random
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W, H, CYCLE = 1180, 470, 14.0
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
THEMES = {
    "dark": dict(bg="#0A101F", win="#0D1628", panel="#101B30", line="#25344C", text="#E6EDF3",
                 muted="#8291A8", accent="#2DD4BF", pitch="#0F2A24", mark="#2DD4BF",
                 home="#E6EDF3", away="#3B82F6", ok="#3FB950"),
    "light": dict(bg="#EEF2F6", win="#FFFFFF", panel="#F6F8FA", line="#D0D7DE", text="#1F2328",
                  muted="#59636E", accent="#0F766E", pitch="#E3F2EE", mark="#0F766E",
                  home="#1F2328", away="#2563EB", ok="#1A7F37"),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def first_row(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[1][0]


def kt(*pairs):
    """keyTimes/values from (fraction-of-cycle, value) pairs."""
    return ";".join(f"{t:.4f}" for t, _ in pairs), ";".join(str(v) for _, v in pairs)


def typed(lines, x, y0, start, dur, t, size=13, lh=19, width=600):
    """Lines that type out left-to-right within the cycle, then reset."""
    out, per = [], dur / max(len(lines), 1)
    for i, line in enumerate(lines):
        s, e = (start + i * per) / CYCLE, (start + (i + 1) * per) / CYCLE
        k, v = kt((0, 0), (s, 0), (e, width), (0.96, width), (1, 0))
        cid = f"c{abs(hash((x, y0, i))) % 10**8}"
        out.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y0 + i * lh - size}" height="{lh}" width="0">'
                   f'<animate attributeName="width" dur="{CYCLE}s" repeatCount="indefinite" keyTimes="{k}" values="{v}"/></rect></clipPath>'
                   f'<text x="{x}" y="{y0 + i * lh}" font-size="{size}" fill="{t["text"]}" clip-path="url(#{cid})">{esc(line)}</text>')
    return "".join(out)


def panel(x, y, w, h, title, tag, t):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{t["panel"]}" stroke="{t["line"]}"/>'
            f'<path d="M{x} {y + 30}H{x + w}" stroke="{t["line"]}"/>'
            f'<text x="{x + 14}" y="{y + 20}" fill="{t["accent"]}" font-size="12" font-weight="700" letter-spacing="1.2">{title}</text>'
            f'<text x="{x + w - 14}" y="{y + 20}" text-anchor="end" fill="{t["muted"]}" font-size="11">{tag}</text>')


def render(theme, caption, narration):
    t = THEMES[theme]
    rnd = random.Random(4)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ti de">',
         '<title id="ti">narrator.py --live</title>',
         '<desc id="de">Animated pipeline: a football pitch with moving players and vision detections, a Gemma caption and a '
         'Qwen narration typing out in Spanish, and an OmniVoice waveform playing — all running locally.</desc>',
         f'<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>',
         f'<rect x="13" y="13" width="{W - 26}" height="{H - 26}" rx="13" fill="{t["win"]}" stroke="{t["line"]}"/>',
         f'<path d="M13 58H{W - 13}" stroke="{t["line"]}"/>',
         '<circle cx="38" cy="36" r="6" fill="#FF5F57"/><circle cx="59" cy="36" r="6" fill="#FEBC2E"/><circle cx="80" cy="36" r="6" fill="#28C840"/>',
         f'<g font-family="{MONO}">',
         f'<text x="{W / 2}" y="41" text-anchor="middle" fill="{t["muted"]}" font-size="13">narrator.py --live · 100% local inference</text>']

    # --- stage 1: frames (synthetic pitch) ---
    px, py, pw, ph = 35, 78, 470, 360
    o.append(panel(px, py, pw, ph, "01 · FRAMES", "2 FPS → Parquet", t))
    fx, fy, fw, fh = px + 16, py + 46, pw - 32, ph - 92
    o.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="4" fill="{t["pitch"]}"/>'
             f'<g fill="none" stroke="{t["mark"]}" stroke-opacity=".45">'
             f'<rect x="{fx + 8}" y="{fy + 8}" width="{fw - 16}" height="{fh - 16}"/>'
             f'<path d="M{fx + fw / 2} {fy + 8}V{fy + fh - 8}"/><circle cx="{fx + fw / 2}" cy="{fy + fh / 2}" r="34"/>'
             f'<rect x="{fx + 8}" y="{fy + fh / 2 - 55}" width="58" height="110"/><rect x="{fx + fw - 66}" y="{fy + fh / 2 - 55}" width="58" height="110"/></g>')
    players = []
    for team, col, xs in (("home", t["home"], (0.18, 0.32, 0.45)), ("away", t["away"], (0.55, 0.68, 0.82))):
        for i in range(10):
            x = fx + fw * (xs[i % 3] + rnd.uniform(-0.05, 0.05))
            y = fy + fh * rnd.uniform(0.12, 0.88)
            dx, dy = rnd.uniform(-38, 38), rnd.uniform(-22, 22)
            players.append((x, y, dx, dy, col))
    for x, y, dx, dy, col in players:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{col}">'
                 f'<animateTransform attributeName="transform" type="translate" dur="{CYCLE}s" repeatCount="indefinite" '
                 f'values="0 0;{dx:.1f} {dy:.1f};{-dx / 2:.1f} {dy / 3:.1f};0 0" keyTimes="0;.4;.75;1"/></circle>')
    bx, by = fx + fw * 0.5, fy + fh * 0.5
    o.append(f'<circle cx="{bx}" cy="{by}" r="3.5" fill="#F2C94C"><animateTransform attributeName="transform" type="translate" '
             f'dur="{CYCLE}s" repeatCount="indefinite" values="0 0;-60 30;40 -50;110 10;0 0" keyTimes="0;.25;.5;.75;1"/></circle>')
    for (x, y, dx, dy, _), name, s in zip(players[1::7], ("Xavi #6", "Iniesta #8", "Di María #22"), (0.10, 0.18, 0.26)):
        k, v = kt((0, 0), (s, 0), (s + .02, 1), (.42, 1), (.45, 0), (1, 0))
        o.append(f'<g opacity="0"><animate attributeName="opacity" dur="{CYCLE}s" repeatCount="indefinite" keyTimes="{k}" values="{v}"/>'
                 f'<g><animateTransform attributeName="transform" type="translate" dur="{CYCLE}s" repeatCount="indefinite" '
                 f'values="0 0;{dx:.1f} {dy:.1f};{-dx / 2:.1f} {dy / 3:.1f};0 0" keyTimes="0;.4;.75;1"/>'
                 f'<rect x="{x - 12:.1f}" y="{y - 12:.1f}" width="24" height="24" fill="none" stroke="{t["accent"]}" stroke-width="1.5"/>'
                 f'<text x="{x - 12:.1f}" y="{y - 16:.1f}" font-size="10" fill="{t["accent"]}">{esc(name)}</text></g></g>')
    o.append(f'<text x="{fx}" y="{py + ph - 16}" font-size="11" fill="{t["muted"]}">frame_col: PNG bytes · zstd-22 · batch of 3 → vision</text>')
    o.append(f'<text x="{fx + fw}" y="{py + ph - 16}" text-anchor="end" font-size="11" fill="{t["accent"]}">00:06:12</text>')

    # --- stages 2–4 ---
    rx, rw = 525, W - 525 - 35
    o.append(panel(rx, 78, rw, 132, "02 · VISION CAPTION", "gemma-4-e4b · LM Studio", t))
    cap = textwrap.wrap(caption, 72)
    if len(cap) > 4:
        cap = cap[:3] + [textwrap.shorten(cap[3], 69, placeholder="") + " …"]
    o.append(typed(cap, rx + 14, 132, 0.6, 4.0, t, size=12, lh=18, width=rw - 28))
    o.append(panel(rx, 222, rw, 104, "03 · NARRATOR", "qwen3.5-9b · ≤22 words / 10 s", t))
    o.append(typed(textwrap.wrap(narration, 72)[:3], rx + 14, 276, 5.0, 3.0, t, size=13, lh=20, width=rw - 28))

    o.append(panel(rx, 338, rw, 100, "04 · VOICE", "OmniVoice · MPS · 24 kHz", t))
    n, x0, base = 64, rx + 16, 410
    for i in range(n):
        h = 6 + 26 * abs(__import__("math").sin(i * 0.55) * rnd.uniform(0.4, 1))
        s = (8.4 + i * 0.045) / CYCLE
        k, v = kt((0, 2), (s, 2), (s + .01, h), (min(s + .06, .95), h * .35), (.95, 2), (1, 2))
        o.append(f'<rect x="{x0 + i * 6.6:.1f}" y="{base - 1}" width="4" height="2" rx="2" fill="{t["accent"]}">'
                 f'<animate attributeName="height" dur="{CYCLE}s" repeatCount="indefinite" keyTimes="{k}" values="{v}"/>'
                 f'<animate attributeName="y" dur="{CYCLE}s" repeatCount="indefinite" keyTimes="{k}" '
                 f'values="{";".join(f"{base - float(x) / 2:.1f}" for x in v.split(";"))}"/></rect>')
    k, v = kt((0, 0), (11.6 / CYCLE, 0), (11.7 / CYCLE, 1), (.96, 1), (1, 0))
    o.append(f'<text x="{rx + rw - 14}" y="{base + 5}" text-anchor="end" font-size="12" font-weight="700" fill="{t["ok"]}" opacity="0">'
             f'<animate attributeName="opacity" dur="{CYCLE}s" repeatCount="indefinite" keyTimes="{k}" values="{v}"/>✓ salida.mp4 · 60 s</text>')
    o.append('</g></svg>')
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    caption = first_row(ROOT / "samples/frame_descriptions.csv")
    narration = first_row(ROOT / "samples/narration.csv")
    (ROOT / "docs").mkdir(exist_ok=True)
    for theme in THEMES:
        p = ROOT / "docs" / f"banner-{theme}.svg"
        p.write_text(render(theme, caption, narration))
        print(p.relative_to(ROOT), f"{p.stat().st_size // 1024} KB")
