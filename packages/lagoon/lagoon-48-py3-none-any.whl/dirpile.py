'''Using OverlayFS create a merged view of the given (read only) dirs plus a (writable) temporary dir, print its path, and stay running until stdin is closed.
The first given directory is the lowest in the pile (this is unlike the lowerdir mount option).
This program requires root and is designed to be invoked via sudo.'''
from argparse import ArgumentParser
from lagoon import mount, umount
from lagoon.util import mapcm
from pathlib import Path
from tempfile import TemporaryDirectory
import json, os, re, sys

maxchunksize = 1 << 10
chown_nop = -1

def _intor(k, default):
    try:
        return int(os.environ[k])
    except KeyError:
        return default

def _escdirpath(p):
    return re.sub(r'[\\:,]', r'\\\g<0>', str(p))

class DirPile:

    def __init__(self, args):
        self.json = args.json
        self.uid = args.u
        self.gid = args.g
        self.dirpaths = args.dirpath

    def _align(self, d):
        os.chown(d, self.uid, self.gid)

    def run(self):
        def mkdir(name):
            d = tempdir / name
            d.mkdir()
            self._align(d)
            return d
        with mapcm(Path, TemporaryDirectory()) as tempdir:
            self._align(tempdir)
            merged = mkdir('merged')
            upperdir = mkdir('upper')
            workdir = mkdir('work')
            mount._t.overlay[print]('-o', f"lowerdir={':'.join(map(_escdirpath, reversed(self.dirpaths)))},upperdir={_escdirpath(upperdir)},workdir={_escdirpath(workdir)}", 'overlay', merged)
            try:
                print(json.dumps(str(merged)) if self.json else merged)
                sys.stdout.flush()
                while sys.stdin.read(maxchunksize):
                    pass
            finally:
                umount[print](merged)

def main():
    parser = ArgumentParser()
    parser.add_argument('--json', action = 'store_true', help = 'print json string')
    parser.add_argument('-u', type = int, default = _intor('SUDO_UID', chown_nop), help = 'numeric user')
    parser.add_argument('-g', type = int, default = _intor('SUDO_GID', chown_nop), help = 'numeric group')
    parser.add_argument('dirpath', nargs = '+', help = 'directories to overlay from low to high')
    DirPile(parser.parse_args()).run()

if '__main__' == __name__:
    main()
