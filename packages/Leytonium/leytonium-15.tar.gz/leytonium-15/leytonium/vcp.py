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

'Copy a Docker volume.'
from . import initlogging
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from lagoon import docker
import logging, shlex

log = logging.getLogger(__name__)

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'vcp.arid')
    parser = ArgumentParser()
    parser.add_argument('--rm', action = 'store_true')
    parser.add_argument('source')
    parser.add_argument('target')
    parser.parse_args(namespace = config.cli)
    target = config.target
    log.info("Create: %s", target)
    docker.volume.create[print](target) # XXX: Can we make this fail if the volume already exists?
    mount_source = config.mount.source
    mount_target = config.mount.target
    source = config.source
    log.info('Copy data.')
    docker.run.__rm[print]('-v', f"{source}:{mount_source}:ro", '-v', f"{target}:{mount_target}", '-w', mount_source, config.image, 'sh', '-c', f"exec cp -av . {shlex.quote(mount_target)}")
    if config.delete:
        log.info("Delete: %s", source)
        docker.volume.rm[print](source)

if '__main__' == __name__:
    main()
