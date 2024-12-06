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

# class describing a text pane
class Pane:

    def __init__(self):
        # list of lines displayed in this pane (including spacing lines)
        self.lines = []
        # high water mark for line length in Pango units (used to determine
        # the required horizontal scroll range)
        self.line_lengths = 0
        # highest line number
        self.max_line_number = 0
        # cache of syntax highlighting information for each line
        # self.syntax_cache[i] corresponds to self.lines[i]
        # the list is truncated when a change to a line invalidates a
        # portion of the cache
        self.syntax_cache = []
        # cache of character differences for each line
        # self.diff_cache[i] corresponds to self.lines[i]
        # portion of the cache are cleared by setting entries to None
        self.diff_cache = []
        # mask indicating the type of line endings present
        self.format = 0
        # number of lines with edits
        self.num_edits = 0

# class describing a single line of a pane
class Line:

    def __init__(self, line_number = None, text = None):
        # line number
        self.line_number = line_number
        # original text for the line
        self.text = text
        # flag indicating modifications are present
        self.is_modified = False
        # actual modified text
        self.modified_text = None
        # cache used to speed up comparison of strings
        # this should be cleared whenever the comparison preferences change
        self.compare_string = None

    # returns the current text for this line
    def getText(self):
        return self.modified_text if self.is_modified else self.text
