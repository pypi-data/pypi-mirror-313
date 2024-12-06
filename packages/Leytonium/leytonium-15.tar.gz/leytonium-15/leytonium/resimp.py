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

'Resolve conflicts in imports and adjacent-line conflicts.'
from .common import stderr, findproject
from lagoon import git
import itertools, os, re

def resimp(path):
    output = []
    chunks = [0]
    def outer(line):
        if line.startswith('<<<<<<< '):
            return Conflict(line)
        else:
            output.append(line)
    class Conflict:
        def __init__(self, intro):
            self.current = self.upper = []
            self.lower = []
            self.intro = intro
        def __call__(self, line):
            if line.startswith('>>>>>>> '):
                for l in itertools.chain(self.upper, self.lower):
                    if not l.startswith('import '):
                        break
                else:
                    output.extend(self.upper)
                    output.extend(self.lower)
                    chunks[0] += 1
                    return outer
                output.append(self.intro)
                output.extend(self.upper)
                output.append(self.sep)
                output.extend(self.lower)
                output.append(line)
                return outer
            elif line.splitlines()[0] == '=======':
                self.sep = line
                self.current = self.lower
            else:
                self.current.append(line)
    handler = outer
    with open(path) as f:
        for line in f:
            handler = handler(line) or handler
    if chunks[0]:
        with open(path, 'w') as g:
            for line in output:
                g.write(line)
        stderr(f"[{path}] Merged {chunks[0]} chunks of imports.")

def getconflictinfos(path):
    conflictinfos = []
    def outer(line):
        if line.startswith('+<<<<<<< '):
            return ConflictInfo()
    class ConflictInfo:
        def __init__(self):
            self.current = self.upper = []
            self.lower = []
        def __call__(self, line):
            if line.startswith('+>>>>>>> '):
                conflictinfos.append(self)
                return outer
            elif line.splitlines()[0] == '+=======':
                self.current = self.lower
            else:
                self.current.append(line)
        def shape(self):
            return [''.join(l[0] for l in part) for part in [self.upper, self.lower]]
    handler = outer
    for line in git.diff.__base.__(path).splitlines(keepends = True):
        handler = handler(line) or handler
    return conflictinfos

def resadj(path):
    conflictinfos = getconflictinfos(path)
    output = []
    resolved = [0]
    def outer(line):
        if line.startswith('<<<<<<< '):
            info = conflictinfos.pop(0) # FIXME: Pop from empty list has happened! Suspect when both sides added the path so there is no base.
            cls = BlankPlusPlusBlank.forshape(info.shape()) or PassConflict
            return cls(line)
        else:
            output.append(line)
    class PassConflict:
        def __init__(self, intro):
            output.append(intro)
        def __call__(self, line):
            output.append(line)
            if line.startswith('>>>>>>> '):
                return outer
    class BlankPlusPlusBlank:
        shapepatterns = [re.compile(s) for s in [' +[+]+', '[+]+ +']]
        @classmethod
        def forshape(cls, shape):
            for p, s in zip(cls.shapepatterns, shape):
                if p.fullmatch(s) is None:
                    return
            return lambda intro: cls(shape, intro)
        def __init__(self, shape, intro):
            self.currentshape = self.uppershape = list(shape[0])
            self.lowershape = list(shape[1])
            self.current = self.upper = []
            self.lower = []
        def __call__(self, line):
            if line.startswith('>>>>>>> '):
                output.extend(self.lower)
                output.extend(self.upper)
                resolved[0] += 1
                return outer
            elif line.splitlines()[0] == '=======':
                self.currentshape = self.lowershape
                self.current = self.lower
            elif '+' == self.currentshape.pop(0):
                self.current.append(line)
    handler = outer
    with open(path) as f:
        for line in f:
            handler = handler(line) or handler
    if resolved[0]:
        with open(path, 'w') as g:
            for line in output:
                g.write(line)
        stderr(f"[{path}] Auto-resolved {resolved[0]} adjacent-line conflicts.")

def main():
    os.chdir(findproject()) # Paths below are relative to project root.
    for path in git.diff.__name_only('--diff-filter=U').splitlines():
        for task in resimp, resadj:
            task(path)

if '__main__' == __name__:
    main()
