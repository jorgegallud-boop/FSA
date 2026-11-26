"""Copy a master deck into source-pptx/ WITHOUT its hidden slides.

    python scripts/publish_pptx.py "<path to master .pptx>" "source-pptx/02 Slides.pptx"

The repo (and GitHub Pages) is public, so anything in source-pptx/ can be
downloaded. Slides hidden in PowerPoint (e.g. exercise solutions) are removed
from the copy, not just skipped by extract_pptx.py.

Some slides stay visible in class but must not reach the site. They are listed
in EXCLUDE below by CONTENT (not by number, so the rule survives reordering);
every rule must match at least one slide, otherwise the script stops so a
reworded slide is noticed instead of slipping through.
"""
import re
import shutil
import sys
import tempfile
import zipfile

import os

from pptx import Presentation


def _text(slide):
    out = []
    for sh in slide.shapes:
        if sh.has_text_frame:
            out.append(sh.text_frame.text)
        if getattr(sh, "has_table", False):
            out += [c.text for r in sh.table.rows for c in r.cells]
    return " ".join(out)


def _table_header_has(slide, *words):
    for sh in slide.shapes:
        if getattr(sh, "has_table", False):
            head = {c.text.strip().lower() for c in sh.table.rows[0].cells}
            if all(w.lower() in head for w in words):
                return True
    return False


# deck file name -> [(description, predicate on the slide)]
EXCLUDE = {
    "05.pptx": [
        ("sources and uses of funds solution (table with Origin and Use columns)",
         lambda s: _table_header_has(s, "Origin", "Use")),
        ("Orbis company card of Talent Hackers / Catenon",
         lambda s: "BvD ID" in _text(s)),
    ],
}

src, dst = sys.argv[1], sys.argv[2]
rules = EXCLUDE.get(os.path.basename(dst), [])
hits = {d: 0 for d, _ in rules}
prs = Presentation(src)
sld_ids = prs.slides._sldIdLst
removed = []
for n, sld_id in enumerate(list(sld_ids), 1):
    rid = sld_id.rId
    slide = prs.part.related_part(rid)
    why = "hidden" if slide._element.get("show") == "0" else None
    for d, pred in rules:
        if why is None and pred(slide.slide):
            why, hits[d] = d, hits[d] + 1
    if why:
        title = slide.slide.shapes.title.text_frame.text if slide.slide.shapes.title else ""
        prs.part.drop_rel(rid)
        sld_ids.remove(sld_id)
        removed.append("%d (%s) [%s]" % (n, title, why))
missing = [d for d, k in hits.items() if k == 0]
if missing:
    sys.exit("EXCLUDE rule(s) matched no slide, check the deck: %s" % missing)
prs.save(dst)

# docProps/app.xml still lists every slide title (python-pptx does not refresh it):
# drop that optional list and fix the counters so no trace of the hidden slides remains.
tmp = tempfile.mktemp(suffix=".pptx")
with zipfile.ZipFile(dst) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "docProps/app.xml":
            xml = data.decode("utf-8")
            xml = re.sub(r"<HeadingPairs>.*?</HeadingPairs>", "", xml, flags=re.S)
            xml = re.sub(r"<TitlesOfParts>.*?</TitlesOfParts>", "", xml, flags=re.S)
            xml = re.sub(r"<Slides>\d+</Slides>", "<Slides>%d</Slides>" % len(prs.slides), xml)
            xml = re.sub(r"<HiddenSlides>\d+</HiddenSlides>", "<HiddenSlides>0</HiddenSlides>", xml)
            data = xml.encode("utf-8")
        zout.writestr(item, data)
shutil.move(tmp, dst)
print("wrote", dst, "| slides:", len(prs.slides), "| hidden slides removed:", removed or "none")
