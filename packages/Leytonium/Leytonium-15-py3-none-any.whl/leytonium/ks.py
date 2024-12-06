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

'Create a kitchen-sink branch.'
from .common import addparents
from lagoon import git
import os, re

def githubuser():
    with open(os.path.join(os.path.expanduser('~'), '.git-credentials')) as f:
        return re.search('//([^:]+):.*github', f.read()).group(1)

def main():
    master, ks = 'master', 'kitchen-sink'
    git.checkout._b[print](ks, master)
    addparents(ks, master, 'controversial/*', f"public/{githubuser()}-*")

if '__main__' == __name__:
    main()
