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

# This file incorporates work covered by the following copyright and
# permission notice:

# Copyright (C) 2006-2019 Derrick Moser <derrick_moser@yahoo.com>
# Copyright (C) 2015-2020 Romain Failliot <romain.failliot@foolstep.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the license, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  You may also obtain a copy of the GNU General Public License
# from the Free Software Foundation by visiting their web site
# (http://www.fsf.org/) or by writing to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from .ui import logError
from .util import globEscape, isWindows, popenRead, popenReadLines, readlines, relpath, strip_eol
from gettext import gettext as _
import glob, os, shlex

# helper function prevent files from being confused with command line options
# by prepending './' to the basename
def safeRelativePath(abspath1, name, prefs, cygwin_pref):
    s = os.path.join(os.curdir, relpath(abspath1, os.path.abspath(name)))
    if isWindows:
        if prefs.getBool(cygwin_pref):
            s = s.replace('\\', '/')
        else:
            s = s.replace('/', '\\')
    return s

# simulate use of popen with xargs to read the output of a command
def popenXArgsReadLines(dn, cmd, args, prefs, bash_pref):
    # os.sysconf() is only available on Unix
    if hasattr(os, 'sysconf'):
        maxsize = os.sysconf('SC_ARG_MAX')
        maxsize -= sum([ len(k) + len(v) + 2 for k, v in os.environ.items() ])
    else:
        # assume the Window's limit to CreateProcess()
        maxsize = 32767
    maxsize -= sum([ len(k) + 1 for k in cmd ])
    ss = []
    i, s, a = 0, 0, []
    while i < len(args):
        f = (len(a) == 0)
        if f:
            # start a new command line
            a = cmd[:]
        elif s + len(args[i]) + 1 <= maxsize:
            f = True
        if f:
            # append another argument to the current command line
            a.append(args[i])
            s += len(args[i]) + 1
            i += 1
        if i == len(args) or not f:
            ss.extend(popenReadLines(dn, a, prefs, bash_pref))
            s, a = 0, []
    return ss

# utility class to help support Git and Monotone
# represents a set of files and folders of interest for "git status" or
# "mtn automate inventory"
class _VcsFolderSet:

    def __init__(self, names):
        self.folders = f = []
        for name in names:
            name = os.path.abspath(name)
            # ensure all names end with os.sep
            if not name.endswith(os.sep):
                name += os.sep
            f.append(name)

    # returns True if the given abspath is a file that should be included in
    # the interesting file subset
    def contains(self, abspath):
        if not abspath.endswith(os.sep):
            abspath += os.sep
        for f in self.folders:
            if abspath.startswith(f):
                return True
        return False

# utility method to help find folders used by version control systems
def _find_parent_dir_with(path, dir_name):
    while True:
        name = os.path.join(path, dir_name)
        if os.path.isdir(name):
            return path
        newpath = os.path.dirname(path)
        if newpath == path:
            break
        path = newpath

# These class implement the set of supported version control systems.  Each
# version control system should implement:
#
#   __init__():
#       the object will initialised with the repository's root folder
#
#   getFileTemplate():
#       indicates which revisions to display for a file when none were
#       explicitly requested
#
#   getCommitTemplate():
#       indicates which file revisions to display for a commit
#
#   getFolderTemplate():
#       indicates which file revisions to display for a set of folders
#
#   getRevision():
#       returns the contents of the specified file revision

# Bazaar support
class _Bzr:

    def __init__(self, root):
        self.root = root

    def getFileTemplate(self, prefs, name):
        # merge conflict
        left = name + '.OTHER'
        right = name + '.THIS'
        if os.path.isfile(left) and os.path.isfile(right):
            return [ (left, None), (name, None), (right, None) ]
        # default case
        return [ (name, '-1'), (name, None) ]

    def getCommitTemplate(self, prefs, rev, names):
        # build command
        args = [ prefs.getString('bzr_bin'), 'log', '-v', '-r', rev ]
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            args.append(safeRelativePath(self.root, name, prefs, 'bzr_cygwin'))
        # run command
        ss = popenReadLines(self.root, args, prefs, 'bzr_bash')
        # parse response
        prev = 'before:' + rev
        fs = _VcsFolderSet(names)
        added, modified, removed, renamed = {}, {}, {}, {}
        i, n = 0, len(ss)
        while i < n:
            s = ss[i]
            i += 1
            if s.startswith('added:'):
                # added files
                while i < n and ss[i].startswith('  '):
                    k = prefs.convertToNativePath(ss[i][2:])
                    i += 1
                    if not k.endswith(os.sep):
                        k = os.path.join(self.root, k)
                        if fs.contains(k):
                            if not isabs:
                                k = relpath(pwd, k)
                            added[k] = [ (None, None), (k, rev) ]
            elif s.startswith('modified:'):
                # modified files
                while i < n and ss[i].startswith('  '):
                    k = prefs.convertToNativePath(ss[i][2:])
                    i += 1
                    if not k.endswith(os.sep):
                        k = os.path.join(self.root, k)
                        if fs.contains(k):
                            if not isabs:
                                k = relpath(pwd, k)
                            modified[k] = [ (k, prev), (k, rev) ]
            elif s.startswith('removed:'):
                # removed files
                while i < n and ss[i].startswith('  '):
                    k = prefs.convertToNativePath(ss[i][2:])
                    i += 1
                    if not k.endswith(os.sep):
                        k = os.path.join(self.root, k)
                        if fs.contains(k):
                            if not isabs:
                                k = relpath(pwd, k)
                            removed[k] = [ (k, prev), (None, None) ]
            elif s.startswith('renamed:'):
                # renamed files
                while i < n and ss[i].startswith('  '):
                    k = ss[i][2:].split(' => ')
                    i += 1
                    if len(k) == 2:
                        k0 = prefs.convertToNativePath(k[0])
                        k1 = prefs.convertToNativePath(k[1])
                        if not k0.endswith(os.sep) and not k1.endswith(os.sep):
                            k0 = os.path.join(self.root, k0)
                            k1 = os.path.join(self.root, k1)
                            if fs.contains(k0) or fs.contains(k1):
                                if not isabs:
                                    k0 = relpath(pwd, k0)
                                    k1 = relpath(pwd, k1)
                                renamed[k1] = [ (k0, prev), (k1, rev) ]
        # sort the results
        result, r = [], set()
        for m in removed, added, modified, renamed:
            r.update(m.keys())
        for k in sorted(r):
            for m in removed, added, modified, renamed:
                if k in m:
                    result.append(m[k])
        return result

    def getFolderTemplate(self, prefs, names):
        # build command
        args = [ prefs.getString('bzr_bin'), 'status', '-SV' ]
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            args.append(safeRelativePath(self.root, name, prefs, 'bzr_cygwin'))
        # run command
        prev = '-1'
        fs = _VcsFolderSet(names)
        added, modified, removed, renamed = {}, {}, {}, {}
        for s in popenReadLines(self.root, args, prefs, 'bzr_bash'):
            # parse response
            if len(s) < 5:
                continue
            y, k = s[1], s[4:]
            if y == 'D':
                # removed
                k = prefs.convertToNativePath(k)
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = relpath(pwd, k)
                        removed[k] = [ (k, prev), (None, None) ]
            elif y == 'N':
                # added
                k = prefs.convertToNativePath(k)
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = relpath(pwd, k)
                        added[k] = [ (None, None), (k, None) ]
            elif y == 'M':
                # modified or merge conflict
                k = prefs.convertToNativePath(k)
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = relpath(pwd, k)
                        modified[k] = self.getFileTemplate(prefs, k)
            elif s[0] == 'R':
                # renamed
                k = k.split(' => ')
                if len(k) == 2:
                    k0 = prefs.convertToNativePath(k[0])
                    k1 = prefs.convertToNativePath(k[1])
                    if not k0.endswith(os.sep) and not k1.endswith(os.sep):
                        k0 = os.path.join(self.root, k0)
                        k1 = os.path.join(self.root, k1)
                        if fs.contains(k0) or fs.contains(k1):
                            if not isabs:
                                k0 = relpath(pwd, k0)
                                k1 = relpath(pwd, k1)
                            renamed[k1] = [ (k0, prev), (k1, None) ]
        # sort the results
        result, r = [], set()
        for m in removed, added, modified, renamed:
            r.update(m.keys())
        for k in sorted(r):
            for m in removed, added, modified, renamed:
                if k in m:
                    result.append(m[k])
        return result

    def getRevision(self, prefs, name, rev):
        return popenRead(self.root, [ prefs.getString('bzr_bin'), 'cat', '--name-from-revision', '-r', rev, safeRelativePath(self.root, name, prefs, 'bzr_cygwin') ], prefs, 'bzr_bash')

def _get_bzr_repo(path, prefs):
    p = _find_parent_dir_with(path, '.bzr')
    if p:
        return _Bzr(p)

# CVS support
class _Cvs:

    def __init__(self, root):
        self.root = root

    def getFileTemplate(self, prefs, name):
        return [ (name, 'BASE'), (name, None) ]

    def getCommitTemplate(self, prefs, rev, names):
        result = []
        try:
            r, prev = rev.split('.'), None
            if len(r) > 1:
                m = int(r.pop())
                if m > 1:
                    r.append(str(m - 1))
                else:
                    m = int(r.pop())
                if len(r):
                    prev = '.'.join(r)
            for k in sorted(names):
                 if prev is None:
                     k0 = None
                 else:
                     k0 = k
                 result.append([ (k0, prev), (k, rev) ])
        except ValueError:
            logError(_('Error parsing revision %s.') % (rev, ))
        return result

    def getFolderTemplate(self, prefs, names):
        # build command
        args = [ prefs.getString('cvs_bin'), '-nq', 'update', '-R' ]
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            args.append(safeRelativePath(self.root, name, prefs, 'cvs_cygwin'))
        # run command
        prev = 'BASE'
        fs = _VcsFolderSet(names)
        modified = {}
        for s in popenReadLines(self.root, args, prefs, 'cvs_bash'):
            # parse response
            if len(s) < 3 or s[0] not in 'ACMR':
                continue
            k = os.path.join(self.root, prefs.convertToNativePath(s[2:]))
            if fs.contains(k):
                if not isabs:
                    k = relpath(pwd, k)
                if s[0] == 'R':
                    # removed
                    modified[k] = [ (k, prev), (None, None) ]
                    pass
                elif s[0] == 'A':
                    # added
                    modified[k] = [ (None, None), (k, None) ]
                else:
                    # modified
                    modified[k] = [ (k, prev), (k, None) ]
        # sort the results
        return [ modified[k] for k in sorted(modified.keys()) ]

    def getRevision(self, prefs, name, rev):
        if rev == 'BASE' and not os.path.exists(name):
            # find revision for removed files
            for s in popenReadLines(self.root, [ prefs.getString('cvs_bin'), 'status', safeRelativePath(self.root, name, prefs, 'cvs_cygwin') ], prefs, 'cvs_bash'):
                if s.startswith('   Working revision:\t-'):
                    rev = s.split('\t')[1][1:]
        return popenRead(self.root, [ prefs.getString('cvs_bin'), '-Q', 'update', '-p', '-r', rev, safeRelativePath(self.root, name, prefs, 'cvs_cygwin') ], prefs, 'cvs_bash')

def _get_cvs_repo(path, prefs):
    if os.path.isdir(os.path.join(path, 'CVS')):
        return _Cvs(path)

# Darcs support
class _Darcs:

    def __init__(self, root):
        self.root = root

    def getFileTemplate(self, prefs, name):
        return [ (name, ''), (name, None) ]

    def _getCommitTemplate(self, prefs, names, rev):
        mods = (rev is None)
        # build command
        args = [ prefs.getString('darcs_bin') ]
        if mods:
            args.extend(['whatsnew', '-s'])
        else:
            args.extend(['log', '--number', '-s'])
            try:
                args.extend(['-n', str(int(rev))])
            except ValueError:
                args.extend(['-h', rev])
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            if mods:
                args.append(safeRelativePath(self.root, name, prefs, 'darcs_cygwin'))
        # run command
        # 'darcs whatsnew' will return 1 if there are no changes
        ss = popenReadLines(self.root, args, prefs, 'darcs_bash', [0, 1])
        # parse response
        i, n = 0, len(ss)
        if mods:
            prev = ''
            rev = None
        else:
            try:
                rev = ss[0].split(':')[0]
                prev = str(int(rev) + 1)
                # skip to the beginning of the summary
                while i < n and len(ss[i]):
                    i += 1
            except (ValueError, IndexError):
                i = n
        fs = _VcsFolderSet(names)
        added, modified, removed, renamed = {}, {}, {}, {}
        while i < n:
            s = ss[i]
            i += 1
            if not mods:
                if s.startswith('    '):
                    s = s[4:]
                else:
                    continue
            if len(s) < 2:
                continue
            x = s[0]
            if x == 'R':
                # removed
                k = prefs.convertToNativePath(s[2:])
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = relpath(pwd, k)
                        removed[k] = [ (k, prev), (None, None) ]
            elif x == 'A':
                # added
                k = prefs.convertToNativePath(s[2:])
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = relpath(pwd, k)
                        added[k] = [ (None, None), (k, rev) ]
            elif x == 'M':
                # modified
                k = prefs.convertToNativePath(s[2:].split(' ')[0])
                if not k.endswith(os.sep):
                    k = os.path.join(self.root, k)
                    if fs.contains(k):
                        if not isabs:
                            k = relpath(pwd, k)
                        if k not in renamed:
                            modified[k] = [ (k, prev), (k, rev) ]
            elif x == ' ':
                # renamed
                k = s[1:].split(' -> ')
                if len(k) == 2:
                    k0 = prefs.convertToNativePath(k[0])
                    k1 = prefs.convertToNativePath(k[1])
                    if not k0.endswith(os.sep):
                        k0 = os.path.join(self.root, k0)
                        k1 = os.path.join(self.root, k1)
                        if fs.contains(k0) or fs.contains(k1):
                            if not isabs:
                                k0 = relpath(pwd, k0)
                                k1 = relpath(pwd, k1)
                            renamed[k1] = [ (k0, prev), (k1, rev) ]
        # sort the results
        result, r = [], set()
        for m in added, modified, removed, renamed:
            r.update(m.keys())
        for k in sorted(r):
            for m in removed, added, modified, renamed:
                if k in m:
                    result.append(m[k])
        return result

    def getCommitTemplate(self, prefs, rev, names):
        return self._getCommitTemplate(prefs, names, rev)

    def getFolderTemplate(self, prefs, names):
        return self._getCommitTemplate(prefs, names, None)

    def getRevision(self, prefs, name, rev):
        args = [ prefs.getString('darcs_bin'), 'show', 'contents' ]
        try:
            args.extend([ '-n', str(int(rev)) ])
        except ValueError:
            args.extend([ '-h', rev ])
        args.append(safeRelativePath(self.root, name, prefs, 'darcs_cygwin'))
        return popenRead(self.root, args, prefs, 'darcs_bash')

def _get_darcs_repo(path, prefs):
    p = _find_parent_dir_with(path, '_darcs')
    if p:
        return _Darcs(p)

# Git support
class _Git:

    def __init__(self, root):
        self.root = root

    def getFileTemplate(self, prefs, name):
        return [ (name, 'HEAD'), (name, None) ]

    def getCommitTemplate(self, prefs, rev, names):
        # build command
        args = [ prefs.getString('git_bin'), 'show', '--pretty=format:', '--name-status', rev ]
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
        # run command
        prev = rev + '^'
        fs = _VcsFolderSet(names)
        modified = {}
        for s in popenReadLines(self.root, args, prefs, 'git_bash'):
            # parse response
            if len(s) < 2 or s[0] not in 'ADM':
                continue
            k = self._extractPath(s[2:], prefs)
            if fs.contains(k):
                if not isabs:
                    k = relpath(pwd, k)
                if s[0] == 'D':
                    # removed
                    modified[k] = [ (k, prev), (None, None) ]
                elif s[0] == 'A':
                    # added
                    modified[k] = [ (None, None), (k, rev) ]
                else:
                    # modified
                    modified[k] = [ (k, prev), (k, rev) ]
        # sort the results
        return [ modified[k] for k in sorted(modified.keys()) ]

    def _extractPath(self, s, prefs):
        return os.path.join(self.root, prefs.convertToNativePath(s.strip()))

    def getFolderTemplate(self, prefs, names):
        # build command
        args = [ prefs.getString('git_bin'), 'status', '--porcelain', '-s', '--untracked-files=no', '--ignore-submodules=all' ]
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
        # run command
        prev = 'HEAD'
        fs = _VcsFolderSet(names)
        modified, renamed = {}, {}
        # 'git status' will return 1 when a commit would fail
        for s in popenReadLines(self.root, args, prefs, 'git_bash', [0, 1]):
            # parse response
            if len(s) < 3:
                continue
            x, y, k = s[0], s[1], s[2:]
            if x == 'R':
                # renamed
                k = k.split(' -> ')
                if len(k) == 2:
                    k0 = self._extractPath(k[0], prefs)
                    k1 = self._extractPath(k[1], prefs)
                    if fs.contains(k0) or fs.contains(k1):
                        if not isabs:
                            k0 = relpath(pwd, k0)
                            k1 = relpath(pwd, k1)
                        renamed[k1] = [ (k0, prev), (k1, None) ]
            elif x == 'U' or y == 'U' or (x == 'D' and y == 'D'):
                # merge conflict
                k = self._extractPath(k, prefs)
                if fs.contains(k):
                    if not isabs:
                        k = relpath(pwd, k)
                    if x == 'D':
                        panes = [ (None, None) ]
                    else:
                        panes = [ (k, ':2') ]
                    panes.append((k, None))
                    if y == 'D':
                        panes.append((None, None))
                    else:
                        panes.append((k, ':3'))
                    if x != 'A' and y != 'A':
                        panes.append((k, ':1'))
                    modified[k] = panes
            else:
                k = self._extractPath(k, prefs)
                if fs.contains(k):
                    if not isabs:
                        k = relpath(pwd, k)
                    if x == 'A':
                        # added
                        panes = [ (None, None) ]
                    else:
                        panes = [ (k, prev) ]
                    # staged changes
                    if x == 'D':
                        panes.append((None, None))
                    elif x != ' ':
                        panes.append((k, ':0'))
                    # working copy changes
                    if y == 'D':
                        panes.append((None, None))
                    elif y != ' ':
                        panes.append((k, None))
                    modified[k] = panes
        # sort the results
        result, r = [], set()
        for m in modified, renamed:
            r.update(m.keys())
        for k in sorted(r):
            for m in modified, renamed:
                if k in m:
                    result.append(m[k])
        return result

    def getRevision(self, prefs, name, rev):
        return popenRead(self.root, [ prefs.getString('git_bin'), 'show', '{}:{}'.format(rev, relpath(self.root, os.path.abspath(name)).replace(os.sep, '/')) ], prefs, 'git_bash')

def _get_git_repo(path, prefs):
    if 'GIT_DIR' in os.environ:
        try:
            d = path
            ss = popenReadLines(d, [ prefs.getString('git_bin'), 'rev-parse', '--show-prefix' ], prefs, 'git_bash')
            if len(ss) > 0:
                # be careful to handle trailing slashes
                d = d.split(os.sep)
                if d[-1] != '':
                    d.append('')
                ss = strip_eol(ss[0]).split('/')
                if ss[-1] != '':
                    ss.append('')
                n = len(ss)
                if n <= len(d):
                    del d[-n:]
                if len(d) == 0:
                    d = os.curdir
                else:
                    d = os.sep.join(d)
            return _Git(d)
        except (IOError, OSError):
            # working tree not found
            pass
    # search for .git direcotry (project) or .git file (submodule)
    while True:
        name = os.path.join(path, '.git')
        if os.path.isdir(name) or os.path.isfile(name):
            return _Git(path)
        newpath = os.path.dirname(path)
        if newpath == path:
            break
        path = newpath

# Mercurial support
class _Hg:

    def __init__(self, root):
        self.root = root
        self.working_rev = None

    def _getPreviousRevision(self, prefs, rev):
        if rev is None:
            if self.working_rev is None:
                ss = popenReadLines(self.root, [ prefs.getString('hg_bin'), 'id', '-i', '-t' ], prefs, 'hg_bash')
                if len(ss) != 1:
                    raise IOError('Unknown working revision')
                ss = ss[0].split(' ')
                prev = ss[-1]
                if len(ss) == 1 and prev.endswith('+'):
                    # remove local modifications indicator
                    prev = prev[:-1]
                self.working_rev = prev
            return self.working_rev
        return f'p1({rev})'

    def getFileTemplate(self, prefs, name):
        return [ (name, self._getPreviousRevision(prefs, None)), (name, None) ]

    def _getCommitTemplate(self, prefs, names, cmd, rev):
        # build command
        args = [ prefs.getString('hg_bin') ]
        args.extend(cmd)
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            args.append(safeRelativePath(self.root, name, prefs, 'hg_cygwin'))
        # run command
        prev = self._getPreviousRevision(prefs, rev)
        fs = _VcsFolderSet(names)
        modified = {}
        for s in popenReadLines(self.root, args, prefs, 'hg_bash'):
            # parse response
            if len(s) < 3 or s[0] not in 'AMR':
                continue
            k = os.path.join(self.root, prefs.convertToNativePath(s[2:]))
            if fs.contains(k):
                if not isabs:
                    k = relpath(pwd, k)
                if s[0] == 'R':
                    # removed
                    modified[k] = [ (k, prev), (None, None) ]
                elif s[0] == 'A':
                    # added
                    modified[k] = [ (None, None), (k, rev) ]
                else:
                    # modified or merge conflict
                    modified[k] = [ (k, prev), (k, rev) ]
        # sort the results
        return [ modified[k] for k in sorted(modified.keys()) ]

    def getCommitTemplate(self, prefs, rev, names):
        return self._getCommitTemplate(prefs, names, [ 'log', '--template', 'A\t{file_adds}\nM\t{file_mods}\nR\t{file_dels}\n', '-r', rev ], rev)

    def getFolderTemplate(self, prefs, names):
        return self._getCommitTemplate(prefs, names, [ 'status', '-q' ], None)

    def getRevision(self, prefs, name, rev):
        return popenRead(self.root, [ prefs.getString('hg_bin'), 'cat', '-r', rev, safeRelativePath(self.root, name, prefs, 'hg_cygwin') ], prefs, 'hg_bash')

def _get_hg_repo(path, prefs):
    p = _find_parent_dir_with(path, '.hg')
    if p:
        return _Hg(p)

# Monotone support
class _Mtn:

    def __init__(self, root):
        self.root = root

    def getFileTemplate(self, prefs, name):
        # FIXME: merge conflicts?
        return [ (name, 'h:'), (name, None) ]

    def getCommitTemplate(self, prefs, rev, names):
        # build command
        vcs_bin = prefs.getString('mtn_bin')
        ss = popenReadLines(self.root, [ vcs_bin, 'automate', 'select', '-q', rev ], prefs, 'mtn_bash')
        if len(ss) != 1:
            raise IOError('Ambiguous revision specifier')
        args = [ vcs_bin, 'automate', 'get_revision', ss[0] ]
        # build list of interesting files
        fs = _VcsFolderSet(names)
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
        # run command
        prev = None
        removed, added, modified, renamed = {}, {}, {}, {}
        ss = popenReadLines(self.root, args, prefs, 'mtn_bash')
        i = 0
        while i < len(ss):
            # process results
            s = shlex.split(ss[i])
            i += 1
            if len(s) < 2:
                continue
            arg, arg1 = s[0], s[1]
            if arg == 'old_revision' and len(arg1) > 2:
                if prev is not None:
                    break
                prev = arg1[1:-1]
                continue
            elif prev is None:
                continue
            if arg == 'delete':
                # deleted file
                k = os.path.join(self.root, prefs.convertToNativePath(arg1))
                if fs.contains(k):
                    removed[arg1] = k
            elif arg == 'add_file':
                # new file
                k = os.path.join(self.root, prefs.convertToNativePath(arg1))
                if fs.contains(k):
                    added[arg1] = k
            elif arg == 'patch':
                # modified file
                k = os.path.join(self.root, prefs.convertToNativePath(arg1))
                if fs.contains(k):
                    modified[arg1] = k
            elif arg == 'rename':
                s = shlex.split(ss[i])
                i += 1
                if len(s) > 1 and s[0] == 'to':
                    # renamed file
                    k0 = os.path.join(self.root, prefs.convertToNativePath(arg1))
                    k1 = os.path.join(self.root, prefs.convertToNativePath(s[1]))
                    if fs.contains(k0) or fs.contains(k1):
                        renamed[s[1]] = (arg1, k0, k1)
        if removed or renamed:
            # remove directories
            removed_dirs = set()
            for s in popenReadLines(self.root, [ vcs_bin, 'automate', 'get_manifest_of', prev ], prefs, 'mtn_bash'):
                s = shlex.split(s)
                if len(s) > 1 and s[0] == 'dir':
                    removed_dirs.add(s[1])
            for k in removed_dirs:
                for m in removed, modified:
                    if k in m:
                        del m[k]
            for k, v in renamed.items():
                arg1, k0, k1 = v
                if arg1 in removed_dirs:
                    del renamed[k]
        # sort results
        result, r = [], set()
        for m in removed, added, modified, renamed:
            r.update(m)
        for k in sorted(r):
            if k in removed:
                k = removed[k]
                if not isabs:
                    k = relpath(pwd, k)
                result.append([ (k, prev), (None, None) ])
            elif k in added:
                k = added[k]
                if not isabs:
                    k = relpath(pwd, k)
                result.append([ (None, None), (k, rev) ])
            else:
                if k in renamed:
                    arg1, k0, k1 = renamed[k]
                else:
                    k0 = k1 = modified[k]
                if not isabs:
                    k0 = relpath(pwd, k0)
                    k1 = relpath(pwd, k1)
                result.append([ (k0, prev), (k1, rev) ])
        return result

    def getFolderTemplate(self, prefs, names):
        fs = _VcsFolderSet(names)
        result = []
        pwd, isabs = os.path.abspath(os.curdir), False
        args = [ prefs.getString('mtn_bin'), 'automate', 'inventory', '--no-ignored', '--no-unchanged', '--no-unknown' ]
        for name in names:
            isabs |= os.path.isabs(name)
        # build list of interesting files
        prev = 'h:'
        ss = popenReadLines(self.root, args, prefs, 'mtn_bash')
        removed, added, modified, renamed = {}, {}, {}, {}
        i = 0
        while i < len(ss):
            # parse properties
            m = {}
            while i < len(ss):
                s = ss[i]
                i += 1
                # properties are terminated by a blank line
                s = shlex.split(s)
                if len(s) == 0:
                    break
                m[s[0]] = s[1:]
            # scan the list of properties for files that interest us
            if len(m.get('path', [])) > 0:
                p, s, processed = m['path'][0], m.get('status', []), False
                if 'dropped' in s and 'file' in m.get('old_type', []):
                    # deleted file
                    k = os.path.join(self.root, prefs.convertToNativePath(p))
                    if fs.contains(k):
                        if not isabs:
                            k = relpath(pwd, k)
                        removed[k] = [ (k, prev), (None, None) ]
                    processed = True
                if 'added' in s and 'file' in m.get('new_type', []):
                    # new file
                    k = os.path.join(self.root, prefs.convertToNativePath(p))
                    if fs.contains(k):
                        if not isabs:
                            k = relpath(pwd, k)
                        added[k] = [ (None, None), (k, None) ]
                    processed = True
                if 'rename_target' in s and 'file' in m.get('new_type', []) and len(m.get('old_path', [])) > 0:
                    # renamed file
                    k0 = os.path.join(self.root, prefs.convertToNativePath(m['old_path'][0]))
                    k1 = os.path.join(self.root, prefs.convertToNativePath(p))
                    if fs.contains(k0) or fs.contains(k1):
                        if not isabs:
                            k0 = relpath(pwd, k0)
                            k1 = relpath(pwd, k1)
                        renamed[k1] = [ (k0, prev), (k1, None) ]
                    processed = True
                if not processed and 'file' in m.get('fs_type', []):
                    # modified file or merge conflict
                    k = os.path.join(self.root, prefs.convertToNativePath(p))
                    if fs.contains(k):
                        if not isabs:
                            k = relpath(pwd, k)
                        modified[k] = [ (k, prev), (k, None) ]
        # sort the results
        r = set()
        for m in removed, added, modified, renamed:
            r.update(m.keys())
        for k in sorted(r):
            for m in removed, added, modified, renamed:
                if k in m:
                    result.append(m[k])
        return result

    def getRevision(self, prefs, name, rev):
        return popenRead(self.root, [ prefs.getString('mtn_bin'), 'automate', 'get_file_of', '-q', '-r', rev, safeRelativePath(self.root, name, prefs, 'mtn_cygwin') ], prefs, 'mtn_bash')

def _get_mtn_repo(path, prefs):
    p = _find_parent_dir_with(path, '_MTN')
    if p:
        return _Mtn(p)

# RCS support
class _Rcs:

    def __init__(self, root):
        self.root = root

    def getFileTemplate(self, prefs, name):
        args = [ prefs.getString('rcs_bin_rlog'), '-L', '-h', safeRelativePath(self.root, name, prefs, 'rcs_cygwin') ]
        rev = ''
        for line in popenReadLines(self.root, args, prefs, 'rcs_bash'):
            if line.startswith('head: '):
                rev = line[6:]
        return [ (name, rev), (name, None) ]

    def getCommitTemplate(self, prefs, rev, names):
        result = []
        try:
            r, prev = rev.split('.'), None
            if len(r) > 1:
                m = int(r.pop())
                if m > 1:
                    r.append(str(m - 1))
                else:
                    m = int(r.pop())
                if len(r):
                    prev = '.'.join(r)
            for k in sorted(names):
                if prev is None:
                    k0 = None
                else:
                    k0 = k
                result.append([ (k0, prev), (k, rev) ])
        except ValueError:
            logError(_('Error parsing revision %s.') % (rev, ))
        return result

    def getFolderTemplate(self, prefs, names):
        # build command
        cmd = [ prefs.getString('rcs_bin_rlog'), '-L', '-h' ]
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        r = []
        for k in names:
            if os.path.isdir(k):
                # the user specified a folder
                n, ex = [ k ], True
                while len(n) > 0:
                    s = n.pop()
                    recurse = os.path.isdir(os.path.join(s, 'RCS'))
                    if ex or recurse:
                        ex = False
                        for v in os.listdir(s):
                            dn = os.path.join(s, v)
                            if v.endswith(',v') and os.path.isfile(dn):
                                # map to checkout name
                                r.append(dn[:-2])
                            elif v == 'RCS' and os.path.isdir(dn):
                                for v in os.listdir(dn):
                                    if os.path.isfile(os.path.join(dn, v)):
                                        if v.endswith(',v'):
                                            v = v[:-2]
                                        r.append(os.path.join(s, v))
                            elif recurse and os.path.isdir(dn) and not os.path.islink(dn):
                                n.append(dn)
            else:
                # the user specified a file
                s = k + ',v'
                if os.path.isfile(s):
                    r.append(k)
                    continue
                s = k.split(os.sep)
                s.insert(-1, 'RCS')
                # old-style RCS repository
                if os.path.isfile(os.sep.join(s)):
                    r.append(k)
                    continue
                # new-style RCS repository
                s[-1] += ',v'
                if os.path.isfile(os.sep.join(s)):
                    r.append(k)
        for k in r:
            isabs |= os.path.isabs(k)
        args = [ safeRelativePath(self.root, k, prefs, 'rcs_cygwin') for k in r ]
        # run command
        r, k = {}, ''
        for line in popenXArgsReadLines(self.root, cmd, args, prefs, 'rcs_bash'):
            # parse response
            if line.startswith('Working file: '):
                k = prefs.convertToNativePath(line[14:])
                k = os.path.join(self.root, os.path.normpath(k))
                if not isabs:
                    k = relpath(pwd, k)
            elif line.startswith('head: '):
                r[k] = line[6:]
        # sort the results
        return [ [ (k, r[k]), (k, None) ] for k in sorted(r.keys()) ]

    def getRevision(self, prefs, name, rev):
        return popenRead(self.root, [ prefs.getString('rcs_bin_co'), '-p', '-q', '-r' + rev, safeRelativePath(self.root, name, prefs, 'rcs_cygwin') ], prefs, 'rcs_bash')

def _get_rcs_repo(path, prefs):
    if os.path.isdir(os.path.join(path, 'RCS')):
        return _Rcs(path)
    # [rfailliot] this code doesn't seem to work, but was in 0.4.8 too.
    # I'm letting it here until further tests are done, but it is possible
    # this code never actually worked.
    try:
        for s in os.listdir(path):
            if s.endswith(',v') and os.path.isfile(os.path.join(path, s)):
                return _Rcs(path)
    except OSError:
        # the user specified an invalid folder name
        pass

# Subversion support
# SVK support subclasses from this
class _Svn:

    def __init__(self, root):
        self.root = root
        self.url = None

    def _getVcs(self):
        return 'svn'

    def _getURLPrefix(self):
        return 'URL: '

    def _parseStatusLine(self, s):
        if len(s) < 8 or s[0] not in 'ACDMR':
            return
        # subversion 1.6 adds a new column
        k = 7
        if k < len(s) and s[k] == ' ':
            k += 1
        return s[0], s[k:]

    def _getPreviousRevision(self, rev):
        if rev is None:
            return 'BASE'
        m = int(rev)
        if m > 1:
            return str(m - 1)

    def _getURL(self, prefs):
        if self.url is None:
            vcs, prefix = self._getVcs(), self._getURLPrefix()
            n = len(prefix)
            args = [ prefs.getString(vcs + '_bin'), 'info' ]
            for s in popenReadLines(self.root, args, prefs, vcs + '_bash'):
                if s.startswith(prefix):
                    self.url = s[n:]
                    break
        return self.url

    def getFileTemplate(self, prefs, name):
        # FIXME: verify this
        # merge conflict
        escaped_name = globEscape(name)
        left = glob.glob(escaped_name + '.merge-left.r*')
        right = glob.glob(escaped_name + '.merge-right.r*')
        if len(left) > 0 and len(right) > 0:
            return [ (left[-1], None), (name, None), (right[-1], None) ]
        # update conflict
        left = sorted(glob.glob(escaped_name + '.r*'))
        right = glob.glob(escaped_name + '.mine')
        right.extend(glob.glob(escaped_name + '.working'))
        if len(left) > 0 and len(right) > 0:
            return [ (left[-1], None), (name, None), (right[0], None) ]
        # default case
        return [ (name, self._getPreviousRevision(None)), (name, None) ]

    def _getCommitTemplate(self, prefs, rev, names):
        result = []
        try:
            prev = self._getPreviousRevision(rev)
        except ValueError:
            logError(_('Error parsing revision %s.') % (rev, ))
            return result
        # build command
        vcs = self._getVcs()
        vcs_bin, vcs_bash = prefs.getString(vcs + '_bin'), vcs + '_bash'
        if rev is None:
            args = [ vcs_bin, 'status', '-q' ]
        else:
            args = [ vcs_bin, 'diff', '--summarize', '-c', rev ]
        # build list of interesting files
        pwd, isabs = os.path.abspath(os.curdir), False
        for name in names:
            isabs |= os.path.isabs(name)
            if rev is None:
                args.append(safeRelativePath(self.root, name, prefs, vcs + '_cygwin'))
        # run command
        fs = _VcsFolderSet(names)
        modified, added, removed = {}, set(), set()
        for s in popenReadLines(self.root, args, prefs, vcs_bash):
            status = self._parseStatusLine(s)
            if status is None:
                continue
            v, k = status
            rel = prefs.convertToNativePath(k)
            k = os.path.join(self.root, rel)
            if fs.contains(k):
                if v == 'D':
                    # deleted file or directory
                    # the contents of deleted folders are not reported
                    # by "svn diff --summarize -c <rev>"
                    removed.add(rel)
                elif v == 'A':
                    # new file or directory
                    added.add(rel)
                elif v == 'M':
                    # modified file or merge conflict
                    k = os.path.join(self.root, k)
                    if not isabs:
                        k = relpath(pwd, k)
                    modified[k] = [ (k, prev), (k, rev) ]
                elif v == 'C':
                    # merge conflict
                    modified[k] = self.getFileTemplate(prefs, k)
                elif v == 'R':
                    # replaced file
                    removed.add(rel)
                    added.add(rel)
        # look for files in the added items
        if rev is None:
            m, added = added, {}
            for k in m:
                if not os.path.isdir(k):
                    # confirmed as added file
                    k = os.path.join(self.root, k)
                    if not isabs:
                        k = relpath(pwd, k)
                    added[k] = [ (None, None), (k, None) ]
        else:
            m = {}
            for k in added:
                d, b = os.path.dirname(k), os.path.basename(k)
                if d not in m:
                    m[d] = set()
                m[d].add(b)
            # remove items we can easily determine to be directories
            for k in m.keys():
                d = os.path.dirname(k)
                if d in m:
                    m[d].discard(os.path.basename(k))
                    if not m[d]:
                        del m[d]
            # determine which are directories
            added = {}
            for p, v in m.items():
                for s in popenReadLines(self.root, [ vcs_bin, 'list', '-r', rev, '{}/{}'.format(self._getURL(prefs), p.replace(os.sep, '/')) ], prefs, vcs_bash):
                    if s in v:
                        # confirmed as added file
                        k = os.path.join(self.root, os.path.join(p, s))
                        if not isabs:
                            k = relpath(pwd, k)
                        added[k] = [ (None, None), (k, rev) ]
        # determine if removed items are files or directories
        if prev == 'BASE':
            m, removed = removed, {}
            for k in m:
                if not os.path.isdir(k):
                    # confirmed item as file
                    k = os.path.join(self.root, k)
                    if not isabs:
                        k = relpath(pwd, k)
                    removed[k] = [ (k, prev), (None, None) ]
        else:
            m = {}
            for k in removed:
                d, b = os.path.dirname(k), os.path.basename(k)
                if d not in m:
                    m[d] = set()
                m[d].add(b)
            removed_dir, removed = set(), {}
            for p, v in m.items():
                for s in popenReadLines(self.root, [ vcs_bin, 'list', '-r', prev, '{}/{}'.format(self._getURL(prefs), p.replace(os.sep, '/')) ], prefs, vcs_bash):
                    if s.endswith('/'):
                        s = s[:-1]
                        if s in v:
                            # confirmed item as directory
                            removed_dir.add(os.path.join(p, s))
                    else:
                        if s in v:
                            # confirmed item as file
                            k = os.path.join(self.root, os.path.join(p, s))
                            if not isabs:
                                k = relpath(pwd, k)
                            removed[k] = [ (k, prev), (None, None) ]
            # recursively find all unreported removed files
            while removed_dir:
                tmp = removed_dir
                removed_dir = set()
                for p in tmp:
                    for s in popenReadLines(self.root, [ vcs_bin, 'list', '-r', prev, '{}/{}'.format(self._getURL(prefs), p.replace(os.sep, '/')) ], prefs, vcs_bash):
                        if s.endswith('/'):
                            # confirmed item as directory
                            removed_dir.add(os.path.join(p, s[:-1]))
                        else:
                            # confirmed item as file
                            k = os.path.join(self.root, os.path.join(p, s))
                            if not isabs:
                                k = relpath(pwd, k)
                            removed[k] = [ (k, prev), (None, None) ]
        # sort the results
        r = set()
        for m in removed, added, modified:
            r.update(m.keys())
        for k in sorted(r):
            for m in removed, added, modified:
                if k in m:
                    result.append(m[k])
        return result

    def getCommitTemplate(self, prefs, rev, names):
        return self._getCommitTemplate(prefs, rev, names)

    def getFolderTemplate(self, prefs, names):
        return self._getCommitTemplate(prefs, None, names)

    def getRevision(self, prefs, name, rev):
        vcs_bin = prefs.getString('svn_bin')
        if rev in [ 'BASE', 'COMMITTED', 'PREV' ]:
            return popenRead(self.root, [ vcs_bin, 'cat', '{}@{}'.format(safeRelativePath(self.root, name, prefs, 'svn_cygwin'), rev) ], prefs, 'svn_bash')
        return popenRead(self.root, [ vcs_bin, 'cat', '{}/{}@{}'.format(self._getURL(prefs), relpath(self.root, os.path.abspath(name)).replace(os.sep, '/'), rev) ], prefs, 'svn_bash')

def _get_svn_repo(path, prefs):
    p = _find_parent_dir_with(path, '.svn')
    if p:
        return _Svn(p)

class _Svk(_Svn):

    def _getVcs(self):
        return 'svk'

    def _getURLPrefix(self):
        return 'Depot Path: '

    def _parseStatusLine(self, s):
        if len(s) < 4 or s[0] not in 'ACDMR':
            return
        return s[0], s[4:]

    def _getPreviousRevision(self, rev):
        if rev is None:
            return 'HEAD'
        if rev.endswith('@'):
            return str(int(rev[:-1]) - 1) + '@'
        return str(int(rev) - 1)

    def getRevision(self, prefs, name, rev):
        return popenRead(self.root, [ prefs.getString('svk_bin'), 'cat', '-r', rev, '{}/{}'.format(self._getURL(prefs), relpath(self.root, os.path.abspath(name)).replace(os.sep, '/')) ], prefs, 'svk_bash')

def _get_svk_repo(path, prefs):
    name = path
    # parse the ~/.svk/config file to discover which directories are part of
    # SVK repositories
    if isWindows:
        name = name.upper()
    svkroot = os.environ.get('SVKROOT', None)
    if svkroot is None:
        svkroot = os.path.expanduser('~/.svk')
    svkconfig = os.path.join(svkroot, 'config')
    if os.path.isfile(svkconfig):
        try:
            # find working copies by parsing the config file
            f = open(svkconfig, 'r')
            ss = readlines(f)
            f.close()
            projs, sep = [], os.sep
            # find the separator character
            for s in ss:
                if s.startswith('  sep: ') and len(s) > 7:
                    sep = s[7]
            # find the project directories
            i = 0
            while i < len(ss):
                s = ss[i]
                i += 1
                if s.startswith('  hash: '):
                    while i < len(ss) and ss[i].startswith('    '):
                        s = ss[i]
                        i += 1
                        if s.endswith(': ') and i < len(ss) and ss[i].startswith('      depotpath: '):
                            key = s[4:-2].replace(sep, os.sep)
                            # parse directory path
                            j, n, tt = 0, len(key), []
                            while j < n:
                                if key[j] == '"':
                                    # quoted string
                                    j += 1
                                    while j < n:
                                        if key[j] == '"':
                                            j += 1
                                            break
                                        elif key[j] == '\\':
                                            # escaped character
                                            j += 1
                                        if j < n:
                                            tt.append(key[j])
                                            j += 1
                                else:
                                    tt.append(key[j])
                                    j += 1
                            key = ''.join(tt).replace(sep, os.sep)
                            if isWindows:
                                key = key.upper()
                            projs.append(key)
                    break
            # check if the file belongs to one of the project directories
            if _VcsFolderSet(projs).contains(name):
                return _Svk(path)
        except IOError:
            logError(_('Error parsing %s.') % (svkconfig, ))

class VCSs:

    repolookup = dict(
            bzr = _get_bzr_repo,
            cvs = _get_cvs_repo,
            darcs = _get_darcs_repo,
            git = _get_git_repo,
            hg = _get_hg_repo,
            mtn = _get_mtn_repo,
            rcs = _get_rcs_repo,
            svk = _get_svk_repo,
            svn = _get_svn_repo)

    def setSearchOrder(self, ordering):
        self._search_order = ordering

    # determines which VCS to use for files in the named folder
    def findByFolder(self, path, prefs):
        path = os.path.abspath(path)
        for vcs in prefs.getString('vcs_search_order').split():
            if vcs in self.repolookup:
                repo = self.repolookup[vcs](path, prefs)
                if repo:
                    return repo

    # determines which VCS to use for the named file
    def findByFilename(self, name, prefs):
        if name is not None:
            return self.findByFolder(os.path.dirname(name), prefs)
