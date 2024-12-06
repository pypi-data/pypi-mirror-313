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

'Create a master-based branch from this non-master-based one.'
from .common import thisbranch, pb, AllBranches, addparents
from lagoon import git, ren

def main():
    master = 'master'
    parent = pb()
    if parent == master:
        raise Exception(f"Parent is already {master}!")
    name = thisbranch()
    allbranches = AllBranches()
    commits = [commit for commit, _ in allbranches.branchcommits(name)]
    ren[print](f"{name}.bak")
    git.checkout._b[print](name, master)
    addparents(name, master)
    git.cherry_pick[print](*commits)

if '__main__' == __name__:
    main()
