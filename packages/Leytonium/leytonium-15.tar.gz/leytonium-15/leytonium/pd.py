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

'Diff from public branch, the other way.'
from .common import getpublic, stderr
from lagoon import git
import sys

def main():
    parent = getpublic()
    stderr(f"Public branch: {parent}")
    git.diff._M25[exec](*sys.argv[1:], 'HEAD', parent)

if '__main__' == __name__:
    main()
