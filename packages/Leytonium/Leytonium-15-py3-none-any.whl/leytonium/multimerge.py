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

'Merge master into all PRs and carrion.'
from .common import findproject, nicely, AllBranches, getpublic, stderr, touchmsg
from lagoon import git, touchb
import os

merge = git.merge.__no_edit

def reportornone(b):
    status = merge(b, check = False).stdout.splitlines()
    conflicts = sum(1 for line in status if 'CONFLICT' in line)
    if conflicts:
        git.reset.__hard[print]()
        return conflicts, b
    for line in status:
        print(line)

def getreports(branches):
    def g():
        for b in branches:
            r = reportornone(b)
            if r is not None:
                yield r
    return list(g())

def mergeintocurrent(parents):
    while True:
        getreports(parents) # Do all automatic merges up-front for accurate conflict counts.
        reports = getreports(parents)
        if not reports:
            break
        for r in reports:
            stderr("%s %s" % r)
        reports.sort()
        _, b = reports[0]
        stderr(f"Merging: {b}")
        merge(b)

def touchifnecessary():
    if [touchmsg()] == git.log._1('--pretty=format:%B').splitlines():
        stderr('No changes, touch not needed.')
    else:
        touchb[print]()

def ispublished(): # TODO: Really this should check whether PR.
    pb = getpublic()
    return pb is not None and not pb.startswith(f"origin/{os.environ['USER']}_")

def multimerge():
    allbranches = AllBranches()
    remaining = allbranches.names
    branchtoparents = {b: allbranches.parents(b) for b in remaining}
    allparents = {p for parents in branchtoparents.values() for p in parents}
    def update(b):
        git.checkout[print](b)
        parents = branchtoparents[b]
        if b in allparents or ispublished():
            mergeintocurrent(parents)
            if len(parents) > 1: # XXX: Is that right?
                touchifnecessary()
        elif len(parents) > 1:
            raise Exception(f"Too many parents for rebase: {b}")
        else:
            p, = parents
            git.rebase[print](p)
    done = set()
    while remaining:
        stderr(f"Remaining: {' '.join(remaining)}")
        done0 = frozenset(done)
        def g():
            for b in remaining:
                badparents = [p for p in branchtoparents[b] if not (allbranches.isremote(p) or p in done0)]
                if badparents:
                    yield b, badparents
                else:
                    update(b)
                    done.add(b)
        status = list(g())
        remaining2 = [b for b, _ in status]
        if remaining2 == remaining:
            for b, deps in status:
                stderr(f"{b}: {' '.join(deps)}")
            raise Exception(f"Still remain: {remaining}")
        remaining = remaining2

def main():
    os.chdir(findproject()) # Don't fail if working directory doesn't exist in some branch.
    nicely(multimerge)

if '__main__' == __name__:
    main()
