from .util import ContextStream, iidfile
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from diapyr.util import invokeall
from errno import EADDRINUSE
from functools import partial
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from lagoon.binary import docker
from pkg_resources import resource_stream
from subprocess import PIPE
import logging, os, pickle, re, time

log = logging.getLogger(__name__)
NORMAL = lambda o: o.exception() is None
'Accept normal outcomes.'
ABRUPT = lambda o: o.exception() is not None
'Accept abrupt outcomes.'
ALWAYS = lambda o: True
'Accept all outcomes.'
NEVER = lambda o: False
'Do not accept any outcome.'

class NormalOutcome:

    def __init__(self, obj):
        self.obj = obj

    def result(self):
        return self.obj

    def exception(self):
        pass

class AbruptOutcome:

    def __init__(self, e):
        self.e = e

    def result(self):
        raise self.e

    def exception(self):
        return self.e

class MissHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_error(HTTPStatus.SERVICE_UNAVAILABLE, 'Cache miss')

class SaveHandler(BaseHTTPRequestHandler):

    def __init__(self, outcome, *args, **kwargs):
        self.outcome = outcome
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        pickle.dump(self.outcome, self.wfile)

class ExpensiveTask:
    'Arbitrary task accelerated by Docker cache.'

    log = log
    port = 41118
    sleeptime = .5

    def __init__(self, context, discriminator, task):
        'Create a task keyed by context directory and discriminator string.'
        self.context = os.path.abspath(context)
        self.discriminator = discriminator
        self.task = task

    @contextmanager
    def _builder(self):
        def build(*args):
            with docker.build.__network.host.__quiet[print, partial](*iid.args, '--build-arg', f"discriminator={self.discriminator}", '--build-arg', f"port={self.port}", '-', *args, stdin = PIPE, check = False) as p, ContextStream.open(p.stdin) as context:
                with resource_stream(__name__, 'Dockerfile.dkr') as f:
                    context.putstream('Dockerfile', f)
                context.put('context', self.context)
            if not p.returncode:
                return iid.read()
        with iidfile() as iid:
            yield build

    def _retryport(self, openport):
        while True:
            try:
                return openport()
            except OSError as e:
                if EADDRINUSE != e.errno:
                    raise
            log.debug("Port %s unavailable, sleep for %s seconds.", self.port, self.sleeptime)
            time.sleep(self.sleeptime)

    def _imageornoneimpl(self, executor, handlercls, build):
        def bgtask():
            try:
                return build()
            finally:
                server.shutdown()
        with HTTPServer(('', self.port), handlercls) as server:
            return invokeall([server.serve_forever, executor.submit(bgtask).result])[1]

    def _imageornone(self, executor, handlercls):
        with self._builder() as build:
            assert build('--target', 'key') is not None
            return self._retryport(partial(self._imageornoneimpl, executor, handlercls, build))

    def _outcomeornone(self, executor, handlercls, force):
        image = self._imageornone(executor, handlercls)
        if image is not None:
            with docker.run.__rm[partial](image) as f:
                outcome = pickle.load(f)
            drop = force(outcome)
            self.log.info("Cache hit%s: %s", ' and drop' if drop else '', image)
            if not drop:
                return outcome
            before = set(_pruneids())
            docker.rmi[print](image)
            # If our object is not in the set then nothing to be done, another process or user must have pruned it.
            # The user can docker builder prune at any time, so pruning too much here is not worse than that.
            for pruneid in set(_pruneids()) - before:
                docker.builder.prune._f[print]('--filter', f"id={pruneid}") # Idempotent.

    def run(self, force = NEVER, cache = NORMAL):
        'Run the task, where `force` can be used to ignore a cached outcome, and `cache` can be used to deny caching an outcome.'
        with ThreadPoolExecutor() as executor:
            outcome = self._outcomeornone(executor, MissHandler, force)
            if outcome is not None:
                return outcome.result()
            try:
                outcome = NormalOutcome(self.task())
            except Exception as e:
                outcome = AbruptOutcome(e)
            if cache(outcome):
                self.log.info("Cached as: %s", self._imageornone(executor, partial(SaveHandler, outcome)))
            return outcome.result()

def _pruneids():
    for block in docker.buildx.du.__verbose().decode().split('\n\n'):
        obj = {k: v for l in block.splitlines() for k, v in [re.split(':\t+', l, 1)]}
        if 'false' == obj['Shared'] and 'mount / from exec /bin/sh -c wget localhost:$port' == obj['Description']:
            yield obj['ID']
