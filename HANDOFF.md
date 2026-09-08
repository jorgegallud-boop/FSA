# FSA course site — status & notes

## What this is

A static mini-site with the slide decks for the "Financial Statement Analysis"
course (taught in English), converted from PowerPoint to a self-contained HTML
site for Jorge to share with students and update through the course.

Repo: `https://github.com/jorgegallud-boop/FSA` (not pushed yet — see below)

## How it is built (see README.md for the short version)

- `scripts/template.html` — the whole page (HTML/CSS/JS) with three tokens:
  `__DECK_JSON__`, `__OVERRIDES_JSON__`, `__ABOUT_JSON__`.
- `scripts/build_site.py` — substitutes the three `data/*.json` files into the
  template and writes `index.html`. No content processing; just string replace.
- `scripts/extract_pptx.py` — regenerates `data/deck_data.json` from
  `source-pptx/*.pptx` (needs `python-pptx`). Speaker notes are deliberately not
  extracted. `#`-prefixed speaker-cue text boxes are dropped.
- The **overrides layer**: `data/overrides.json` is merged over `deck_data.json`
  *in the browser* (`applyOverrides()` in the template). This is why re-running
  the extractor never disturbs the hand fixes. Keyed by unit id + 1-based slide
  number as shown in the site.
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

## Not done / next steps

- **Course-evaluation slide (U1)**: Jorge is fixing the stale dates / bullet
  nesting / "calification" typo directly in `01 Slides.pptx`. After that, drop
  the new pptx in `source-pptx/` and push (CI re-extracts).
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
