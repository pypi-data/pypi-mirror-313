import math
from ..base import Element, Manager


@Manager.element
class Circle(Element):
    spec = dict(
        c='black', f='none', w=1, i=True,
        x=lambda w: w / 2, y=lambda _, h: h / 2,
        a=lambda w: w / 2, b=lambda _, h: h / 2,
    )

    def draw(self, proxy):
        sw = self.pv(proxy.w)
        rx = proxy.a
        ry = proxy.b
        if proxy.i:  # rect inner
            swf = math.ceil(sw / 2)
            rx -= swf
            ry -= swf
        return {
            "ellipse": {
                "cx": proxy.x,
                "cy": proxy.y,
                "rx": rx,
                "ry": ry,
                "stroke": proxy.c,
                "stroke-width": sw,
                "fill": proxy.f,
            }
        }
