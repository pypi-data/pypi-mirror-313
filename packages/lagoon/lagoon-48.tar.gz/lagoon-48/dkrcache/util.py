from contextlib import contextmanager
from lagoon.util import mapcm
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import tarfile

class ContextStream:
    'Fully customisable docker build context.'

    @classmethod
    @contextmanager
    def open(cls, dockerstdin):
        'Attach to the given stdin of docker build, which should have been given `-` as context.'
        with tarfile.open(mode = 'w:gz', fileobj = dockerstdin) as tar:
            yield cls(tar)

    def __init__(self, tar):
        self.tar = tar

    def put(self, name, path):
        'Add the given path as the given archive name.'
        self.tar.add(path, name)

    def putstream(self, name, stream):
        'Add the given stream as the given archive name.'
        self.tar.addfile(self.tar.gettarinfo(arcname = name, fileobj = stream), stream)

    def mkdir(self, name):
        'Create a directory in the context.'
        with TemporaryDirectory() as empty:
            self.put(name, empty)

@contextmanager
def iidfile():
    'Context manager yielding an object with `args` to pass to docker build, and a `read` function to get the image ID.'
    with mapcm(Path, TemporaryDirectory()) as tempdir:
        path = tempdir / 'iid'
        yield SimpleNamespace(args = ('--iidfile', path), read = path.read_text)
