from collections import defaultdict
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import local
from unittest import TestCase
import os, re, sys

mangled = re.compile('_.*(__.*[^_]_?)')
PYTHONPATH = os.pathsep.join(sys.path[1:]) # XXX: Include first entry?

def unmangle(name):
    'Undo name mangling.'
    m = mangled.fullmatch(name)
    return name if m is None else m.group(1)

@contextmanager
def atomic(path):
    'Context manager yielding a temporary Path for atomic write to the given path. Parent directories are created automatically. Also suitable for making a symlink atomically. Leaves the given path unchanged if an exception happens.'
    path.parent.mkdir(parents = True, exist_ok = True)
    with TemporaryDirectory(dir = path.parent) as d:
        q = Path(d, f"{path.name}.part")
        yield q
        q.rename(path) # XXX: Or replace?

class threadlocalproperty:
    'Like `property` but each thread has its own per-object values.'

    def __init__(self, defaultfactory):
        'The `defaultfactory` should return the initial value per object (per thread).'
        self.local = local()
        self.defaultfactory = defaultfactory

    def _lookup(self):
        try:
            return self.local.lookup
        except AttributeError:
            self.local.lookup = lookup = defaultdict(self.defaultfactory)
            return lookup

    def __get__(self, obj, objtype):
        return self._lookup()[obj]

    def __set__(self, obj, value):
        self._lookup()[obj] = value

@contextmanager
def onerror(f):
    'Context manager that runs the given function if an exception happens, like `finally` excluding the happy path.'
    try:
        yield
    except:
        f()
        raise

@contextmanager
def mapcm(f, obj):
    'Invoke `obj` as a context manager, apply `f` to its yielded value, and yield that. For example apply `Path` to the string yielded by `TemporaryDirectory()`.'
    with obj as cm:
        yield f(cm)

def stripansi(text):
    'Remove ANSI control sequences from the given text, to make it black and white.'
    return re.sub('\x1b\\[[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]', '', text) # XXX: Duplicated code?

class HarnessCase(TestCase):
    'Enter context managers in setUp and exit them in tearDown.'

    def harness(self):
        'Must yield exactly once.'
        raise NotImplementedError

    def setUp(self):
        self.continuation = c = self.harness()
        try:
            next(c)
        except StopIteration:
            raise RuntimeError('Generator did not yield.')

    def tearDown(self):
        try:
            next(self.continuation)
        except StopIteration:
            return
        e = RuntimeError('Generator did not stop.')
        while True:
            try:
                self.continuation.throw(e) # XXX: Or leave generator dangling in this case?
            except StopIteration:
                break
