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

'Extract the audio from the given video files.'
from . import initlogging
from argparse import ArgumentParser
from lagoon import ffmpeg
from lagoon.program import partial
from pathlib import Path
import logging

log = logging.getLogger(__name__)

def main():
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('-d', action = 'store_true')
    parser.add_argument('path', nargs = '+', type = Path)
    args = parser.parse_args()
    for inpath in args.path:
        outpath = inpath.with_suffix('.aac')
        log.info("Extract: %s", outpath)
        ffmpeg._i[partial](inpath)._vn._acodec.copy(outpath)
        if args.d:
            log.info("Delete: %s", inpath)
            inpath.unlink()

if '__main__' == __name__:
    main()
