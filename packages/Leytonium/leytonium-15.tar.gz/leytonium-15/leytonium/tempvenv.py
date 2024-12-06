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

'Activate a writable venv from the pool with the given requires.'
from . import initlogging
from argparse import ArgumentParser
from lagoon.program import Program
from pathlib import Path
from pyven.projectinfo import SimpleInstallDeps
from venvpool import Pool
import logging, os, sys

log = logging.getLogger(__name__)
shellpath = os.environ['SHELL']

def main():
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('-p', type = int, default = sys.version_info.major)
    parser.add_argument('reqs', nargs = '*')
    args = parser.parse_args()
    with Pool(args.p).readwrite(SimpleInstallDeps(args.reqs)) as venv:
        Program.text(shellpath)._c[print]('. "$1" && exec "$2"', '-c', Path(venv.venvpath, 'bin', 'activate'), shellpath)

if '__main__' == __name__:
    main()
