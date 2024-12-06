import math
from ..base import Element, Manager
from dektools.num import near_zero
from ...utils.path import path_text


class TextPath(Element):
    spec = dict(
        cur=0.0, ac=0.0, g=0.1,
        ff='', fs='', fw='', fy=1.0,
        f='black',
        t='',
    )

    def path(self, proxy):
        raise NotImplementedError()

    def draw(self, proxy):
        texts = {}
        for i, (c, (x, y, a)) in enumerate(path_text(
                self.path(proxy), proxy.t, proxy.cur, proxy.ac, proxy.g * self.width
        )):
            texts["text " + "-" * i] = {
                "transform": f"translate({x},{y}) rotate({a}) scale(1,{proxy.fy})",
                "+": c
            }
        return {
            "g": {
                "text-anchor": "middle",
                "dominant-baseline": "central",
                "font-family": proxy.ff,
                "font-size": self.pv(proxy.fs),
                "font-weight": self.pv(proxy.fw),
                "fill": proxy.f,
                "+": texts
            }
        }


@Manager.element
class TextPathCircle(TextPath):
    spec = dict(
        **TextPath.spec,
        x=lambda w: w / 2, y=lambda _, h: h / 2,
        a=lambda w: w / 2, b=lambda _, h: h / 2,
        p=1,  # percent
    )

    def path(self, proxy):
        rx = proxy.a * proxy.p
        ry = proxy.b * proxy.p
        return (
            f"M{proxy.x} {proxy.y + ry}"
            f"A{rx} {ry} 0 1 1 {proxy.x + rx * math.sin(near_zero)} {proxy.y + ry * math.cos(near_zero)}"
        )
