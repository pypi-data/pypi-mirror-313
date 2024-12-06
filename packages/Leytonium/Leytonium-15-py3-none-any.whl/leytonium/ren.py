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

'Rename current branch.'
from .common import thisbranch, args, findproject, infodirname
from lagoon import git
import os

def main():
    fromname = thisbranch()
    git.branch._m[print](*args())
    d = os.path.join(findproject(), infodirname)
    target = os.path.join(d, thisbranch())
    os.makedirs(os.path.dirname(target), exist_ok = True)
    os.rename(os.path.join(d, fromname), target)

if '__main__' == __name__:
    main()
