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

'Insert SHLVL indicator into given prompt.'
import sys

def main():
    print(insertshlvl(*sys.argv[1:]))

def insertshlvl(ps1, shlvl):
    try:
        colon = ps1.rindex(':')
    except ValueError:
        return ps1
    n = int(shlvl)
    tally = '"' * (n // 2) + ("'" if n % 2 else '')
    return f"{ps1[:colon]}{tally}{ps1[colon + 1:]}"

if '__main__' == __name__:
    main()
