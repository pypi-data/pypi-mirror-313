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

'Reset branch to given commit number.'
from .common import AllBranches, showmenu, pb, savecommits, savedcommits
from lagoon import git
import sys

def main():
    items = AllBranches().branchcommits() + [[pb(), '']]
    # TODO: Use argparse.
    args = sys.argv[1:]
    if '-f' == args[0]:
        save = False
        n, = args[1:]
    else:
        save = True
        n, = args
    n = int(n)
    if n > 0:
        commit = showmenu(items, False)[n - 1] + '^'
        if save:
            savecommits([item[0] for item in items[:n - 1]])
        git.reset.__hard[exec](commit)
    else:
        saved = savedcommits()
        i = len(saved) - 1 + n
        commit = saved[i]
        if save:
            savecommits(saved[:i], True)
        git.cherry_pick[exec](*reversed(saved[i:]))

if '__main__' == __name__:
    main()
