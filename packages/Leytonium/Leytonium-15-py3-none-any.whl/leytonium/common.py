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

from lagoon import git, pkill, toilet
from lagoon.program import ONELINE
import subprocess, os, sys, traceback, re, collections, termcolor

infodirname = '.pb'
publicprefix = 'public/'

class UnknownParentException(Exception): pass

def stderr(*args, **kwargs):
    return termcolor.cprint(*args + ('red',), file = sys.stderr, **kwargs)

def highlight(*args, **kwargs):
    return termcolor.cprint(*args + ('yellow',), attrs = ['reverse'], **kwargs)

def addparents(branch, *parents, clobber = False):
    path = os.path.join(findproject(), infodirname, branch) # Note branch may contain slashes.
    os.makedirs(os.path.dirname(path), exist_ok = True)
    with open(path, 'w' if clobber else 'a') as f:
        for p in parents:
            print(p, file = f)

def savecommits(commits, clobber = False):
    path = os.path.join(findproject(), infodirname, f"{thisbranch()} slammed")
    os.makedirs(os.path.dirname(path), exist_ok = True)
    with open(path, 'w' if clobber else 'a') as f:
        for c in commits:
            print(c, file = f)

def savedcommits():
    path = os.path.join(findproject(), infodirname, f"{thisbranch()} slammed")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return f.read().splitlines()

def pb(b = None):
    if b is None:
        b = thisbranch()
    path = os.path.join(findproject(), infodirname, b)
    if not os.path.exists(path):
        raise UnknownParentException(b)
    with open(path) as f:
        return f.readline().splitlines()[0]

class AllBranches:

    def _published(self, name):
        try:
            lines = git.rev_parse(f"origin/{name}", stderr = subprocess.DEVNULL).splitlines()
        except:
            return None
        published, = lines # May be a merge.
        # Find parent of the first unpublished non-merge commit:
        nonmerges = set(id for id, _ in self.branchcommits(name))
        allcommits = git.log('--format=%H', name).splitlines()
        mergeableindex = 0
        for i, commit in enumerate(allcommits):
            if commit == published:
                return allcommits[mergeableindex] if mergeableindex else name
            if commit in nonmerges:
                mergeableindex = i + 1
        return published # What commit is this?

    def __init__(self):
        self.names = [line[2:] for line in git.branch().splitlines()]
        self.remotenames = set(git.remote().splitlines())

    def _matching(self, glob):
        regex = re.compile('.*'.join(re.escape(text) for text in re.split('[*]', glob)))
        for name in self.names:
            if regex.fullmatch(name):
                yield name

    def parents(self, b):
        def g():
            path = os.path.join(findproject(), infodirname, b)
            if not os.path.exists(path):
                return
            with open(path) as f:
                for line in f:
                    line, = line.splitlines()
                    if '*' in line:
                        public = line.startswith(publicprefix)
                        glob = line[len(publicprefix):] if public else line
                        for match in self._matching(glob):
                            if public:
                                mergeable = self._published(match)
                                if mergeable is not None:
                                    yield mergeable
                            else:
                                yield match
                    else:
                        yield line
        return list(g())

    def isremote(self, b):
        i = b.find('/')
        if -1 != i:
            return b[:i] in self.remotenames

    def branchcommits(self, b = None):
        if b is None:
            b = thisbranch()
        intersection = None # Logically this is the set of all commits.
        for pb in self.parents(b):
            nextinter = collections.OrderedDict()
            for line in reversed(git.cherry._v(pb, b).splitlines()):
                if intersection is None or line in intersection:
                    nextinter[line] = None
            intersection = nextinter
        if intersection is None:
            raise UnknownParentException(b) # Rebasing?
        def g():
            for line in intersection:
                commit, message = line.split(' ', 2)[1:]
                stat = ''.join("%%%sd%%s" % w % (n, u) for n, w, u in zip(map(int, re.findall('[0-9]+', git.show.__shortstat(commit).splitlines()[-1])), [2, 3, 3], 'f+-'))
                yield commit, f"{stat} {message}"
        return list(g())

def thisbranch():
    return git.rev_parse.__abbrev_ref.HEAD[ONELINE]()

def findproject(context = None):
    context = [] if context is None else [context]
    name = ['.git']
    k = 0
    path = os.path.join(*context + name)
    while not os.path.exists(path):
        k += 1
        parent = os.path.join(*context + k * ['..'] + name)
        if os.path.abspath(parent) == os.path.abspath(path):
            raise Exception('No project found.')
        path = parent
    return os.path.join(*k * ['..']) if k else '.'

def args():
    args = sys.argv[1:]
    del sys.argv[1:] # In case we call another main function.
    return args

def showmenu(entries, show = True, xform = lambda i: 1 + i, print = print):
    entries = [(xform(i), k, v) for i, (k, v) in enumerate(entries)]
    if show:
        for e in entries:
            print("%3d %s %s" % e, file = sys.stderr)
    return {n: k for n, k, _ in entries}

def menu(entries, prompt):
    ids = showmenu(entries)
    sys.stderr.write(f"{prompt}? ")
    n = int(input())
    return n, ids[n]

def showexception():
    for line in traceback.format_exception_only(*sys.exc_info()[:2]):
        sys.stderr.write(line)

def publicbranches():
    def g():
        for line in git.branch._vv().splitlines():
            if re.search(r' \[[^/]+/', line) is None:
                continue
            yield re.search(r'\S+', line[2:]).group()
    return list(g())

def getpublic(b = None):
    if b is None:
        b = thisbranch()
    lines = git.rev_parse.__abbrev_ref(f"{b}@{{upstream}}",
            check = False,
            stderr = subprocess.DEVNULL).stdout.splitlines()
    if lines:
        pub, = lines
        return pub

def nicely(task):
    killide = lambda sig: pkill._f[print](f"-{sig}", 'com.intellij.idea.Main', check = False)
    killide('STOP')
    try:
        nicelyimpl(task)
    finally:
        killide('CONT')

def nicelyimpl(task):
    stashed = ['No local changes to save'] != git.stash().splitlines()
    branch = thisbranch()
    try:
        task()
    except:
        if stashed:
            toilet[print]('-w', 500, '-f', 'smmono12', '--metal', 'You have a new stash:')
            git.stash.list[print]()
        raise
    git.checkout[print](branch)
    if stashed:
        git.stash.pop[print]()

def touchmsg():
    return f"WIP Touch {thisbranch()}"
