import json, base64, os, re
from pptx import Presentation
from pptx.util import Emu

SRC = os.path.join(os.path.dirname(__file__), "..", "source-pptx")
FILES = [
    ("unit1", "01 Slides.pptx", "Unit 1", "Introduction"),
    ("unit2", "02.pptx", "Unit 2", "Financial Statements I"),
    ("unit3", "03.pptx", "Unit 3", "Financial Statements II"),
    ("unit4", "04.pptx", "Unit 4", "Financial Statement Analysis"),
]

def clean(t):
    if t is None:
        return ""
    t = t.replace("\x0b", "\n").replace("\x0c", "\n")
    t = re.sub(r"[ \t]+\n", "\n", t)
    return t.strip()

def para_text(p):
    return "".join(r.text for r in p.runs) or p.text

def extract_table(shape):
    tbl = shape.table
    rows = []
    for r_i, row in enumerate(tbl.rows):
        cells = []
        for c_i, cell in enumerate(row.cells):
            if cell.is_spanned:
                continue
            colspan = cell.span_width if cell.is_merge_origin else 1
            rowspan = cell.span_height if cell.is_merge_origin else 1
            cells.append({
                "text": clean(cell.text),
                "colspan": colspan,
                "rowspan": rowspan,
            })
        rows.append(cells)
    return rows

def img_datauri(part):
    ext = part.partname.ext.lower()
    mime = {"png": "image/png", "jpeg": "image/jpeg", "jpg": "image/jpeg",
            "gif": "image/gif", "emf": "image/emf", "wmf": "image/wmf"}.get(ext, "application/octet-stream")
    if ext in ("emf", "wmf"):
        return None
    b64 = base64.b64encode(part.blob).decode("ascii")
    return f"data:{mime};base64,{b64}"

def extract_deck(path):
    p = Presentation(path)
    slides_out = []
    for slide in p.slides:
        is_title = slide.slide_layout.name == "Diapositiva de título"
        title_text = ""
        subtitle_text = ""
        bullets = []
        asides = []
        tables = []
        images = []
        for shape in slide.shapes:
            nm = shape.name
            if shape.has_text_frame:
                txt = clean(shape.text_frame.text)
                if not txt:
                    continue
                if nm.startswith("Título") or nm.startswith("Titulo"):
                    title_text = txt
                elif nm.startswith("Subtítulo") or nm.startswith("Subtitulo"):
                    subtitle_text = txt
                elif nm.startswith("Marcador de contenido") or nm.startswith("Marcador de texto"):
                    for para in shape.text_frame.paragraphs:
                        t = clean(para_text(para))
                        if t:
                            bullets.append({"level": para.level, "text": t})
                elif nm.startswith("Marcador de número"):
                    pass
                elif nm.startswith("TextBox") or "Cuadro de texto" in nm:
                    asides.append(txt)
                else:
                    # fallback: treat unknown text placeholders as bullets
                    if nm.startswith("Marcador"):
                        for para in shape.text_frame.paragraphs:
                            t = clean(para_text(para))
                            if t:
                                bullets.append({"level": para.level, "text": t})
            if getattr(shape, "has_table", False):
                tables.append(extract_table(shape))
            if shape.shape_type == 13:  # PICTURE
                try:
                    part = shape.image
                    uri = None
                    ext = part.ext.lower()
                    if ext not in ("emf", "wmf"):
                        mime = {"png": "image/png", "jpeg": "image/jpeg", "jpg": "image/jpeg", "gif": "image/gif"}.get(ext, "application/octet-stream")
                        uri = f"data:{mime};base64,{base64.b64encode(part.blob).decode('ascii')}"
                    if uri:
                        images.append({
                            "src": uri,
                            "w": shape.width, "h": shape.height,
                        })
                except Exception as e:
                    pass
        slides_out.append({
            "isTitle": is_title,
            "title": title_text,
            "subtitle": subtitle_text,
            "bullets": bullets,
            "asides": asides,
            "tables": tables,
            "images": images,
        })
    return slides_out

deck_data = {}
for key, fname, unit_no, unit_name in FILES:
    path = os.path.join(SRC, fname)
    slides = extract_deck(path)
    deck_data[key] = {
        "unit": unit_no,
        "name": unit_name,
        "slides": slides,
    }
    print(key, fname, "->", len(slides), "slides")

out_path = os.path.join(os.path.dirname(__file__), "..", "data", "deck_data.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(deck_data, f, ensure_ascii=False)

sz = os.path.getsize(out_path)
print("json size MB:", sz / 1024 / 1024)
