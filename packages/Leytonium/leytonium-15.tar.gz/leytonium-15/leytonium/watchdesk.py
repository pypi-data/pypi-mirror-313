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

'Different background for each desktop.'
from aridity.config import ConfigCtrl
from lagoon import gsettings, xprop
from lagoon.program import bg
from pathlib import Path
import logging, re

log = logging.getLogger(__name__)
number = re.compile('[0-9]+')

def main():
    config = ConfigCtrl().loadappconfig(main, 'watchdesk.arid').path
    with xprop._root._spy[bg]('_NET_CURRENT_DESKTOP') as f: # FIXME: May die with status 1.
        for line in f:
            m = number.search(line)
            if m is not None:
                key = str(1 + int(m.group()))
                try:
                    path = getattr(config, key)
                except AttributeError:
                    log.exception('No such path:')
                else:
                    gsettings.set[print]('org.gnome.desktop.background', 'picture-uri', Path(path).as_uri())

if '__main__' == __name__:
    main()
