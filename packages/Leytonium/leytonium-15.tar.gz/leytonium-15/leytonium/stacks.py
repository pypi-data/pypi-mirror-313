# Copyright 2020 Andrzej Cichocki

# This file is part of Leytonium.
#
# Leytonium is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leytonium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Leytonium.  If not, see <http://www.gnu.org/licenses/>.

'Compare stack traces across build logs.'
import sys, tempfile, subprocess, re, datetime

class Stack:

    def __init__(self, lines):
        self.lines = lines

class Stacks:

    logtimepattern = re.compile('([0-9]{2}):([0-9]{2}):([0-9]{2}),([0-9]{3})')

    @classmethod
    def totime(cls, m):
        return datetime.timedelta(hours = int(m.group(1)), minutes = int(m.group(2)), seconds = int(m.group(3)), milliseconds = int(m.group(4)))

    def __init__(self):
        self.firstlogtime = None
        self.stacks = []

    def startproc(self, line):
        if '[Test Error Output]' in line:
            self.prevproc = self.startproc
            return self.errproc
        elif line.startswith('\t'):
            self.stack = Stack(self.intro + [line])
            del self.intro
            return self.endproc
        else:
            self.intro.append(line)
            del self.intro[:-2] # Log message and exception message.

    def endproc(self, line):
        if '[Test Error Output]' in line:
            self.prevproc = self.endproc
            return self.errproc
        elif line.startswith('\t') or line.startswith('Caused by: '):
            self.stack.lines.append(line)
        else:
            self.stacks.append(self.stack)
            del self.stack
            self.intro = [line]
            return self.startproc

    def errproc(self, line):
        if '[Test Output]' in line:
            proc = self.prevproc
            del self.prevproc
            return proc

    def load(self, f):
        self.intro = []
        proc = self.startproc
        for line in f:
            if self.firstlogtime is None:
                m = self.logtimepattern.search(line)
                if m is not None:
                    self.firstlogtime = self.totime(m)
            proc = proc(line) or proc
        proc('')

    def fixlogtime(self, line):
        m = self.logtimepattern.search(line)
        if m is None: return line
        reltime = (datetime.datetime.min + (self.totime(m) - self.firstlogtime)).time().strftime("%M:%S,%f")[:-3]
        return f"{line[:m.start()]}{reltime}{line[m.end():]}"

    def tofile(self):
        f = tempfile.NamedTemporaryFile('w')
        def separator(i): print(str(i) * 40, file = f)
        for i, s in enumerate(self.stacks):
            separator(i)
            for l in s.lines:
                f.write(self.fixlogtime(l))
        separator(len(self.stacks))
        f.flush()
        return f

def compare(stackslist):
    files = [stacks.tofile() for stacks in stackslist]
    subprocess.run(['vim' if 1 == len(files) else 'diffuse'] + [f.name for f in files])
    for f in files:
        f.close()

def main():
    paths = sys.argv[1:]
    stackslist = []
    for path in paths:
        stacks = Stacks()
        with open(path) as f:
            stacks.load(f)
        stackslist.append(stacks)
    compare(stackslist)

if '__main__' == __name__:
    main()
