# FSA course site — status & notes

## What this is

A static mini-site with the slide decks for the "Financial Statement Analysis"
course (taught in English), converted from PowerPoint to a self-contained HTML
site for Jorge to share with students and update through the course.

Repo: `https://github.com/jorgegallud-boop/FSA` · live at
`https://jorgegallud-boop.github.io/FSA/`

Local working copy: `OneDrive - UVa\OTROS\Claude\FSA` (moved here 2026-09-09 from
`OneDrive - UVa\DOCENCIA\FSA\site`). The raw course materials stay in
`DOCENCIA\FSA`; when a deck changes, copy it into this repo's `source-pptx/` and
push. From 2026-09-10 Jorge works on this from **one machine only** (university),
so the folder can stay inside OneDrive; normal flow is edit → commit → push (no
`git pull` needed).

## How it is built (see README.md for the short version)

- `scripts/template.html` — the whole page (HTML/CSS/JS) with one `__*_JSON__`
  token per `data/*.json` file (deck, overrides, about, materials, glossary,
  accounts).
- `scripts/build_site.py` — substitutes the `data/*.json` files into the template
  and writes `index.html`. No content processing; just string replace.
- PWA static files at the repo root — `manifest.webmanifest`, `sw.js`, the icons
  — are **not** built; Pages serves them as-is. `scripts/make_icons.py` (Pillow)
  regenerates the icon set when the mark changes.
- `scripts/extract_pptx.py` — regenerates `data/deck_data.json` from
  `source-pptx/*.pptx` (needs `python-pptx`). Speaker notes are deliberately not
  extracted. `#`-prefixed speaker-cue text boxes are dropped.
- The **overrides layer**: `data/overrides.json` is merged over `deck_data.json`
  *in the browser* (`applyOverrides()` in the template). This is why re-running
  the extractor never disturbs the hand fixes. Keyed by unit id + 1-based slide
  number in `deck_data.json` (= the site number unless the unit uses `drop`).
- `.github/workflows/build.yml` — on every push touching `source-pptx/`,
  `scripts/`, `data/` or the workflow, CI rebuilds `index.html` (and re-extracts
  if a `.pptx` changed) and commits the result. So **no local Python is needed**
  for normal edits.

## Done in the second session (Claude Code)

- Repo moved into `FSA/site/` inside the course folder.
- Split the monolithic `build_site.py` into `template.html` + a tiny builder.
- Added the `overrides.json` layer and, on top of `deck_data.json`:
  - removed the `#faithful_image` speaker tag (U1);
  - fixed the "Unit 1 / introduction" divider capitalisation;
  - gave the six untitled PGC balance-sheet / income-statement screenshots real
    titles + captions (U2);
  - rebuilt the three PowerPoint T-account "shape" slides as CSS concept
    diagrams instead of broken HTML tables (U2 slides 6, 7, 12);
  - renamed the "TH" slides to "Talent Hackers …" and labelled the
    Talent Hackers / Catenon worked-example company (U4);
  - disambiguated the duplicate "Example 1/2/3" slide titles (U4).
- New **About the course** page (`#/about`), content in `data/about.json`,
  summarised from `00 UVa_GuiaDocente_2026_english_rev.docx`. Linked from the
  index footer.
- `index.html` now carries `<meta charset>` + viewport and per-view
  `document.title`; images have alt text and a "click to enlarge" hint.
- CI workflow added.

## Third session (2026-09-08)

- Pushed to GitHub; Pages live at https://jorgegallud-boop.github.io/FSA/.
- Added **per-unit exercise / reference pages** — separate routes
  `#/unitN/exercises` and `#/unitN/references`, content in `data/materials.json`
  (`.exercises` / `.references`), rendered by `renderExercises()` /
  `renderReferences()`. Linked separately from the index (sub-rows under the
  unit) and the deck top bar.
  - U2: MAPACHE / CUERDA / LINUX (financial statements) + two corporate-income-tax
    exercises, all transcribed from the `Exercises` .docx; CUERDA's given
    statements and the small CIT tables are rendered inline.
  - U3: the cash-flow exercise (`03 Exercise CF`) with its income statement, and
    TRES, S.A. (`03 Exercise complete` — a .docx despite the `.doc` extension)
    rendered as prompt + note pointing to the download (its comparative balance
    sheet / P&L / 6 notes / blank templates are large and left in the file only).
  - Reference material for U2: FS models (`02 Models` PDF + Excel) and the
    Spanish GAAP text (`02 SGAP.pdf`).
  - Source files copied into `site/materials/` with clean, space-free names and
    served by Pages as downloads. `.gitattributes` marks doc/docx/xlsx/pdf binary.
- `data/materials.json` is keyed by unit id; slide-number-independent, so it is
  unaffected by re-extraction. Only U2 and U3 have entries.

## Fourth session (2026-09-09)

- `01 Slides.pptx` refreshed (Jorge's course-evaluation edits).
- Jorge split the old 15-slide unit 4 into `04.pptx` ("Financial Analysis",
  3 slides) + `05.pptx` ("Profitability Analysis", 13 slides). Added `unit5` to
  `extract_pptx.py` FILES and to `ORDER`. The old `unit4` overrides moved to
  `unit5` verbatim (slide order matched); new `unit4` only fixes its divider.
- **`overrides.json` `_config.hidden`** = `["unit3","unit4","unit5"]`. Hidden
  units get no index row and no nav but still build and are reachable by direct
  `#/unitN/1` link (for previewing). Empty the list to publish. Wiring:
  `visibleUnits()` / `isHidden()` in the template.
- **Bug fixed:** `extract_pptx.py` `TITLE_LAYOUTS` matched by `startswith`, so
  `"título"` caught the normal content layout `"Título y objetos"` and, on the
  first real CI run of this (session-2) extractor, every content slide came out
  as a divider with its bullets/tables dropped. Now matches the layout name
  exactly. The workflow also re-extracts when `scripts/extract_pptx.py` changes,
  not only when a `.pptx` does.
- **Glossary** (`data/glossary.json`, `#/glossary`) and **PGC accounts**
  (`data/accounts.json`, `#/accounts`) support pages added. English. Accounts
  are a course-curated subset of the PGC Part-4 chart (English names from
  `02 SGAP.pdf`). Published 2026-09-09 (`_config.hiddenPages` now empty); linked
  from the index footer.

## Fifth session (2026-09-10)

- **Unit 1 trimmed to just the unit.** The three pre-unit slides (course-title,
  "Course programme", "Course evaluation") are dropped, so U1 now opens on its
  "Unit 1 — Introduction" divider like every other unit. Their substance already
  lived on the About page (Contents + Assessment); added one line there about the
  exam calendar. This retires the "course-evaluation slide" to-do.
  - New **`drop`** key in `overrides.json` (bool, removes a slide from the
    rendered deck). `applyOverrides()` collects dropped indices and splices them
    **after** applying every other keyed fix, so override keys stay aligned with
    positions in `deck_data.json` no matter what is dropped. `unit1` keys `1`,
    `2`, `3` = `{drop:true}`; keys `4`/`7` unchanged and still land correctly.
- **PWA / installable app.** `manifest.webmanifest`, `sw.js` and the icon set
  (`icon-192/512.png`, `apple-touch-icon.png`, `favicon-32.png`, `favicon.svg`)
  live at the repo root and are served by Pages as-is. `scripts/make_icons.py`
  (needs Pillow) regenerates the icons — an "FSA" serif wordmark, cream on teal.
  Head links + apple/theme-color meta + the SW registration are in
  `template.html`. SW = network-first for same-origin, cache-first for Google
  Fonts, offline navigations fall back to the cached `index.html`. Bump `CACHE`
  in `sw.js` to force old entries out. Install: Android/desktop Chrome from the
  manifest; iOS via Add to Home Screen (apple-touch-icon + `apple-mobile-web-app-
  capable`). Verified live 2026-09-10: SW active and controlling, cache populated,
  manifest + icons all 200. "Add to Home Screen" on a real phone still to confirm.
- **Glossary search.** `#/glossary` has a live filter box: `renderGlossary()`
  emits `.gl-search` + a clear button + a `.gl-nomatch` line; `wireGlossarySearch()`
  matches the query against the term (`<dt>`) only, not the definition
  (diacritic-folded via `foldText()`), hides non-matching items and empty
  sections, and hides the section-jump nav while a query is active. `#/accounts`
  is unchanged.
- **Glossary content.** Added Income / Expense / Collection / Payment to *Income
  statement items* (to teach that income ≠ collection and expense ≠ payment);
  expanded "Asset" / "Liability" with the economic-structure / financial-structure
  framing (use of funds vs origin of funds). Also linked the Weygandt textbook
  (About → Main references) to its authorised Campus Virtual copy; About list
  items now accept `{t, href, suffix}`.
- Office 145 now shows next to the email (index footer + About → Contact).
- **QR page + full-screen key.** `#/qr` (`renderQr()`, linked from the index
  footer) shows the `qr.svg` code — clickable, links to `SITE_URL`
  (`https://jorgegallud-boop.github.io/FSA/`, the string `scripts/make_qr.py`
  encodes; needs `segno`). `qr.svg` + `qr.png` at the repo root. Press **F**
  anywhere (except in a text field) to toggle the Fullscreen API —
  `toggleFullscreen()` on the global keydown handler.

## Not done / next steps

- Confirm "Add to Home Screen" gives a standalone window with the FSA icon on a
  real phone (Android Chrome / iOS Safari).
- `gh` is installed (portable, `%LOCALAPPDATA%\Programs\GitHubCLI\bin`) but not
  `gh auth login`'d in the bash context — the push works via git + Git
  Credential Manager. Old fine-grained PAT was revoked.
- Possible later: exercises/materials for U1 and U4; more reference material per
  unit as it comes up.
- Possible later: expand into a course hub (syllabus already on the About page)
  with the exercise sheets, Excel models and annual-report cases from the parent
  `FSA/` folder.

## Design decisions carried over (keep unless Jorge asks otherwise)

- English only, no Spanish strings on the page.
- Only the 4 English decks (01–04). `02.3 Auditoria - Impuestos.pptx` is a
  different course and stays out.
- Speaker notes not shown to students.
- Dense PGC reference screenshots kept as images with click-to-zoom, not rebuilt
  as tables. Clean numeric tables ARE real HTML tables.
- "Ledger" aesthetic: cool paper background, deep teal accent, hairline rules.
  Newsreader / Public Sans / IBM Plex Mono. Light + dark via CSS custom
  properties.
- Hash routing (`#/unit1/7`, `#/about`) so links are shareable.
