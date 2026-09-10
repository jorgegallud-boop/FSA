"""Generate the PWA / favicon image set into the repo root.

    python scripts/make_icons.py

Needs Pillow and a serif TTF (Georgia Bold on Windows, DejaVu Serif elsewhere).
Run by hand whenever the mark changes; the output PNGs are committed, so CI
never needs to run this.

Mark: "FSA" in a serif face, cool-paper cream on deep-teal, with the site's
hairline rule beneath — the same "ledger" palette as the page itself.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
TEAL = (15, 107, 87)        # --accent  #0f6b57
PAPER = (238, 241, 239)     # --paper   #eef1ef

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\georgiab.ttf",
    r"C:\Windows\Fonts\timesbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/Library/Fonts/Georgia Bold.ttf",
]


def font_path():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    raise SystemExit("no serif TTF found; edit FONT_CANDIDATES")


FONT = font_path()


def blend(fg, bg, a):
    return tuple(round(f * a + b * (1 - a)) for f, b in zip(fg, bg))


def render(size, *, full_bleed, text_frac):
    """One square icon. full_bleed=True keeps the teal edge-to-edge (maskable /
    apple-touch); False insets the teal into a rounded tile on transparency."""
    scale = 4
    S = size * scale
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if full_bleed:
        d.rectangle([0, 0, S, S], fill=TEAL + (255,))
    else:
        r = int(S * 0.22)
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=r, fill=TEAL + (255,))

    f = ImageFont.truetype(FONT, int(S * text_frac))
    cx, cy = S / 2, S / 2 - S * 0.04
    d.text((cx, cy), "FSA", font=f, fill=PAPER + (255,), anchor="mm")

    # hairline rule beneath the wordmark
    rule_w = S * 0.30
    rule_y = S * 0.70
    rule_h = max(1, int(S * 0.014))
    d.rectangle([cx - rule_w / 2, rule_y, cx + rule_w / 2, rule_y + rule_h],
                fill=blend(PAPER, TEAL, 0.6) + (255,))

    return img.resize((size, size), Image.LANCZOS)


def save(img, name):
    path = os.path.join(ROOT, name)
    img.save(path)
    print("wrote", name, f"{os.path.getsize(path) / 1024:.1f} KB")


# maskable / apple: full-bleed, wordmark kept inside the ~80% safe zone
save(render(512, full_bleed=True, text_frac=0.34), "icon-512.png")
save(render(192, full_bleed=True, text_frac=0.34), "icon-192.png")
save(render(180, full_bleed=True, text_frac=0.34), "apple-touch-icon.png")
save(render(32, full_bleed=True, text_frac=0.40).convert("RGB"), "favicon-32.png")

with open(os.path.join(ROOT, "favicon.svg"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        '  <rect width="64" height="64" fill="#0f6b57"/>\n'
        '  <text x="32" y="34" text-anchor="middle" dominant-baseline="central"\n'
        '        font-family="Georgia, \'Times New Roman\', serif" font-weight="700"\n'
        '        font-size="24" fill="#eef1ef">FSA</text>\n'
        '  <rect x="22" y="42" width="20" height="1.6" fill="#7fb0a4"/>\n'
        '</svg>\n'
    )
print("wrote favicon.svg")
