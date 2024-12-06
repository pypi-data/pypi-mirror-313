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

'Show list of branches and outgoing changes.'
from .common import showmenu, UnknownParentException, showexception, getpublic, savedcommits, AllBranches, highlight
from lagoon import clear, git
try:
    from lagoon import gls as ls
except ImportError:
    from lagoon import ls
from lagoon.util import stripansi
from termcolor import colored
import re, subprocess

limit = 20

class Row:

    def __init__(self, allbranches, line):
        name = stripansi(re.search('[\S]+', line).group())
        if '(no' == name:
            self.parent = '(void)'
        else:
            parents = allbranches.parents(name)
            if parents:
                self.parent = '[...]' if parents[0] == getpublic(name) else parents[0]
                if len(parents) > 1:
                    self.parent += f"+{len(parents) - 1}"
            else:
                self.parent = '<!>'
        self.line = line

    def branch(self):
        return self.line[:self.line.index(' ')]

    def colorline(self, ispr):
        return colored(self.line, 'green', attrs = ['reverse']) if ispr else self.line

def title(commit):
    return git.log('-n', 1, '--pretty=format:%B', commit).splitlines()[0]

def main():
    clear[print]()
    try:
        allbranches = AllBranches()
    except subprocess.CalledProcessError:
        ls._l[print]('--color=always')
        return
    rows = [Row(allbranches, l[2:]) for l in git('-c', 'color.ui=always', 'branch', '-vv').splitlines()]
    fmt = "%%-%ss %%s" % max(len(r.parent) for r in rows)
    for r in rows:
        print(fmt % (r.parent, r.colorline(False)))
    saved = savedcommits()
    showmenu([(c, title(c)) for c in saved], xform = lambda i: i - len(saved) + 1, print = highlight)
    try:
        entries = allbranches.branchcommits()
        showmenu(entries[:limit])
        count = len(entries) - limit
        if count > 0:
            print(f"({count} more)")
    except UnknownParentException:
        showexception()
    git.status._v[print](check = False)
    git.stash.list[print]()

if '__main__' == __name__:
    main()
