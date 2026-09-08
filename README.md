# Financial Statement Analysis — course site

Static site with the slide decks for the course (taught in English), built from
the original PowerPoint files. Published with GitHub Pages at:

https://jorgegallud-boop.github.io/FSA/

## Structure

```
index.html              the site — self-contained, no build step needed to view it
scripts/
  template.html         page shell (HTML/CSS/JS) with the JSON placeholders
  extract_pptx.py       source-pptx/*.pptx  ->  data/deck_data.json   (needs python-pptx)
  build_site.py         template.html + data/*.json  ->  index.html
data/
  deck_data.json        slide content extracted from the decks (generated)
  overrides.json        hand-written fixes layered on top of deck_data.json
  about.json            content of the "About the course" page
  materials.json        per-unit "Exercises & materials" pages
source-pptx/            the original .pptx files
materials/              exercise statements + reference files, served as downloads
.github/workflows/      CI that rebuilds index.html on every push
```

`overrides.json` is where slide titles, image captions and the hand-built
concept diagrams live. It is merged over `deck_data.json` **in the browser**, so
re-extracting the decks never wipes those fixes.

## Updating the site

**You do not need Python.** Edit the relevant file, commit, push — the GitHub
Action rebuilds `index.html` and commits it back.

- Fix a title / caption / diagram → edit `data/overrides.json`
- Edit the About page → edit `data/about.json`
- Add / change exercises or reference material → edit `data/materials.json` and,
  for a new download, add the file under `materials/` (no spaces in the name)
- Change the layout, styling or behaviour → edit `scripts/template.html`
- Replace a slide deck → drop the new file in `source-pptx/` (same name); the
  Action re-runs `extract_pptx.py` automatically

To build locally instead (optional):

```
pip install python-pptx        # only needed if a .pptx changed
python scripts/extract_pptx.py # only needed if a .pptx changed
python scripts/build_site.py
```

### Preview locally

`index.html` opens straight from disk. To exercise it exactly as served, run any
static file server from this folder (e.g. `python -m http.server`) and open the
printed URL.
