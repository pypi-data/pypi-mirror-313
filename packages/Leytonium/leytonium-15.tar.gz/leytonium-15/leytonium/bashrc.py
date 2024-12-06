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

'To eval in your .bashrc file.'
from .git_completion_path import git_completion_path
from .insertshlvl import insertshlvl
import shlex, sys

def main():
    sys.stdout.write(f""". {shlex.quote(str(git_completion_path()))}
PS1={shlex.quote(insertshlvl(*sys.argv[1:]))}
""")

if '__main__' == __name__:
    main()
