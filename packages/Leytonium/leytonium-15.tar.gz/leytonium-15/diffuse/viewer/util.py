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

from ..girepo import Gdk, Gtk, Pango
from ..util import Format, strip_eol
import os

# avoid some dictionary lookups when string.whitespace is used in loops
# this is sorted based upon frequency to speed up code for stripping whitespace
whitespace = ' \t\n\r\x0b\x0c'

# True if the string ends with '\r\n'
def has_dos_line_ending(s):
    return s.endswith('\r\n')

# True if the string ends with '\r'
def has_mac_line_ending(s):
    return s.endswith('\r')

# True if the string ends with '\n' but not '\r\n'
def has_unix_line_ending(s):
    return s.endswith('\n') and not s.endswith('\r\n')

# returns the format mask for a list of strings
def getFormat(ss):
    flags = 0
    for s in ss:
        if s is not None:
            if has_dos_line_ending(s):
                flags |= Format.DOS
            elif has_mac_line_ending(s):
                flags |= Format.MAC
            elif has_unix_line_ending(s):
                flags |= Format.UNIX
    return flags

# convenience method to change the line ending of a string
def convert_to_format(s, format):
    if s is not None and format != 0:
        old_format = getFormat([ s ])
        if old_format != 0 and (old_format & format) == 0:
            s = strip_eol(s)
            # prefer the host line ending style
            if (format & Format.DOS) and os.linesep == '\r\n':
                s += os.linesep
            elif (format & Format.MAC) and os.linesep == '\r':
                s += os.linesep
            elif (format & Format.UNIX) and os.linesep == '\n':
                s += os.linesep
            elif format & Format.UNIX:
                s += '\n'
            elif format & Format.DOS:
                s += '\r\n'
            elif format & Format.MAC:
                s += '\r'
    return s

# utility method to step advance an adjustment
def step_adjustment(adj, delta):
    v = adj.get_value() + delta
    # clamp to the allowed range
    v = max(v, int(adj.get_lower()))
    v = min(v, int(adj.get_upper() - adj.get_page_size()))
    adj.set_value(v)

# This is a replacement for Gtk.ScrolledWindow as it forced expose events to be
# handled immediately after changing the viewport position.  This could cause
# the application to become unresponsive for a while as it processed a large
# queue of keypress and expose event pairs.
class ScrolledWindow(Gtk.Grid):

    scroll_directions = {
            Gdk.ScrollDirection.UP,
            Gdk.ScrollDirection.DOWN,
            Gdk.ScrollDirection.LEFT,
            Gdk.ScrollDirection.RIGHT}

    def __init__(self, hadj, vadj):
        super().__init__()
        self.position = (0, 0)
        self.scroll_count = 0
        self.partial_redraw = False
        self.hadj, self.vadj = hadj, vadj
        vport = Gtk.Viewport.new()
        darea = Gtk.DrawingArea.new()
        darea.add_events(Gdk.EventMask.SCROLL_MASK)
        self.darea = darea
        # replace darea's queue_draw_area with our own so we can tell when
        # to disable/enable our scrolling optimisation
        self.darea_queue_draw_area = darea.queue_draw_area
        darea.queue_draw_area = self.redraw_region
        vport.add(darea)
        darea.show()
        self.attach(vport, 0, 0, 1, 1)
        vport.set_vexpand(True)
        vport.set_hexpand(True)
        vport.show()
        self.vbar = bar = Gtk.Scrollbar.new(Gtk.Orientation.VERTICAL, vadj)
        self.attach(bar, 1, 0, 1, 1)
        bar.show()
        self.hbar = bar = Gtk.Scrollbar.new(Gtk.Orientation.HORIZONTAL, hadj)
        self.attach(bar, 0, 1, 1, 1)
        bar.show()
        # listen to our signals
        hadj.connect('value-changed', self.value_changed_cb)
        vadj.connect('value-changed', self.value_changed_cb)
        darea.connect('configure-event', self.configure_cb)
        darea.connect('scroll-event', self.scroll_cb)
        darea.connect('draw', self.draw_cb)

    # updates the adjustments to match the new widget size
    def configure_cb(self, widget, event):
        w, h = event.width, event.height
        for adj, d in (self.hadj, w), (self.vadj, h):
            v = adj.get_value()
            if v + d > adj.get_upper():
                adj.set_value(max(0, adj.get_upper() - d))
            adj.set_page_size(d)
            adj.set_page_increment(d)

    # update the vertical adjustment when the mouse's scroll wheel is used
    def scroll_cb(self, widget, event):
        d = event.direction
        if d in self.scroll_directions:
            delta = 100
            if d in (Gdk.ScrollDirection.UP, Gdk.ScrollDirection.LEFT):
                delta = -delta
            vertical = (d in (Gdk.ScrollDirection.UP, Gdk.ScrollDirection.DOWN))
            if event.state & Gdk.ModifierType.SHIFT_MASK:
                vertical = not vertical
            if vertical:
                adj = self.vadj
            else:
                adj = self.hadj
            step_adjustment(adj, delta)

    def value_changed_cb(self, widget):
        old_x, old_y = self.position
        pos_x = int(self.hadj.get_value())
        pos_y = int(self.vadj.get_value())
        self.position = (pos_x, pos_y)
        if self.darea.get_window() is not None:
            # window.scroll() although visually nice, is slow, revert to
            # queue_draw() if scroll a lot without seeing an expose event
            if self.scroll_count < 2 and not self.partial_redraw:
                self.scroll_count += 1
                self.darea.get_window().scroll(old_x - pos_x, old_y - pos_y)
            else:
                self.partial_redraw = False
                self.darea.queue_draw()

    def draw_cb(self, widget, cr):
        self.scroll_count = 0

    # replacement for darea.queue_draw_area that notifies us when a partial
    # redraw happened
    def redraw_region(self, x, y, w, h):
        self.partial_redraw = True
        self.darea_queue_draw_area(x, y, w, h)

# Enforcing manual alignment is accomplished by dividing the lines of text into
# sections that are matched independently.  'blocks' is an array of integers
# describing how many lines (including null lines for spacing) that are in each
# section starting from the begining of the files.  When no manual alignment
# has been specified, all lines are in the same section so 'blocks' should
# contain a single entry equal to the number of lines.  Zeros are not allowed
# in this array so 'blocks' will be an empty array when there are no lines.  A
# 'cut' at location 'i' means a line 'i-1' and line 'i' belong to different
# sections

def createBlock(n):
    return [n] if n > 0 else []

# returns the two sets of blocks after cutting at 'i'
def cutBlocks(i, blocks):
    pre, post, nlines = [], [], 0
    for b in blocks:
        if nlines >= i:
            post.append(b)
        elif nlines + b <= i:
            pre.append(b)
        else:
            n = i - nlines
            pre.append(n)
            post.append(b - n)
        nlines += b
    return pre, post

# returns a set of blocks containing all of the cuts in the inputs
def mergeBlocks(leftblocks, rightblocks):
    leftblocks, rightblocks, b = leftblocks[:], rightblocks[:], []
    while len(leftblocks) > 0:
        nleft, nright = leftblocks[0], rightblocks[0]
        n = min(nleft, nright)
        if n < nleft:
            leftblocks[0] -= n
        else:
            del leftblocks[0]
        if n < nright:
            rightblocks[0] -= n
        else:
            del rightblocks[0]
        b.append(n)
    return b

# utility method to simplify working with structures used to describe character
# differences of a line
#
# ranges of character differences are indicated by (start, end, flags) tuples
# where 'flags' is a mask used to indicate if the characters are different from
# the line to the left, right, or both
#
# this method will return the union of two sorted lists of ranges
def mergeRanges(r1, r2):
    r1, r2, result, start = r1[:], r2[:], [], 0
    rs = [ r1, r2 ]
    while len(r1) > 0 and len(r2) > 0:
        flags, start = 0, min(r1[0][0], r2[0][0])
        if start == r1[0][0]:
            r1end = r1[0][1]
            flags |= r1[0][2]
        else:
            r1end = r1[0][0]
        if start == r2[0][0]:
            r2end = r2[0][1]
            flags |= r2[0][2]
        else:
            r2end = r2[0][0]
        end = min(r1end, r2end)
        result.append((start, end, flags))
        for r in rs:
            if start == r[0][0]:
                if end == r[0][1]:
                    del r[0]
                else:
                    r[0] = (end, r[0][1], r[0][2])
    result.extend(r1)
    result.extend(r2)
    return result

# eliminates lines that are spacing lines in all panes
def removeNullLines(blocks, lines_set):
    bi, bn, i = 0, 0, 0
    while bi < len(blocks):
        while i < bn + blocks[bi]:
            for lines in lines_set:
                if lines[i] is not None:
                    i += 1
                    break
            else:
                for lines in lines_set:
                    del lines[i]
                blocks[bi] -= 1
        if blocks[bi] == 0:
            del blocks[bi]
        else:
            bn += blocks[bi]
            bi += 1

# returns true if the string only contains whitespace characters
def isBlank(s):
    for c in whitespace:
        s = s.replace(c, '') # FIXME: Very inefficient!
    return len(s) == 0

# use Pango.SCALE instead of Pango.PIXELS to avoid overflow exception
def pixels(size):
    return int(size / Pango.SCALE + .5)

# mapping to column width of a character (tab will never be in this map)
char_width_cache = {}

ALPHANUMERIC_CLASS = 0
WHITESPACE_CLASS = 1
OTHER_CLASS = 2

# maps similar types of characters to a group
def getCharacterClass(c):
    if c.isalnum() or c == '_':
        return ALPHANUMERIC_CLASS
    elif c.isspace():
        return WHITESPACE_CLASS
    return OTHER_CLASS
