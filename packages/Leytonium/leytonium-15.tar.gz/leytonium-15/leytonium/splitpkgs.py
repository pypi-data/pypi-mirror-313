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

'Show packages that exist in more than one module.'
import os

def relativise(context, path):
    if context == path:
        return []
    else:
        return path[len(context + os.sep):].split(os.sep)

def main():
    packagetomodules = {}
    def register(module, package):
        try:
            packagetomodules[package].add(module)
        except KeyError:
            packagetomodules[package] = set([module])
    def findpackages(langpath):
        for dirpath, dirnames, filenames in os.walk(langpath):
            if filenames:
                package = relativise(langpath, dirpath)
                if not package:
                    yield '<unnamed>'
                elif 'META-INF' != package[0]:
                    yield '.'.join(package)
            dirnames.sort()
    def process(module, modulepath):
        srcpath = os.path.join(modulepath, 'src')
        if os.path.exists(srcpath):
            for scope in sorted(os.listdir(srcpath)):
                scopepath = os.path.join(srcpath, scope)
                for lang in sorted(os.listdir(scopepath)):
                    for package in findpackages(os.path.join(scopepath, lang)):
                        register(module, package)
    projectpath = '.'
    for dirpath, dirnames, filenames in os.walk(projectpath):
        if 'build.gradle' in filenames:
            process(''.join(f":{w}" for w in relativise(projectpath, dirpath)), dirpath)
        dirnames.sort()
    for package, modules in sorted(packagetomodules.items()):
        if 1 != len(modules):
            print(package)
            for m in modules:
                print(f"\t{m}")

if '__main__' == __name__:
    main()
