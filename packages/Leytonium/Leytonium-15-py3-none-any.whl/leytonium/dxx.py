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

'Short diff from parent branch or of passed-in commit number.'
from .common import AllBranches, pb, savedcommits, showmenu, stderr
from lagoon import git
import sys

def main():
    args = sys.argv[1:]
    if args:
        n, = args
        n = int(n)
        if n > 0:
            commit = showmenu(AllBranches().branchcommits(), False)[n]
        else:
            saved = savedcommits()
            commit = saved[len(saved) - 1 + n]
        commits = f"{commit}^", commit
    else:
        parent = pb()
        stderr(f"Parent branch: {parent}")
        commits = parent,
    git.diff._M25.__name_status[exec](*commits)

if '__main__' == __name__:
    main()
