import fitz
from itertools import chain
from io import BytesIO
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from ..core import trans_image_core


def svg_to_png(src, sizes=None, dpi=None):
    if dpi is None:
        if sizes:
            dpi = max(chain(*sizes))
        else:
            dpi = 256
    drawing = svg2rlg(src)
    pdf = renderPDF.drawToString(drawing)
    doc = fitz.Document(stream=pdf)
    pix = doc.load_page(0).get_pixmap(alpha=True, dpi=dpi)
    bytes_out = BytesIO()
    pix.pil_save(bytes_out, "PNG")
    return bytes_out


def trans_image(src, outputs, sizes=None, dpi=None):
    trans_image_core(svg_to_png(src, sizes, dpi), outputs, sizes)
