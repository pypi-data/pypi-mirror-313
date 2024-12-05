import re
from matplotlib import font_manager


def is_font_family(s):
    return re.fullmatch(r'^[ 0-9a-zA-Z_-]+$', s)


def find_font_path(font_name):
    return font_manager.findfont(font_manager.FontProperties(family=font_name))


def get_font_source(name):
    if name is None:
        name = 'simsun'
    if isinstance(name, str):
        if is_font_family(name):
            font_path = find_font_path(name)
        else:
            font_path = name
        with open(font_path, 'rb') as f:
            return f.read()
    elif isinstance(name, bytes):
        return name
    else:
        return name.getvalue()
