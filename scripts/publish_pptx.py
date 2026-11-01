"""Copy a master deck into source-pptx/ WITHOUT its hidden slides.

    python scripts/publish_pptx.py "<path to master .pptx>" source-pptx/02.pptx

The repo (and GitHub Pages) is public, so anything in source-pptx/ can be
downloaded. Slides hidden in PowerPoint (e.g. exercise solutions) are removed
from the copy, not just skipped by extract_pptx.py.
"""
import re
import shutil
import sys
import tempfile
import zipfile

from pptx import Presentation

src, dst = sys.argv[1], sys.argv[2]
prs = Presentation(src)
sld_ids = prs.slides._sldIdLst
removed = []
for n, sld_id in enumerate(list(sld_ids), 1):
    rid = sld_id.rId
    slide = prs.part.related_part(rid)
    if slide._element.get("show") == "0":
        title = slide.slide.shapes.title.text_frame.text if slide.slide.shapes.title else ""
        prs.part.drop_rel(rid)
        sld_ids.remove(sld_id)
        removed.append("%d (%s)" % (n, title))
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
