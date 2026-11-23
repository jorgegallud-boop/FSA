"""Replace drawn diagrams (groups of shapes) in a PUBLISHED deck copy with a picture of them.

    python scripts/rasterise_diagrams.py "source-pptx/05.pptx"

Why: extract_pptx.py turns loose shapes (boxes, arrows, labels) into a list of unconnected text
notes, so a cycle or timeline drawn in PowerPoint would be unreadable on the site. Run this after
publish_pptx.py, before extract_pptx.py. Windows only: it renders the slides with PowerPoint (COM).
PowerPoint is single-instance, so it only opens throw-away copies and never calls Quit().

Which shapes form each diagram is set in DIAGRAMS below, per deck file name and slide title.
"""
import os
import shutil
import sys
import tempfile

from PIL import Image
from pptx import Presentation
from pptx.util import Emu

DIAGRAMS = {
    "05.pptx": {
        # slide title: rule deciding which shapes belong to the diagram
        "Average maturation period": "all",                       # cash cycle
        "Sub-periods of the cycle": "all_but:Days that pass",     # timeline; intro sentence stays text
        "Inventory flows": "tables_and_lines",                    # the three T-accounts and their arrows
    },
}
SCALE = 2  # export at 2 x 1280 px wide


def in_diagram(shape, rule):
    if shape.is_placeholder:
        return False
    if rule == "all":
        return True
    if rule.startswith("all_but:"):
        return not (shape.has_text_frame and shape.text_frame.text.strip().startswith(rule.split(":", 1)[1]))
    if rule == "tables_and_lines":
        return getattr(shape, "has_table", False) or shape.shape_type == 9  # LINE / connector
    raise ValueError(rule)


def main(path):
    rules = DIAGRAMS.get(os.path.basename(path))
    if not rules:
        print("no diagrams configured for", path)
        return
    import win32com.client
    prs = Presentation(path)
    sw, sh = prs.slide_width, prs.slide_height
    targets = []
    for i, s in enumerate(prs.slides):
        title = s.shapes.title.text_frame.text.strip() if s.shapes.title is not None else ""
        if title in rules:
            shapes = [x for x in s.shapes if in_diagram(x, rules[title])]
            if shapes:
                targets.append((i, title, shapes))
    missing = set(rules) - {t for _, t, _ in targets}
    if missing:
        raise SystemExit("slides not found or already rasterised: %s" % sorted(missing))

    tmp = tempfile.mkdtemp()
    try:
        # 1. a copy in which each target slide keeps ONLY its diagram shapes (white background)
        only = Presentation(path)
        for i, _, shapes in targets:
            keep = {x.shape_id for x in shapes}
            tree = only.slides[i].shapes._spTree
            for x in list(only.slides[i].shapes):
                if x.shape_id not in keep:
                    tree.remove(x._element)
        only_path = os.path.join(tmp, "only.pptx")
        only.save(only_path)

        # 2. export those slides with PowerPoint
        app = win32com.client.Dispatch("PowerPoint.Application")
        pres = app.Presentations.Open(only_path, True, False, False)
        try:
            wpx, hpx = 1280 * SCALE, 960 * SCALE
            for i, _, _ in targets:
                pres.Slides.Item(i + 1).Export(os.path.join(tmp, "s%d.png" % i), "PNG", wpx, hpx)
        finally:
            pres.Close()

        # 3. crop to the diagram and swap the shapes for the picture
        for i, title, shapes in targets:
            pad = Emu(int(0.15 * 360000))
            l = max(0, min(x.left for x in shapes) - pad)
            t = max(0, min(x.top for x in shapes) - pad)
            r = min(sw, max(x.left + x.width for x in shapes) + pad)
            b = min(sh, max(x.top + x.height for x in shapes) + pad)
            im = Image.open(os.path.join(tmp, "s%d.png" % i))
            fx, fy = im.width / sw, im.height / sh
            crop = im.crop((int(l * fx), int(t * fy), int(r * fx), int(b * fy)))
            png = os.path.join(tmp, "crop%d.png" % i)
            crop.save(png, optimize=True)
            slide = prs.slides[i]
            for x in shapes:
                x._element.getparent().remove(x._element)
            pic = slide.shapes.add_picture(png, l, t, r - l, b - t)
            pic.name = "Diagram (rasterised)"
            print("slide %d %r: %d shapes -> picture %dx%d px" % (i + 1, title, len(shapes), crop.width, crop.height))
        prs.save(path)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main(sys.argv[1])
