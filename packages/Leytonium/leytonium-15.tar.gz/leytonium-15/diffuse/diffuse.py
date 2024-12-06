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

'Compare an arbitrary number of text files.'
from .girepo import Gdk, GdkPixbuf, GObject, Gtk, Pango
from .main import main
from .preferences import Preferences
from .ui import createMenu, EncodingMenu, MessageDialog
from .util import APP_NAME, bin_dir, Format, isWindows, lang, logDebug, Mode, readlines, splitlines, VERSION, WEBSITE
from .viewer.viewer import FileDiffViewer
from gettext import gettext as _
from urllib.parse import urlparse
import codecs, os, shlex, stat, webbrowser

# convenience method for creating a menu bar according to a template
def createMenuBar(resources, specs, radio, accel_group):
    menu_bar = Gtk.MenuBar.new()
    for label, spec in specs:
        menu = Gtk.MenuItem.new_with_mnemonic(label)
        menu.set_submenu(createMenu(resources, spec, radio, accel_group))
        menu.set_use_underline(True)
        menu.show()
        menu_bar.append(menu)
    return menu_bar

# convenience method for packing buttons into a container according to a
# template
def appendButtons(box, size, specs):
    for spec in specs:
        if len(spec) > 0:
            button = Gtk.Button.new()
            button.set_relief(Gtk.ReliefStyle.NONE)
            button.set_can_focus(False)
            image = Gtk.Image.new()
            image.set_from_stock(spec[0], size)
            button.add(image)
            image.show()
            if len(spec) > 2:
                button.connect('clicked', spec[1], spec[2])
                if len(spec) > 3:
                    button.set_tooltip_text(spec[3])
            box.pack_start(button, False, False, 0)
            button.show()
        else:
            separator = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
            box.pack_start(separator, False, False, 5)
            separator.show()

# constructs a full URL for the named file
def path2url(path, proto='file'):
    r = [ proto, ':///' ]
    s = os.path.abspath(path)
    i = 0
    while i < len(s) and s[i] == os.sep:
        i += 1
    for c in s[i:]:
        if c == os.sep:
            c = '/'
        elif c == ':' and isWindows:
            c = '|'
        else:
            v = ord(c)
            if v <= 0x20 or v >= 0x7b or c in '$&+,/:;=?@"<>#%\\^[]`':
                c = '%%%02X' % (v, )
        r.append(c)
    return ''.join(r)

# dialogue used to search for text
class SearchDialog(Gtk.Dialog):

    def __init__(self, parent, pattern=None, history=None):
        super().__init__(title=_('Find...'), parent=parent, destroy_with_parent=True)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)

        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        vbox.set_border_width(10)

        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        label = Gtk.Label.new(_('Search For: '))
        hbox.pack_start(label, False, False, 0)
        label.show()
        combo = Gtk.ComboBoxText.new_with_entry()
        self.entry = combo.get_child()
        self.entry.connect('activate', self.entry_cb)

        if pattern is not None:
            self.entry.set_text(pattern)

        if history is not None:
            completion = Gtk.EntryCompletion.new()
            liststore = Gtk.ListStore(GObject.TYPE_STRING)
            completion.set_model(liststore)
            completion.set_text_column(0)
            for h in history:
                liststore.append([h])
                combo.append_text(h)
            self.entry.set_completion(completion)

        hbox.pack_start(combo, True, True, 0)
        combo.show()
        vbox.pack_start(hbox, False, False, 0)
        hbox.show()

        button = Gtk.CheckButton.new_with_mnemonic(_('Match Case'))
        self.match_case_button = button
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = Gtk.CheckButton.new_with_mnemonic(_('Search Backwards'))
        self.backwards_button = button
        vbox.pack_start(button, False, False, 0)
        button.show()

        self.vbox.pack_start(vbox, False, False, 0) # pylint: disable=no-member
        vbox.show()

    # callback used when the Enter key is pressed
    def entry_cb(self, widget):
        self.response(Gtk.ResponseType.ACCEPT)

# convenience method to request confirmation when closing the last tab
def confirmTabClose(parent):
    dialog = MessageDialog(parent, Gtk.MessageType.WARNING, _('Closing this tab will quit %s.') % (APP_NAME, ))
    end = (dialog.run() == Gtk.ResponseType.OK)
    dialog.destroy()
    return end

# custom dialogue for picking files with widgets for specifying the encoding
# and revision
class FileChooserDialog(Gtk.FileChooserDialog):
    # record last chosen folder so the file chooser can start at a more useful
    # location for empty panes
    last_chosen_folder = os.path.realpath(os.curdir)

    def __current_folder_changed_cb(self, widget):
        FileChooserDialog.last_chosen_folder = widget.get_current_folder()

    def __init__(self, title, parent, prefs, action, accept, rev=False):
        super().__init__(title=title, parent=parent, action=action)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(accept, Gtk.ResponseType.OK)
        self.prefs = prefs
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        hbox.set_border_width(5)
        label = Gtk.Label.new(_('Encoding: '))
        hbox.pack_start(label, False, False, 0)
        label.show()
        self.encoding = entry = EncodingMenu(prefs, action in [ Gtk.FileChooserAction.OPEN, Gtk.FileChooserAction.SELECT_FOLDER ])
        hbox.pack_start(entry, False, False, 5)
        entry.show()
        if rev:
            self.revision = entry = Gtk.Entry.new()
            hbox.pack_end(entry, False, False, 0)
            entry.show()
            label = Gtk.Label.new(_('Revision: '))
            hbox.pack_end(label, False, False, 0)
            label.show()

        self.vbox.pack_start(hbox, False, False, 0) # pylint: disable=no-member
        hbox.show()
        self.set_current_folder(self.last_chosen_folder)
        self.connect('current-folder-changed', self.__current_folder_changed_cb)

    def set_encoding(self, encoding):
        self.encoding.set_text(encoding)

    def get_encoding(self):
        return self.encoding.get_text()

    def get_revision(self):
        return self.revision.get_text()

    def get_filename(self):
        # convert from UTF-8 string to unicode
        return Gtk.FileChooserDialog.get_filename(self)

# dialogue used to search for text
class NumericDialog(Gtk.Dialog):

    def __init__(self, parent, title, text, val, lower, upper, step=1, page=0):
        super().__init__(title=title, parent=parent, destroy_with_parent=True)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)

        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        vbox.set_border_width(10)

        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        label = Gtk.Label.new(text)
        hbox.pack_start(label, False, False, 0)
        label.show()
        adj = Gtk.Adjustment.new(val, lower, upper, step, page, 0)
        self.button = button = Gtk.SpinButton.new(adj, 1.0, 0)
        button.connect('activate', self.button_cb)
        hbox.pack_start(button, True, True, 0)
        button.show()

        vbox.pack_start(hbox, True, True, 0)
        hbox.show()

        self.vbox.pack_start(vbox, False, False, 0) # pylint: disable=no-member
        vbox.show()

    def button_cb(self, widget):
        self.response(Gtk.ResponseType.ACCEPT)

# the about dialogue
class AboutDialog(Gtk.AboutDialog):

    def __init__(self, copyright):
        super().__init__()
        self.set_logo_icon_name('diffuse')
        if hasattr(self, 'set_program_name'):
            # only available in pygtk >= 2.12
            self.set_program_name(APP_NAME)
        self.set_version(VERSION)
        self.set_comments(_('Diffuse is a graphical tool for merging and comparing text files.'))
        self.set_copyright(copyright)
        self.set_website(WEBSITE)
        self.set_authors([ 'Derrick Moser <derrick_moser@yahoo.com>',
                           'Romain Failliot <romain.failliot@foolstep.com>' ])
        self.set_translator_credits(_('translator-credits'))
        ss = [ APP_NAME + ' ' + VERSION + '\n',
               copyright + '\n\n',
               _("""This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the licence, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  You may also obtain a copy of the GNU General Public License from the Free Software Foundation by visiting their web site (http://www.fsf.org/) or by writing to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
""") ]
        self.set_license(''.join(ss))
        self.set_wrap_license(True)

# widget classed to create notebook tabs with labels and a close button
# use notebooktab.button.connect() to be notified when the button is pressed
# make this a Gtk.EventBox so signals can be connected for MMB and RMB button
# presses.
class NotebookTab(Gtk.EventBox):

    def __init__(self, name, stock):
        super().__init__()
        self.set_visible_window(False)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        if stock is not None:
            image = Gtk.Image.new()
            image.set_from_stock(stock, Gtk.IconSize.MENU)
            hbox.pack_start(image, False, False, 5)
            image.show()
        self.label = label = Gtk.Label.new(name)
        # left justify the widget
        label.set_xalign(0.0)
        label.set_yalign(0.5)
        hbox.pack_start(label, True, True, 0)
        label.show()
        self.button = button = Gtk.Button.new()
        button.set_relief(Gtk.ReliefStyle.NONE)
        image = Gtk.Image.new()
        image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        button.add(image)
        image.show()
        button.set_tooltip_text(_('Close Tab'))
        hbox.pack_start(button, False, False, 0)
        button.show()
        self.add(hbox)
        hbox.show()

    def get_text(self):
        return self.label.get_text()

    def set_text(self, s):
        self.label.set_text(s)

# contains information about a file
class FileInfo:
    def __init__(self, name=None, encoding=None, vcs=None, revision=None, label=None):
        # file name
        self.name = name
        # name of codec used to translate the file contents to unicode text
        self.encoding = encoding
        # the VCS object
        self.vcs = vcs
        # revision used to retrieve file from the VCS
        self.revision = revision
        # alternate text to display instead of the actual file name
        self.label = label
        # 'stat' for files read from disk -- used to warn about changes to the
        # file on disk before saving
        self.stat = None
        # most recent 'stat' for files read from disk -- used on focus change
        # to warn about changes to file on disk
        self.last_stat = None

# assign user specified labels to the corresponding files
def assign_file_labels(items, labels):
    new_items = []
    ss = labels[::-1]
    for name, data in items:
        if ss:
            s = ss.pop()
        else:
            s = None
        new_items.append((name, data, s))
    return new_items

# the main application class containing a set of file viewers
# this class displays tab for switching between viewers and dispatches menu
# commands to the current viewer
class Diffuse(Gtk.Window):
    # specialisation of FileDiffViewer for Diffuse
    class FileDiffViewer(FileDiffViewer):
        # pane header
        class PaneHeader(Gtk.Box):

            def __init__(self):
                super().__init__(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
                appendButtons(self, Gtk.IconSize.MENU, [
                   [ Gtk.STOCK_OPEN, self.button_cb, 'open', _('Open File...') ],
                   [ Gtk.STOCK_REFRESH, self.button_cb, 'reload', _('Reload File') ],
                   [ Gtk.STOCK_SAVE, self.button_cb, 'save', _('Save File') ],
                   [ Gtk.STOCK_SAVE_AS, self.button_cb, 'save_as', _('Save File As...') ] ])

                self.label = label = Gtk.Label.new()
                label.set_selectable(True)
                label.set_ellipsize(Pango.EllipsizeMode.START)
                label.set_max_width_chars(1)

                self.pack_start(label, True, True, 0)

                # file's name and information about how to retrieve it from a
                # VCS
                self.info = FileInfo()
                self.has_edits = False
                self.updateTitle()
                self.show_all()

            # callback for buttons
            def button_cb(self, widget, s):
                self.emit(s)

            # creates an appropriate title for the pane header
            def updateTitle(self):
                ss = []
                info = self.info
                if info.label is not None:
                    # show the provided label instead of the file name
                    ss.append(info.label)
                else:
                    if info.name is not None:
                        ss.append(info.name)
                    if info.revision is not None:
                        ss.append('(' + info.revision + ')')
                if self.has_edits:
                    ss.append('*')
                s = ' '.join(ss)
                self.label.set_text(s)
                self.label.set_tooltip_text(s)
                self.emit('title_changed')

            # set num edits
            def setEdits(self, has_edits):
                if self.has_edits != has_edits:
                    self.has_edits = has_edits
                    self.updateTitle()

        # pane footer
        class PaneFooter(Gtk.Box):

            def __init__(self):
                super().__init__(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
                self.cursor = label = Gtk.Label.new()
                self.cursor.set_size_request(-1, -1)
                self.pack_start(label, False, False, 0)

                separator = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
                self.pack_end(separator, False, False, 10)

                self.encoding = label = Gtk.Label.new()
                self.pack_end(label, False, False, 0)

                separator = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
                self.pack_end(separator, False, False, 10)

                self.format = label = Gtk.Label.new()
                self.pack_end(label, False, False, 0)

                separator = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
                self.pack_end(separator, False, False, 10)

                self.set_size_request(0, self.get_size_request()[1])
                self.show_all()

            # set the cursor label
            def updateCursor(self, viewer, f):
                if viewer.mode == Mode.CHAR and viewer.current_pane == f:
                    ## TODO: Find a fix for the column bug (resizing issue when editing a line)
                    #j = viewer.current_char
                    #if j > 0:
                    #    text = viewer.getLineText(viewer.current_pane, viewer.current_line)[:j]
                    #    j = viewer.stringWidth(text)
                    #s = _('Column %d') % (j, )
                    s = ''
                else:
                    s = ''
                self.cursor.set_text(s)

            # set the format label
            def setFormat(self, s):
                v = []
                if s & Format.DOS:
                    v.append('DOS')
                if s & Format.MAC:
                    v.append('Mac')
                if s & Format.UNIX:
                    v.append('Unix')
                self.format.set_text('/'.join(v))

            # set the format label
            def setEncoding(self, s):
                if s is None:
                    s = ''
                self.encoding.set_text(s)

        def __init__(self, resources, vcss, n, prefs, title):
            super().__init__(resources, n, prefs)
            self.title = title
            self.status = ''

            self.headers = []
            self.footers = []
            for i in range(n):
                # pane header
                w = self.PaneHeader()
                self.headers.append(w)
                self.attach(w, i, 0, 1, 1)
                w.connect('title-changed', self.title_changed_cb)
                w.connect('open', self.open_file_button_cb, i)
                w.connect('reload', self.reload_file_button_cb, i)
                w.connect('save', self.save_file_button_cb, i)
                w.connect('save-as', self.save_file_as_button_cb, i)
                w.show()
                # pane footer
                w = self.PaneFooter()
                self.footers.append(w)
                self.attach(w, i, 2, 1, 1)
                w.show()

            self.connect('swapped-panes', self.swapped_panes_cb)
            self.connect('num-edits-changed', self.num_edits_changed_cb)
            self.connect('mode-changed', self.mode_changed_cb)
            self.connect('cursor-changed', self.cursor_changed_cb)
            self.connect('format-changed', self.format_changed_cb)

            for i, darea in enumerate(self.dareas):
                darea.drag_dest_set(Gtk.DestDefaults.ALL, [ Gtk.TargetEntry.new('text/uri-list', 0, 0) ], Gdk.DragAction.COPY)
                darea.connect('drag-data-received', self.drag_data_received_cb, i)
            # initialise status
            self.updateStatus()
            self.vcss = vcss

        # convenience method to request confirmation before loading a file if
        # it will cause existing edits to be lost
        def loadFromInfo(self, f, info):
            if self.headers[f].has_edits:
                # warn users of any unsaved changes they might lose
                dialog = Gtk.MessageDialog(self.get_toplevel(), Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.WARNING, Gtk.ButtonsType.NONE, _('Save changes before loading the new file?'))
                dialog.set_title(APP_NAME)
                dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
                dialog.add_button(Gtk.STOCK_NO, Gtk.ResponseType.REJECT)
                dialog.add_button(Gtk.STOCK_YES, Gtk.ResponseType.OK)
                dialog.set_default_response(Gtk.ResponseType.CANCEL)
                response = dialog.run()
                dialog.destroy()
                if response == Gtk.ResponseType.OK:
                    # save the current pane contents
                    if not self.save_file(f):
                        # cancel if the save failed
                        return
                elif response != Gtk.ResponseType.REJECT:
                    # cancel if the user did not choose 'yes' or 'no'
                    return
            self.openUndoBlock()
            self.recordEditMode()
            self.load(f, info)
            self.recordEditMode()
            self.closeUndoBlock()

        # callback used when receiving drag-n-drop data
        def drag_data_received_cb(self, widget, context, x, y, selection, targettype, eventtime, f):
            # get uri list
            uris = selection.get_uris()
            # load the first valid file
            for uri in uris:
                path = urlparse(uri).path
                if os.path.isfile(path):
                    self.loadFromInfo(f, FileInfo(path))
                    break

        # change the file info for pane 'f' to 'info'
        def setFileInfo(self, f, info):
            h, footer = self.headers[f], self.footers[f]
            h.info = info
            h.updateTitle()
            footer.setFormat(self.panes[f].format)
            footer.setEncoding(info.encoding)
            footer.updateCursor(self, f)

        # callback used when a pane header's title changes
        def title_changed_cb(self, widget):
            # choose a short but descriptive title for the viewer
            has_edits = False
            names = []
            unique_names = set()
            for header in self.headers:
                has_edits |= header.has_edits
                s = header.info.label
                if s is None:
                    # no label provided, show the file name instead
                    s = header.info.name
                    if s is not None:
                        s = os.path.basename(s)
                if s is not None:
                    names.append(s)
                    unique_names.add(s)

            if len(unique_names) > 0:
                if len(unique_names) == 1:
                    self.title = names[0]
                else:
                    self.title = ' : '.join(names)
            s = self.title
            if has_edits:
                s += ' *'
            self.emit('title_changed', s)

        def setEncoding(self, f, encoding):
            h = self.headers[f]
            h.info.encoding = encoding
            self.footers[f].setEncoding(encoding)

        # load a new file into pane 'f'
        # 'info' indicates the name of the file and how to retrieve it from the
        # version control system if applicable
        def load(self, f, info):
            name = info.name
            encoding = info.encoding
            stat = None
            if name is None:
                # reset to an empty pane
                ss = []
            else:
                rev = info.revision
                try:
                    if rev is None:
                        # load the contents of a plain file
                        fd = open(name, 'rb')
                        s = fd.read()
                        fd.close()
                        # get the file's modification times so we can detect changes
                        stat = os.stat(name)
                    else:
                        if info.vcs is None:
                            raise IOError('Not under version control.')
                        fullname = os.path.abspath(name)
                        # retrieve the revision from the version control system
                        s = info.vcs.getRevision(self.prefs, fullname, rev)
                    # convert file contents to unicode
                    if encoding is None:
                        s, encoding = self.prefs.convertToUnicode(s)
                    else:
                        s = str(s, encoding=encoding)
                    ss = splitlines(s)
                except (IOError, OSError, UnicodeDecodeError, LookupError):
                    # FIXME: this can occur before the toplevel window is drawn
                    if rev is not None:
                        msg = _('Error reading revision %(rev)s of %(file)s.') % { 'rev': rev, 'file': name }
                    else:
                        msg = _('Error reading %s.') % (name, )
                    dialog = MessageDialog(self.get_toplevel(), Gtk.MessageType.ERROR, msg)
                    dialog.run()
                    dialog.destroy()
                    return
            # update the panes contents, last modified time, and title
            self.replaceContents(f, ss)
            info.encoding = encoding
            info.last_stat = info.stat = stat
            self.setFileInfo(f, info)
            # use the file name to choose appropriate syntax highlighting rules
            if name is not None:
                syntax = self.resources.guessSyntaxForFile(name, ss)
                if syntax is not None:
                    self.setSyntax(syntax)

        # load a new file into pane 'f'
        def open_file(self, f, reload=False):
            h = self.headers[f]
            info = h.info
            if not reload:
                # we need to ask for a file name if we are not reloading the
                # existing file
                dialog = FileChooserDialog(_('Open File'), self.get_toplevel(), self.prefs, Gtk.FileChooserAction.OPEN, Gtk.STOCK_OPEN, True)
                if info.name is not None:
                    dialog.set_filename(os.path.realpath(info.name))
                dialog.set_encoding(info.encoding)
                dialog.set_default_response(Gtk.ResponseType.OK)
                end = (dialog.run() != Gtk.ResponseType.OK)
                name = dialog.get_filename()
                rev = None
                vcs = None
                revision = dialog.get_revision().strip()
                if revision != '':
                    rev = revision
                    vcs = self.vcss.findByFilename(name, self.prefs)
                info = FileInfo(name, dialog.get_encoding(), vcs, rev)
                dialog.destroy()
                if end:
                    return
            self.loadFromInfo(f, info)

        # callback for open file button
        def open_file_button_cb(self, widget, f):
            self.open_file(f)

        # callback for open file menu item
        def open_file_cb(self, widget, data):
            self.open_file(self.current_pane)

        # callback for reload file button
        def reload_file_button_cb(self, widget, f):
            self.open_file(f, True)

        # callback for reload file menu item
        def reload_file_cb(self, widget, data):
            self.open_file(self.current_pane, True)

        # check changes to files on disk when receiving keyboard focus
        def focus_in(self, widget, event):
            for f, h in enumerate(self.headers):
                info = h.info
                try:
                    if info.last_stat is not None:
                        info = h.info
                        new_stat = os.stat(info.name)
                        if info.last_stat[stat.ST_MTIME] < new_stat[stat.ST_MTIME]:
                            # update our notion of the most recent modification
                            info.last_stat = new_stat
                            if info.label is not None:
                                s = info.label
                            else:
                                s = info.name
                            msg = _('The file %s changed on disk.  Do you want to reload the file?') % (s, )
                            dialog = MessageDialog(self.get_toplevel(), Gtk.MessageType.QUESTION, msg)
                            ok = (dialog.run() == Gtk.ResponseType.OK)
                            dialog.destroy()
                            if ok:
                                self.open_file(f, True)
                except OSError:
                    pass

        # save contents of pane 'f' to file
        def save_file(self, f, save_as=False):
            h = self.headers[f]
            info = h.info
            name, encoding, rev, label = info.name, info.encoding, info.revision, info.label
            if name is None or rev is not None:
                # we need to prompt for a file name the current contents were
                # not loaded from a regular file
                save_as = True
            if save_as:
                # prompt for a file name
                dialog = FileChooserDialog(_('Save %(title)s Pane %(pane)d') % { 'title': self.title, 'pane': f + 1 }, self.get_toplevel(), self.prefs, Gtk.FileChooserAction.SAVE, Gtk.STOCK_SAVE)
                if name is not None:
                    dialog.set_filename(os.path.abspath(name))
                if encoding is None:
                    encoding = self.prefs.getDefaultEncoding()
                dialog.set_encoding(encoding)
                name, label = None, None
                dialog.set_default_response(Gtk.ResponseType.OK)
                if dialog.run() == Gtk.ResponseType.OK:
                    name = dialog.get_filename()
                    encoding = dialog.get_encoding()
                    if encoding is None:
                        if info.encoding is not None:
                            # this case can occur if the user provided the
                            # encoding and it is not an encoding we know about
                            encoding = info.encoding
                        else:
                            encoding = self.prefs.getDefaultEncoding()
                dialog.destroy()
            if name is None:
                return False
            try:
                msg = None
                # warn if we are about to overwrite an existing file
                if save_as:
                    if os.path.exists(name):
                        msg = _('A file named %s already exists.  Do you want to overwrite it?') % (name, )
                # warn if we are about to overwrite a file that has changed
                # since we last read it
                elif info.stat is not None:
                    if info.stat[stat.ST_MTIME] < os.stat(name)[stat.ST_MTIME]:
                        msg = _('The file %s has been modified by another process since reading it.  If you save, all the external changes could be lost.  Save anyways?') % (name, )
                if msg is not None:
                    dialog = MessageDialog(self.get_toplevel(), Gtk.MessageType.QUESTION, msg)
                    end = (dialog.run() != Gtk.ResponseType.OK)
                    dialog.destroy()
                    if end:
                        return False
            except OSError:
                pass
            try:
                # convert the text to the output encoding
                # refresh the lines to contain new objects with updated line
                # numbers and no local edits
                ss = []
                for line in self.panes[f].lines:
                    if line is not None:
                        s = line.getText()
                        if s is not None:
                            ss.append(s)
                encoded = codecs.encode(''.join(ss), encoding)

                # write file
                fd = open(name, 'wb')
                fd.write(encoded)
                fd.close()

                # make the edits look permanent
                self.openUndoBlock()
                self.bakeEdits(f)
                self.closeUndoBlock()
                # update the pane file info
                info.name, info.encoding, info.revision, info.label = name, encoding, None, label
                info.last_stat = info.stat = os.stat(name)
                self.setFileInfo(f, info)
                # update the syntax highlighting incase we changed the file
                # extension
                syntax = self.resources.guessSyntaxForFile(name, ss)
                if syntax is not None:
                    self.setSyntax(syntax)
                return True
            except (UnicodeEncodeError, LookupError):
                dialog = MessageDialog(self.get_toplevel(), Gtk.MessageType.ERROR, _('Error encoding to %s.') % (encoding, ))
                dialog.run()
                dialog.destroy()
            except IOError:
                dialog = MessageDialog(self.get_toplevel(), Gtk.MessageType.ERROR, _('Error writing %s.') % (name, ))
                dialog.run()
                dialog.destroy()
            return False

        # callback for save file menu item
        def save_file_cb(self, widget, data):
            self.save_file(self.current_pane)

        # callback for save file as menu item
        def save_file_as_cb(self, widget, data):
            self.save_file(self.current_pane, True)

        # callback for save all menu item
        def save_all_cb(self, widget, data):
            for f, h in enumerate(self.headers):
                if h.has_edits:
                    self.save_file(f)

        # callback for save file button
        def save_file_button_cb(self, widget, f):
            self.save_file(f)

        # callback for save file as button
        def save_file_as_button_cb(self, widget, f):
            self.save_file(f, True)

        # callback for go to line menu item
        def go_to_line_cb(self, widget, data):
            parent = self.get_toplevel()
            dialog = NumericDialog(parent, _('Go To Line...'), _('Line Number: '), 1, 1, self.panes[self.current_pane].max_line_number + 1)
            okay = (dialog.run() == Gtk.ResponseType.ACCEPT)
            i = dialog.button.get_value_as_int()
            dialog.destroy()
            if okay:
                self.go_to_line(i)

        # callback to receive notification when the name of a file changes
        def swapped_panes_cb(self, widget, f_dst, f_src):
            f0, f1 = self.headers[f_dst], self.headers[f_src]
            f0.has_edits, f1.has_edits = f1.has_edits, f0.has_edits
            info0, info1 = f1.info, f0.info
            self.setFileInfo(f_dst, info0)
            self.setFileInfo(f_src, info1)

        # callback to receive notification when the name of a file changes
        def num_edits_changed_cb(self, widget, f):
            self.headers[f].setEdits(self.panes[f].num_edits > 0)

        # callback to record changes to the viewer's mode
        def mode_changed_cb(self, widget):
            self.updateStatus()

        # update the viewer's current status message
        def updateStatus(self):
            if self.mode == Mode.LINE:
                s = _('Press the enter key or double click to edit.  Press the space bar or use the RMB menu to manually align.')
            elif self.mode == Mode.CHAR:
                s = _('Press the escape key to finish editing.')
            elif self.mode == Mode.ALIGN:
                s = _('Select target line and press the space bar to align.  Press the escape key to cancel.')
            else:
                s = None
            self.status = s
            self.emit('status_changed', s)

        # gets the status bar text
        def getStatus(self):
            return self.status

        # callback to display the cursor in a pane
        def cursor_changed_cb(self, widget):
            for f, footer in enumerate(self.footers):
                footer.updateCursor(self, f)

        # callback to display the format of a pane
        def format_changed_cb(self, widget, f, format):
            self.footers[f].setFormat(format)

    def __init__(self, resources, vcss, copyright, rc_dir):
        super().__init__(type = Gtk.WindowType.TOPLEVEL)
        self.prefs = Preferences(os.path.join(rc_dir, 'prefs'))
        # number of created viewers (used to label some tabs)
        self.viewer_count = 0

        # get monitor resolution
        monitor_geometry = Gdk.Display.get_default().get_monitor(0).get_geometry()

        # state information that should persist across sessions
        self.bool_state = { 'window_maximized': False, 'search_matchcase': False, 'search_backwards': False }
        self.int_state = { 'window_width': 1024, 'window_height': 768 }
        self.int_state['window_x'] = max(0, (monitor_geometry.width - self.int_state['window_width']) / 2)
        self.int_state['window_y'] = max(0, (monitor_geometry.height - self.int_state['window_height']) / 2)
        self.connect('configure-event', self.configure_cb)
        self.connect('window-state-event', self.window_state_cb)

        # search history is application wide
        self.search_pattern = None
        self.search_history = []

        self.connect('delete-event', self.delete_cb)
        accel_group = Gtk.AccelGroup()

        # create a Box for our contents
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # create some custom icons for merging
        DIFFUSE_STOCK_NEW_2WAY_MERGE = 'diffuse-new-2way-merge'
        DIFFUSE_STOCK_NEW_3WAY_MERGE = 'diffuse-new-3way-merge'
        DIFFUSE_STOCK_LEFT_RIGHT = 'diffuse-left-right'
        DIFFUSE_STOCK_RIGHT_LEFT = 'diffuse-right-left'

        # get default theme and window scale factor
        default_theme = Gtk.IconTheme.get_default()
        scale_factor = self.get_scale_factor()

        icon_size = Gtk.IconSize.lookup(Gtk.IconSize.LARGE_TOOLBAR).height
        factory = Gtk.IconFactory()

        # render the base item used to indicate a new document
        p0 = default_theme.load_icon_for_scale("document-new", icon_size, scale_factor, 0)
        w, h = p0.get_width(), p0.get_height()

        # render new 2-way merge icon
        s = 0.8
        sw, sh = int(s * w), int(s * h)
        w1, h1 = w - sw, h - sh
        p = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, w, h)
        p.fill(0)
        p0.composite(p, 0, 0, sw, sh, 0, 0, s, s, GdkPixbuf.InterpType.BILINEAR, 255)
        p0.composite(p, w1, h1, sw, sh, w1, h1, s, s, GdkPixbuf.InterpType.BILINEAR, 255)
        factory.add(DIFFUSE_STOCK_NEW_2WAY_MERGE, Gtk.IconSet.new_from_pixbuf(p))

        # render new 3-way merge icon
        s = 0.7
        sw, sh = int(s * w), int(s * h)
        w1, h1 = (w - sw) / 2, (h - sh) / 2
        w2, h2 = w - sw, h - sh
        p = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, w, h)
        p.fill(0)
        p0.composite(p, 0, 0, sw, sh, 0, 0, s, s, GdkPixbuf.InterpType.BILINEAR, 255)
        p0.composite(p, w1, h1, sw, sh, w1, h1, s, s, GdkPixbuf.InterpType.BILINEAR, 255)
        p0.composite(p, w2, h2, sw, sh, w2, h2, s, s, GdkPixbuf.InterpType.BILINEAR, 255)
        factory.add(DIFFUSE_STOCK_NEW_3WAY_MERGE, Gtk.IconSet.new_from_pixbuf(p))

        # render the left and right arrow we will use in our custom icons
        p0 = default_theme.load_icon_for_scale("go-next", icon_size, scale_factor, 0)
        p1 = default_theme.load_icon_for_scale("go-previous", icon_size, scale_factor, 0)
        w, h, s = p0.get_width(), p0.get_height(), 0.65
        sw, sh = int(s * w), int(s * h)
        w1, h1 = w - sw, h - sh

        # create merge from left then right icon
        p = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, w, h)
        p.fill(0)
        p1.composite(p, w1, h1, sw, sh, w1, h1, s, s, GdkPixbuf.InterpType.BILINEAR, 255)
        p0.composite(p, 0, 0, sw, sh, 0, 0, s, s, GdkPixbuf.InterpType.BILINEAR, 255)
        factory.add(DIFFUSE_STOCK_LEFT_RIGHT, Gtk.IconSet.new_from_pixbuf(p))

        # create merge from right then left icon
        p = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, w, h)
        p.fill(0)
        p0.composite(p, 0, h1, sw, sh, 0, h1, s, s, GdkPixbuf.InterpType.BILINEAR, 255)
        p1.composite(p, w1, 0, sw, sh, w1, 0, s, s, GdkPixbuf.InterpType.BILINEAR, 255)
        factory.add(DIFFUSE_STOCK_RIGHT_LEFT, Gtk.IconSet.new_from_pixbuf(p))

        # make the icons available for use
        factory.add_default()

        menuspecs = []
        menuspecs.append([ _('_File'), [
                     [_('_Open File...'), self.open_file_cb, None, Gtk.STOCK_OPEN, 'open_file'],
                     [_('Open File In New _Tab...'), self.open_file_in_new_tab_cb, None, None, 'open_file_in_new_tab'],
                     [_('Open _Modified Files...'), self.open_modified_files_cb, None, None, 'open_modified_files'],
                     [_('Open Commi_t...'), self.open_commit_cb, None, None, 'open_commit'],
                     [_('_Reload File'), self.reload_file_cb, None, Gtk.STOCK_REFRESH, 'reload_file'],
                     [],
                     [_('_Save File'), self.save_file_cb, None, Gtk.STOCK_SAVE, 'save_file'],
                     [_('Save File _As...'), self.save_file_as_cb, None, Gtk.STOCK_SAVE_AS, 'save_file_as'],
                     [_('Save A_ll'), self.save_all_cb, None, None, 'save_all'],
                     [],
                     [_('New _2-Way File Merge'), self.new_2_way_file_merge_cb, None, DIFFUSE_STOCK_NEW_2WAY_MERGE, 'new_2_way_file_merge'],
                     [_('New _3-Way File Merge'), self.new_3_way_file_merge_cb, None, DIFFUSE_STOCK_NEW_3WAY_MERGE, 'new_3_way_file_merge'],
                     [_('New _N-Way File Merge...'), self.new_n_way_file_merge_cb, None, None, 'new_n_way_file_merge'],
                     [],
                     [_('_Close Tab'), self.close_tab_cb, None, Gtk.STOCK_CLOSE, 'close_tab'],
                     [_('_Undo Close Tab'), self.undo_close_tab_cb, None, None, 'undo_close_tab'],
                     [_('_Quit'), self.quit_cb, None, Gtk.STOCK_QUIT, 'quit'] ] ])

        menuspecs.append([ _('_Edit'), [
                     [_('_Undo'), self.button_cb, 'undo', Gtk.STOCK_UNDO, 'undo'],
                     [_('_Redo'), self.button_cb, 'redo', Gtk.STOCK_REDO, 'redo'],
                     [],
                     [_('Cu_t'), self.button_cb, 'cut', Gtk.STOCK_CUT, 'cut'],
                     [_('_Copy'), self.button_cb, 'copy', Gtk.STOCK_COPY, 'copy'],
                     [_('_Paste'), self.button_cb, 'paste', Gtk.STOCK_PASTE, 'paste'],
                     [],
                     [_('Select _All'), self.button_cb, 'select_all', None, 'select_all'],
                     [_('C_lear Edits'), self.button_cb, 'clear_edits', Gtk.STOCK_CLEAR, 'clear_edits'],
                     [_('_Dismiss All Edits'), self.button_cb, 'dismiss_all_edits', None, 'dismiss_all_edits'],
                     [],
                     [_('_Find...'), self.find_cb, None, Gtk.STOCK_FIND, 'find'],
                     [_('Find _Next'), self.find_next_cb, None, None, 'find_next'],
                     [_('Find Pre_vious'), self.find_previous_cb, None, None, 'find_previous'],
                     [_('_Go To Line...'), self.go_to_line_cb, None, Gtk.STOCK_JUMP_TO, 'go_to_line'],
                     [],
                     [_('Pr_eferences...'), self.preferences_cb, None, Gtk.STOCK_PREFERENCES, 'preferences'] ] ])

        submenudef = [ [_('None'), self.syntax_cb, None, None, 'no_syntax_highlighting', True, None, ('syntax', None) ] ]
        names = resources.getSyntaxNames()
        if len(names) > 0:
            submenudef.append([])
            names.sort(key=str.lower)
            for name in names:
                submenudef.append([name, self.syntax_cb, name, None, 'syntax_highlighting_' + name, True, None, ('syntax', name) ])

        menuspecs.append([ _('_View'), [
                     [_('_Syntax Highlighting'), None, None, None, None, True, submenudef],
                     [],
                     [_('Re_align All'), self.button_cb, 'realign_all', Gtk.STOCK_EXECUTE, 'realign_all'],
                     [_('_Isolate'), self.button_cb, 'isolate', None, 'isolate'],
                     [],
                     [_('_First Difference'), self.button_cb, 'first_difference', Gtk.STOCK_GOTO_TOP, 'first_difference'],
                     [_('_Previous Difference'), self.button_cb, 'previous_difference', Gtk.STOCK_GO_UP, 'previous_difference'],
                     [_('_Next Difference'), self.button_cb, 'next_difference', Gtk.STOCK_GO_DOWN, 'next_difference'],
                     [_('_Last Difference'), self.button_cb, 'last_difference', Gtk.STOCK_GOTO_BOTTOM, 'last_difference'],
                     [],
                     [_('Fir_st Tab'), self.first_tab_cb, None, None, 'first_tab'],
                     [_('Pre_vious Tab'), self.previous_tab_cb, None, None, 'previous_tab'],
                     [_('Next _Tab'), self.next_tab_cb, None, None, 'next_tab'],
                     [_('Las_t Tab'), self.last_tab_cb, None, None, 'last_tab'],
                     [],
                     [_('Shift Pane _Right'), self.button_cb, 'shift_pane_right', None, 'shift_pane_right'],
                     [_('Shift Pane _Left'), self.button_cb, 'shift_pane_left', None, 'shift_pane_left'] ] ])

        menuspecs.append([ _('F_ormat'), [
                     [_('Convert To _Upper Case'), self.button_cb, 'convert_to_upper_case', None, 'convert_to_upper_case'],
                     [_('Convert To _Lower Case'), self.button_cb, 'convert_to_lower_case', None, 'convert_to_lower_case'],
                     [],
                     [_('Sort Lines In _Ascending Order'), self.button_cb, 'sort_lines_in_ascending_order', Gtk.STOCK_SORT_ASCENDING, 'sort_lines_in_ascending_order'],
                     [_('Sort Lines In D_escending Order'), self.button_cb, 'sort_lines_in_descending_order', Gtk.STOCK_SORT_DESCENDING, 'sort_lines_in_descending_order'],
                     [],
                     [_('Remove Trailing _White Space'), self.button_cb, 'remove_trailing_white_space', None, 'remove_trailing_white_space'],
                     [_('Convert Tabs To _Spaces'), self.button_cb, 'convert_tabs_to_spaces', None, 'convert_tabs_to_spaces'],
                     [_('Convert Leading Spaces To _Tabs'), self.button_cb, 'convert_leading_spaces_to_tabs', None, 'convert_leading_spaces_to_tabs'],
                     [],
                     [_('_Increase Indenting'), self.button_cb, 'increase_indenting', Gtk.STOCK_INDENT, 'increase_indenting'],
                     [_('De_crease Indenting'), self.button_cb, 'decrease_indenting', Gtk.STOCK_UNINDENT, 'decrease_indenting'],
                     [],
                     [_('Convert To _DOS Format'), self.button_cb, 'convert_to_dos', None, 'convert_to_dos'],
                     [_('Convert To _Mac Format'), self.button_cb, 'convert_to_mac', None, 'convert_to_mac'],
                     [_('Convert To Uni_x Format'), self.button_cb, 'convert_to_unix', None, 'convert_to_unix'] ] ])

        menuspecs.append([ _('_Merge'), [
                     [_('Copy Selection _Right'), self.button_cb, 'copy_selection_right', Gtk.STOCK_GOTO_LAST, 'copy_selection_right'],
                     [_('Copy Selection _Left'), self.button_cb, 'copy_selection_left', Gtk.STOCK_GOTO_FIRST, 'copy_selection_left'],
                     [],
                     [_('Copy Left _Into Selection'), self.button_cb, 'copy_left_into_selection', Gtk.STOCK_GO_FORWARD, 'copy_left_into_selection'],
                     [_('Copy Right I_nto Selection'), self.button_cb, 'copy_right_into_selection', Gtk.STOCK_GO_BACK, 'copy_right_into_selection'],
                     [_('_Merge From Left Then Right'), self.button_cb, 'merge_from_left_then_right', DIFFUSE_STOCK_LEFT_RIGHT, 'merge_from_left_then_right'],
                     [_('M_erge From Right Then Left'), self.button_cb, 'merge_from_right_then_left', DIFFUSE_STOCK_RIGHT_LEFT, 'merge_from_right_then_left'] ] ])

        menuspecs.append([ _('_Help'), [
                     [_('_Help Contents...'), self.help_contents_cb, None, Gtk.STOCK_HELP, 'help_contents'],
                     [],
                     [_('_About %s...') % (APP_NAME, ), self.about_cb, None, Gtk.STOCK_ABOUT, 'about'] ] ])

        # used to disable menu events when switching tabs
        self.menu_update_depth = 0
        # build list of radio menu items so we can update them to match the
        # currently viewed pane
        self.radio_menus = radio_menus = {}
        menu_bar = createMenuBar(resources, menuspecs, radio_menus, accel_group)
        vbox.pack_start(menu_bar, False, False, 0)
        menu_bar.show()

        # create button bar
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        appendButtons(hbox, Gtk.IconSize.LARGE_TOOLBAR, [
           [ DIFFUSE_STOCK_NEW_2WAY_MERGE, self.new_2_way_file_merge_cb, None, _('New 2-Way File Merge') ],
           [ DIFFUSE_STOCK_NEW_3WAY_MERGE, self.new_3_way_file_merge_cb, None, _('New 3-Way File Merge') ],
           [],
           [ Gtk.STOCK_EXECUTE, self.button_cb, 'realign_all', _('Realign All') ],
           [ Gtk.STOCK_GOTO_TOP, self.button_cb, 'first_difference', _('First Difference') ],
           [ Gtk.STOCK_GO_UP, self.button_cb, 'previous_difference', _('Previous Difference') ],
           [ Gtk.STOCK_GO_DOWN, self.button_cb, 'next_difference', _('Next Difference') ],
           [ Gtk.STOCK_GOTO_BOTTOM, self.button_cb, 'last_difference', _('Last Difference') ],
           [],
           [ Gtk.STOCK_GOTO_LAST, self.button_cb, 'copy_selection_right', _('Copy Selection Right') ],
           [ Gtk.STOCK_GOTO_FIRST, self.button_cb, 'copy_selection_left', _('Copy Selection Left') ],
           [ Gtk.STOCK_GO_FORWARD, self.button_cb, 'copy_left_into_selection', _('Copy Left Into Selection') ],
           [ Gtk.STOCK_GO_BACK, self.button_cb, 'copy_right_into_selection', _('Copy Right Into Selection') ],
           [ DIFFUSE_STOCK_LEFT_RIGHT, self.button_cb, 'merge_from_left_then_right', _('Merge From Left Then Right') ],
           [ DIFFUSE_STOCK_RIGHT_LEFT, self.button_cb, 'merge_from_right_then_left', _('Merge From Right Then Left') ],
           [],
           [ Gtk.STOCK_UNDO, self.button_cb, 'undo', _('Undo') ],
           [ Gtk.STOCK_REDO, self.button_cb, 'redo', _('Redo') ],
           [ Gtk.STOCK_CUT, self.button_cb, 'cut', _('Cut') ],
           [ Gtk.STOCK_COPY, self.button_cb, 'copy', _('Copy') ],
           [ Gtk.STOCK_PASTE, self.button_cb, 'paste', _('Paste') ],
           [ Gtk.STOCK_CLEAR, self.button_cb, 'clear_edits', _('Clear Edits') ] ])
        # avoid the button bar from dictating the minimum window size
        hbox.set_size_request(0, hbox.get_size_request()[1])
        vbox.pack_start(hbox, False, False, 0)
        hbox.show()

        self.closed_tabs = []
        self.notebook = notebook = Gtk.Notebook.new()
        notebook.set_scrollable(True)
        notebook.connect('switch-page', self.switch_page_cb)
        vbox.pack_start(notebook, True, True, 0)
        notebook.show()

        # Add a status bar to the bottom
        self.statusbar = statusbar = Gtk.Statusbar.new()
        vbox.pack_start(statusbar, False, False, 0)
        statusbar.show()

        self.add_accel_group(accel_group)
        self.add(vbox)
        vbox.show()
        self.connect('focus-in-event', self.focus_in_cb)
        self.resources = resources
        self.vcss = vcss
        self.copyright = copyright

    # notifies all viewers on focus changes so they may check for external
    # changes to files
    def focus_in_cb(self, widget, event):
        for i in range(self.notebook.get_n_pages()):
            self.notebook.get_nth_page(i).focus_in(widget, event)

    # record the window's position and size
    def configure_cb(self, widget, event):
        # read the state directly instead of using window_maximized as the order
        # of configure/window_state events is undefined
        if (widget.get_window().get_state() & Gdk.WindowState.MAXIMIZED) == 0:
            self.int_state['window_x'], self.int_state['window_y'] = widget.get_window().get_root_origin()
            self.int_state['window_width'] = event.width
            self.int_state['window_height'] = event.height

    # record the window's maximised state
    def window_state_cb(self, window, event):
        self.bool_state['window_maximized'] = ((event.new_window_state & Gdk.WindowState.MAXIMIZED) != 0)

    # load state information that should persist across sessions
    def loadState(self, statepath):
        if os.path.isfile(statepath):
            try:
                f = open(statepath, 'r')
                ss = readlines(f)
                f.close()
                for j, s in enumerate(ss):
                    try:
                        a = shlex.split(s, True)
                        if len(a) > 0:
                            if len(a) == 2 and a[0] in self.bool_state:
                                self.bool_state[a[0]] = (a[1] == 'True')
                            elif len(a) == 2 and a[0] in self.int_state:
                                self.int_state[a[0]] = int(a[1])
                            else:
                                raise ValueError()
                    except ValueError:
                        # this may happen if the state was written by a
                        # different version -- don't bother the user
                        logDebug(f'Error processing line {j + 1} of {statepath}.')
            except IOError:
                # bad $HOME value? -- don't bother the user
                logDebug(f'Error reading {statepath}.')

        self.move(self.int_state['window_x'], self.int_state['window_y'])
        self.resize(self.int_state['window_width'], self.int_state['window_height'])
        if self.bool_state['window_maximized']:
            self.maximize()

    # save state information that should persist across sessions
    def saveState(self, statepath):
        try:
            ss = []
            for k, v in self.bool_state.items():
                ss.append(f'{k} {v}\n')
            for k, v in self.int_state.items():
                ss.append(f'{k} {v}\n')
            ss.sort()
            f = open(statepath, 'w')
            f.write(f"# This state file was generated by {APP_NAME} {VERSION}.\n\n")
            for s in ss:
                f.write(s)
            f.close()
        except IOError:
            # bad $HOME value? -- don't bother the user
            logDebug(f'Error writing {statepath}.')

    # select viewer for a newly selected file in the confirm close dialogue
    def __confirmClose_row_activated_cb(self, tree, path, col, model):
        self.notebook.set_current_page(self.notebook.page_num(model[path][3]))

    # toggle save state for a file listed in the confirm close dialogue
    def __confirmClose_toggle_cb(self, cell, path, model):
        model[path][0] = not model[path][0]

    # returns True if the list of viewers can be closed.  The user will be
    # given a chance to save any modified files before this method completes.
    def confirmCloseViewers(self, viewers):
        # make a list of modified files
        model = Gtk.ListStore.new([
            GObject.TYPE_BOOLEAN,
            GObject.TYPE_STRING,
            GObject.TYPE_INT,
            GObject.TYPE_OBJECT])
        for v in viewers:
            for f, h in enumerate(v.headers):
                if h.has_edits:
                    model.append((True, v.title, f + 1, v))
        if len(model) == 0:
            # there are no modified files, the viewers can be closed
            return True

        # ask the user which files should be saved
        dialog = Gtk.MessageDialog(parent=self.get_toplevel(),
                                   destroy_with_parent=True,
                                   message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.NONE,
                                   text=_('Some files have unsaved changes.  Select the files to save before closing.'))
        dialog.set_resizable(True)
        dialog.set_title(APP_NAME)
        # add list of files with unsaved changes
        sw = Gtk.ScrolledWindow.new()
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        treeview = Gtk.TreeView.new_with_model(model)
        r = Gtk.CellRendererToggle.new()
        r.connect('toggled', self.__confirmClose_toggle_cb, model)
        column = Gtk.TreeViewColumn(None, r)
        column.add_attribute(r, 'active', 0)
        treeview.append_column(column)
        r = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn(_('Tab'), r, text=1)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_sort_column_id(1)
        treeview.append_column(column)
        column = Gtk.TreeViewColumn(_('Pane'), r, text=2)
        column.set_resizable(True)
        column.set_sort_column_id(2)
        treeview.append_column(column)
        treeview.connect('row-activated', self.__confirmClose_row_activated_cb, model)
        sw.add(treeview)
        treeview.show()
        dialog.vbox.pack_start(sw, True, True, 0) # pylint: disable=no-member
        sw.show()
        # add custom set of action buttons
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        button = Gtk.Button.new_with_mnemonic(_('Close _Without Saving'))
        dialog.add_action_widget(button, Gtk.ResponseType.REJECT)
        button.show()
        dialog.add_button(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.CANCEL)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.OK:
            # save all checked files
            it = model.get_iter_first()
            while it:
                if model.get_value(it, 0):
                    f = model.get_value(it, 2) - 1
                    v = model.get_value(it, 3)
                    if not v.save_file(f):
                        # cancel if we failed to save a file
                        return False
                it = model.iter_next(it)
            return True
        # cancel if the user did not choose 'Close Without Saving' or 'Save'
        return response == Gtk.ResponseType.REJECT

    # callback for the close button on each tab
    def remove_tab_cb(self, widget, data):
        nb = self.notebook
        if nb.get_n_pages() > 1:
            # warn about losing unsaved changes before removing a tab
            if self.confirmCloseViewers([ data ]):
                self.closed_tabs.append((nb.page_num(data), data, nb.get_tab_label(data)))
                nb.remove(data)
                nb.set_show_tabs(self.prefs.getBool('tabs_always_show') or nb.get_n_pages() > 1)
        elif not self.prefs.getBool('tabs_warn_before_quit') or confirmTabClose(self.get_toplevel()):
            self.quit_cb(widget, data)

    # callback for RMB menu on notebook tabs
    def notebooktab_pick_cb(self, widget, data):
        self.notebook.set_current_page(data)

    # callback used when a mouse button is pressed on a notebook tab
    def notebooktab_button_press_cb(self, widget, event, data):
        if event.button == 2:
            # remove the tab on MMB
            self.remove_tab_cb(widget, data)
        elif event.button == 3:
            # create a popup to pick a tab for focus on RMB
            menu = Gtk.Menu.new()
            nb = self.notebook
            for i in range(nb.get_n_pages()):
                viewer = nb.get_nth_page(i)
                item = Gtk.MenuItem.new_with_label(nb.get_tab_label(viewer).get_text())
                item.connect('activate', self.notebooktab_pick_cb, i)
                menu.append(item)
                item.show()
                if viewer is data:
                    menu.select_item(item)
            menu.popup(None, None, None, event.button, event.time)

    # update window's title
    def updateTitle(self, viewer):
        title = self.notebook.get_tab_label(viewer).get_text()
        self.set_title(f'{title} - {APP_NAME}')

    # update the message in the status bar
    def setStatus(self, s):
        sb = self.statusbar
        context = sb.get_context_id('Message')
        sb.pop(context)
        if s is None:
            s = ''
        sb.push(context, s)

    # update the label in the status bar
    def setSyntax(self, s):
        # update menu
        t = self.radio_menus.get('syntax', None)
        if t is not None:
            t = t[1]
            if s in t:
                self.menu_update_depth += 1
                t[s].set_active(True)
                self.menu_update_depth -= 1

    # callback used when switching notebook pages
    def switch_page_cb(self, widget, ptr, page_num):
        viewer = widget.get_nth_page(page_num)
        self.updateTitle(viewer)
        self.setStatus(viewer.getStatus())
        self.setSyntax(viewer.getSyntax())

    # callback used when a viewer's title changes
    def title_changed_cb(self, widget, title):
        # update the label in the notebook's tab
        self.notebook.get_tab_label(widget).set_text(title)
        if widget is self.getCurrentViewer():
            self.updateTitle(widget)

    # callback used when a viewer's status changes
    def status_changed_cb(self, widget, s):
        # update the label in the notebook's tab
        if widget is self.getCurrentViewer():
            self.setStatus(s)

    # callback used when a viewer's syntax changes
    def syntax_changed_cb(self, widget, s):
        # update the label
        if widget is self.getCurrentViewer():
            self.setSyntax(s)

    # create an empty viewer with 'n' panes
    def newFileDiffViewer(self, n):
        self.viewer_count += 1
        tabname = _('File Merge %d') % (self.viewer_count, )
        tab = NotebookTab(tabname, Gtk.STOCK_FILE)
        viewer = self.FileDiffViewer(self.resources, self.vcss, n, self.prefs, tabname)
        tab.button.connect('clicked', self.remove_tab_cb, viewer)
        tab.connect('button-press-event', self.notebooktab_button_press_cb, viewer)
        self.notebook.append_page(viewer, tab)
        if hasattr(self.notebook, 'set_tab_reorderable'):
            # some PyGTK packages incorrectly omit this method
            self.notebook.set_tab_reorderable(viewer, True)
        tab.show()
        viewer.show()
        self.notebook.set_show_tabs(self.prefs.getBool('tabs_always_show') or self.notebook.get_n_pages() > 1)
        viewer.connect('title-changed', self.title_changed_cb)
        viewer.connect('status-changed', self.status_changed_cb)
        viewer.connect('syntax-changed', self.syntax_changed_cb)
        return viewer

    # create a new viewer to display 'items'
    def newLoadedFileDiffViewer(self, items):
        specs = []
        if len(items) == 0:
            for i in range(self.prefs.getInt('tabs_default_panes')):
                specs.append(FileInfo())
        elif len(items) == 1 and len(items[0][1]) == 1:
            # one file specified
            # determine which other files to compare it with
            name, data, label = items[0]
            rev, encoding = data[0]
            vcs = self.vcss.findByFilename(name, self.prefs)
            if vcs is None:
                # shift the existing file so it will be in the second pane
                specs.append(FileInfo())
                specs.append(FileInfo(name, encoding, None, None, label))
            else:
                if rev is None:
                    # no revision specified assume defaults
                    for name, rev in vcs.getFileTemplate(self.prefs, name):
                        if rev is None:
                            s = label
                        else:
                            s = None
                        specs.append(FileInfo(name, encoding, vcs, rev, s))
                else:
                    # single revision specified
                    specs.append(FileInfo(name, encoding, vcs, rev))
                    specs.append(FileInfo(name, encoding, None, None, label))
        else:
            # multiple files specified, use one pane for each file
            for name, data, label in items:
                for rev, encoding in data:
                    if rev is None:
                        vcs, s = None, label
                    else:
                        vcs, s = self.vcss.findByFilename(name, self.prefs), None
                    specs.append(FileInfo(name, encoding, vcs, rev, s))

        # open a new viewer
        viewer = self.newFileDiffViewer(max(2, len(specs)))

        # load the files
        for i, spec in enumerate(specs):
            viewer.load(i, spec)
        return viewer

    # create a new viewer for 'items'
    def createSingleTab(self, items, labels, options):
        if len(items) > 0:
            self.newLoadedFileDiffViewer(assign_file_labels(items, labels)).setOptions(options)

    # create a new viewer for each item in 'items'
    def createSeparateTabs(self, items, labels, options):
        # all tabs inherit the first tab's revision and encoding specifications
        items = [ (name, items[0][1]) for name, data in items ]
        for item in assign_file_labels(items, labels):
            self.newLoadedFileDiffViewer([ item ]).setOptions(options)

    # create a new viewer for each modified file found in 'items'
    def createCommitFileTabs(self, items, labels, options):
        new_items = []
        for item in items:
            name, data = item
            # get full path to an existing ancessor directory
            dn = os.path.abspath(name)
            while not os.path.isdir(dn):
                dn, old_dn = os.path.dirname(dn), dn
                if dn == old_dn:
                    break
            if len(new_items) == 0 or dn != new_items[-1][0]:
                new_items.append([ dn, None, [] ])
            dst = new_items[-1]
            dst[1] = data[-1][1]
            dst[2].append(name)
        for dn, encoding, names in new_items:
            vcs = self.vcss.findByFolder(dn, self.prefs)
            if vcs is not None:
                try:
                    for specs in vcs.getCommitTemplate(self.prefs, options['commit'], names):
                        viewer = self.newFileDiffViewer(len(specs))
                        for i, spec in enumerate(specs):
                            name, rev = spec
                            viewer.load(i, FileInfo(name, encoding, vcs, rev))
                        viewer.setOptions(options)
                except (IOError, OSError):
                    dialog = MessageDialog(self.get_toplevel(), Gtk.MessageType.ERROR, _('Error retrieving commits for %s.') % (dn, ))
                    dialog.run()
                    dialog.destroy()

    # create a new viewer for each modified file found in 'items'
    def createModifiedFileTabs(self, items, labels, options):
        new_items = []
        for item in items:
            name, data = item
            # get full path to an existing ancessor directory
            dn = os.path.abspath(name)
            while not os.path.isdir(dn):
                dn, old_dn = os.path.dirname(dn), dn
                if dn == old_dn:
                    break
            if len(new_items) == 0 or dn != new_items[-1][0]:
                new_items.append([ dn, None, [] ])
            dst = new_items[-1]
            dst[1] = data[-1][1]
            dst[2].append(name)
        for dn, encoding, names in new_items:
            vcs = self.vcss.findByFolder(dn, self.prefs)
            if vcs is not None:
                try:
                    for specs in vcs.getFolderTemplate(self.prefs, names):
                        viewer = self.newFileDiffViewer(len(specs))
                        for i, spec in enumerate(specs):
                            name, rev = spec
                            viewer.load(i, FileInfo(name, encoding, vcs, rev))
                        viewer.setOptions(options)
                except (IOError, OSError):
                    dialog = MessageDialog(self.get_toplevel(), Gtk.MessageType.ERROR, _('Error retrieving modifications for %s.') % (dn, ))
                    dialog.run()
                    dialog.destroy()

    # close all tabs without differences
    def closeOnSame(self):
        for i in range(self.notebook.get_n_pages() - 1, -1, -1):
            if not self.notebook.get_nth_page(i).hasDifferences():
                self.notebook.remove_page(i)

    # returns True if the application can safely quit
    def confirmQuit(self):
        nb = self.notebook
        return self.confirmCloseViewers([ nb.get_nth_page(i) for i in range(nb.get_n_pages()) ])

    # respond to close window request from the window manager
    def delete_cb(self, widget, event):
        if self.confirmQuit():
            Gtk.main_quit()
            return False
        return True

    # returns the currently focused viewer
    def getCurrentViewer(self):
        return self.notebook.get_nth_page(self.notebook.get_current_page())

    # callback for the open file menu item
    def open_file_cb(self, widget, data):
        self.getCurrentViewer().open_file_cb(widget, data)

    # callback for the open file menu item
    def open_file_in_new_tab_cb(self, widget, data):
        dialog = FileChooserDialog(_('Open File In New Tab'), self.get_toplevel(), self.prefs, Gtk.FileChooserAction.OPEN, Gtk.STOCK_OPEN, True)
        dialog.set_default_response(Gtk.ResponseType.OK)
        accept = (dialog.run() == Gtk.ResponseType.OK)
        name, encoding = dialog.get_filename(), dialog.get_encoding()
        rev = dialog.get_revision().strip()
        if rev == '':
            rev = None
        dialog.destroy()
        if accept:
            viewer = self.newLoadedFileDiffViewer([ (name, [ (rev, encoding) ], None) ])
            self.notebook.set_current_page(self.notebook.get_n_pages() - 1)
            viewer.grab_focus()

    # callback for the open modified files menu item
    def open_modified_files_cb(self, widget, data):
        parent = self.get_toplevel()
        dialog = FileChooserDialog(_('Choose Folder With Modified Files'), parent, self.prefs, Gtk.FileChooserAction.SELECT_FOLDER, Gtk.STOCK_OPEN)
        dialog.set_default_response(Gtk.ResponseType.OK)
        accept = (dialog.run() == Gtk.ResponseType.OK)
        name, encoding = dialog.get_filename(), dialog.get_encoding()
        dialog.destroy()
        if accept:
            n = self.notebook.get_n_pages()
            self.createModifiedFileTabs([ (name, [ (None, encoding) ]) ], [], {})
            if self.notebook.get_n_pages() > n:
                # we added some new tabs, focus on the first one
                self.notebook.set_current_page(n)
                self.getCurrentViewer().grab_focus()
            else:
                m = MessageDialog(parent, Gtk.MessageType.ERROR, _('No modified files found.'))
                m.run()
                m.destroy()

    # callback for the open commit menu item
    def open_commit_cb(self, widget, data):
        parent = self.get_toplevel()
        dialog = FileChooserDialog(_('Choose Folder With Commit'), parent, self.prefs, Gtk.FileChooserAction.SELECT_FOLDER, Gtk.STOCK_OPEN, True)
        dialog.set_default_response(Gtk.ResponseType.OK)
        accept = (dialog.run() == Gtk.ResponseType.OK)
        name, rev, encoding = dialog.get_filename(), dialog.get_revision(), dialog.get_encoding()
        dialog.destroy()
        if accept:
            n = self.notebook.get_n_pages()
            self.createCommitFileTabs([ (name, [ (None, encoding) ]) ], [], { 'commit': rev })
            if self.notebook.get_n_pages() > n:
                # we added some new tabs, focus on the first one
                self.notebook.set_current_page(n)
                self.getCurrentViewer().grab_focus()
            else:
                m = MessageDialog(parent, Gtk.MessageType.ERROR, _('No committed files found.'))
                m.run()
                m.destroy()

    # callback for the reload file menu item
    def reload_file_cb(self, widget, data):
        self.getCurrentViewer().reload_file_cb(widget, data)

    # callback for the save file menu item
    def save_file_cb(self, widget, data):
        self.getCurrentViewer().save_file_cb(widget, data)

    # callback for the save file as menu item
    def save_file_as_cb(self, widget, data):
        self.getCurrentViewer().save_file_as_cb(widget, data)

    # callback for the save all menu item
    def save_all_cb(self, widget, data):
        for i in range(self.notebook.get_n_pages()):
            self.notebook.get_nth_page(i).save_all_cb(widget, data)

    # callback for the new 2-way file merge menu item
    def new_2_way_file_merge_cb(self, widget, data):
        viewer = self.newFileDiffViewer(2)
        self.notebook.set_current_page(self.notebook.get_n_pages() - 1)
        viewer.grab_focus()

    # callback for the new 3-way file merge menu item
    def new_3_way_file_merge_cb(self, widget, data):
        viewer = self.newFileDiffViewer(3)
        self.notebook.set_current_page(self.notebook.get_n_pages() - 1)
        viewer.grab_focus()

    # callback for the new n-way file merge menu item
    def new_n_way_file_merge_cb(self, widget, data):
        parent = self.get_toplevel()
        dialog = NumericDialog(parent, _('New N-Way File Merge...'), _('Number of panes: '), 4, 2, 16)
        okay = (dialog.run() == Gtk.ResponseType.ACCEPT)
        npanes = dialog.button.get_value_as_int()
        dialog.destroy()
        if okay:
            viewer = self.newFileDiffViewer(npanes)
            self.notebook.set_current_page(self.notebook.get_n_pages() - 1)
            viewer.grab_focus()

    # callback for the close tab menu item
    def close_tab_cb(self, widget, data):
        self.remove_tab_cb(widget, self.notebook.get_nth_page(self.notebook.get_current_page()))

    # callback for the undo close tab menu item
    def undo_close_tab_cb(self, widget, data):
        if len(self.closed_tabs) > 0:
            i, tab, tab_label = self.closed_tabs.pop()
            self.notebook.insert_page(tab, tab_label, i)
            self.notebook.set_current_page(i)
            self.notebook.set_show_tabs(True)

    # callback for the quit menu item
    def quit_cb(self, widget, data):
        if self.confirmQuit():
            Gtk.main_quit()

    # request search parameters if force=True and then perform a search in the
    # current viewer pane
    def find(self, force, reverse):
        viewer = self.getCurrentViewer()
        if force or self.search_pattern is None:
            # construct search dialog
            history = self.search_history
            pattern = viewer.getSelectedText()
            for c in '\r\n':
                i = pattern.find(c)
                if i >= 0:
                    pattern = pattern[:i]
            dialog = SearchDialog(self.get_toplevel(), pattern, history)
            dialog.match_case_button.set_active(self.bool_state['search_matchcase'])
            dialog.backwards_button.set_active(self.bool_state['search_backwards'])
            keep = (dialog.run() == Gtk.ResponseType.ACCEPT)
            # persist the search options
            pattern = dialog.entry.get_text()
            match_case = dialog.match_case_button.get_active()
            backwards = dialog.backwards_button.get_active()
            dialog.destroy()
            if not keep or pattern == '':
                return
            # perform the search
            self.search_pattern = pattern
            if pattern in history:
                del history[history.index(pattern)]
            history.insert(0, pattern)
            self.bool_state['search_matchcase'] = match_case
            self.bool_state['search_backwards'] = backwards

        # determine where to start searching from
        reverse ^= self.bool_state['search_backwards']
        from_start, more = False, True
        while more:
            if viewer.find(self.search_pattern, self.bool_state['search_matchcase'], reverse, from_start):
                break

            if reverse:
                msg = _('Phrase not found.  Continue from the end of the file?')
            else:
                msg = _('Phrase not found.  Continue from the start of the file?')
            dialog = MessageDialog(self.get_toplevel(), Gtk.MessageType.QUESTION, msg)
            dialog.set_default_response(Gtk.ResponseType.OK)
            more = (dialog.run() == Gtk.ResponseType.OK)
            dialog.destroy()
            from_start = True

    # callback for the find menu item
    def find_cb(self, widget, data):
        self.find(True, False)

    # callback for the find next menu item
    def find_next_cb(self, widget, data):
        self.find(False, False)

    # callback for the find previous menu item
    def find_previous_cb(self, widget, data):
        self.find(False, True)

    # callback for the go to line menu item
    def go_to_line_cb(self, widget, data):
        self.getCurrentViewer().go_to_line_cb(widget, data)

    # notify all viewers of changes to the preferences
    def preferences_updated(self):
        n = self.notebook.get_n_pages()
        self.notebook.set_show_tabs(self.prefs.getBool('tabs_always_show') or n > 1)
        for i in range(n):
            self.notebook.get_nth_page(i).prefsUpdated()

    # callback for the preferences menu item
    def preferences_cb(self, widget, data):
        if self.prefs.runDialog(self.get_toplevel()):
            self.preferences_updated()

    # callback for all of the syntax highlighting menu items
    def syntax_cb(self, widget, data):
        # ignore events while we update the menu when switching tabs
        # also ignore notification of the newly disabled item
        if self.menu_update_depth == 0 and widget.get_active():
            self.getCurrentViewer().setSyntax(data)

    # callback for the first tab menu item
    def first_tab_cb(self, widget, data):
        self.notebook.set_current_page(0)

    # callback for the previous tab menu item
    def previous_tab_cb(self, widget, data):
        i, n = self.notebook.get_current_page(), self.notebook.get_n_pages()
        self.notebook.set_current_page((n + i - 1) % n)

    # callback for the next tab menu item
    def next_tab_cb(self, widget, data):
        i, n = self.notebook.get_current_page(), self.notebook.get_n_pages()
        self.notebook.set_current_page((i + 1) % n)

    # callback for the last tab menu item
    def last_tab_cb(self, widget, data):
        self.notebook.set_current_page(self.notebook.get_n_pages() - 1)

    # callback for most menu items and buttons
    def button_cb(self, widget, data):
        self.getCurrentViewer().button_cb(widget, data)

    # display help documenation
    def help_contents_cb(self, widget, data):
        help_url = None
        if isWindows:
            # help documentation is distributed as local HTML files
            # search for localised manual first
            parts = [ 'manual' ]
            if lang is not None:
                parts = [ 'manual' ]
                parts.extend(lang.split('_'))
            while len(parts) > 0:
                help_file = os.path.join(bin_dir, '_'.join(parts) + '.html')
                if os.path.isfile(help_file):
                    # we found a help file
                    help_url = path2url(help_file)
                    break
                del parts[-1]
        else:
            # verify gnome-help is available
            browser = None
            p = os.environ.get('PATH', None)
            if p is not None:
                for s in p.split(os.pathsep):
                    fp = os.path.join(s, 'gnome-help')
                    if os.path.isfile(fp):
                        browser = fp
                        break
            if browser is not None:
                # find localised help file
                if lang is None:
                    parts = []
                else:
                    parts = lang.split('_')
                s = os.path.abspath(os.path.join(bin_dir, '../share/gnome/help/diffuse'))
                while True:
                    if len(parts) > 0:
                        d = '_'.join(parts)
                    else:
                        # fall back to using 'C'
                        d = 'C'
                    help_file = os.path.join(os.path.join(s, d), 'diffuse.xml')
                    if os.path.isfile(help_file):
                        args = [ browser, path2url(help_file, 'ghelp') ]
                        # spawnvp is not available on some systems, use spawnv instead
                        os.spawnv(os.P_NOWAIT, args[0], args)
                        return
                    if len(parts) == 0:
                        break
                    del parts[-1]
        if help_url is None:
            # no local help file is available, show on-line help
            help_url = WEBSITE + 'manual.html'
            # ask for localised manual
            if lang is not None:
                help_url += '?lang=' + lang
        # use a web browser to display the help documentation
        webbrowser.open(help_url)

    # callback for the about menu item
    def about_cb(self, widget, data):
        dialog = AboutDialog(self.copyright)
        dialog.run()
        dialog.destroy()

if '__main__' == __name__:
    main()
