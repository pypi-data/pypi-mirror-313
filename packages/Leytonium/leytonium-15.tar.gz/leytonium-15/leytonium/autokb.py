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

'Automatically switch to/from USB keyboard layout.'
from . import initlogging
from aridity.config import ConfigCtrl
from lagoon import lsusb, setxkbmap
from lagoon.program import partial
import logging, re

log = logging.getLogger(__name__)

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'autokb.arid')
    layout = config.layout.default if lsusb[print]('-d', config.usb, check=False) else config.layout.device
    xkbmap = setxkbmap[partial]('-display', config.display)
    current = re.search(r'^layout:\s*(.+)', xkbmap._query(), re.MULTILINE).group(1)
    log.debug("Current layout: %s", current)
    if current != layout:
        log.info("Set layout: %s", layout)
        xkbmap[print](layout)

if '__main__' == __name__:
    main()
