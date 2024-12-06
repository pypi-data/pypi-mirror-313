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

from .girepo import Gtk
from .util import APP_NAME, norm_encoding
from gettext import gettext as _

# widget to help pick an encoding
class EncodingMenu(Gtk.Box):

    def __init__(self, prefs, autodetect=False):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.combobox = combobox = Gtk.ComboBoxText.new()
        self.encodings = prefs.getEncodings()[:]
        for e in self.encodings:
            combobox.append_text(e)
        if autodetect:
            self.encodings.insert(0, None)
            combobox.prepend_text(_('Auto Detect'))
        self.pack_start(combobox, False, False, 0)
        combobox.show()

    def set_text(self, encoding):
        encoding = norm_encoding(encoding)
        if encoding in self.encodings:
            self.combobox.set_active(self.encodings.index(encoding))

    def get_text(self):
        i = self.combobox.get_active()
        if i >= 0:
            return self.encodings[i]

# convenience method for creating a menu according to a template
def createMenu(resources, specs, radio=None, accel_group=None):
    menu = Gtk.Menu.new()
    for spec in specs:
        if len(spec) > 0:
            if len(spec) > 7 and spec[7] is not None:
                g, k = spec[7]
                if g not in radio:
                    item = Gtk.RadioMenuItem.new_with_mnemonic_from_widget(None, spec[0])
                    radio[g] = (item, {})
                else:
                    item = Gtk.RadioMenuItem.new_with_mnemonic_from_widget(radio[g][0], spec[0])
                radio[g][1][k] = item
            else:
                item = Gtk.ImageMenuItem.new_with_mnemonic(spec[0])
            cb = spec[1]
            if cb is not None:
                data = spec[2]
                item.connect('activate', cb, data)
            if len(spec) > 3 and spec[3] is not None:
                image = Gtk.Image.new()
                image.set_from_stock(spec[3], Gtk.IconSize.MENU)
                item.set_image(image)
            if accel_group is not None and len(spec) > 4:
                a = resources.getKeyBindings('menu', spec[4])
                if len(a) > 0:
                    key, modifier = a[0]
                    item.add_accelerator('activate', accel_group, key, modifier, Gtk.AccelFlags.VISIBLE)
            if len(spec) > 5:
                item.set_sensitive(spec[5])
            if len(spec) > 6 and spec[6] is not None:
                item.set_submenu(createMenu(resources, spec[6], radio, accel_group))
            item.set_use_underline(True)
        else:
            item = Gtk.SeparatorMenuItem.new()
        item.show()
        menu.append(item)
    return menu

# convenience class for displaying a message dialogue
class MessageDialog(Gtk.MessageDialog):

    def __init__(self, parent, type, s):
        if type == Gtk.MessageType.ERROR:
            buttons = Gtk.ButtonsType.OK
        else:
            buttons = Gtk.ButtonsType.OK_CANCEL
        super().__init__(parent = parent, destroy_with_parent = True, message_type = type, buttons = buttons, text = s)
        self.set_title(APP_NAME)

# report error messages
def logError(s):
    m = MessageDialog(None, Gtk.MessageType.ERROR, s)
    m.run()
    m.destroy()
