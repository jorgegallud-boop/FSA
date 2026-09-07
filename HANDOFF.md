# FSA course site — handoff to Claude Code

Context for continuing this project locally with Claude Code. Paste this file's
content (or just point Claude Code at it) when you open the `FSA/` folder.

## What this is

A mini-site with the slide decks for the "Financial Statement Analysis"
course (taught in English), converted from PowerPoint to a self-contained
HTML site — built for Jorge to share with students and update over the
course.

Currently live (built via Claude/Cowork, not this repo yet):
https://claude.ai/code/artifact/3116f639-59eb-48dd-863d-1c5365c95baf

## What's in this folder

```
FSA/
  index.html              the site itself (self-contained, no build step to view)
  source-pptx/            original .pptx files it's generated from
    01 Slides.pptx        Unit 1 — Introduction (13 slides)
    02.pptx                Unit 2 — Financial Statements I (27 slides)
    03.pptx                Unit 3 — Financial Statements II (9 slides)
    04.pptx                Unit 4 — Financial Statement Analysis (15 slides)
  data/deck_data.json     text/tables/images extracted from the pptx files
  scripts/extract_pptx.py reads source-pptx/*.pptx -> writes data/deck_data.json
  scripts/build_site.py   reads data/deck_data.json -> writes index.html
  README.md               same instructions, shorter
```

Regenerating after replacing a file in `source-pptx/`:
```
pip install python-pptx
cd scripts
python3 extract_pptx.py
python3 build_site.py
```

## Immediate task: push to GitHub

Target repo (already created, empty): `https://github.com/jorgegallud-boop/FSA`

The `.git` history is already included in this folder with one commit ready.
From inside `FSA/`:
```
gh auth login          # browser-based login, no token needed
git push -u origin HEAD:main
```
Then, if you want it hosted via GitHub Pages: repo Settings → Pages → Source
= "Deploy from a branch" → `main` / `/ (root)`. Site ends up at
`https://jorgegallud-boop.github.io/FSA/`.

(A fine-grained PAT scoped to this repo was generated earlier and pasted into
a chat session — low risk since the repo was empty and it's a single-repo
token, but worth revoking/regenerating at github.com/settings/tokens for
hygiene, since it's no longer needed with browser-based `gh auth login`.)

## Design decisions already made (keep these unless Jorge asks otherwise)

- **English only** — all UI copy and content must be in English (the course
  is taught in English). No Spanish strings anywhere on the page.
- **Scope** — only the 4 English-taught decks (01–04) are in the site.
  `02.3 Auditoria - Impuestos.pptx` (also in the source FSA folder) was
  deliberately excluded: it's a different course, in Spanish, taught by
  other instructors (David de Juan / Marina Zurdo), different template.
- **Speaker notes are not shown** to students — they exist in several slides
  (esp. Unit 4, 11/15 slides) but were left out of the extraction/render on
  purpose. Easy to add back as a toggle if Jorge wants it.
- **Dense reference images** (the official PGC balance-sheet model screenshots
  in Unit 2) are embedded as-is with a click-to-zoom lightbox, not rebuilt as
  HTML tables — recreating that legal table faithfully as text was judged
  higher-risk than keeping the image.
- **Native PPT tables** (clean numeric tables, e.g. Unit 4 ratio examples) ARE
  rebuilt as real HTML tables with tabular-nums right-alignment — these
  convert cleanly and look better than the original.
- **Aesthetic**: "ledger" concept — cool paper background (not the common
  warm-cream AI look), deep teal accent, hairline rules instead of cards.
  Fonts: Newsreader (headings/serif), Public Sans (body/UI), IBM Plex Mono
  (numbers, unit index, slide counters). Both light and dark mode supported
  via CSS custom properties (see `:root` / `prefers-color-scheme` /
  `[data-theme]` in `index.html`).
- **Navigation**: hash-based routing (`#/unit1/7` = unit1, slide 7) so links
  are shareable/bookmarkable. Keyboard arrows, click/tap on left/right thirds
  of the stage, and explicit Prev/Next buttons all work.
- One quirk left as-is: Unit 1's "introduction" divider slide renders in
  lowercase because that's the literal text in the pptx (likely a small-caps
  visual effect in PowerPoint that doesn't carry over to plain text
  extraction) — cosmetic, not fixed.

## Open items / natural next steps

- Push to GitHub + decide on GitHub Pages vs. keeping the Claude Artifact
  link (or both — they can coexist, just keep them in sync manually).
- As the course progresses, Jorge will likely ask to add more units/slides —
  just drop the new `.pptx` in `source-pptx/`, add an entry to the `FILES`
  list in `scripts/extract_pptx.py`, and re-run both scripts.
- If Jorge wants instructor notes visible (toggle), the notes text just
  needs to be extracted again in `extract_pptx.py` (removed in the current
  version) and rendered behind a button in `index.html`.
