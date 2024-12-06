from typing import Iterable, Literal
from io import BytesIO
from PIL import Image as PilImage, ImageDraw, ImageFont
from dektools.func import FuncAnyArgs
from ..font import get_font_source


def get_spacing(font, spacing=None):
    if spacing is None:
        spacing = 1.0
    if isinstance(spacing, float):
        spacing = font.font.descent * spacing
    return spacing


def generate_image(text: str, size=100, angle=0, font=None, color=None, bgc=None, spacing=None):
    color = color or (0, 0, 0)
    bgc = bgc or (255, 255, 255)
    ftf = ImageFont.truetype(BytesIO(get_font_source(font)), size)
    spacing = get_spacing(ftf, spacing)
    image = PilImage.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    box = draw.multiline_textbbox((0, 0), text, font=ftf, spacing=spacing)
    image = PilImage.new('RGBA' if len(bgc) == 4 else 'RGB', (box[2], box[3] + ftf.font.descent), bgc)
    draw = ImageDraw.Draw(image)
    draw.text(box[:2], text, font=ftf, fill=color, spacing=spacing)
    if angle:
        image = image.rotate(angle, expand=True, fillcolor=bgc)
    return image


def get_text_size(font, text):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def get_text_box_info(font, text: Iterable[str], width):
    lines = ['']
    widths = [0]
    heights = [0]
    for word in text:
        t = lines[-1] + word
        w, h = get_text_size(font, t)
        if w > width:
            widths.append(w)
            heights.append(h)
            lines.append(word)
        else:
            lines[-1] += word
            widths[-1] = w
            heights[-1] = h
    return lines, heights, widths


def text_in_box(draw: ImageDraw, text: Iterable[str], xy, width, spacing=None, font=None, size=30, color=None,
                align: Literal['left', 'right', 'middle'] = 'left', hidden=None):
    ftf = ImageFont.truetype(BytesIO(get_font_source(font)), size)
    if color is None:
        color = (0, 0, 0)
    spacing = get_spacing(ftf, spacing)
    lines, heights, widths = get_text_box_info(ftf, text, width)
    x, y = xy
    cursor = 0
    hidden = FuncAnyArgs(hidden) if hidden else None
    for i, line in enumerate(lines):
        if align == 'left':
            offset = 0
        elif align == 'right':
            offset = width - widths[i]
        else:
            offset = (width - widths[i]) // 2
        if not hidden or not hidden(cursor + heights[i], cursor, i, len(lines)):
            draw.text((x + offset, y + cursor), line, font=ftf, fill=color)
        cursor += heights[i] + spacing


class Text:
    def __init__(self, s: str):
        self.content = s

    @property
    def block(self):
        return list(self.content)

    @property
    def words(self):
        result = []
        last_ascii = False
        for c in self.content:
            if c.isascii():
                if c.isalpha():
                    if last_ascii:
                        result[-1] += c
                    else:
                        result.append(c)
                    last_ascii = True
                else:
                    result.append(c)
                    last_ascii = False
            else:
                result.append(c)
                last_ascii = False
        return result
