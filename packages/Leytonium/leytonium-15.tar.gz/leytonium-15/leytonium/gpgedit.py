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

'Edit gpg-encrypted file.'
from . import initlogging
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from lagoon import gpg, gpgconf
from lagoon.program import Program
from lagoon.util import atomic, mapcm
from pathlib import Path
from tempfile import TemporaryDirectory
import logging, os

log = logging.getLogger(__name__)

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'gpgedit.arid')
    parser = ArgumentParser()
    parser.add_argument('-f', action = 'store_true')
    parser.add_argument('path', type = Path)
    parser.parse_args(namespace = config.cli)
    if config.force:
        gpgconf.__reload.gpg_agent[print]()
    path = config.path
    with mapcm(Path, TemporaryDirectory()) as tempdir:
        x = tempdir / path.name
        if path.exists():
            gpg.__decrypt[print]('--output', x, path)
            os.utime(x, (0, 0))
        Program.text(os.environ['EDITOR'])[print](x)
        try:
            mtime = x.stat().st_mtime
        except FileNotFoundError:
            log.info('File not created.')
        else:
            if mtime:
                with atomic(path) as y:
                    gpg.__symmetric.__batch[print]('--output', y, '--passphrase-fd', 0, x, input = config.passphrase)
            else:
                log.info('File not modified.')

if '__main__' == __name__:
    main()
