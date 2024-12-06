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

'Edit project files containing identifier.'
from .common import findproject
from lagoon import ag
from lagoon.program import Program
import os, sys

def main():
    search = sys.argv[1:]
    editor = os.environ['EDITOR']
    if 1 == len(search) and 'vim' == editor:
        args = [rf"+/\<{search[0]}\>"]
    else:
        args = []
    os.chdir(findproject())
    Program.text(editor)[exec](*args, *ag._wsl(*search).splitlines())

if '__main__' == __name__:
    main()
