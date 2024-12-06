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

'''Show tree with hidden descendants but not their descendants.
Each hidden directory is annotated with a slash per direct child.
Useful for showing hidden items in a Git repository without also showing the whole `.git` tree.
By default all options are passed to the `tree` command, use `--` to pass (preceding) options to this command.
Use `-v` to show errors that are normally suppressed.'''
from . import initlogging
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from lagoon import tree
from lagoon.program import partial
from lagoon.util import stripansi
from pathlib import Path
import logging, os, re, sys

log = logging.getLogger(__name__)
intro = '\u2500\u2500 '
indent = 4

def _wrappercli():
    'Send all options to wrapped command by default.'
    args = sys.argv[1:]
    if '--' not in args:
        args.insert(0, '--')
    return args

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 't.arid')
    parser = ArgumentParser()
    parser.add_argument('-v', action = 'store_true')
    parser.add_argument('treearg', nargs = '*')
    parser.parse_args(_wrappercli(), config.cli)
    if not config.verbose:
        logging.getLogger().setLevel(logging.INFO)
    denymatch = re.compile(f"{re.escape(intro)}(?:{'|'.join(config.hiddenregex)})$").search
    allow = True
    allowmatch = None
    parts = []
    with tree._aC[partial](*config.treearg) as f:
        for line in f:
            bwline = stripansi(line)
            if not allow and allowmatch(bwline) is not None:
                allow = True
            if allow:
                try:
                    depth, r = divmod(bwline.index(intro) + len(intro), indent)
                    assert not r
                except ValueError:
                    depth = 0
                name, = bwline[depth * indent:].splitlines()
                del parts[depth:]
                parts.append(name)
                path = Path(*parts)
                m = denymatch(bwline)
                if m is None:
                    sys.stdout.write(line)
                else:
                    sanseol, = line.splitlines()
                    sys.stdout.write(sanseol)
                    try:
                        n = sum(1 for _ in path.iterdir())
                    except (FileNotFoundError, NotADirectoryError) as e:
                        log.debug(e)
                    else:
                        sys.stdout.write(os.sep * n)
                    sys.stdout.write(line[len(sanseol):])
                    allow = False
                    allowmatch = re.compile(f".{{,{m.start()}}}{re.escape(intro)}").match

if '__main__' == __name__:
    main()
