from io import BytesIO
from PIL import Image as PilImage, ImageDraw, ImageFont
from ..font import get_font_source


def generate_image(text: str, size=100, angle=0, font=None, color=None, bgc=None, spacing=None):
    color = color or (0, 0, 0)
    bgc = bgc or (255, 255, 255)
    ftf = ImageFont.truetype(BytesIO(get_font_source(font)), size)
    if spacing is None:
        spacing = ftf.font.descent
    image = PilImage.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    box = draw.multiline_textbbox((0, 0), text, font=ftf, spacing=spacing)
    image = PilImage.new('RGBA' if len(bgc) == 4 else 'RGB', (box[2], box[3] + ftf.font.descent), bgc)
    draw = ImageDraw.Draw(image)
    draw.text(box[:2], text, font=ftf, fill=color, spacing=spacing)
    if angle:
        image = image.rotate(angle, expand=True, fillcolor=bgc)
    return image
