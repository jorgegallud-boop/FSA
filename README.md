# Financial Statement Analysis — course slides

Static site with the slide decks for the four units of the course, built from
the original PowerPoint files. Published with GitHub Pages at:

https://jorgegallud-boop.github.io/FSA/

## Structure

- `index.html` — the site itself (self-contained, no build step needed to view it).
- `source-pptx/` — the original `.pptx` files the site is generated from.
- `data/deck_data.json` — text, tables and images extracted from the pptx files.
- `scripts/extract_pptx.py` — reads `source-pptx/*.pptx` with `python-pptx` and writes `data/deck_data.json`.
- `scripts/build_site.py` — reads `data/deck_data.json` and writes `index.html`.

## Updating the slides

1. Replace the relevant file in `source-pptx/` with the new version.
2. From the `scripts/` folder:
   ```
   pip install python-pptx
   python3 extract_pptx.py
   python3 build_site.py
   ```
3. Commit and push. GitHub Pages picks up `index.html` automatically.
