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

'Extract Adobe Ascii85-encoded images from given file.'
import sys, re, base64, os

pattern = re.compile('<~(.+?)~>', re.DOTALL)

def main():
    if os.listdir():
        raise Exception
    path, = sys.argv[1:]
    with open(path) as f:
        text = f.read()
    for i, image in enumerate(pattern.findall(text)):
        print(i)
        with open(f"{i}.png", 'wb') as g:
            g.write(base64.a85decode(image))

if '__main__' == __name__:
    main()
