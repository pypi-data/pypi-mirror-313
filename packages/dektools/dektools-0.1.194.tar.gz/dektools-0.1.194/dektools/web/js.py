import os
import codecs
from uuid import uuid4
from hashlib import sha256
from urllib.parse import quote


def encode_uri_component(s):
    return quote(s, safe="!~*'()")


class ResToJs:
    def __init__(self, html=None, js=None, css=None, html_append='document.body.appendChild'):
        self._html = html or []
        self._js = js or []
        self._css = css or []
        self._html_append = html_append

    def new_var(self):
        return '_' + sha256(f"{self.__class__.__name__}:{uuid4().hex}".encode('utf-8')).hexdigest()

    @classmethod
    def from_dir(cls, src, **kwargs):
        def read_text(fn):
            with codecs.open(fn, encoding='utf-8') as fh:
                return fh.read()

        html = []
        js = []
        css = []
        if os.path.isdir(src):
            for base, _, files in os.walk(src):
                for file in files:
                    p = os.path.join(base, file)
                    ext = os.path.splitext(p)[-1]
                    if ext == '.html':
                        html.append(read_text(p))
                    elif ext == '.js':
                        js.append(read_text(p))
                    elif ext == '.css':
                        css.append(read_text(p))
        html = (kwargs.pop('html', None) or []) + html
        js = (kwargs.pop('js', None) or []) + js
        css = (kwargs.pop('css', None) or []) + css
        return cls(html=html, js=js, css=css, **kwargs)

    @staticmethod
    def new_str(s):
        return f'decodeURIComponent("{encode_uri_component(s)}")'

    def css(self):
        if not self._css:
            return ''
        _content = '\n'.join(self._css)
        _var = self.new_var()
        return f"""
let {_var} = document.createElement('style');
{_var}.type = 'text/css';
{_var}.innerHTML = {self.new_str(_content)}
document.head.appendChild({_var})
        """

    def html(self):
        if not self._html:
            return ''
        _content = '\n'.join(self._html)
        _var = self.new_var()
        return f"""
let {_var} = document.createElement('div');
{self._html_append}({_var})
{_var}.outerHTML = {self.new_str(_content)}
        """

    def js(self):
        return '\n'.join(self._js)

    def result(self):
        return '\n'.join([self.css(), self.html(), self.js()])
