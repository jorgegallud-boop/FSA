"""Generate the QR code for the site into the repo root.

    python scripts/make_qr.py

Needs `segno` (pure Python, no other deps). Run by hand if the site URL
changes; the output files are committed, so CI never runs this.

Encodes the GitHub Pages URL. Deep teal modules on white, quiet zone included.
"""

import os
import segno

ROOT = os.path.join(os.path.dirname(__file__), "..")
URL = "https://jorgegallud-boop.github.io/FSA/"
DARK = "#0f6b57"   # --accent
LIGHT = "#ffffff"

qr = segno.make(URL, error="q")
qr.save(os.path.join(ROOT, "qr.svg"), scale=8, border=4, dark=DARK, light=LIGHT)
qr.save(os.path.join(ROOT, "qr.png"), scale=16, border=4, dark=DARK, light=LIGHT)

for name in ("qr.svg", "qr.png"):
    p = os.path.join(ROOT, name)
    print("wrote", name, f"{os.path.getsize(p) / 1024:.1f} KB")
print("encodes:", URL)
