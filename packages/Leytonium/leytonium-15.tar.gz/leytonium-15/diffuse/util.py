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

from diapyr.util import singleton
from gettext import gettext as _
import locale, os, subprocess, sys

APP_NAME = 'Diffuse'
# use the program's location as a starting place to search for supporting files
# such as icon and help documentation
bin_dir = os.path.dirname(sys.executable if hasattr(sys, 'frozen') else os.path.realpath(sys.argv[0]))
# platform test
isWindows = os.name == 'nt'
VERSION = '0.6.0'
WEBSITE = 'https://github.com/MightyCreak/diffuse'

def getcopyright():
    copyright = _('Copyright')
    return f"""{copyright} \N{COPYRIGHT SIGN} 2006-2019 Derrick Moser
{copyright} \N{COPYRIGHT SIGN} 2015-2020 Romain Failliot"""

@singleton
def lang():
    # translation location: '../share/locale/<LANG>/LC_MESSAGES/diffuse.mo'
    # where '<LANG>' is the language key
    if isWindows:
        for v in 'LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG':
            if v in os.environ:
                lang = os.environ[v]
                # remove any additional languages, encodings, or modifications
                for v in ':.@':
                    lang = lang.split(v)[0]
                return lang
    return locale.getdefaultlocale()[0]

# masks used to indicate the presence of particular line endings
class Format:

    DOS, MAC, UNIX = (1 << i for i in range(3))

# the file diff viewer is always in one of these modes defining the cursor,
# and hotkey behaviour
class Mode:

    LINE, CHAR, ALIGN = range(3)

# convenience function to display debug messages
def logDebug(s):
    pass #sys.stderr.write(f'{APP_NAME}: {s}\n')

# escape special glob characters
def globEscape(s):
    m = {c: f"[{c}]" for c in '[]?*'} # XXX: Does this work for close square bracket?
    return ''.join(m.get(c, c) for c in s)

def readconfiglines(fd):
    return fd.read().replace('\r', '').split('\n')

# map an encoding name to its standard form
def norm_encoding(e):
    if e is not None:
        return e.replace('-', '_').lower()

def nullToEmpty(s):
    return '' if s is None else s

# split string into lines based upon DOS, Mac, and Unix line endings
def splitlines(s):
    # split on new line characters
    temp, i, n = [], 0, len(s)
    while i < n:
        j = s.find('\n', i)
        if j < 0:
            temp.append(s[i:])
            break
        j += 1
        temp.append(s[i:j])
        i = j
    # split on carriage return characters
    ss = []
    for s in temp:
        i, n = 0, len(s)
        while i < n:
            j = s.find('\r', i)
            if j < 0:
                ss.append(s[i:])
                break
            j += 1
            if j < n and s[j] == '\n':
                j += 1
            ss.append(s[i:j])
            i = j
    return ss

# also recognise old Mac OS line endings
def readlines(fd):
    return strip_eols(splitlines(fd.read()))

# returns the number of characters in the string excluding any line ending
# characters
def len_minus_line_ending(s):
    if s is None:
        return 0
    n = len(s)
    if s.endswith('\r\n'):
        n -= 2
    elif s.endswith('\r') or s.endswith('\n'):
        n -= 1
    return n

# returns the string without the line ending characters
def strip_eol(s):
    if s is not None:
        return s[:len_minus_line_ending(s)]

# returns the list of strings without line ending characters
def strip_eols(ss):
    return [ strip_eol(s) for s in ss ]

# returns the Windows drive or share from a from an absolute path
def drive_from_path(s):
    c = s.split(os.sep)
    if len(c) > 3 and c[0] == '' and c[1] == '':
        return os.path.join(c[:4])
    return c[0]

# constructs a relative path from 'a' to 'b', both should be absolute paths
def relpath(a, b):
    if isWindows:
        if drive_from_path(a) != drive_from_path(b):
            return b
    c1 = [ c for c in a.split(os.sep) if c != '' ]
    c2 = [ c for c in b.split(os.sep) if c != '' ]
    i, n = 0, len(c1)
    while i < n and i < len(c2) and c1[i] == c2[i]:
        i += 1
    r = (n - i) * [ os.pardir ]
    r.extend(c2[i:])
    return os.sep.join(r)

# escape arguments for use with bash
def bashEscape(s):
    return "'" + s.replace("'", "'\\''") + "'"

# use popen to read the output of a command
def popenRead(dn, cmd, prefs, bash_pref, success_results=None):
    if success_results is None:
        success_results = [ 0 ]
    if isWindows and prefs.getBool(bash_pref):
        # launch the command from a bash shell is requested
        cmd = [ prefs.convertToNativePath('/bin/bash.exe'), '-l', '-c', 'cd {}; {}'.format(bashEscape(dn), ' '.join([ bashEscape(arg) for arg in cmd ])) ]
        dn = None
    # use subprocess.Popen to retrieve the file contents
    if isWindows:
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE
    else:
        info = None
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dn, startupinfo=info)
    proc.stdin.close()
    proc.stderr.close()
    fd = proc.stdout
    # read the command's output
    s = fd.read()
    fd.close()
    if proc.wait() not in success_results:
        raise IOError('Command failed.')
    return s

# use popen to read the output of a command
def popenReadLines(dn, cmd, prefs, bash_pref, success_results=None):
    return strip_eols(splitlines(popenRead(dn, cmd, prefs, bash_pref, success_results).decode('utf-8', errors='ignore')))
