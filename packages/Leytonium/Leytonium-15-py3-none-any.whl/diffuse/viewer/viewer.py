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

from .model import Line, Pane
from .patience import patience_diff
from .undo import AlignmentChangeUndo, EditModeUndo, InsertNullUndo, InstanceLineUndo, InvalidateLineMatchingUndo, ReplaceLinesUndo, SetFormatUndo, SwapPanesUndo, UpdateBlocksUndo, UpdateLineTextUndo
from .util import char_width_cache, convert_to_format, createBlock, cutBlocks, getCharacterClass, getFormat, isBlank, mergeBlocks, mergeRanges, pixels, removeNullLines, ScrolledWindow, step_adjustment, whitespace, WHITESPACE_CLASS
from ..girepo import Gdk, Gtk, Pango, PangoCairo
from ..ui import createMenu
from ..util import Format, len_minus_line_ending, Mode, nullToEmpty, splitlines, strip_eol
from gettext import gettext as _
import difflib, os, unicodedata

# widget used to compare and merge text files
class FileDiffViewer(Gtk.Grid):

    def __init__(self, resources, n, prefs):
        # verify we have a valid number of panes
        if n < 2:
            raise ValueError('Invalid number of panes')
        super().__init__()
        self.set_can_focus(True)
        self.prefs = prefs
        self.string_width_cache = {}
        self.options = {}

        # diff blocks
        self.blocks = []

        # undos
        self.undos = []
        self.redos = []
        self.undoblock = None

        # cached data
        self.syntax = None
        self.diffmap_cache = None

        # editing mode
        self.mode = Mode.LINE
        self.current_pane = 1
        self.current_line = 0
        self.current_char = 0
        self.selection_line = 0
        self.selection_char = 0
        self.align_pane = 0
        self.align_line = 0
        self.cursor_column = -1

        # keybindings
        self._line_mode_actions = {
            'enter_align_mode': self._line_mode_enter_align_mode,
            'enter_character_mode': self.setCharMode,
            'first_line': self._first_line,
            'extend_first_line': self._extend_first_line,
            'last_line': self._last_line,
            'extend_last_line': self._extend_last_line,
            'up': self._line_mode_up,
            'extend_up': self._line_mode_extend_up,
            'down': self._line_mode_down,
            'extend_down': self._line_mode_extend_down,
            'left': self._line_mode_left,
            'extend_left': self._line_mode_extend_left,
            'right': self._line_mode_right,
            'extend_right': self._line_mode_extend_right,
            'page_up': self._line_mode_page_up,
            'extend_page_up': self._line_mode_extend_page_up,
            'page_down': self._line_mode_page_down,
            'extend_page_down': self._line_mode_extend_page_down,
            'delete_text': self._delete_text,
            'clear_edits': self.clear_edits,
            'isolate': self.isolate,
            'first_difference': self.first_difference,
            'previous_difference': self.previous_difference,
            'next_difference': self.next_difference,
            'last_difference': self.last_difference,
            'copy_selection_right': self.copy_selection_right,
            'copy_selection_left': self.copy_selection_left,
            'copy_left_into_selection': self.copy_left_into_selection,
            'copy_right_into_selection': self.copy_right_into_selection,
            'merge_from_left_then_right': self.merge_from_left_then_right,
            'merge_from_right_then_left': self.merge_from_right_then_left }
        self._align_mode_actions = {
            'enter_line_mode': self._align_mode_enter_line_mode,
            'enter_character_mode': self.setCharMode,
            'first_line': self._first_line,
            'last_line': self._last_line,
            'up': self._line_mode_up,
            'down': self._line_mode_down,
            'left': self._line_mode_left,
            'right': self._line_mode_right,
            'page_up': self._line_mode_page_up,
            'page_down': self._line_mode_page_down,
            'align': self._align_text }
        self._character_mode_actions = {
            'enter_line_mode': self.setLineMode }
        self._button_actions = {
            'undo': self.undo,
            'redo': self.redo,
            'cut': self.cut,
            'copy': self.copy,
            'paste': self.paste,
            'select_all': self.select_all,
            'clear_edits': self.clear_edits,
            'dismiss_all_edits': self.dismiss_all_edits,
            'realign_all': self.realign_all,
            'isolate': self.isolate,
            'first_difference': self.first_difference,
            'previous_difference': self.previous_difference,
            'next_difference': self.next_difference,
            'last_difference': self.last_difference,
            'shift_pane_right': self.shift_pane_right,
            'shift_pane_left': self.shift_pane_left,
            'convert_to_upper_case': self.convert_to_upper_case,
            'convert_to_lower_case': self.convert_to_lower_case,
            'sort_lines_in_ascending_order': self.sort_lines_in_ascending_order,
            'sort_lines_in_descending_order': self.sort_lines_in_descending_order,
            'remove_trailing_white_space': self.remove_trailing_white_space,
            'convert_tabs_to_spaces': self.convert_tabs_to_spaces,
            'convert_leading_spaces_to_tabs': self.convert_leading_spaces_to_tabs,
            'increase_indenting': self.increase_indenting,
            'decrease_indenting': self.decrease_indenting,
            'convert_to_dos': self.convert_to_dos,
            'convert_to_mac': self.convert_to_mac,
            'convert_to_unix': self.convert_to_unix,
            'copy_selection_right': self.copy_selection_right,
            'copy_selection_left': self.copy_selection_left,
            'copy_left_into_selection': self.copy_left_into_selection,
            'copy_right_into_selection': self.copy_right_into_selection,
            'merge_from_left_then_right': self.merge_from_left_then_right,
            'merge_from_right_then_left': self.merge_from_right_then_left }

        # create panes
        self.dareas = []
        self.panes = []
        self.hadj = Gtk.Adjustment.new(0, 0, 0, 0, 0, 0)
        self.vadj = Gtk.Adjustment.new(0, 0, 0, 0, 0, 0)
        for i in range(n):
            pane = Pane()
            self.panes.append(pane)
            # pane contents
            sw = ScrolledWindow(self.hadj, self.vadj)
            sw.set_vexpand(True)
            sw.set_hexpand(True)
            darea = sw.darea
            darea.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                             Gdk.EventMask.BUTTON1_MOTION_MASK)
            darea.connect('button-press-event', self.darea_button_press_cb, i)
            darea.connect('motion-notify-event', self.darea_motion_notify_cb, i)
            darea.connect('draw', self.darea_draw_cb, i)
            self.dareas.append(darea)
            self.attach(sw, i, 1, 1, 1)
            sw.show()

        self.hadj.connect('value-changed', self.hadj_changed_cb)
        self.vadj.connect('value-changed', self.vadj_changed_cb)

        # add diff map
        self.diffmap = diffmap = Gtk.DrawingArea.new()
        diffmap.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                       Gdk.EventMask.BUTTON1_MOTION_MASK |
                       Gdk.EventMask.SCROLL_MASK)
        diffmap.connect('button-press-event', self.diffmap_button_press_cb)
        diffmap.connect('motion-notify-event', self.diffmap_button_press_cb)
        diffmap.connect('scroll-event', self.diffmap_scroll_cb)
        diffmap.connect('draw', self.diffmap_draw_cb)
        self.attach(diffmap, n, 1, 1, 1)
        diffmap.show()
        diffmap.set_size_request(16 * n, 0)
        self.add_events(Gdk.EventMask.KEY_PRESS_MASK |
                        Gdk.EventMask.FOCUS_CHANGE_MASK)
        self.connect('focus-in-event', self.focus_in_cb)
        self.connect('focus-out-event', self.focus_out_cb)
        self.connect('key-press-event', self.key_press_cb)

        # input method
        self.im_context = im = Gtk.IMMulticontext.new()
        im.connect('commit', self.im_commit_cb)
        im.connect('preedit-changed', self.im_preedit_changed_cb)
        im.connect('retrieve-surrounding', self.im_retrieve_surrounding_cb)
        self.im_preedit = None
        # Cache our keyboard focus state so we know when to change the
        # input method's focus.  We ensure the input method is given focus
        # if and only if (self.has_focus and self.mode == Mode.CHAR).
        self.has_focus = False

        # font
        self.setFont(Pango.FontDescription.from_string(prefs.getString('display_font')))
        self.cursor_pos = (0, 0)

        # scroll to first difference when realised
        darea.connect_after('realize', self._realise_cb)
        self.resources = resources

    # callback used when the viewer is first displayed
    # this must be connected with 'connect_after()' so the final widget sizes
    # are known and the scroll bar can be moved to the first difference
    def _realise_cb(self, widget):
        self.im_context.set_client_window(self.get_window())
        try:
            self.go_to_line(self.options['line'])
        except KeyError:
            self.first_difference()

    # callback for most menu items and buttons
    def button_cb(self, widget, data):
        self.openUndoBlock()
        self._button_actions[data]()
        self.closeUndoBlock()

    # set startup options
    def setOptions(self, options):
        self.options = options

    # updates the display font and resizes viewports as necessary
    def setFont(self, font):
        self.font = font
        metrics = self.get_pango_context().get_metrics(self.font)
        self.font_height = max(pixels(metrics.get_ascent() + metrics.get_descent()), 1)
        self.digit_width = metrics.get_approximate_digit_width()
        self.updateSize(True)
        self.diffmap.queue_draw()

    # returns the 'column width' for a string -- used to help position
    # characters when tabs and other special characters are present
    # This is an inline loop over self.characterWidth() for performance reasons.
    def stringWidth(self, s):
        if not self.prefs.getBool('display_show_whitespace'):
            s = strip_eol(s)
        col = 0
        for c in s:
            try:
                w = char_width_cache[c]
            except KeyError:
                v = ord(c)
                if v < 32:
                    if c == '\t':
                        tab_width = self.prefs.getInt('display_tab_width')
                        w = tab_width - col % tab_width
                    elif c == '\n':
                        w = 1
                        char_width_cache[c] = w
                    else:
                        w = 2
                        char_width_cache[c] = w
                else:
                    if unicodedata.east_asian_width(c) in 'WF':
                        w = 2
                    else:
                        w = 1
                    char_width_cache[c] = w
            col += w
        return col

    # returns the 'column width' for a single character created at column 'i'
    def characterWidth(self, i, c):
        try:
            return char_width_cache[c]
        except KeyError:
            v = ord(c)
            if v < 32:
                if c == '\t':
                    tab_width = self.prefs.getInt('display_tab_width')
                    return tab_width - i % tab_width
                elif c == '\n':
                    w = 1
                else:
                    w = 2
            elif unicodedata.east_asian_width(c) in 'WF':
                w = 2
            else:
                w = 1
            char_width_cache[c] = w
            return w

    # translates a string into an array of the printable representation for
    # each character
    def expand(self, s):
        visible = self.prefs.getBool('display_show_whitespace')
        if not visible:
            s = strip_eol(s)
        tab_width = self.prefs.getInt('display_tab_width')
        col = 0
        result = []
        for c in s:
            v = ord(c)
            if v <= 32:
                if c == ' ':
                    if visible:
                        # show spaces using a centre-dot
                        result.append('\u00b7')
                    else:
                        result.append(c)
                elif c == '\t':
                    width = tab_width - col % tab_width
                    if visible:
                        # show tabs using a right double angle quote
                        result.append('\u00bb' + (width - 1) * ' ')
                    else:
                        result.append(width * ' ')
                elif c == '\n' and visible:
                    # show newlines using a pilcrow
                    result.append('\u00b6')
                else:
                    # prefix with a ^
                    result.append('^' + chr(v + 64))
            else:
                result.append(c)
            col += self.characterWidth(col, c)
        return result

    # changes the viewer's mode to Mode.LINE
    def setLineMode(self):
        if self.mode != Mode.LINE:
            if self.mode == Mode.CHAR:
                self._im_focus_out()
                self.im_context.reset()
                self._im_set_preedit(None)
                self.current_char = 0
                self.selection_char = 0
                self.dareas[self.current_pane].queue_draw()
            elif self.mode == Mode.ALIGN:
                self.dareas[self.align_pane].queue_draw()
                self.dareas[self.current_pane].queue_draw()
                self.align_pane = 0
                self.align_line = 0
            self.mode = Mode.LINE
            self.emit('cursor_changed')
            self.emit('mode_changed')

    # changes the viewer's mode to Mode.CHAR
    def setCharMode(self):
        if self.mode != Mode.CHAR:
            if self.mode == Mode.LINE:
                self.cursor_column = -1
                self.setCurrentChar(self.current_line, 0)
            elif self.mode == Mode.ALIGN:
                self.dareas[self.align_pane].queue_draw()
                self.cursor_column = -1
                self.align_pane = 0
                self.align_line = 0
                self.setCurrentChar(self.current_line, 0)
            self._im_focus_in()
            self.im_context.reset()
            self.mode = Mode.CHAR
            self.emit('cursor_changed')
            self.emit('mode_changed')

    # sets the syntax hightlighting rules
    def setSyntax(self, s):
        if self.syntax is not s:
            self.syntax = s
            # invalidate the syntax caches
            for pane in self.panes:
                pane.syntax_cache = []
            self.emit('syntax_changed', s)
            # force all panes to redraw
            for darea in self.dareas:
                darea.queue_draw()

    # gets the syntax
    def getSyntax(self):
        return self.syntax

    # returns True if any pane contains edits
    def hasEdits(self):
        for pane in self.panes:
            if pane.num_edits > 0:
                return True
        return False

    # Changes to the diff viewer's state is recorded so they can be later
    # undone.  The recorded changes are organised into blocks that correspond
    # to high level action initiated by the user.  For example, pasting some
    # text may modify some lines and cause insertion of spacing lines to keep
    # proper alignment with the rest of the panes.  An undo operation initiated
    # by the user should undo all of these changes in a single step.
    # openUndoBlock() should be called when the action from a user, like a
    # mouse button press, menu item, etc. may cause change to the diff viewer's
    # state
    def openUndoBlock(self):
        self.undoblock = []

    # all changes to the diff viewer's state should create an Undo object and
    # add it to the current undo block using this method
    # this method does not need to be called when the state change is a result
    # of an undo/redo operation (self.undoblock is None in these cases)
    def addUndo(self, u):
        self.undoblock.append(u)

    # all openUndoBlock() calls should also have a matching closeUndoBlock()
    # this method collects all Undos created since the openUndoBlock() call
    # and pushes them onto the undo stack as a single unit
    def closeUndoBlock(self):
        if len(self.undoblock) > 0:
            self.redos = []
            self.undos.append(self.undoblock)
        self.undoblock = None

    # 'undo' action
    def undo(self):
        self.undoblock, old_block = None, self.undoblock
        if self.mode == Mode.CHAR:
            # avoid implicit preedit commit when an undo changes the mode
            self.im_context.reset()
        if self.mode == Mode.LINE or self.mode == Mode.CHAR:
            if len(self.undos) > 0:
                # move the block to the redo stack
                block = self.undos.pop()
                self.redos.append(block)
                # undo all changes in the block in reverse order
                for u in block[::-1]:
                    u.undo(self)
        self.undoblock = old_block

    # 'redo' action
    def redo(self):
        self.undoblock, old_block = None, self.undoblock
        if self.mode == Mode.LINE or self.mode == Mode.CHAR:
            if self.mode == Mode.CHAR:
                # avoid implicit preedit commit when an redo changes the mode
                self.im_context.reset()
            if len(self.redos) > 0:
                # move the block to the undo stack
                block = self.redos.pop()
                self.undos.append(block)
                # re-apply all changes in the block
                for u in block:
                    u.redo(self)
        self.undoblock = old_block

    # returns the width of the viewport's line number column in Pango units
    def getLineNumberWidth(self):
        # find the maximum number of digits for a line number from all panes
        n = 0
        if self.prefs.getBool('display_show_line_numbers'):
            for pane in self.panes:
                n = max(n, len(str(pane.max_line_number)))
            # pad the total width by the width of a digit on either side
            n = (n + 2) * self.digit_width
        return n

    # returns the width of a string in Pango units
    def getTextWidth(self, text):
        if len(text) == 0:
            return 0
        layout = self.create_pango_layout(text)
        layout.set_font_description(self.font)
        return layout.get_size()[0]

    # updates the size of the viewport
    # set 'compute_width' to False if the high water mark for line length can
    # be used to determine the required width for the viewport, use True for
    # this value otherwise
    def updateSize(self, compute_width, f=None):
        digit_width, stringWidth = self.digit_width, self.stringWidth
        string_width_cache = self.string_width_cache
        if compute_width:
            if f is None:
                panes = self.panes
            else:
                panes = [ self.panes[f] ]
            for f, pane in enumerate(panes):
                del pane.syntax_cache[:]
                del pane.diff_cache[:]
                # re-compute the high water mark
                pane.line_lengths = 0
                for line in pane.lines:
                    if line is not None:
                        line.compare_string = None
                        text = [ line.text ]
                        if line.is_modified:
                            text.append(line.modified_text)
                        for s in text:
                            if s is not None:
                                w = string_width_cache.get(s, None)
                                if w is None:
                                    string_width_cache[s] = w = stringWidth(s)
                                pane.line_lengths = max(pane.line_lengths, digit_width * w)
        # compute the maximum extents
        num_lines, line_lengths = 0, 0
        for pane in self.panes:
            num_lines = max(num_lines, len(pane.lines))
            line_lengths = max(line_lengths, pane.line_lengths)
        # account for any preedit text
        if self.im_preedit is not None:
            w = self._preedit_layout().get_size()[0]
            s = self.getLineText(self.current_pane, self.current_line)
            if s is not None:
                w += digit_width * stringWidth(s)
            line_lengths = max(line_lengths, w)
        # the cursor can move one line past the last line of text, add it so we
        # can scroll to see this line
        num_lines += 1
        width = self.getLineNumberWidth() + digit_width + line_lengths
        width = pixels(width)
        height = self.font_height * num_lines
        # update the adjustments
        self.hadj.set_upper(width)
        self.hadj.step_increment = self.font_height
        self.vadj.set_upper(height)
        self.vadj.step_increment = self.font_height

    # returns a line from the specified pane and offset
    def getLine(self, f, i):
        lines = self.panes[f].lines
        if i < len(lines):
            return lines[i]

    # returns the text for the specified line
    def getLineText(self, f, i):
        line = self.getLine(f, i)
        if line is not None:
            return line.getText()

    # sets the cached line ending style
    def setFormat(self, f, format):
        pane = self.panes[f]
        if self.undoblock is not None:
            # create an Undo object for the action
            self.addUndo(SetFormatUndo(f, format, pane.format))
        pane.format = format
        self.emit('format_changed', f, format)

    # creates an instance of a Line object for the specified pane and offset
    # deletes an instance when 'reverse' is set to True
    def instanceLine(self, f, i, reverse=False):
        if self.undoblock is not None:
            # create an Undo object for the action
            self.addUndo(InstanceLineUndo(f, i, reverse))
        pane = self.panes[f]
        if reverse:
            pane.lines[i] = None
        else:
            line = Line()
            pane.lines[i] = line

    def getMapFlags(self, f, i):
        flags = 0
        compare_text = self.getCompareString(f, i)
        if f > 0 and self.getCompareString(f - 1, i) != compare_text:
            flags |= 1
        if f + 1 < len(self.panes) and self.getCompareString(f + 1, i) != compare_text:
            flags |= 2
        line = self.getLine(f, i)
        if line is not None and line.is_modified:
            flags |= 4
        return flags

    # update line 'i' in pane 'f' to contain 'text'
    def updateLineText(self, f, i, is_modified, text):
        pane = self.panes[f]
        line = pane.lines[i]
        flags = self.getMapFlags(f, i)
        if self.undoblock is not None:
            # create an Undo object for the action
            self.addUndo(UpdateLineTextUndo(f, i, line.is_modified, line.modified_text, is_modified, text))
        old_num_edits = pane.num_edits
        if is_modified and not line.is_modified:
            pane.num_edits += 1
        elif not is_modified and line.is_modified:
            pane.num_edits -= 1
        if pane.num_edits != old_num_edits:
            self.emit('num_edits_changed', f)
        line.is_modified = is_modified
        line.modified_text = text
        line.compare_string = None

        # update/invalidate all relevent caches and queue widgets for redraw
        if text is not None:
            pane.line_lengths = max(pane.line_lengths, self.digit_width * self.stringWidth(text))
        self.updateSize(False)

        fs = []
        if f > 0:
            fs.append(f - 1)
        if f + 1 < len(self.panes):
            fs.append(f + 1)
        for fn in fs:
            otherpane = self.panes[fn]
            if i < len(otherpane.diff_cache):
                otherpane.diff_cache[i] = None
            self._queue_draw_lines(fn, i)
        if i < len(pane.syntax_cache):
            del pane.syntax_cache[i:]
        if i < len(pane.diff_cache):
            pane.diff_cache[i] = None
        self.dareas[f].queue_draw()
        if self.getMapFlags(f, i) != flags:
            self.diffmap_cache = None
            self.diffmap.queue_draw()

    # insert a spacing line at line 'i' in pane 'f'
    # this caller must ensure the blocks and number of lines in each pane
    # are valid again
    def insertNull(self, f, i, reverse):
        if self.undoblock is not None:
            # create an Undo object for the action
            self.addUndo(InsertNullUndo(f, i, reverse))
        pane = self.panes[f]
        lines = pane.lines
        # update/invalidate all relevent caches
        if reverse:
            del lines[i]
            if i < len(pane.syntax_cache):
                del pane.syntax_cache[i]
        else:
            lines.insert(i, None)
            if i < len(pane.syntax_cache):
                state = pane.syntax_cache[i][0]
                pane.syntax_cache.insert(i, [state, state, None, None])

    # manipulate a section of the line matching data
    def invalidateLineMatching(self, i, n, new_n):
        if self.undoblock is not None:
            # create an Undo object for the action
            self.addUndo(InvalidateLineMatchingUndo(i, n, new_n))
        # update/invalidate all relevent caches and queue widgets for redraw
        i2 = i + n
        for f, pane in enumerate(self.panes):
            if i < len(pane.diff_cache):
                if i2 + 1 < len(pane.diff_cache):
                    pane.diff_cache[i:i2] = new_n * [ None ]
                else:
                    del pane.diff_cache[i:]
            self.dareas[f].queue_draw()
        self.diffmap_cache = None
        self.diffmap.queue_draw()

    # update viewer in response to alignment changes
    def alignmentChange(self, finished):
        if self.undoblock is not None:
            # create an Undo object for the action
            self.addUndo(AlignmentChangeUndo(finished))
        if finished:
            self.updateSize(False)

    # updates the alignment of 'n' lines starting from 'i'
    def updateAlignment(self, i, n, lines):
        self.alignmentChange(False)
        new_n = len(lines[0])
        i2 = i + n
        # insert spacing lines
        for f in range(len(self.panes)):
            for j in range(i2-1, i-1, -1):
                if self.getLine(f, j) is None:
                    self.insertNull(f, j, True)
            temp = lines[f]
            for j in range(new_n):
                if temp[j] is None:
                    self.insertNull(f, i + j, False)
        # update line matching for this block

        # FIXME: we should be able to do something more intelligent here...
        # the syntax cache will become invalidated.... we don't really need to
        # do that...
        self.invalidateLineMatching(i, n, new_n)
        self.alignmentChange(True)

    # change how lines are cut into blocks for alignment
    def updateBlocks(self, blocks):
        if self.undoblock is not None:
            # create an Undo object for the action
            self.addUndo(UpdateBlocksUndo(self.blocks, blocks))
        self.blocks = blocks

    # insert 'n' blank lines in all panes
    def insertLines(self, i, n):
        # insert lines
        self.updateAlignment(i, 0, [ n * [ None ] for pane in self.panes ])
        pre, post = cutBlocks(i, self.blocks)
        pre.append(n)
        pre.extend(post)
        self.updateBlocks(pre)

        # update selection
        if self.current_line >= i:
            self.current_line += n
        if self.selection_line >= i:
            self.selection_line += n
        # queue redraws
        self.updateSize(False)
        self.diffmap_cache = None
        self.diffmap.queue_draw()

    # remove a line
    def removeSpacerLines(self, i, n, skip=-1):
        npanes, removed = len(self.panes), []
        for j in range(i, i + n):
            for f in range(npanes):
                line = self.getLine(f, j)
                if line is not None:
                    if line.line_number is not None or (f != skip and line.getText() is not None):
                        break
            else:
                # remove line
                for f in range(npanes):
                    line = self.getLine(f, j)
                    if line is not None:
                        # create undo to record any edits to the line before
                        # removing it
                        self.updateLineText(f, j, False, None)
                        # remove the line so it doesn't persist as a spacer
                        self.instanceLine(f, j, True)
                removed.append(j)

        nremoved = len(removed)
        if nremoved > 0:
            # update blocks
            bi, bii, blocks = 0, 0, self.blocks[:]
            for j in removed:
                while bii + blocks[bi] < j:
                    bii += blocks[bi]
                    bi += 1
                if blocks[bi] == 1:
                    del blocks[bi]
                else:
                    blocks[bi] -= 1
                bii += 1
            self.updateBlocks(blocks)

            self.alignmentChange(False)
            removed.reverse()
            for j in removed:
                for f in range(npanes):
                    self.insertNull(f, j, True)
            # FIXME: we should be able to do something more intelligent here...
            # the syntax cache will become invalidated.... we don't really need
            # to do that...
            self.invalidateLineMatching(i, n, n - nremoved)
            self.alignmentChange(True)

            # queue redraws
            self.updateSize(False)
            self.diffmap_cache = None
            self.diffmap.queue_draw()
        return nremoved

    # replace the lines for a single pane with a new set
    def replaceLines(self, f, lines, new_lines, max_num, new_max_num):
        if self.undoblock is not None:
            # create an Undo object for the action
            self.addUndo(ReplaceLinesUndo(f, lines, new_lines, max_num, new_max_num))
        pane = self.panes[f]
        pane.lines = new_lines
        # update/invalidate all relevent caches and queue widgets for redraw
        old_num_edits = pane.num_edits
        pane.num_edits = 0
        for line in new_lines:
            if line is not None and line.is_modified:
                pane.num_edits += 1
        if pane.num_edits != old_num_edits:
            self.emit('num_edits_changed', f)
        del pane.syntax_cache[:]
        pane.max_line_number = new_max_num
        self.dareas[f].queue_draw()
        self.updateSize(True, f)
        self.diffmap_cache = None
        self.diffmap.queue_draw()

    # create a hash for a line to use for line matching
    def _alignmentHash(self, line):
        text = line.getText()
        if text is None:
            return None
        pref = self.prefs.getBool
        if pref('align_ignore_whitespace'):
            # strip all white space from the string
            for c in whitespace:
                text = text.replace(c, '')
        else:
            # hashes for non-null lines should start with '+' to distinguish
            # them from blank lines
            if pref('align_ignore_endofline'):
                text = strip_eol(text)
            if pref('align_ignore_blanklines') and isBlank(text):
                # consider all lines containing only white space as the same
                return ''

            if pref('align_ignore_whitespace_changes'):
                # replace all blocks of white space with a single space
                pc = True
                r = []
                append = r.append
                for c in text:
                    if c in whitespace:
                        if pc:
                            append(' ')
                            pc = False
                    else:
                        append(c)
                        pc = True
                text = ''.join(r)
        if pref('align_ignore_case'):
            # convert everything to upper case
            text = text.upper()
        return text

    # align sets of lines by inserting null spacers and updating the size
    # of blocks to which they belong
    #
    # Leftlines and rightlines are list of list of lines.  Only the inner list
    # of lines are aligned (leftlines[-1] and rightlines[0]). Any spacers
    # needed for alignment are inserted in all lists of lines for a particular
    # side to keep them all in sync.
    def alignBlocks(self, leftblocks, leftlines, rightblocks, rightlines):
        blocks = ( leftblocks, rightblocks )
        lines = ( leftlines, rightlines )
        # get the inner lines we are to match
        middle = ( leftlines[-1], rightlines[0] )
        # eliminate any existing spacer lines
        mlines = ( [ line for line in middle[0] if line is not None ],
                   [ line for line in middle[1] if line is not None ] )
        s1, s2 = mlines
        n1, n2 = 0, 0
        # hash lines according to the alignment preferences
        a = self._alignmentHash
        t1 = [ a(s) for s in s1 ]
        t2 = [ a(s) for s in s2 ]
        # align s1 and s2 by inserting spacer lines
        # this will be used to determine which lines from the inner lists of
        # lines should be neighbours
        for block in patience_diff(t1, t2):
            delta = (n1 + block[0]) - (n2 + block[1])
            if delta < 0:
                # insert spacer lines in s1
                i = n1 + block[0]
                s1[i:i] = -delta * [ None ]
                n1 -= delta
            elif delta > 0:
                # insert spacer lines in s2
                i = n2 + block[1]
                s2[i:i] = delta * [ None ]
                n2 += delta
        nmatch = len(s1)

        # insert spacer lines in leftlines and rightlines and increase the
        # size of blocks in leftblocks and rightblocks as spacer lines are
        # inserted
        #
        # advance one row at a time inserting spacer lines as we go
        # 'i' indicates which row we are processing
        # 'k' indicates which pair of neighbours we are processing
        i, k = 0, 0
        bi = [ 0, 0 ]
        bn = [ 0, 0 ]
        while True:
            # if we have reached the end of the list for any side, it needs
            # spacer lines to align with the other side
            insert = [ i >= len(m) for m in middle ]
            if insert == [ True, True ]:
                # we have reached the end of both inner lists of lines
                # we are done
                break
            if insert == [ False, False ] and k < nmatch:
                # determine if either side needs spacer lines to make the
                # inner list of lines match up
                accept = True
                for j in range(2):
                    m = mlines[j][k]
                    if middle[j][i] is not m:
                        # this line does not correspond to the pair of
                        # neighbours we expected
                        if m is None:
                            # we expected to find a null here so insert one
                            insert[j] = True
                        else:
                            # we have a null but didn't expect one we will not
                            # obtain the pairing we expected by iserting nulls
                            accept = False
                if accept:
                    # our lines will be correctly paired up
                    # move on to the next pair
                    k += 1
                else:
                    # insert spacer lines as needed
                    insert = [ m[i] is not None for m in middle ]
            for j in range(2):
                if insert[j]:
                    # insert spacers lines for side 'j'
                    for temp in lines[j]:
                        temp.insert(i, None)
                    blocksj = blocks[j]
                    bij = bi[j]
                    bnj = bn[j]
                    # append a new block if needed
                    if len(blocksj) == 0:
                        blocksj.append(0)
                    # advance to the current block
                    while bnj + blocksj[bij] < i:
                        bnj += blocksj[bij]
                        bij += 1
                    # increase the current block size
                    blocksj[bij] += 1
            # advance to the next row
            i += 1

    # replace the contents of pane 'f' with the strings list of strings 'ss'
    def replaceContents(self, f, ss):
        self.alignmentChange(False)
        # determine the format for the text
        self.setFormat(f, getFormat(ss))

        # create an initial set of blocks for the lines
        blocks = []
        n = len(ss)
        if n > 0:
            blocks.append(n)
        # create line objects for the text
        mid = [[Line(j + 1, ss[j]) for j in range(n)]]
        if f > 0:
            # align with panes to the left
            # use copies so the originals can be used by the Undo object
            leftblocks = self.blocks[:]
            leftlines = [ pane.lines[:] for pane in self.panes[:f] ]
            removeNullLines(leftblocks, leftlines)
            self.alignBlocks(leftblocks, leftlines, blocks, mid)
            mid[:0] = leftlines
            blocks = mergeBlocks(leftblocks, blocks)
        if f + 1 < len(self.panes):
            # align with panes to the right
            # use copies so the originals can be used by the Undo object
            rightblocks = self.blocks[:]
            rightlines = [ pane.lines[:] for pane in self.panes[f + 1:] ]
            removeNullLines(rightblocks, rightlines)
            self.alignBlocks(blocks, mid, rightblocks, rightlines)
            mid.extend(rightlines)
            blocks = mergeBlocks(blocks, rightblocks)

        # update the lines for this pane
        pane = self.panes[f]
        old_n = len(pane.lines)
        new_n = len(mid[f])
        self.replaceLines(f, pane.lines, mid[f], pane.max_line_number, n)

        # insert or remove spacer lines from the other panes
        insertNull, getLine = self.insertNull, self.getLine
        for f_idx in range(len(self.panes)):
            if f_idx != f:
                for j in range(old_n-1, -1, -1):
                    if getLine(f_idx, j) is None:
                        insertNull(f_idx, j, True)
                temp = mid[f_idx]
                for j in range(new_n):
                    if temp[j] is None:
                        insertNull(f_idx, j, False)

        # update the blocks
        self.invalidateLineMatching(0, old_n, new_n)
        self.updateBlocks(blocks)
        self.alignmentChange(True)
        # update cursor
        self.setLineMode()
        self.setCurrentLine(self.current_pane, min(self.current_line, len(pane.lines) + 1))

    # refresh the lines to contain new objects with updated line numbers and
    # no local edits
    def bakeEdits(self, f):
        pane, lines, line_num = self.panes[f], [], 0
        for i in range(len(pane.lines)):
            s = self.getLineText(f, i)
            if s is None:
                lines.append(None)
            else:
                line_num += 1
                lines.append(Line(line_num, s))
        # update loaded pane
        self.replaceLines(f, pane.lines, lines, pane.max_line_number, line_num)

    # update the contents for a line, creating the line if necessary
    def updateText(self, f, i, text, is_modified=True):
        if self.panes[f].lines[i] is None:
            self.instanceLine(f, i)
        self.updateLineText(f, i, is_modified, text)

    # replace the current selection with 'text'
    def replaceText(self, text):
        # record the edit mode as we will be updating the selection too
        self.recordEditMode()

        # find the extents of the current selection
        f = self.current_pane
        pane = self.panes[f]
        nlines = len(pane.lines)
        line0, line1 = self.selection_line, self.current_line
        if self.mode == Mode.LINE:
            col0, col1 = 0, 0
            if line1 < line0:
                line0, line1 = line1, line0
            if line1 < nlines:
                line1 += 1
        else:
            col0, col1 = self.selection_char, self.current_char
            if line1 < line0 or (line1 == line0 and col1 < col0):
                line0, col0, line1, col1 = line1, col1, line0, col0

        # update text
        if text is None:
            text = ''
        # split the replacement text into lines
        ss = splitlines(text)
        if len(ss) == 0 or len(ss[-1]) != len_minus_line_ending(ss[-1]):
            ss.append('')
        # change the format to that of the target pane
        if pane.format == 0:
            self.setFormat(f, getFormat(ss))
        ss = [ convert_to_format(s, pane.format) for s in ss ]
        # prepend original text that was before the selection
        if col0 > 0:
            pre = self.getLineText(f, line0)[:col0]
            ss[0] = pre + ss[0]
        # remove the last line as it needs special casing
        lastcol = 0
        if len(ss) > 0:
            last = ss[-1]
            if len(last) == len_minus_line_ending(last):
                del ss[-1]
                lastcol = len(last)
        cur_line = line0 + len(ss)
        if lastcol > 0:
            # the replacement text does not end with a new line character
            # we need more text to finish the line, search forward for some
            # more text
            while line1 < nlines:
                s = self.getLineText(f, line1)
                line1 += 1
                if s is not None:
                    last = last + s[col1:]
                    break
                col1 = 0
            ss.append(last)
        elif col1 > 0:
            # append original text that was after the selection
            s = self.getLineText(f, line1)
            ss.append(s[col1:])
            line1 += 1

        # remove blank rows if possible
        n_need = len(ss)
        n_have = line1 - line0
        n_have -= self.removeSpacerLines(line0, n_have, f)
        delta = n_have - n_need
        if delta < 0:
            self.insertLines(line0 + n_have, -delta)
            delta = 0
        # update the text
        for i, s in enumerate(ss):
            self.updateText(f, line0 + i, s)
        # clear all unused lines
        for i in range(delta):
            self.updateText(f, line0 + n_need + i, None)
        # update selection
        if self.mode == Mode.LINE:
            self.setCurrentLine(f, line0 + max(n_need, 1) - 1, line0)
        else:
            self.setCurrentChar(cur_line, lastcol)
        self.recordEditMode()

    # manually adjust line matching so 'line1' of pane 'f' is a neighbour of
    # 'line2' from pane 'f+1'
    def align(self, f, line1, line2):
        # record the edit mode as we will be updating the selection too
        self.recordEditMode()

        # find the smallest span of blocks that inclues line1 and line2
        start = line1
        end = line2
        if end < start:
            start, end = end, start
        pre_blocks = []
        mid = []
        post_blocks = []
        n = 0
        for b in self.blocks:
            if n + b <= start:
                dst = pre_blocks
            elif n <= end:
                dst = mid
            else:
                dst = post_blocks
            dst.append(b)
            n += b
        start = sum(pre_blocks)
        end = start + sum(mid)

        # cut the span of blocks into three sections:
        # 1. lines before the matched pair
        # 2. the matched pair
        # 3. lines after the matched pair
        # each section has lines and blocks for left and right sides
        lines_s = [ [], [], [] ]
        cutblocks = [ [], [], [] ]
        lines = [ pane.lines for pane in self.panes ]
        nlines = len(lines[0])
        for temp, m in zip([ lines[:f + 1], lines[f + 1:] ], [ line1, line2 ]):
            # cut the blocks just before the line being matched
            pre, post = cutBlocks(m - start, mid)
            if len(temp) == 1:
                # if we only have one pane on this side, we don't need to
                # preserve other cuts
                pre = createBlock(sum(pre))
            # the first section of lines to match
            lines_s[0].append([ s[start:m] for s in temp ])
            cutblocks[0].append(pre)
            # the line to match may be after the actual lines
            if m < nlines:
                m1 = [ [ s[m] ] for s in temp ]
                m2 = [ s[m + 1:end] for s in temp ]
                # cut the blocks just after the line being matched
                b1, b2 = cutBlocks(1, post)
                if len(temp) == 1:
                    # if we only have one pane on this side, we don't need to
                    # preserve other cuts
                    b2 = createBlock(sum(b2))
            else:
                m1 = [ [] for s in temp ]
                m2 = [ [] for s in temp ]
                b1, b2 = [], []
            # the second section of lines to match
            lines_s[1].append(m1)
            cutblocks[1].append(b1)
            # the third section of lines to match
            lines_s[2].append(m2)
            cutblocks[2].append(b2)

        # align each section and concatenate the results
        finallines = [ [] for s in lines ]
        for b, lines_t in zip(cutblocks, lines_s):
            removeNullLines(b[0], lines_t[0])
            removeNullLines(b[1], lines_t[1])
            self.alignBlocks(b[0], lines_t[0], b[1], lines_t[1])
            temp = lines_t[0]
            temp.extend(lines_t[1])
            for dst, s in zip(finallines, temp):
                dst.extend(s)
            pre_blocks.extend(mergeBlocks(b[0], b[1]))
        pre_blocks.extend(post_blocks)

        # update the actual lines and blocks
        self.updateAlignment(start, end - start, finallines)
        self.updateBlocks(pre_blocks)

        i = len(lines_s[0][0][0])
        self.removeSpacerLines(start + i, len(finallines[0]) - i)
        i -= min(self.removeSpacerLines(start, i), i - 1)

        # update selection
        self.setCurrentLine(self.current_pane, start + i)
        self.recordEditMode()

    # appends an undo to reset to the specified selection mode and range
    # this should be called before and after actions that also change the
    # selection
    def recordEditMode(self):
        if self.undoblock is not None:
            self.addUndo(EditModeUndo(self.mode, self.current_pane, self.current_line, self.current_char, self.selection_line, self.selection_char, self.cursor_column))

    # change the selection mode
    def setEditMode(self, mode, f, current_line, current_char, selection_line, selection_char, cursor_column):
        old_f = self.current_pane
        self.mode = mode
        self.current_pane = f
        self.current_line = current_line
        self.current_char = current_char
        self.selection_line = selection_line
        self.selection_char = selection_char
        self.cursor_column = cursor_column
        if mode == Mode.CHAR:
            self.setCurrentChar(self.current_line, self.current_char, True)
        else:
            self.setCurrentLine(self.current_pane, self.current_line, self.selection_line)
        self.emit('cursor_changed')
        self.emit('mode_changed')
        # queue a redraw to show the updated selection
        self.dareas[old_f].queue_draw()

    # queue a range of lines for redrawing
    def _queue_draw_lines(self, f, line0, line1=None):
        if line1 is None:
            line1 = line0
        elif line0 > line1:
            line0, line1 = line1, line0
        darea = self.dareas[f]
        w, h = darea.get_allocation().width, self.font_height
        darea.queue_draw_area(0, line0 * h - int(self.vadj.get_value()), w, (line1 - line0 + 1) * h)

    # scroll vertically to ensure the current line is visible
    def _ensure_line_is_visible(self, i):
        h = self.font_height
        lower = i * h
        upper = lower + h
        vadj = self.vadj
        v = vadj.get_value()
        ps = vadj.get_page_size()
        if lower < v:
            vadj.set_value(lower)
        elif upper > v + ps:
            vadj.set_value(upper - ps)

    # change the current selection in Mode.LINE
    # use extend=True to extend the selection
    def setCurrentLine(self, f, i, selection=None):
        # remember old cursor position so we can just redraw what is necessary
        old_f = self.current_pane
        line0, line1 = self.current_line, self.selection_line

        # clamp input values
        f = max(min(f, len(self.panes) - 1), 0)
        i = max(min(i, len(self.panes[f].lines)), 0)

        # update cursor
        self.current_pane = f
        self.current_line = i
        if selection is None:
            self.selection_line = i
        else:
            self.selection_line = selection

        self.emit('cursor_changed')

        # invalidate old selection area
        self._queue_draw_lines(old_f, line0, line1)
        # invalidate new selection area
        self._queue_draw_lines(f, i, self.selection_line)

        # ensure the new cursor position is visible
        self._ensure_line_is_visible(i)

    # returns True if the line has preedit text
    def hasPreedit(self, f, i):
        return self.mode == Mode.CHAR and self.current_pane == f and self.current_line == i and self.im_preedit is not None

    # create a layout for the existing preedit text
    def _preedit_layout(self, partial=False):
        s, a, c = self.im_preedit
        if partial:
            s = s[:c]
        layout = self.create_pango_layout(s)
        layout.set_font_description(self.font)
        layout.set_attributes(a)
        return layout

    # inform input method about cursor motion
    def _cursor_position_changed(self, recompute):
        if self.mode == Mode.CHAR:
            # update input method
            h = self.font_height
            if recompute:
                self.cursor_pos = (pixels(self._get_cursor_x_offset()), self.current_line * h)
            x, y = self.cursor_pos
            x -= int(self.hadj.get_value())
            y -= int(self.vadj.get_value())
            # translate to a position relative to the window
            x, y = self.dareas[self.current_pane].translate_coordinates(self.get_toplevel(), x, y)
            # input methods support widgets are centred horizontally about the
            # cursor, a width of 50 seems to give a better widget positions
            rect = Gdk.Rectangle()
            rect.x = x
            rect.y = y
            rect.width = 50
            rect.height = h

            self.im_context.set_cursor_location(rect)

    # get the position of the cursor in Pango units
    def _get_cursor_x_offset(self):
        j = self.current_char
        if j > 0:
            text = self.getLineText(self.current_pane, self.current_line)[:j]
            return self.getTextWidth(''.join(self.expand(text)))
        return 0

    # scroll to ensure the current cursor position is visible
    def _ensure_cursor_is_visible(self):
        current_line = self.current_line

        # find the cursor's horizontal range
        lower = self._get_cursor_x_offset()
        if self.im_preedit is not None:
            lower += self._preedit_layout(True).get_size()[0]
        upper = lower + self.getLineNumberWidth() + self.digit_width
        lower, upper = pixels(lower), pixels(upper)

        # scroll horizontally
        hadj = self.hadj
        v = hadj.get_value()
        ps = hadj.get_page_size()
        if lower < v:
            hadj.set_value(lower)
        elif upper > v + ps:
            hadj.set_value(upper - ps)

        # scroll vertically to current line
        self._ensure_line_is_visible(current_line)

    def __set_clipboard_text(self, clipboard, s):
        # remove embedded nulls as the clipboard cannot handle them
        Gtk.Clipboard.get(clipboard).set_text(s.replace('\0', ''), -1)

    # change the current selection in Mode.CHAR
    # use extend=True to extend the selection
    def setCurrentChar(self, i, j, si=None, sj=None):
        f = self.current_pane

        # remember old cursor position so we can just redraw what is necessary
        line0, line1 = self.current_line, self.selection_line

        # clear remembered cursor column
        self.cursor_column = -1
        # update cursor and selection
        extend = (si is not None and sj is not None)
        if not extend:
            si, sj = i, j
        self.current_line = i
        self.current_char = j
        self.selection_line = si
        self.selection_char = sj

        if extend:
            self.__set_clipboard_text(Gdk.SELECTION_PRIMARY, self.getSelectedText())

        self._cursor_position_changed(True)
        self.emit('cursor_changed')

        # invalidate old selection area
        self._queue_draw_lines(f, line0, line1)
        # invalidate new selection area
        self._queue_draw_lines(f, i, self.selection_line)

        # ensure the new cursor position is visible
        self._ensure_cursor_is_visible()

    # returns the currently selected text
    def getSelectedText(self):
        f = self.current_pane
        start, end = self.selection_line, self.current_line
        # find extents of selection
        if self.mode == Mode.LINE:
            if end < start:
                start, end = end, start
            end += 1
            col0, col1 = 0, 0
        else:
            col0, col1 = self.selection_char, self.current_char
            if end < start or (end == start and col1 < col0):
                start, col0, end, col1 = end, col1, start, col0
            if col1 > 0:
               end += 1
        # get the text for the selected lines
        end = min(end, len(self.panes[f].lines))
        ss = [ self.getLineText(f, i) for i in range(start, end) ]
        # trim out the unselected parts of the lines
        # check for col > 0 as some lines may be null
        if col1 > 0:
            ss[-1] = ss[-1][:col1]
        if col0 > 0:
            ss[0] = ss[0][col0:]
        return ''.join([ s for s in ss if s is not None ])

    # expands the selection to include everything
    def select_all(self):
        if self.mode == Mode.LINE or self.mode == Mode.CHAR:
            f = self.current_pane
            self.selection_line = 0
            self.current_line = len(self.panes[f].lines)
            if self.mode == Mode.CHAR:
                self.selection_char = 0
                self.current_char = 0
            self.dareas[f].queue_draw()

    # returns the index of the last character in text that should be left of
    # 'x' pixels from the edge of the darea widget
    # if partial=True, include characters only partially to the left of 'x'
    def _getPickedCharacter(self, text, x, partial):
        if text is None:
            return 0
        n = len(text)
        w = self.getLineNumberWidth()
        for i, s in enumerate(self.expand(text)):
            width = self.getTextWidth(s)
            tmp = w
            if partial:
                tmp += width // 2
            else:
                tmp += width
            if x < pixels(tmp):
                return i
            w += width
        return n

    # update the selection in response to a mouse button press
    def button_press(self, f, x, y, extend):
        if y < 0:
            x, y = -1, 0
        i = min(y // self.font_height, len(self.panes[f].lines))
        if self.mode == Mode.CHAR and f == self.current_pane:
            text = strip_eol(self.getLineText(f, i))
            j = self._getPickedCharacter(text, x, True)
            if extend:
                si, sj = self.selection_line, self.selection_char
            else:
                si, sj = None, None
            self.setCurrentChar(i, j, si, sj)
        else:
            if self.mode == Mode.ALIGN:
                extend = False
            elif self.mode == Mode.CHAR:
                self.setLineMode()
            if extend and f == self.current_pane:
                selection = self.selection_line
            else:
                selection = None
            self.setCurrentLine(f, i, selection)

    # callback for mouse button presses in the text window
    def darea_button_press_cb(self, widget, event, f):
        self.get_toplevel().set_focus(self)
        x = int(event.x + self.hadj.get_value())
        y = int(event.y + self.vadj.get_value())
        nlines = len(self.panes[f].lines)
        i = min(y // self.font_height, nlines)
        if event.button == 1:
            # left mouse button
            if event.type == Gdk.EventType._2BUTTON_PRESS:
                # double click
                if self.mode == Mode.ALIGN:
                    self.setLineMode()
                if self.mode == Mode.LINE:
                    # change to Mode.CHAR
                    self.setCurrentLine(f, i)
                    # silently switch mode so the viewer does not scroll yet.
                    self.mode = Mode.CHAR
                    self._im_focus_in()
                    self.button_press(f, x, y, False)
                    self.emit('mode_changed')
                elif self.mode == Mode.CHAR and self.current_pane == f:
                    # select word
                    text = strip_eol(self.getLineText(f, i))
                    if text is not None:
                        n = len(text)
                        j = self._getPickedCharacter(text, x, False)
                        if j < n:
                            c = getCharacterClass(text[j])
                            k = j
                            while k > 0 and getCharacterClass(text[k - 1]) == c:
                                k -= 1
                            while j < n and getCharacterClass(text[j]) == c:
                                j += 1
                            self.setCurrentChar(i, j, i, k)
            elif event.type == Gdk.EventType._3BUTTON_PRESS:
                # triple click, select a whole line
                if self.mode == Mode.CHAR and self.current_pane == f:
                    i2 = min(i + 1, nlines)
                    self.setCurrentChar(i2, 0, i, 0)
            else:
                # update the selection
                is_shifted = event.state & Gdk.ModifierType.SHIFT_MASK
                extend = (is_shifted and f == self.current_pane)
                self.button_press(f, x, y, extend)
        elif event.button == 2:
            # middle mouse button, paste primary selection
            if self.mode == Mode.CHAR and f == self.current_pane:
                self.button_press(f, x, y, False)
                self.openUndoBlock()
                Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY).request_text(self.receive_clipboard_text_cb, None)
                self.closeUndoBlock()
        elif event.button == 3:
            # right mouse button, raise context sensitive menu
            can_align = (self.mode == Mode.LINE and (f == self.current_pane + 1 or f == self.current_pane - 1))
            can_isolate = (self.mode == Mode.LINE and f == self.current_pane)
            can_merge = (self.mode == Mode.LINE and f != self.current_pane)
            can_select = ((self.mode == Mode.LINE or self.mode == Mode.CHAR) and f == self.current_pane)
            can_swap = (f != self.current_pane)
            menu = createMenu(self.resources, [
                      [_('Align with Selection'), self.align_with_selection_cb, [f, i], Gtk.STOCK_EXECUTE, None, can_align],
                      [_('Isolate'), self.button_cb, 'isolate', None, None, can_isolate],
                      [_('Merge Selection'), self.merge_lines_cb, f, None, None, can_merge],
                      [],
                      [_('Cut'), self.button_cb, 'cut', Gtk.STOCK_CUT, None, can_select],
                      [_('Copy'), self.button_cb, 'copy', Gtk.STOCK_COPY, None, can_select],
                      [_('Paste'), self.button_cb, 'paste', Gtk.STOCK_PASTE, None, can_select],
                      [],
                      [_('Select All'), self.button_cb, 'select_all', None, None, can_select],
                      [_('Clear Edits'), self.button_cb, 'clear_edits', Gtk.STOCK_CLEAR, None, can_isolate],
                      [],
                      [_('Swap with Selected Pane'), self.swap_panes_cb, f, None, None, can_swap]])
            menu.attach_to_widget(self)
            menu.popup(None, None, None, None, event.button, event.time)

    # callback used to notify us about click and drag motion
    def darea_motion_notify_cb(self, widget, event, f):
        if event.state & Gdk.ModifierType.BUTTON1_MASK:
            # left mouse button
            extend = (f == self.current_pane)
            x = int(event.x + self.hadj.get_value())
            y = int(event.y + self.vadj.get_value())
            self.button_press(f, x, y, extend)

    # return a list of (begin, end, flag) tuples marking characters that differ
    # from the text in line 'i' from panes 'f' and 'f+1'
    # return the results for pane 'f' if idx=0 and 'f+1' if idx=1
    def getDiffRanges(self, f, i, idx, flag):
        result = []
        s1 = nullToEmpty(self.getLineText(f, i))
        s2 = nullToEmpty(self.getLineText(f + 1, i))

        # ignore blank lines if specified
        if self.prefs.getBool('display_ignore_blanklines') and isBlank(s1) and isBlank(s2):
            return result

        # ignore white space preferences
        ignore_whitespace = self.prefs.getBool('display_ignore_whitespace')
        if ignore_whitespace or self.prefs.getBool('display_ignore_whitespace_changes'):
            if idx == 0:
                s = s1
            else:
                s = s2
            if self.prefs.getBool('display_ignore_endofline'):
                s = strip_eol(s)

            s1 = nullToEmpty(self.getCompareString(f, i))
            s2 = nullToEmpty(self.getCompareString(f + 1, i))

            # build a mapping from characters in compare string to those in the
            # original string
            v = 0
            lookup = []
            # we only need to consider white space here as those are the only
            # ones that can change the number of characters in the compare
            # string
            if ignore_whitespace:
                # all white space characters were removed
                for c in s:
                    if c not in whitespace:
                        lookup.append(v)
                    v += 1
            else:
                # all white space characters were replaced with a single space
                first = True
                for c in s:
                    if c in whitespace:
                        # only include the first white space character of a span
                        if first:
                            lookup.append(v)
                            first = False
                    else:
                        lookup.append(v)
                        first = True
                    v += 1
            lookup.append(v)
        else:
            lookup = None

        start = 0
        for block in difflib.SequenceMatcher(None, s1, s2).get_matching_blocks():
            end = block[idx]
            # skip zero length blocks
            if start < end:
                if lookup is None:
                    result.append((start, end, flag))
                else:
                    # map to indices for the original string
                    lookup_start = lookup[start]
                    lookup_end = lookup[end]
                    # scan for whitespace and skip those sections if specified
                    for j in range(lookup_start, lookup_end):
                        if ignore_whitespace and s[j] in whitespace:
                            if lookup_start != j:
                                result.append((lookup_start, j, flag))
                            lookup_start = j + 1
                    if lookup_start != lookup_end:
                        result.append((lookup_start, lookup_end, flag))
            start = end + block[2]
        return result

    # returns a hash of a string that can be used to quickly compare strings
    # according to the display preferences
    def getCompareString(self, f, i):
        line = self.getLine(f, i)
        if line is None:
            return None
        # if a cached value exists, use it
        s = line.compare_string
        if s is not None:
            return s
        # compute a new hash and cache it
        s = line.getText()
        if s is not None:
            if self.prefs.getBool('display_ignore_endofline'):
                s = strip_eol(s)
            if self.prefs.getBool('display_ignore_blanklines') and isBlank(s):
                return None
            if self.prefs.getBool('display_ignore_whitespace'):
                # strip all white space characters
                for c in whitespace:
                    s = s.replace(c, '')
            elif self.prefs.getBool('display_ignore_whitespace_changes'):
                # map all spans of white space characters to a single space
                first = True
                temp = []
                for c in s:
                    if c in whitespace:
                        if first:
                            temp.append(' ')
                            first = False
                    else:
                        temp.append(c)
                        first = True
                s = ''.join(temp)
            if self.prefs.getBool('display_ignore_case'):
                # force everything to be upper case
                s = s.upper()
            # cache the hash
            line.compare_string = s
        return s

    # draw the text viewport
    def darea_draw_cb(self, widget, cr, f):
        pane = self.panes[f]
        syntax = self.resources.getSyntax(self.syntax)
        rect = widget.get_allocation()
        x = rect.x + int(self.hadj.get_value())
        y = rect.y + int(self.vadj.get_value())

        cr.translate(-x, -y)

        maxx = x + rect.width
        maxy = y + rect.height
        line_number_width = pixels(self.getLineNumberWidth())
        h = self.font_height
        diffcolours = [self.resources.getDifferenceColour(f), self.resources.getDifferenceColour(f + 1)]
        diffcolours.append((diffcolours[0] + diffcolours[1]) * 0.5)

        # iterate over each exposed line
        i = y // h
        y_start = i * h
        while y_start < maxy:
            line = self.getLine(f, i)

            # line numbers
            if line_number_width > 0 and 0 < maxx and line_number_width > x:
                cr.save()
                cr.rectangle(0, y_start, line_number_width, h)
                cr.clip()
                colour = self.resources.getColour('line_number_background')
                cr.set_source_rgb(colour.red, colour.green, colour.blue)
                cr.paint()

                # draw the line number
                if line is not None and line.line_number is not None:
                    colour = self.resources.getColour('line_number')
                    cr.set_source_rgb(colour.red, colour.green, colour.blue)
                    layout = self.create_pango_layout(str(line.line_number))
                    layout.set_font_description(self.font)
                    w = pixels(layout.get_size()[0] + self.digit_width)
                    cr.move_to(line_number_width - w, y_start)
                    PangoCairo.show_layout(cr, layout)
                cr.restore()

            x_start = line_number_width
            if x_start < maxx:
                cr.save()
                cr.rectangle(x_start, y_start, maxx - x_start, h)
                cr.clip()

                text = self.getLineText(f, i)
                ss = None

                # enlarge cache to fit pan.diff_cache[i]
                if i >= len(pane.diff_cache):
                    pane.diff_cache.extend((i - len(pane.diff_cache) + 1) * [ None ])
                # construct a list of ranges for this lines character
                # differences if not already cached
                if pane.diff_cache[i] is None:
                    flags = 0
                    temp_diff = []
                    comptext = self.getCompareString(f, i)
                    if f > 0:
                        # compare with neighbour to the left
                        if self.getCompareString(f - 1, i) != comptext:
                            flags |= 1
                            if text is not None:
                                temp_diff = mergeRanges(temp_diff, self.getDiffRanges(f - 1, i, 1, 1))
                    if f + 1 < len(self.panes):
                        # compare with neighbour to the right
                        if self.getCompareString(f + 1, i) != comptext:
                            flags |= 2
                            if text is not None:
                                temp_diff = mergeRanges(temp_diff, self.getDiffRanges(f, i, 0, 2))

                    chardiff = []
                    if text is not None:
                        # expand text into a list of visual representations
                        ss = self.expand(text)

                        # find the size of each region in Pango units
                        old_end = 0
                        x_temp = 0
                        for start, end, tflags in temp_diff:
                            layout = self.create_pango_layout(''.join(ss[old_end:start]))
                            layout.set_font_description(self.font)
                            x_temp += layout.get_size()[0]
                            layout = self.create_pango_layout(''.join(ss[start:end]))
                            layout.set_font_description(self.font)
                            w = layout.get_size()[0]
                            chardiff.append((start, end, x_temp, w, diffcolours[tflags - 1]))
                            old_end = end
                            x_temp += w
                    # cache flags and character diff ranges
                    pane.diff_cache[i] = (flags, chardiff)
                else:
                    flags, chardiff = pane.diff_cache[i]

                # account for preedit changes
                if f > 0 and self.hasPreedit(f - 1, i):
                    flags |= 1
                if f + 1 < len(self.panes) and self.hasPreedit(f + 1, i):
                    flags |= 2
                has_preedit = self.hasPreedit(f, i)
                if has_preedit:
                    # we have preedit text
                    preeditlayout = self._preedit_layout()
                    preeditwidth = preeditlayout.get_size()[0]
                    if f > 0:
                        flags |= 1
                    if f + 1 < len(self.panes):
                        flags |= 2
                else:
                    preeditwidth = 0
                # draw background
                colour = self.resources.getColour('text_background')
                alpha = self.resources.getFloat('character_difference_opacity')
                if flags != 0:
                    colour = (diffcolours[flags - 1] * self.resources.getFloat('line_difference_opacity')).over(colour)
                cr.set_source_rgb(colour.red, colour.green, colour.blue)
                cr.paint()

                # make preedit text appear as a modified line that differs from
                # both neighbours
                preedit_bg_colour = (diffcolours[flags - 1] * alpha).over(colour)

                if text is not None:
                    # draw char diffs
                    for starti, endi, start, w, colour in chardiff:
                        if has_preedit:
                            # make space for preedit text
                            if self.current_char <= starti:
                                start += preeditwidth
                            elif self.current_char < endi:
                                w += preeditwidth
                        cr.set_source_rgba(colour.red, colour.green, colour.blue, alpha)
                        cr.rectangle(x_start + pixels(start), y_start, pixels(w), h)
                        cr.fill()

                if has_preedit or (line is not None and line.is_modified):
                    # draw modified
                    colour = self.resources.getColour('edited')
                    alpha = self.resources.getFloat('edited_opacity')
                    preedit_bg_colour = (colour * alpha).over(preedit_bg_colour)
                    cr.set_source_rgba(colour.red, colour.green, colour.blue, alpha)
                    cr.paint()
                if self.mode == Mode.ALIGN:
                    # draw align
                    if self.align_pane == f and self.align_line == i:
                        colour = self.resources.getColour('alignment')
                        alpha = self.resources.getFloat('alignment_opacity')
                        cr.set_source_rgba(colour.red, colour.green, colour.blue, alpha)
                        cr.paint()
                elif self.mode == Mode.LINE:
                    # draw line selection
                    if self.current_pane == f:
                        start, end = self.selection_line, self.current_line
                        if end < start:
                            start, end = end, start
                        if i >= start and i <= end:
                            colour = self.resources.getColour('line_selection')
                            alpha = self.resources.getFloat('line_selection_opacity')
                            cr.set_source_rgba(colour.red, colour.green, colour.blue, alpha)
                            cr.paint()
                elif self.mode == Mode.CHAR:
                    # draw char selection
                    if self.current_pane == f and text is not None:
                        start, end = self.selection_line, self.current_line
                        start_char, end_char = self.selection_char, self.current_char
                        if end < start or (end == start and end_char < start_char):
                            start, start_char, end, end_char = end, end_char, start, start_char
                        if start <= i and end >= i:
                            if start < i:
                                start_char = 0
                            if end > i:
                                end_char = len(text)
                            if start_char < end_char:
                                if ss is None:
                                    ss = self.expand(text)
                                layout = self.create_pango_layout(''.join(ss[:start_char]))
                                layout.set_font_description(self.font)
                                x_temp = layout.get_size()[0]
                                layout = self.create_pango_layout(''.join(ss[start_char:end_char]))
                                layout.set_font_description(self.font)
                                w = layout.get_size()[0]
                                colour = self.resources.getColour('character_selection')
                                alpha = self.resources.getFloat('character_selection_opacity')
                                cr.set_source_rgba(colour.red, colour.green, colour.blue, alpha)
                                cr.rectangle(x_start + pixels(x_temp), y_start, pixels(w), h)
                                cr.fill()

                if self.prefs.getBool('display_show_right_margin'):
                    # draw margin
                    x_temp = line_number_width + pixels(self.prefs.getInt('display_right_margin') * self.digit_width)
                    if x_temp >= x and x_temp < maxx:
                        colour = self.resources.getColour('margin')
                        cr.set_source_rgb(colour.red, colour.green, colour.blue)
                        cr.set_line_width(1)
                        cr.move_to(x_temp, y_start)
                        cr.rel_line_to(0, h)
                        cr.stroke()

                if text is None:
                    # draw hatching
                    colour = self.resources.getColour('hatch')
                    cr.set_source_rgb(colour.red, colour.green, colour.blue)
                    cr.set_line_width(1)
                    h2 = 2 * h
                    temp = line_number_width
                    if temp < x:
                        temp += ((x - temp) // h) * h
                    h_half = 0.5 * h
                    phase = [ h_half, h_half, -h_half, -h_half ]
                    for j in range(4):
                        x_temp = temp
                        y_temp = y_start
                        for k in range(j):
                            y_temp += phase[k]
                        cr.move_to(x_temp, y_temp)
                        for k in range(j, 4):
                            cr.rel_line_to(h_half, phase[k])
                            x_temp += h_half
                        while x_temp < maxx:
                            cr.rel_line_to(h, h)
                            cr.rel_line_to(h, -h)
                            x_temp += h2
                        cr.stroke()
                else:
                    # continue populating the syntax highlighting cache until
                    # line 'i' is included
                    n = len(pane.syntax_cache)
                    while i >= n:
                        temp = self.getLineText(f, n)
                        if syntax is None:
                            initial_state, end_state = None, None
                            if temp is None:
                                blocks = None
                            else:
                                blocks = [ (0, len(temp), 'text') ]
                        else:
                            # apply the syntax highlighting rules to identify
                            # ranges of similarly coloured characters
                            if n == 0:
                                initial_state = syntax.initial_state
                            else:
                                initial_state = pane.syntax_cache[-1][1]
                            if temp is None:
                                end_state, blocks = initial_state, None
                            else:
                                end_state, blocks = syntax.parse(initial_state, temp)
                        pane.syntax_cache.append([initial_state, end_state, blocks, None])
                        n += 1

                    # use the cache the position, layout, and colour of each
                    # span of characters
                    blocks = pane.syntax_cache[i][3]
                    if blocks is None:
                        # populate the cache item if it didn't exist
                        if ss is None:
                            ss = self.expand(text)
                        x_temp = 0
                        blocks = []
                        for start, end, tag in pane.syntax_cache[i][2]:
                            layout = self.create_pango_layout(''.join(ss[start:end]))
                            layout.set_font_description(self.font)
                            colour = self.resources.getColour(tag)
                            blocks.append((start, end, x_temp, layout, colour))
                            x_temp += layout.get_size()[0]
                        pane.syntax_cache[i][3] = blocks

                    # draw text
                    for starti, endi, start, layout, colour in blocks:
                        cr.set_source_rgb(colour.red, colour.green, colour.blue)
                        if has_preedit:
                            # make space for preedit text
                            if self.current_char <= starti:
                                start += preeditwidth
                            elif self.current_char < endi:
                                # divide text into 2 segments
                                ss = self.expand(text)
                                layout = self.create_pango_layout(''.join(ss[starti:self.current_char]))
                                layout.set_font_description(self.font)
                                cr.move_to(x_start + pixels(start), y_start)
                                PangoCairo.show_layout(cr, layout)
                                start += layout.get_size()[0] + preeditwidth
                                layout = self.create_pango_layout(''.join(ss[self.current_char:endi]))
                                layout.set_font_description(self.font)
                        cr.move_to(x_start + pixels(start), y_start)
                        PangoCairo.show_layout(cr, layout)

                if self.current_pane == f and self.current_line == i:
                    # draw the cursor and preedit text
                    if self.mode == Mode.CHAR:
                        x_pos = x_start + pixels(self._get_cursor_x_offset())
                        if has_preedit:
                            # we have preedit text
                            layout = self._preedit_layout()
                            w = pixels(layout.get_size()[0])

                            # clear the background
                            colour = preedit_bg_colour
                            cr.set_source_rgb(colour.red, colour.green, colour.blue)
                            cr.rectangle(x_pos, y_start, w, h)
                            cr.fill()
                            # draw the preedit text
                            colour = self.resources.getColour('preedit')
                            cr.set_source_rgb(colour.red, colour.green, colour.blue)
                            cr.move_to(x_pos, y_start)
                            PangoCairo.show_layout(cr, layout)
                            # advance to the preedit's cursor position
                            x_pos += pixels(self._preedit_layout(True).get_size()[0])
                        # draw the character editing cursor
                        colour = self.resources.getColour('cursor')
                        cr.set_source_rgb(colour.red, colour.green, colour.blue)
                        cr.set_line_width(1)
                        cr.move_to(x_pos + 0.5, y_start)
                        cr.rel_line_to(0, h)
                        cr.stroke()
                    elif self.mode == Mode.LINE or self.mode == Mode.ALIGN:
                        # draw the line editing cursor
                        colour = self.resources.getColour('cursor')
                        cr.set_source_rgb(colour.red, colour.green, colour.blue)
                        cr.set_line_width(1)
                        cr.move_to(maxx, y_start + 0.5)
                        cr.line_to(x_start + 0.5, y_start + 0.5)
                        cr.line_to(x_start + 0.5, y_start + h - 0.5)
                        cr.line_to(maxx, y_start + h - 0.5)
                        cr.stroke()
                cr.restore()
            # advance to the next exposed line
            i += 1
            y_start += h

    # callback used when panes are scrolled horizontally
    def hadj_changed_cb(self, adj):
        self._cursor_position_changed(False)

    # callback used when panes are scrolled vertically
    def vadj_changed_cb(self, adj):
        self._cursor_position_changed(False)
        self.diffmap.queue_draw()

    # callback to handle button presses on the overview map
    def diffmap_button_press_cb(self, widget, event):
        vadj = self.vadj

        h = widget.get_allocation().height
        hmax = max(int(vadj.get_upper()), h)

        # centre view about picked location
        y = event.y * hmax // h
        v = y - int(vadj.get_page_size() / 2)
        v = max(v, int(vadj.get_lower()))
        v = min(v, int(vadj.get_upper() - vadj.get_page_size()))
        vadj.set_value(v)

    # callback to handle mouse scrollwheel events
    def diffmap_scroll_cb(self, widget, event):
        delta = 100
        if event.direction == Gdk.ScrollDirection.UP:
            step_adjustment(self.vadj, -delta)
        elif event.direction == Gdk.ScrollDirection.DOWN:
            step_adjustment(self.vadj, delta)

    # redraws the overview map when a portion is exposed
    def diffmap_draw_cb(self, widget, cr):
        n = len(self.panes)

        # compute map if it hasn't already been cached
        # the map is a list of (start, end, flags) tuples for each pane
        # flags & 1 indicates differences with the pane to the left
        # flags & 2 indicates differences with the pane to the right
        # flags & 4 indicates modified lines
        # flags & 8 indicates regular lines with text
        if self.diffmap_cache is None:
            nlines = len(self.panes[0].lines)
            start = n * [ 0 ]
            flags = n * [ 0 ]
            self.diffmap_cache = [ [] for f in range(n) ]
            # iterate over each row of lines
            for i in range(nlines):
                nextflag = 0
                # iterate over each pane
                for f in range(n):
                    flag = nextflag
                    nextflag = 0
                    s0 = self.getCompareString(f, i)
                    # compare with neighbour to the right
                    if f + 1 < n:
                        if s0 != self.getCompareString(f + 1, i):
                            flag |= 2
                            nextflag |= 1
                    line = self.getLine(f, i)
                    if line is not None and line.is_modified:
                        # modified line
                        flag = 4
                    elif line is None or line.getText() is None:
                        # empty line
                        flag = 0
                    elif flag == 0:
                        # regular line
                        flag = 8
                    if flags[f] != flag:
                        if flags[f] != 0:
                            self.diffmap_cache[f].append([start[f], i, flags[f]])
                        start[f] = i
                        flags[f] = flag
            # finish any incomplete ranges
            for f in range(n):
                if flags[f] != 0:
                    self.diffmap_cache[f].append([start[f], nlines, flags[f]])
        # clear
        colour = self.resources.getColour('map_background')
        cr.set_source_rgb(colour.red, colour.green, colour.blue)
        cr.paint()
        bg_colour = self.resources.getColour('text_background')
        edited_colour = self.resources.getColour('edited')
        rect = widget.get_allocation()

        # get scroll position and total size
        vadj = self.vadj
        hmax = max(vadj.get_upper(), rect.height)

        # draw diff blocks
        wn = rect.width / n
        pad = 1
        for f in range(n):
            diffcolours = [self.resources.getDifferenceColour(f), self.resources.getDifferenceColour(f + 1)]
            diffcolours.append((diffcolours[0] + diffcolours[1]) * 0.5)
            wx = f * wn
            # draw in two passes, more important stuff in the second pass
            # this ensures less important stuff does not obscure more important
            # data
            for p in range(2):
                for start, end, flag in self.diffmap_cache[f]:
                    if p == 0 and flag == 8:
                        colour = bg_colour
                    elif p == 1 and flag & 7:
                        if flag & 4:
                            colour = edited_colour
                        else:
                            colour = diffcolours[(flag & 3) - 1]
                    else:
                        continue

                    # ensure the line is visible in the map
                    ymin = rect.height * self.font_height * start // hmax
                    if ymin >= rect.y + rect.height:
                        break
                    yh = max(rect.height * self.font_height * end // hmax - ymin, 1)

                    #if ymin + yh <= rect.y:
                    #    continue

                    cr.set_source_rgb(colour.red, colour.green, colour.blue)
                    cr.rectangle(wx + pad, ymin, wn - 2 * pad, yh)
                    cr.fill()

        # draw cursor
        vmin = int(vadj.get_value())
        vmax = vmin + vadj.get_page_size()
        ymin = rect.height * vmin // hmax
        if ymin < rect.y + rect.height:
            yh = rect.height * vmax // hmax - ymin
            if yh > 1:
                yh -= 1
            #if ymin + yh > rect.y:
            colour = self.resources.getColour('line_selection')
            alpha = self.resources.getFloat('line_selection_opacity')
            cr.set_source_rgba(colour.red, colour.green, colour.blue, alpha)
            cr.rectangle(0.5, ymin + 0.5, rect.width - 1, yh - 1)
            cr.fill()
            colour = self.resources.getColour('cursor')
            cr.set_source_rgb(colour.red, colour.green, colour.blue)
            cr.set_line_width(1)
            cr.rectangle(0.5, ymin + 0.5, rect.width - 1, yh - 1)
            cr.stroke()

    # returns the maximum valid offset for a cursor position
    # cursors cannot be moved to the right of line ending characters
    def getMaxCharPosition(self, i):
        return len_minus_line_ending(self.getLineText(self.current_pane, i))

    # 'enter_align_mode' keybinding action
    def _line_mode_enter_align_mode(self):
        if self.mode == Mode.CHAR:
            self._im_focus_out()
            self.im_context.reset()
            self._im_set_preedit(None)
        self.mode = Mode.ALIGN
        self.selection_line = self.current_line
        self.align_pane = self.current_pane
        self.align_line = self.current_line
        self.emit('mode_changed')
        self.dareas[self.align_pane].queue_draw()

    # 'first_line' keybinding action
    def _first_line(self):
        self.setCurrentLine(self.current_pane, 0)

    # 'extend_first_line' keybinding action
    def _extend_first_line(self):
        self.setCurrentLine(self.current_pane, 0, self.selection_line)

    # 'last_line' keybinding action
    def _last_line(self):
        f = self.current_pane
        self.setCurrentLine(f, len(self.panes[f].lines))

    # 'extend_last_line' keybinding action
    def _extend_last_line(self):
        f = self.current_pane
        self.setCurrentLine(f, len(self.panes[f].lines), self.selection_line)

    # 'up' keybinding action
    def _line_mode_up(self, selection=None):
        self.setCurrentLine(self.current_pane, self.current_line - 1, selection)

    # 'extend_up' keybinding action
    def _line_mode_extend_up(self):
        self._line_mode_up(self.selection_line)

    # 'down' keybinding action
    def _line_mode_down(self, selection=None):
        self.setCurrentLine(self.current_pane, self.current_line + 1, selection)

    # 'extend_down' keybinding action
    def _line_mode_extend_down(self):
        self._line_mode_down(self.selection_line)

    # 'left' keybinding action
    def _line_mode_left(self, selection=None):
        self.setCurrentLine(self.current_pane - 1, self.current_line, selection)

    # 'extend_left' keybinding action
    def _line_mode_extend_left(self):
        self._line_mode_left(self.selection_line)

    # 'right' keybinding action
    def _line_mode_right(self, selection=None):
        self.setCurrentLine(self.current_pane + 1, self.current_line, selection)

    # 'extend_right' keybinding action
    def _line_mode_extend_right(self):
        self._line_mode_right(self.selection_line)

    # 'page_up' keybinding action
    def _line_mode_page_up(self, selection=None):
        delta = int(self.vadj.get_page_size() // self.font_height)
        self.setCurrentLine(self.current_pane, self.current_line - delta, selection)

    # 'extend_page_up' keybinding action
    def _line_mode_extend_page_up(self):
        self._line_mode_page_up(self.selection_line)

    # 'page_down' keybinding action
    def _line_mode_page_down(self, selection=None):
        delta = int(self.vadj.get_page_size() // self.font_height)
        self.setCurrentLine(self.current_pane, self.current_line + delta, selection)

    # 'extend_page_down' keybinding action
    def _line_mode_extend_page_down(self):
        self._line_mode_page_down(self.selection_line)

    # 'delete_text' keybinding action
    def _delete_text(self):
        self.replaceText('')

    # 'enter_line_mode' keybinding action
    def _align_mode_enter_line_mode(self):
        self.selection_line = self.current_line
        self.setLineMode()

    # 'align' keybinding action
    def _align_text(self):
        f1 = self.align_pane
        line1 = self.align_line
        line2 = self.current_line
        self.selection_line = line2
        self.setLineMode()
        if self.current_pane == f1 + 1:
            self.align(f1, line1, line2)
        elif self.current_pane + 1 == f1:
            self.align(self.current_pane, line2, line1)

    # give the input method focus
    def _im_focus_in(self):
        if self.has_focus:
            self.im_context.focus_in()

    # remove input method focus
    def _im_focus_out(self):
        if self.has_focus:
            self.im_context.focus_out()

    # input method callback for committed text
    def im_commit_cb(self, im, s):
        if self.mode == Mode.CHAR:
            self.openUndoBlock()
            self.replaceText(s)
            self.closeUndoBlock()

    # update the cached preedit text
    def _im_set_preedit(self, p):
        self.im_preedit = p
        if self.mode == Mode.CHAR:
            f, i = self.current_pane, self.current_line
            self._queue_draw_lines(f, i)
            if f > 0:
                self._queue_draw_lines(f - 1, i)
            if f + 1 < len(self.panes):
                self._queue_draw_lines(f + 1, i)
        self.updateSize(False)

    # queue a redraw for location of preedit text
    def im_preedit_changed_cb(self, im):
        if self.mode == Mode.CHAR:
            s, a, c = self.im_context.get_preedit_string()
            if len(s) > 0:
                # we have preedit text, draw that instead
                p = (s, a, c)
            else:
                p = None
            self._im_set_preedit(p)
            self._ensure_cursor_is_visible()

    # callback to respond to retrieve_surrounding signals from input methods
    def im_retrieve_surrounding_cb(self, im):
        if self.mode == Mode.CHAR:
            # notify input method of text surrounding the cursor
            s = nullToEmpty(self.getLineText(self.current_pane, self.current_line))
            im.set_surrounding(s, len(s), self.current_char)

    # callback for 'focus_in_event'
    def focus_in_cb(self, widget, event):
        self.has_focus = True
        if self.mode == Mode.CHAR:
            # notify the input method of the focus change
            self._im_focus_in()

    # callback for 'focus_out_event'
    def focus_out_cb(self, widget, event):
        if self.mode == Mode.CHAR:
            # notify the input method of the focus change
            self._im_focus_out()
        self.has_focus = False

    # callback for keyboard events
    # only keypresses that are not handled by menu item accelerators reach here
    def key_press_cb(self, widget, event):
        if self.mode == Mode.CHAR:
            # update input method
            if self.im_context.filter_keypress(event):
                return True
        retval = False
        # determine the modified keys used
        mask = event.state & (Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK)
        if event.state & Gdk.ModifierType.LOCK_MASK:
            mask ^= Gdk.ModifierType.SHIFT_MASK
        self.openUndoBlock()
        if self.mode == Mode.LINE:
            # check if the keyval matches a line mode action
            action = self.resources.getActionForKey('line_mode', event.keyval, mask)
            if action in self._line_mode_actions:
                self._line_mode_actions[action]()
                retval = True
        elif self.mode == Mode.CHAR:
            f = self.current_pane
            if event.state & Gdk.ModifierType.SHIFT_MASK:
                si, sj = self.selection_line, self.selection_char
            else:
                si, sj = None, None
            is_ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
            retval = True
            # check if the keyval matches a character mode action
            action = self.resources.getActionForKey('character_mode', event.keyval, mask)
            if action in self._character_mode_actions:
                self._character_mode_actions[action]()
            # allow CTRL-Tab for widget navigation
            elif event.keyval == Gdk.KEY_Tab and event.state & Gdk.ModifierType.CONTROL_MASK:
                retval = False
            # up/down cursor navigation
            elif event.keyval in [ Gdk.KEY_Up, Gdk.KEY_Down, Gdk.KEY_Page_Up, Gdk.KEY_Page_Down ]:
                i = self.current_line
                # move back to the remembered cursor column if possible
                col = self.cursor_column
                if col < 0:
                    # find the current cursor column
                    s = nullToEmpty(self.getLineText(f, i))[:self.current_char]
                    col = self.stringWidth(s)
                if event.keyval in [ Gdk.KEY_Up, Gdk.KEY_Down ]:
                    delta = 1
                else:
                    delta = int(self.vadj.get_page_size() // self.font_height)
                if event.keyval in [ Gdk.KEY_Up, Gdk.KEY_Page_Up ]:
                    delta = -delta
                i += delta
                j = 0
                nlines = len(self.panes[f].lines)
                if i < 0:
                    i = 0
                elif i > nlines:
                    i = nlines
                else:
                    # move the cursor to column 'col' if possible
                    s = self.getLineText(f, i)
                    if s is not None:
                        s = strip_eol(s)
                        idx = 0
                        for c in s:
                            w = self.characterWidth(idx, c)
                            if idx + w > col:
                                break
                            idx += w
                            j += 1
                self.setCurrentChar(i, j, si, sj)
                self.cursor_column = col
            # home key
            elif event.keyval == Gdk.KEY_Home:
                if is_ctrl:
                    i = 0
                else:
                    i = self.current_line
                self.setCurrentChar(i, 0, si, sj)
            # end key
            elif event.keyval == Gdk.KEY_End:
                if is_ctrl:
                    i = len(self.panes[f].lines)
                    j = 0
                else:
                    i = self.current_line
                    j = self.getMaxCharPosition(i)
                self.setCurrentChar(i, j, si, sj)
            # cursor left and cursor right navigation
            elif event.keyval == Gdk.KEY_Left or event.keyval == Gdk.KEY_Right:
                i = self.current_line
                j = self.current_char
                while True:
                    if event.keyval == Gdk.KEY_Left:
                        if j > 0:
                            j -= 1
                        elif i > 0:
                            i -= 1
                            j = self.getMaxCharPosition(i)
                        else:
                            break
                    else:
                        if j < self.getMaxCharPosition(i):
                            j += 1
                        elif i < len(self.panes[f].lines):
                            i += 1
                            j = 0
                        else:
                            break
                    if event.state & Gdk.ModifierType.CONTROL_MASK == 0:
                        break
                    # break if we are at the beginning of a word
                    text = self.getLineText(f, i)
                    if text is not None and j < len(text):
                        c = getCharacterClass(text[j])
                        if c != WHITESPACE_CLASS and (j < 1 or j - 1 >= len(text) or getCharacterClass(text[j - 1]) != c):
                            break
                self.setCurrentChar(i, j, si, sj)
            # backspace
            elif event.keyval == Gdk.KEY_BackSpace:
                s = ''
                i = self.current_line
                j = self.current_char
                if self.selection_line == i and self.selection_char == j:
                    if j > 0:
                        # delete back to the last soft-tab location if there
                        # are only spaces and tabs from the beginning of the
                        # line to the current cursor position
                        text = self.getLineText(f, i)[:j]
                        for c in text:
                            if c not in ' \t':
                                j -= 1
                                break
                        else:
                            w = self.stringWidth(text)
                            width = self.prefs.getInt('editor_soft_tab_width')
                            w = (w - 1) // width * width
                            if self.prefs.getBool('editor_expand_tabs'):
                                s = ' ' * w
                            else:
                                width = self.prefs.getInt('display_tab_width')
                                s = '\t' * (w // width) + ' ' * (w % width)
                            j = 0
                    else:
                        # delete back to an end of line character from the
                        # previous line
                        while i > 0:
                            i -= 1
                            text = self.getLineText(f, i)
                            if text is not None:
                                j = self.getMaxCharPosition(i)
                                break
                    self.current_line = i
                    self.current_char = j
                self.replaceText(s)
            # delete key
            elif event.keyval == Gdk.KEY_Delete:
                i = self.current_line
                j = self.current_char
                if self.selection_line == i and self.selection_char == j:
                    # advance the selection to the next character so we can
                    # delete it
                    text = self.getLineText(f, i)
                    while text is None and i < len(self.panes[f].lines):
                        i += 1
                        j = 0
                        text = self.getLineText(f, i)
                    if text is not None:
                        if j < self.getMaxCharPosition(i):
                            j += 1
                        else:
                            i += 1
                            j = 0
                    self.current_line = i
                    self.current_char = j
                self.replaceText('')
            # return key, add the platform specific end of line characters
            elif event.keyval in [ Gdk.KEY_Return, Gdk.KEY_KP_Enter ]:
                s = os.linesep
                if self.prefs.getBool('editor_auto_indent'):
                    start_i, start_j = self.selection_line, self.selection_char
                    end_i, end_j = self.current_line, self.current_char
                    if end_i < start_i or (end_i == start_i and end_j < start_j):
                        start_i, start_j = end_i, end_j
                    if start_j > 0:
                        j, text = 0, self.getLineText(f, start_i)
                        while j < start_j and text[j] in ' \t':
                            j += 1
                        w = self.stringWidth(text[:j])
                        if self.prefs.getBool('editor_expand_tabs'):
                            # convert to spaces
                            s += ' ' * w
                        else:
                            tab_width = self.prefs.getInt('display_tab_width')
                            # replace with tab characters where possible
                            s += '\t' * (w // tab_width)
                            s += ' ' * (w % tab_width)
                self.replaceText(s)
            # insert key
            elif event.keyval in [ Gdk.KEY_Tab, Gdk.KEY_ISO_Left_Tab ]:
                start_i, start_j = self.selection_line, self.selection_char
                end_i, end_j = self.current_line, self.current_char
                if start_i != end_i or start_j != end_j or event.keyval == Gdk.KEY_ISO_Left_Tab:
                    # find range of lines to operate upon
                    start, end, offset = start_i, end_i, 1
                    if end < start:
                        start, end = end, start
                    if event.keyval == Gdk.KEY_ISO_Left_Tab:
                        offset = -1
                    self.recordEditMode()
                    for i in range(start, end + 1):
                        text = self.getLineText(f, i)
                        if text is not None and len_minus_line_ending(text) > 0:
                            # count spacing before the first non-whitespace character
                            j, w = 0, 0
                            while j < len(text) and text[j] in ' \t':
                                w += self.characterWidth(w, text[j])
                                j += 1
                            # adjust by a multiple of the soft tab width
                            ws = max(0, w + offset * self.prefs.getInt('editor_soft_tab_width'))
                            if ws != w:
                                if self.prefs.getBool('editor_expand_tabs'):
                                    s = ' ' * ws
                                else:
                                    tab_width = self.prefs.getInt('display_tab_width')
                                    s = '\t' * (ws // tab_width) + ' ' * (ws % tab_width)
                                if i == start_i:
                                    start_j = len(s) + max(0, start_j - j)
                                if i == end_i:
                                    end_j = len(s) + max(0, end_j - j)
                                self.updateText(f, i, s + text[j:])
                    self.setCurrentChar(end_i, end_j, start_i, start_j)
                    self.recordEditMode()
                else:
                    # insert soft-tabs if there are only spaces and tabs from the
                    # beginning of the line to the cursor location
                    if end_i < start_i or (end_i == start_i and end_j < start_j):
                        start_i, start_j, end_i, end_j = end_i, end_j, start_i, start_j
                    temp = start_j
                    if temp > 0:
                        text = self.getLineText(f, start_i)[:start_j]
                        w = self.stringWidth(text)
                        while temp > 0 and text[temp - 1] in ' \t':
                            temp -= 1
                    else:
                        w = 0
                    tab_width = self.prefs.getInt('display_tab_width')
                    if temp > 0:
                        # insert a regular tab
                        ws = tab_width - w % tab_width
                    else:
                        # insert a soft tab
                        self.selection_line = start_i
                        self.selection_char = 0
                        self.current_line = end_i
                        self.current_char = end_j
                        width = self.prefs.getInt('editor_soft_tab_width')
                        ws = w + width - w % width
                        w = 0
                    if self.prefs.getBool('editor_expand_tabs'):
                        # convert to spaces
                        s = ' ' * ws
                    else:
                        # replace with tab characters where possible
                        s = '\t' * ((w + ws) // tab_width - w // tab_width)
                        s += ' ' * ((w + ws) % tab_width)
                    self.replaceText(s)
            # handle all other printable characters
            elif len(event.string) > 0:
                self.replaceText(event.string)
        elif self.mode == Mode.ALIGN:
            # check if the keyval matches an align mode action
            action = self.resources.getActionForKey('align_mode', event.keyval, mask)
            if action in self._align_mode_actions:
                self._align_mode_actions[action]()
                retval = True
        self.closeUndoBlock()
        return retval

    # 'copy' action
    def copy(self):
        if self.mode == Mode.LINE or self.mode == Mode.CHAR:
            self.__set_clipboard_text(Gdk.SELECTION_CLIPBOARD, self.getSelectedText())

    # 'cut' action
    def cut(self):
        if self.mode == Mode.LINE or self.mode == Mode.CHAR:
            self.copy()
            self.replaceText('')

    # callback used when receiving clipboard text
    def receive_clipboard_text_cb(self, clipboard, text, data):
        if self.mode == Mode.LINE or self.mode == Mode.CHAR:
            # there is no guarantee this will be called before finishing
            # Gtk.Clipboard.get so we may need to create our own undo block
            needs_block = (self.undoblock is None)
            if needs_block:
                self.openUndoBlock()
            self.replaceText(nullToEmpty(text))
            if needs_block:
                self.closeUndoBlock()

    # 'paste' action
    def paste(self):
         Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).request_text(self.receive_clipboard_text_cb, None)

    # 'clear_edits' action
    def clear_edits(self):
        self.setLineMode()
        self.recordEditMode()
        f = self.current_pane
        start, end = self.selection_line, self.current_line
        if end < start:
            start, end = end, start
        end = min(end + 1, len(self.panes[0].lines))
        for i in range(start, end):
            line = self.getLine(f, i)
            if line is not None and line.is_modified:
                # remove the edits to the line
                self.updateText(f, i, None, False)
                if line.text is None:
                    # remove the line so it doesn't persist as a spacer
                    self.instanceLine(f, i, True)
        self.recordEditMode()

    # 'dismiss_all_edits' action
    def dismiss_all_edits(self):
        if self.mode == Mode.LINE or self.mode == Mode.CHAR:
            self.bakeEdits(self.current_pane)

    # callback for find menu item
    def find(self, pattern, match_case, backwards, from_start):
        self.setCharMode()
        # determine where to start searching from
        f = self.current_pane
        nlines = len(self.panes[f].lines)
        i, j = self.current_line, self.current_char
        si, sj = self.selection_line, self.selection_char
        if backwards:
            if from_start:
                i, j = nlines, 0
            elif si < i or (i == si and sj < j):
                i, j = si, sj
        else:
            if from_start:
                i, j = 0, 0
            elif i < si or (i == si and j < sj):
                i, j = si, sj

        if not match_case:
            pattern = pattern.upper()

        # iterate over all valid lines
        while i < nlines + 1:
            text = self.getLineText(f, i)
            if text is not None:
                if not match_case:
                    text = text.upper()
                # search for pattern
                if backwards:
                    idx = text.rfind(pattern, 0, j)
                else:
                    idx = text.find(pattern, j)
                if idx >= 0:
                    # we found a match
                    end = idx + len(pattern)
                    if backwards:
                        idx, end = end, idx
                    self.setCurrentChar(i, end, i, idx)
                    return True
            # advance
            if backwards:
                if i == 0:
                    break
                i -= 1
                text = self.getLineText(f, i)
                if text is None:
                    j = 0
                else:
                    j = len(text)
            else:
                i += 1
                j = 0
        # we have reached the end without finding a match
        return False

    # move cursor to a given line
    def go_to_line(self, i):
        f, idx = self.current_pane, 0
        if i > 0:
            # search for a line matching that number
            # we want to leave the cursor at the end of the file
            # if 'i' is greater than the last numbered line
            lines = self.panes[f].lines
            while idx < len(lines):
                line = lines[idx]
                if line is not None and line.line_number == i:
                    break
                idx += 1
        # select the line and make sure it is visible
        self.setLineMode()
        self.centre_view_about_y((idx + 0.5) * self.font_height)
        self.setCurrentLine(f, idx)

    # recompute viewport size and redraw as the display preferences may have
    # changed
    def prefsUpdated(self):
        # clear cache as tab width may have changed
        self.string_width_cache = {}
        self.setFont(Pango.FontDescription.from_string(self.prefs.getString('display_font')))
        # update preedit text
        self._cursor_position_changed(True)

        for pane in self.panes:
            del pane.diff_cache[:]
        # tab width may have changed
        self.emit('cursor_changed')
        for darea in self.dareas:
            darea.queue_draw()
        self.diffmap_cache = None
        self.diffmap.queue_draw()

    # 'realign_all' action
    def realign_all(self):
        self.setLineMode()
        f = self.current_pane
        self.recordEditMode()
        lines = []
        blocks = []
        for pane in self.panes:
            # create a new list of lines with no spacers
            newlines = [ [ line for line in pane.lines if line is not None ] ]
            newblocks = createBlock(len(newlines[0]))
            if len(lines) > 0:
                # match with neighbour to the left
                self.alignBlocks(blocks, lines, newblocks, newlines)
                blocks = mergeBlocks(blocks, newblocks)
            else:
                blocks = newblocks
            lines.extend(newlines)
        self.updateAlignment(0, len(self.panes[f].lines), lines)
        self.updateBlocks(blocks)
        self.setCurrentLine(f, min(self.current_line, len(self.panes[f].lines)))
        self.recordEditMode()

    # callback for the align with selection menu item
    def align_with_selection_cb(self, widget, data):
        self.setLineMode()
        self.openUndoBlock()
        self.recordEditMode()
        # get the line and pane where the user right clicked
        f, line1 = data
        f2 = self.current_pane
        line2 = self.current_line
        if f2 < f:
            f = f2
            line1, line2 = line2, line1
        self.align(f, line1, line2)
        self.recordEditMode()
        self.closeUndoBlock()

    # 'isolate' action
    def isolate(self):
        self.setLineMode()
        self.recordEditMode()
        f = self.current_pane
        start, end = self.selection_line, self.current_line
        if end < start:
            start, end = end, start
        end += 1
        nlines = len(self.panes[f].lines)
        end = min(end, nlines)
        n = end - start
        if n > 0:
            lines = [ pane.lines[start:end] for pane in self.panes ]
            space = [ n * [ None ] for pane in self.panes ]
            lines[f], space[f] = space[f], lines[f]

            pre, post = cutBlocks(end, self.blocks)
            pre, middle = cutBlocks(start, pre)

            # remove nulls
            b = createBlock(n)
            removeNullLines(b, space)
            end = start + sum(b)
            if end > start:
                end -= 1
            removeNullLines(middle, lines)

            for s, line in zip(space, lines):
                s.extend(line)

            # update lines and blocks
            self.updateAlignment(start, n, space)
            pre.extend(b)
            pre.extend(middle)
            pre.extend(post)
            self.updateBlocks(pre)
            self.removeSpacerLines(end, sum(middle))
            end -= self.removeSpacerLines(start, sum(b))
            self.setCurrentLine(f, end, start)
        self.recordEditMode()

    # returns True if line 'i' in pane 'f' has an edit or is different from its
    # neighbour
    def hasEditsOrDifference(self, f, i):
        line = self.getLine(f, i)
        if line is not None and line.is_modified:
            return True
        text = self.getCompareString(f, i)
        return (f > 0 and self.getCompareString(f - 1, i) != text) or (f + 1 < len(self.panes) and text != self.getCompareString(f + 1, i))

    # returns True if there are any differences
    def hasDifferences(self):
        n = len(self.panes)
        nlines = len(self.panes[0].lines)
        for i in range(nlines):
            text = self.getCompareString(0, i)
            for f in range(1, n):
                if self.getCompareString(f, i) != text:
                    return True
        return False

    # scroll the viewport so pixels at position 'y' are centred
    def centre_view_about_y(self, y):
        vadj = self.vadj
        y = min(max(0, y - vadj.get_page_size() / 2), vadj.get_upper() - vadj.get_page_size())
        vadj.set_value(y)

    # move the cursor from line 'i' to the next difference in direction 'delta'
    def go_to_difference(self, i, delta):
        f = self.current_pane
        nlines = len(self.panes[f].lines)
        # back up to beginning of difference
        if i >= 0 and i <= nlines:
            while self.hasEditsOrDifference(f, i):
                i2 = i - delta
                if i2 < 0 or i2 > nlines:
                    break
                i = i2
        # step over non-difference
        while i >= 0 and i <= nlines and not self.hasEditsOrDifference(f, i):
            i += delta
        # find extent of difference
        if i >= 0 and i <= nlines:
            start = i
            while i >= 0 and i <= nlines and self.hasEditsOrDifference(f, i):
                i += delta
            i -= delta
            if i < start:
                start, i = i, start
            # centre the view on the selection
            self.centre_view_about_y((start + i) * self.font_height / 2)
            self.setCurrentLine(f, start, i)

    # 'first_difference' action
    def first_difference(self):
        self.setLineMode()
        self.go_to_difference(0, 1)

    # 'previous_difference' action
    def previous_difference(self):
        self.setLineMode()
        i = min(self.current_line, self.selection_line) - 1
        self.go_to_difference(i, -1)

    # 'next_difference' action
    def next_difference(self):
        self.setLineMode()
        i = max(self.current_line, self.selection_line) + 1
        self.go_to_difference(i, 1)

    # 'last_difference' action
    def last_difference(self):
        self.setLineMode()
        i = len(self.panes[self.current_pane].lines)
        self.go_to_difference(i, -1)

    # swap the contents of two panes
    def swapPanes(self, f_dst, f_src):
        if self.undoblock is not None:
            self.addUndo(SwapPanesUndo(f_dst, f_src))
        self.current_pane = f_dst
        f0 = self.panes[f_dst]
        f1 = self.panes[f_src]
        self.panes[f_dst], self.panes[f_src] = f1, f0
        npanes = len(self.panes)
        for f_idx in f_dst, f_src:
            for f in range(f_idx - 1, f_idx + 2):
                if f >= 0 and f < npanes:
                    # clear the diff cache and redraw as the pane has a new
                    # neighour
                    del self.panes[f].diff_cache[:]
                    self.dareas[f].queue_draw()
        # queue redraw
        self.diffmap_cache = None
        self.diffmap.queue_draw()
        self.emit('swapped_panes', f_dst, f_src)

    # swap the contents of two panes
    def swap_panes(self, f_dst, f_src):
        if f_dst >= 0 and f_dst < len(self.panes):
            if self.mode == Mode.ALIGN:
                self.setLineMode()
            self.recordEditMode()
            self.swapPanes(f_dst, f_src)
            self.recordEditMode()

    # callback for swap panes menu item
    def swap_panes_cb(self, widget, data):
        self.openUndoBlock()
        self.swap_panes(data, self.current_pane)
        self.closeUndoBlock()

    # 'shift_pane_left' action
    def shift_pane_left(self):
        f = self.current_pane
        self.swap_panes(f - 1, f)

    # 'shift_pane_right' action
    def shift_pane_right(self):
        f = self.current_pane
        self.swap_panes(f + 1, f)

    # 'convert_to_upper_case' action
    def _convert_case(self, to_upper):
        # find range of characters to operate upon
        if self.mode == Mode.CHAR:
            start, end = self.current_line, self.selection_line
            j0, j1 = self.current_char, self.selection_char
            if end < start or (start == end and j1 < j0):
                start, j0, end, j1 = end, j1, start, j0
        else:
            self.setLineMode()
            start, end = self.current_line, self.selection_line
            if end < start:
                start, end = end, start
            end += 1
            j0, j1 = 0, 0
        self.recordEditMode()
        f = self.current_pane
        for i in range(start, end + 1):
            text = self.getLineText(f, i)
            if text is not None:
                s = text
                # skip characters after the selection
                if i == end:
                    s, post = s[:j1], s[j1:]
                else:
                    post = ''
                # skip characters before the selection
                if i == start:
                    pre, s = s[:j0], s[j0:]
                else:
                    pre = ''
                # change the case
                if to_upper:
                    s = s.upper()
                else:
                    s = s.lower()
                s = ''.join([pre, s, post])
                # only update the line if it changed
                if s != text:
                    self.updateText(f, i, s)

    # 'convert_to_upper_case' action
    def convert_to_upper_case(self):
        self._convert_case(True)

    # 'convert_to_lower_case' action
    def convert_to_lower_case(self):
        self._convert_case(False)

    # sort lines
    def _sort_lines(self, descending):
        if self.mode != Mode.CHAR:
            self.setLineMode()
        self.recordEditMode()
        f = self.current_pane
        # find cursor range
        start, end = self.selection_line, self.current_line
        if end < start:
            start, end = end, start
        # get set of lines
        ss = [ self.getLineText(f, i) for i in range(start, end + 1) ]
        # create sorted list, removing any nulls
        temp = [ s for s in ss if s is not None ]
        temp.sort()
        if descending:
            temp.reverse()
        # add back in the nulls
        temp.extend((len(ss) - len(temp)) * [ None ])
        for i, s in enumerate(temp):
            # update line if it changed
            if ss[i] != s:
                self.updateText(f, start + i, s)
        if self.mode == Mode.CHAR:
            # ensure the cursor position is valid
            self.setCurrentChar(self.current_line, 0, self.selection_line, 0)
        self.recordEditMode()

    # 'sort_lines_in_ascending_order' action
    def sort_lines_in_ascending_order(self):
        self._sort_lines(False)

    # 'sort_lines_in_descending_order' action
    def sort_lines_in_descending_order(self):
        self._sort_lines(True)

    # 'remove_trailing_white_space' action
    def remove_trailing_white_space(self):
        if self.mode != Mode.CHAR:
            self.setLineMode()
        self.recordEditMode()
        f = self.current_pane
        # find cursor range
        start, end = self.selection_line, self.current_line
        if end < start:
            start, end = end, start
        # get set of lines
        for i in range(start, end + 1):
            text = self.getLineText(f, i)
            if text is not None:
                # locate trailing whitespace
                old_n = n = len_minus_line_ending(text)
                while n > 0 and text[n - 1] in whitespace:
                    n -= 1
                # update line if it changed
                if n < old_n:
                    self.updateText(f, i, text[:n] + text[old_n:])
        if self.mode == Mode.CHAR:
            # ensure the cursor position is valid
            self.setCurrentChar(self.current_line, 0, self.selection_line, 0)
        self.recordEditMode()

    # 'convert_tabs_to_spaces' action
    def convert_tabs_to_spaces(self):
        # find range of characters to operate upon
        if self.mode == Mode.CHAR:
            start, end = self.current_line, self.selection_line
            j0, j1 = self.current_char, self.selection_char
            if end < start or (start == end and j1 < j0):
                start, j0, end, j1 = end, j1, start, j0
        else:
            self.setLineMode()
            start, end = self.current_line, self.selection_line
            if end < start:
                start, end = end, start
            end += 1
            j0, j1 = 0, 0
        self.recordEditMode()
        f = self.current_pane
        for i in range(start, end + 1):
            text = self.getLineText(f, i)
            if text is not None:
                # expand tabs
                ss, col = [], 0
                for c in text:
                    w = self.characterWidth(col, c)
                    # replace tab with spaces
                    if c == '\t':
                        c = w * ' '
                    ss.append(c)
                    col += w
                # determine the range of interest
                if i == start:
                    k0 = j0
                else:
                    k0 = 0
                if i == end:
                    k1 = j1
                else:
                    k1 = len(ss)
                # compute leading and converted text
                s = text[:k0] + ''.join(ss[k0:k1])
                if i == end:
                    # update the end cursor location
                    j1 = len(s)
                # append the trailing text
                s += text[k1:]
                # update line only if it changed
                if text != s:
                    self.updateText(f, i, s)
        if self.mode == Mode.CHAR:
            # ensure the cursor position is valid
            self.setCurrentChar(end, j1, start, j0)
        self.recordEditMode()

    # 'convert_leading_spaces_to_tabs' action
    def convert_leading_spaces_to_tabs(self):
        if self.mode != Mode.CHAR:
            self.setLineMode()
        self.recordEditMode()
        f = self.current_pane
        tab_width = self.prefs.getInt('display_tab_width')
        # find cursor range
        start, end = self.selection_line, self.current_line
        if end < start:
            start, end = end, start
        for i in range(start, end + 1):
            text = self.getLineText(f, i)
            if text is not None:
                # find leading white space
                j, col = 0, 0
                while j < len(text) and text[j] in ' \t':
                    col += self.characterWidth(col, text[j])
                    j += 1
                if col >= tab_width:
                    # convert to tabs
                    s = ''.join([ '\t' * (col // tab_width), ' ' * (col % tab_width), text[j:] ])
                    # update line only if it changed
                    if text != s:
                        self.updateText(f, i, s)
        if self.mode == Mode.CHAR:
            # ensure the cursor position is valid
            self.setCurrentChar(self.current_line, 0, self.selection_line, 0)
        self.recordEditMode()

    # adjust indenting of the selected lines by 'offset' soft tabs
    def _adjust_indenting(self, offset):
        if self.mode != Mode.CHAR:
            self.setLineMode()
        # find range of lines to operate upon
        f = self.current_pane
        start, end = self.selection_line, self.current_line
        if end < start:
            start, end = end, start

        self.recordEditMode()
        for i in range(start, end + 1):
            text = self.getLineText(f, i)
            if text is not None and len_minus_line_ending(text) > 0:
                # count spacing before the first non-whitespace character
                j, w = 0, 0
                while j < len(text) and text[j] in ' \t':
                    w += self.characterWidth(w, text[j])
                    j += 1
                # adjust by a multiple of the soft tab width
                ws = max(0, w + offset * self.prefs.getInt('editor_soft_tab_width'))
                if ws != w:
                    if self.prefs.getBool('editor_expand_tabs'):
                        s = ' ' * ws
                    else:
                        tab_width = self.prefs.getInt('display_tab_width')
                        s = '\t' * (ws // tab_width) + ' ' * (ws % tab_width)
                    self.updateText(f, i, s + text[j:])
        if self.mode == Mode.CHAR:
            # ensure the cursor position is valid
            self.setCurrentChar(self.current_line, 0, self.selection_line, 0)
        self.recordEditMode()

    # 'increase_indenting' action
    def increase_indenting(self):
        self._adjust_indenting(1)

    # 'decrease_indenting' action
    def decrease_indenting(self):
        self._adjust_indenting(-1)

    def convert_format(self, format):
        self.setLineMode()
        self.recordEditMode()
        f = self.current_pane
        for i in range(len(self.panes[f].lines)):
            text = self.getLineText(f, i)
            s = convert_to_format(text, format)
            # only modify lines that actually change
            if s != text:
                self.updateText(f, i, s)
        self.setFormat(f, format)

    # 'convert_to_dos' action
    def convert_to_dos(self):
        self.convert_format(Format.DOS)

    # 'convert_to_mac' action
    def convert_to_mac(self):
        self.convert_format(Format.MAC)

    # 'convert_to_unix' action
    def convert_to_unix(self):
        self.convert_format(Format.UNIX)

    # copies the selected range of lines from pane 'f_src' to 'f_dst'
    def merge_lines(self, f_dst, f_src):
        self.recordEditMode()
        self.setLineMode()
        pane = self.panes[f_dst]
        start, end = self.selection_line, self.current_line
        if end < start:
            start, end = end, start
        end = min(end + 1, len(pane.lines))
        ss = [ self.getLineText(f_src, i) for i in range(start, end) ]
        if pane.format == 0:
            # copy the format of the source pane if the format for the
            # destination pane as not yet been determined
            self.setFormat(f_dst, getFormat(ss))
        for i, s in enumerate(ss):
            self.updateText(f_dst, start + i, convert_to_format(s, pane.format))
        n = len(ss)
        delta = min(self.removeSpacerLines(start, n), n - 1)
        if self.selection_line > start:
            self.selection_line -= delta
        if self.current_line > start:
            self.current_line -= delta
        self.recordEditMode()

    # callback for merge lines menu item
    def merge_lines_cb(self, widget, data):
        self.openUndoBlock()
        self.merge_lines(data, self.current_pane)
        self.closeUndoBlock()

    # 'copy_selection_right' action
    def copy_selection_right(self):
        f = self.current_pane + 1
        if f > 0 and f < len(self.panes):
            self.merge_lines(f, f - 1)

    # 'copy_selection_left' action
    def copy_selection_left(self):
        f = self.current_pane - 1
        if f >= 0 and f + 1 < len(self.panes):
            self.merge_lines(f, f + 1)

    # 'copy_left_into_selection' action
    def copy_left_into_selection(self):
        f = self.current_pane
        if f > 0 and f < len(self.panes):
            self.merge_lines(f, f - 1)

    # 'copy_right_into_selection' action
    def copy_right_into_selection(self):
        f = self.current_pane
        if f >= 0 and f + 1 < len(self.panes):
            self.merge_lines(f, f + 1)

    # merge from both left and right into the current pane
    def _mergeBoth(self, right_first):
        self.recordEditMode()
        self.setLineMode()
        f = self.current_pane
        start, end = self.selection_line, self.current_line
        if end < start:
            start, end = end, start
        end += 1
        npanes = len(self.panes)
        nlines = len(self.panes[f].lines)
        end = min(end, nlines)
        n = end - start
        if n > 0:
            lines = [ pane.lines[start:end] for pane in self.panes ]
            spaces = [ n * [ None ] for pane in self.panes ]
            old_content = [ line for line in lines[f] if line is not None ]
            for i in range(f + 1, npanes):
                lines[i], spaces[i] = spaces[i], lines[i]
            # replace f's lines with merge content
            if f > 0:
                lines[f] = lines[f - 1][:]
            else:
                lines[f] = n * [ None ]
            if f + 1 < npanes:
                spaces[f] = spaces[f + 1][:]
            else:
                spaces[f] = n * [ None ]
            if right_first:
                lines, spaces = spaces, lines

            pre, post = cutBlocks(end, self.blocks)
            pre, b = cutBlocks(start, pre)

            #  join and remove null lines
            b.extend(b)
            for l, s in zip(lines, spaces):
                l.extend(s)
            removeNullLines(b, lines)

            # replace f's lines with original, growing if necessary
            new_content = lines[f]
            new_n = len(new_content)
            lines[f] = old_content
            min_n = len(old_content)

            delta = new_n - min_n
            if delta < 0:
                delta = -delta
                for i in range(npanes):
                    if i != f:
                        lines[i].extend(delta * [ None ])
                # grow last block
                if len(b) > 0:
                    b[-1] += delta
                else:
                    b = createBlock(delta)
            elif delta > 0:
                old_content.extend(delta * [ None ])
                new_n = len(old_content)

            # update lines and blocks
            self.updateAlignment(start, n, lines)
            pre.extend(b)
            pre.extend(post)
            self.updateBlocks(pre)

            for i in range(new_n):
                s = None
                if i < len(new_content):
                    line = new_content[i]
                    if line is not None:
                        s = line.getText()
                self.updateText(f, start + i, s)

            # update selection
            end = start + new_n
            if end > start:
                end -= 1
            self.setCurrentLine(f, end, start)
        self.recordEditMode()

    # 'merge_from_left_then_right' keybinding action
    def merge_from_left_then_right(self):
        self._mergeBoth(False)

    # 'merge_from_right_then_left' keybinding action
    def merge_from_right_then_left(self):
        self._mergeBoth(True)
