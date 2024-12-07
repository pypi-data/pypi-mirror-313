import os
import typer
from typing import List
from typing_extensions import Annotated

app = typer.Typer(add_completion=False)


@app.command()
def trans(src, outputs: Annotated[List[str], typer.Argument()] = None, sizes=''):
    if not outputs:
        return
    if os.path.splitext(src)[-1].lower() == '.svg':
        from ..image.svg import trans_image
    else:
        from ..image.core import trans_image_core as trans_image
    trans_image(src, outputs, parse_sizes(sizes))


def parse_sizes(sizes):
    if sizes:
        ss = [int(n) for n in sizes.split(',')]
        return list(zip(ss[::2], ss[1::2]))
