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

## Not done / next steps

- **Push to GitHub.** `gh` is not installed on this machine. Options:
  `winget install GitHub.cli` then `gh auth login`, or push over HTTPS with a
  PAT, or use GitHub Desktop. The repo has a clean commit history on `master`;
  the workflow triggers on `main`, so push as `main`
  (`git push -u origin HEAD:main`) or rename the branch.
- **GitHub Pages**: repo Settings → Pages → Deploy from a branch → `main` / root.
  Ends up at `https://jorgegallud-boop.github.io/FSA/`.
- **Course-evaluation slide (U1)**: Jorge is fixing the stale dates / bullet
  nesting / "calification" typo directly in `01 Slides.pptx`. After that, drop
  the new pptx in `source-pptx/` and push (CI re-extracts).
- **Revoke** the old fine-grained PAT at github.com/settings/tokens — no longer
  needed once `gh auth login` (browser) is used.
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
