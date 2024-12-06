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

'Move given slammed commit (default top) to the bottom.'
from .common import savedcommits, savecommits, args as getargs

def main():
    v = savedcommits()
    args = getargs()
    if args:
        n, = args
        n = int(n)
        if n < 0:
            raise Exception("Don't bother with the minus.")
        i = len(v) - int(n) - 1
    else:
        i = 0
    savecommits(v[:i] + v[i + 1:] + [v[i]], True)

if '__main__' == __name__:
    main()
