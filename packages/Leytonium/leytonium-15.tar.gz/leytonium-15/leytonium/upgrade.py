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

'Upgrade the system and silence the nag.'
from . import initlogging
from argparse import ArgumentParser
from lagoon import docker, sudo
from pathlib import Path
import logging

log = logging.getLogger(__name__)
boot = Path('/boot')

def main():
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('-k', action = 'store_true', help = 'first remove all kernels except old and current')
    args = parser.parse_args()
    apt_get = sudo.apt_get[print]
    if args.k:
        keep = {(boot / name).resolve() for name in ['vmlinuz.old', 'vmlinuz']}
        apt_get.remove(*(p.name.replace('vmlinuz', 'linux-image') for p in boot.glob('vmlinuz-*-generic') if p not in keep))
        apt_get.autoremove()
    apt_get.update()
    apt_get.__with_new_pkgs.upgrade()
    apt_get.autoremove()
    touchpath = Path.home() / 'var' / 'last-upgrade'
    touchpath.parent.mkdir(parents = True, exist_ok = True)
    touchpath.write_text('')
    log.info('Phased updates:')
    apt_get.upgrade.__dry_run('-o', 'APT::Get::Always-Include-Phased-Updates=true')
    log.info('Containers still up:')
    docker.ps[print]()

if '__main__' == __name__:
    main()
