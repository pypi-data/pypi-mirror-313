import os
import re
from dektools.func import FuncAnyArgs
from dektools.yaml import yaml
from dektools.file import read_text, iter_relative_path
from ...utils.common import optimize_svg


class Node:
    need_g_wrapper = False

    def __init__(self, manager):
        self.manager = manager

    def render(self, params, attrs):
        raise NotImplementedError()


class Canvas(Node):
    def __init__(self, manager, width, height):
        super().__init__(manager)
        self.width = width
        self.height = height

    def pv(self, value, ratio=1):
        if isinstance(value, float):
            return self.width * value * ratio
        return value


class Function(Canvas):
    def __init__(self, manager, width, height, name, params, body):
        super().__init__(manager, width, height)
        self.name = name
        self.body = body
        self.params = params

    @staticmethod
    def _translate_data(params, data):
        result = {}
        for k, v in data.items():
            if isinstance(v, str):
                r = re.match(r"^\$\$([0-9a-zA-Z_]+)$", v)
                if r:
                    v = params.get(r.groups()[0])
            if v is not None:
                result[k] = v
        return result

    def render(self, params, attrs):
        params = {**self.params, **params}
        result = ""
        for key, value in self.body.items():
            value = value or {}
            name, trans = self.manager.parse_call_label(key, self)
            node = self.manager.get_node(name, self.width, self.height)
            content = node.render(params, self._translate_data(params, value))
            result += f"""<g{trans}>{content}</g>""" if trans or node.need_g_wrapper else content
        return result


class Svg(Node):
    need_g_wrapper = True

    def __init__(self, manager, content):
        super().__init__(manager)
        self.content = content

    def render(self, params, attrs):
        if attrs:
            return self.manager.render_by_struct({'g': {**attrs, '+': self.content}})
        return self.content


class Tag(Node):
    def __init__(self, manager, name):
        super().__init__(manager)
        self.name = name

    def render(self, params, attrs):
        return self.manager.render_by_struct({self.name: attrs})


class Element(Canvas):
    name = None
    spec = {}

    class Proxy:
        def __init__(self):
            self.params = {}

        def __getattr__(self, item):
            return self.params[item]

        def __setitem__(self, key, value):
            self.params[key] = value

    def new_proxy(self, attrs):
        proxy = self.Proxy()
        attrs = {**self.spec, **attrs}
        for k, v in attrs.items():
            if callable(v):
                v = FuncAnyArgs(v)(self.width, self.height, proxy)
            proxy[k] = v
        return proxy

    def render(self, params, attrs):
        return self.manager.render_by_struct(self.draw(self.new_proxy(attrs)))

    def draw(self, proxy):
        raise NotImplementedError()


class Manager:
    default_width = 1024
    default_height = default_width
    function_cls = Function
    svg_cls = Svg
    tag_cls = Tag

    element_map = {}

    @classmethod
    def parse_function_label(cls, label):
        kl = label.split(" ", 1)
        name = kl[0]
        if len(kl) == 2:
            rest = kl[1]
            rr = re.match(r"^[0-9. ]+", rest)
            if rr:
                wh = rr.group()
                sp = rest[len(wh):]
            else:
                wh = ""
                sp = rest
            params = dict([y.strip() for y in x.split(":", 1)] for x in sp.split(","))
        else:
            wh = ""
            params = {}
        items = [x.strip() for x in wh.strip().split()]
        items = items + (2 - len(items)) * [""]
        items = [int([cls.default_width, cls.default_height][i] if x == "" else x) for i, x in enumerate(items)]
        return items[0], items[1], name, params

    @classmethod
    def parse_call_label(cls, label, node=None):
        def pv(tf, value):
            if node and tf in {'translate'}:
                return node.pv(value)
            return value

        def transform(s):
            for k, v in transform_map.items():
                if s.startswith(k):
                    tf = [str(pv(v, float(x) if '.' in x else int(x))) for x in s[len(k):].split(',')]
                    return f"{v}({','.join(tf)})"
            return ""

        transform_map = {'t': 'translate', 's': 'scale', 'sk': 'skew'}

        kl = label.split(" ", 1)
        name = kl[0]
        if len(kl) == 2:
            items = [transform(x) for x in kl[1].split() if x and not x.startswith('-')]
        else:
            items = []
        if items:
            trans = f' transform="{" ".join(items)}"'
        else:
            trans = ""
        return name, trans

    def __init__(self):
        self.function_map = {}
        self.svg_map = {}
        self.id_cursor = 0

    def new_id(self):
        self.id_cursor += 1
        return str(self.id_cursor)

    def make_svg(self, name, params=None, attrs=None):
        node = self.get_node(name)
        content = node.render(params or {}, attrs or {})
        return optimize_svg(
            f'<svg viewBox="0 0 {node.width} {node.height}" '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink">{content}</svg>'
        )

    def get_node(self, name, width=None, height=None):
        return self.function_map.get(name) or \
            self.svg_map.get(name) or \
            self.element_map.get(name) and self.element_map[name](
                self,
                self.default_width if width is None else width,
                self.default_height if height is None else height,
            ) or \
            self.tag_cls(self, name)

    @classmethod
    def render_by_struct(cls, data):
        if isinstance(data, str):
            return data
        result = ""
        for label, attrs in data.items():
            tag, trans = cls.parse_call_label(label)
            children = attrs.pop('+', None)
            sa = "".join(f' {k}="{v}"' for k, v in attrs.items() if v not in ('', None))
            if children is None:
                result += f"<{tag}{trans}{sa}/>"
            else:
                result += f"<{tag}{trans}{sa}>{cls.render_by_struct(children)}</{tag}>"
        return result

    def load_file_yaml(self, path):
        data_map = yaml.load(path)
        for label, body in data_map.items():
            width, height, name, params = self.parse_function_label(label)
            self.function_map[name] = self.function_cls(self, width, height, name, params, body)

    def load_file_svg(self, path):
        name = os.path.splitext(os.path.basename(path))[0]
        self.svg_map[name] = self.svg_cls(self, read_text(path))

    def load_path(self, path):
        for _, fp in iter_relative_path(path):
            ext = os.path.splitext(fp)[-1].lower()
            if ext == '.svg':
                self.load_file_svg(fp)
            elif ext == '.yaml':
                self.load_file_yaml(fp)

    @classmethod
    def element(cls, element_cls):
        if element_cls.name:
            name = element_cls.name
        else:
            name = element_cls.__name__
        cls.element_map[name] = element_cls
        return element_cls
