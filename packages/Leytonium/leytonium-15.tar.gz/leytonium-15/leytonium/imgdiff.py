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

'Use container-diff to compare Docker images.'
from . import initlogging
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from lagoon import container_diff, diff, docker
from lagoon.program import partial
from lagoon.util import mapcm
from pathlib import Path
from tempfile import TemporaryDirectory

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'imgdiff.arid')
    parser = ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('tag', nargs = 2)
    parser.parse_args(namespace = config.cli)
    images = [f"{config.prefix}{config.name}:{t}" for t in config.tag]
    for image in images:
        docker.pull[print](image)
    with mapcm(Path, TemporaryDirectory()) as tempdir, docker.inspect[partial](images[0]) as f, docker.inspect[partial](images[1]) as g:
        p, q = (tempdir / t for t in config.tag)
        p.write_text(f.read())
        q.write_text(g.read())
        assert diff._u[print](p, q, check = False) in {0, 1}
    container_diff.diff._t.file[exec](*(f"daemon://{image}" for image in images))

if '__main__' == __name__:
    main()
