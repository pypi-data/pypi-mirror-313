from .program import partial
from parabject import Parabject, register
from urllib.parse import parse_qs, quote, quote_plus, urlsplit, urlunsplit
from urllib.request import Request, urlopen
import functools, json, sys

def _joinpath(path, args, safe):
    for arg in args:
        path = f"{path}{'' if path.endswith('/') else '/'}{quote(arg, safe)}"
    return path

class URL:

    @classmethod
    def binary(cls, url):
        url = urlsplit(url)
        return cls(url._replace(query = ''), dict(query = {k: tuple(v) for k, v in parse_qs(url.query).items()}), None, 0).handle

    @classmethod
    def of(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __init__(self, url, kwargs, lift, ttl):
        self.handle = register(self, URLHandle)
        self.url = url
        self.kwargs = kwargs
        self.lift = lift
        self.ttl = ttl

    def getattr(self, name):
        return self.of(self.url._replace(path = _joinpath(self.url.path, [name], '')), self.kwargs, self.lift, self.ttl).handle

    def getitem(self, keys):
        for k in keys:
            self = styles[k](self)
        return self.handle

    def _mergedkwargs(self, kwargs):
        merged = {**self.kwargs, **kwargs}
        k = 'query'
        if k in self.kwargs and k in kwargs:
            merged[k] = {**self.kwargs[k], **kwargs[k]}
        return merged

    def call(self, args, kwargs):
        kwargs = self._mergedkwargs(kwargs if self.lift is None else {self.lift: kwargs})
        if self.ttl:
            return self.of(self.url._replace(path = _joinpath(self.url.path, args, '/')), kwargs, None, self.ttl - 1).handle
        query = ['='.join(map(quote_plus, [k, v])) for k, u in kwargs.get('query', {}).items() for v in (u if isinstance(u, tuple) else [u])]
        try:
            xform = kwargs['stdout']
        except KeyError:
            xform = lambda x: x
        else:
            if xform is None:
                def xform(x):
                    sys.stdout.buffer.write(x)
        openkwargs = {k: v for k, v in kwargs.items() if k in {'timeout'}}
        with urlopen(Request(urlunsplit([self.url.scheme, self.url.netloc, _joinpath(self.url.path, args, '/'), '&'.join(query), self.url.fragment]), method = kwargs.get('method')), **openkwargs) as f:
            return xform(f.read())

class URLHandle(Parabject):

    def __getattr__(self, name):
        return (-self).getattr(name)

    def __getitem__(self, key):
        return (-self).getitem(key if isinstance(key, tuple) else [key])

    def __call__(self, *args, **kwargs):
        return (-self).call(args, kwargs)

def _partialstyle(ctrl):
    return ctrl.of(ctrl.url, ctrl.kwargs, ctrl.lift, ctrl.ttl + 1)

def _stdoutstyle(token):
    return lambda ctrl: -ctrl.handle[partial](stdout = token)

def _querystyle(ctrl):
    assert ctrl.lift is None
    return ctrl.of(ctrl.url, ctrl.kwargs, 'query', ctrl.ttl)

styles = {
    functools.partial: _partialstyle,
    json: _stdoutstyle(json.loads),
    partial: _partialstyle,
    print: _stdoutstyle(None),
    '?': _querystyle,
}
