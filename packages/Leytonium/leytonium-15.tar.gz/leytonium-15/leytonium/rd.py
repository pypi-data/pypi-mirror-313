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

'Run git add on conflicted path(s), with completion.'
from itertools import islice
from lagoon import git
from pathlib import Path
import sys

def main():
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if not a.startswith('-'):
            break
        if '--' == a:
            i += 1
            break
    for p in map(Path, islice(args, i, None)):
        with p.open() as f: # Effectively assert not directory.
            for l in f:
                assert '=======' != l.rstrip()
    git.add[exec](*args)

if '__main__' == __name__:
    main()
