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

# Undo for changes to the cached line ending style
class SetFormatUndo:

    def __init__(self, f, format, old_format):
        self.data = (f, format, old_format)

    def undo(self, viewer):
        f, _, old_format = self.data
        viewer.setFormat(f, old_format)

    def redo(self, viewer):
        f, format, _ = self.data
        viewer.setFormat(f, format)

# Undo for the creation of Line objects
class InstanceLineUndo:

    def __init__(self, f, i, reverse):
        self.data = (f, i, reverse)

    def undo(self, viewer):
        f, i, reverse = self.data
        viewer.instanceLine(f, i, not reverse)

    def redo(self, viewer):
        f, i, reverse = self.data
        viewer.instanceLine(f, i, reverse)

# Undo for changing the text for a Line object
class UpdateLineTextUndo:

    def __init__(self, f, i, old_is_modified, old_text, is_modified, text):
        self.data = (f, i, old_is_modified, old_text, is_modified, text)

    def undo(self, viewer):
        f, i, old_is_modified, old_text, _, _ = self.data
        viewer.updateLineText(f, i, old_is_modified, old_text)

    def redo(self, viewer):
        f, i, _, _, is_modified, text = self.data
        viewer.updateLineText(f, i, is_modified, text)

# Undo for inserting a spacing line in a single pane
class InsertNullUndo:

    def __init__(self, f, i, reverse):
        self.data = (f, i, reverse)

    def undo(self, viewer):
        f, i, reverse = self.data
        viewer.insertNull(f, i, not reverse)

    def redo(self, viewer):
        f, i, reverse = self.data
        viewer.insertNull(f, i, reverse)

# Undo for manipulating a section of the line matching data
class InvalidateLineMatchingUndo:

    def __init__(self, i, n, new_n):
        self.data = (i, n, new_n)

    def undo(self, viewer):
        i, n, new_n = self.data
        viewer.invalidateLineMatching(i, new_n, n)

    def redo(self, viewer):
        i, n, new_n = self.data
        viewer.invalidateLineMatching(i, n, new_n)

# Undo for alignment changes
class AlignmentChangeUndo:

    def __init__(self, finished):
        self.data = finished

    def undo(self, viewer):
        finished = self.data
        viewer.alignmentChange(not finished)

    def redo(self, viewer):
        finished = self.data
        viewer.alignmentChange(finished)

# Undo for changing how lines are cut into blocks for alignment
class UpdateBlocksUndo:

    def __init__(self, old_blocks, blocks):
        self.data = (old_blocks, blocks)

    def undo(self, viewer):
        old_blocks, _ = self.data
        viewer.updateBlocks(old_blocks)

    def redo(self, viewer):
        _, blocks = self.data
        viewer.updateBlocks(blocks)

# Undo for replacing the lines for a single pane with a new set
class ReplaceLinesUndo:

    def __init__(self, f, lines, new_lines, max_num, new_max_num):
        self.data = (f, lines, new_lines, max_num, new_max_num)

    def undo(self, viewer):
        f, lines, new_lines, max_num, new_max_num = self.data
        viewer.replaceLines(f, new_lines, lines, new_max_num, max_num)

    def redo(self, viewer):
        f, lines, new_lines, max_num, new_max_num = self.data
        viewer.replaceLines(f, lines, new_lines, max_num, new_max_num)

# Undo for changing the selection mode and range
class EditModeUndo:

    def __init__(self, mode, current_pane, current_line, current_char, selection_line, selection_char, cursor_column):
        self.data = (mode, current_pane, current_line, current_char, selection_line, selection_char, cursor_column)

    def undo(self, viewer):
        mode, current_pane, current_line, current_char, selection_line, selection_char, cursor_column = self.data
        viewer.setEditMode(mode, current_pane, current_line, current_char, selection_line, selection_char, cursor_column)

    def redo(self, viewer):
        self.undo(viewer)

# Undo for changes to the pane ordering
class SwapPanesUndo:

    def __init__(self, f_dst, f_src):
        self.data = (f_dst, f_src)

    def undo(self, viewer):
        f_dst, f_src = self.data
        viewer.swapPanes(f_src, f_dst)

    def redo(self, viewer):
        f_dst, f_src = self.data
        viewer.swapPanes(f_dst, f_src)
