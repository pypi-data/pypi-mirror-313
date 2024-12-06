'GNU Screen interface, smoothing over its many gotchas.'
from lagoon import screen
from lagoon.program import partial
import re

def stuffablescreen(doublequotekey):
    'Return text mode Program for screen, with the given environment variable set to double quote.'
    return screen[partial](env = {doublequotekey: '"'})

class Stuff:

    class Part:

        def __init__(self, text):
            self.data = text.encode()

        def consume(self, chunk, maxsize):
            if len(self.data) <= maxsize:
                chunk.append(self.data)
                return True

    class Text(Part):

        def consume(self, chunk, maxsize):
            if super().consume(chunk, maxsize):
                return True
            chunk.append(self.data[:maxsize])
            self.data = self.data[maxsize:]

    replpattern = re.compile(r'[$^\\"]')
    buffersize = 756

    def toparts(self, text):
        mark = 0
        for m in self.replpattern.finditer(text):
            yield self.Text(text[mark:m.start()])
            char = m.group()
            yield self.doublequoteatom if '"' == char else self.Part(r"\%s" % char)
            mark = m.end()
        yield self.Text(text[mark:])

    def __init__(self, session, window, doublequotekey):
        'Target the given screen session and window, using the given environment variable for double quote.'
        self.session = session
        self.window = window
        self.doublequoteatom = self.Part("${%s}" % doublequotekey)

    def __call__(self, text):
        'Send the given text so that it is received literally.'
        parts = list(self.toparts(text))
        k = 0
        while k < len(parts):
            maxsize = self.buffersize
            chunk = []
            while k < len(parts) and parts[k].consume(chunk, maxsize):
                maxsize -= len(chunk[-1])
                k += 1
            self._juststuff(b''.join(chunk))

    def interrupt(self):
        self._juststuff('^C')

    def eof(self):
        'Send EOF, may have no effect if not at the start of a line.'
        self._juststuff('^D')

    def _juststuff(self, data):
        screen[print]('-S', self.session, '-p', self.window, '-X', 'stuff', data)
