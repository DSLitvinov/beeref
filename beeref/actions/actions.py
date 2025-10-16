# This file is part of BeeRef.
#
# BeeRef is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BeeRef is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BeeRef.  If not, see <https://www.gnu.org/licenses/>.

from beeref.localization import tr

def get_actions():
    """Get actions with current translations."""
    return [
    {
        'id': 'open',
        'text': tr('open'),
        'shortcuts': ['Ctrl+O'],
        'callback': 'on_action_open',
    },
    {
        'id': 'save',
        'text': tr('save'),
        'shortcuts': ['Ctrl+S'],
        'callback': 'on_action_save',
    },
    {
        'id': 'save_as',
        'text': tr('save_as'),
        'shortcuts': ['Ctrl+Shift+S'],
        'callback': 'on_action_save_as',
    },
    {
        'id': 'quit',
        'text': tr('quit'),
        'shortcuts': ['Ctrl+Q'],
        'callback': 'on_action_quit',
    },
    {
        'id': 'insert_images',
        'text': tr('insert_images'),
        'shortcuts': ['Ctrl+I'],
        'callback': 'on_action_insert_images',
    },
    {
        'id': 'insert_text',
        'text': tr('insert_text'),
        'shortcuts': ['Ctrl+T'],
        'callback': 'on_action_insert_text',
    },
    {
        'id': 'undo',
        'text': tr('undo'),
        'shortcuts': ['Ctrl+Z'],
        'callback': 'on_action_undo',
        'group': 'active_when_can_undo',
    },
    {
        'id': 'redo',
        'text': tr('redo'),
        'shortcuts': ['Ctrl+Shift+Z'],
        'callback': 'on_action_redo',
        'group': 'active_when_can_redo',
    },
    {
        'id': 'copy',
        'text': tr('copy'),
        'shortcuts': ['Ctrl+C'],
        'callback': 'on_action_copy',
        'group': 'active_when_selection',
    },
    {
        'id': 'cut',
        'text': tr('cut'),
        'shortcuts': ['Ctrl+X'],
        'callback': 'on_action_cut',
        'group': 'active_when_selection',
    },
    {
        'id': 'paste',
        'text': tr('paste'),
        'shortcuts': ['Ctrl+V'],
        'callback': 'on_action_paste',
    },
    {
        'id': 'delete',
        'text': tr('delete'),
        'shortcuts': ['Del'],
        'callback': 'on_action_delete_items',
        'group': 'active_when_selection',
    },
    {
        'id': 'raise_to_top',
        'text': tr('raise_to_top'),
        'shortcuts': ['PgUp'],
        'callback': 'on_action_raise_to_top',
        'group': 'active_when_selection',
    },
    {
        'id': 'lower_to_bottom',
        'text': tr('lower_to_bottom'),
        'shortcuts': ['PgDown'],
        'callback': 'on_action_lower_to_bottom',
        'group': 'active_when_selection',
    },
    {
        'id': 'normalize_height',
        'text': tr('normalize_height'),
        'shortcuts': ['Shift+H'],
        'callback': 'on_action_normalize_height',
        'group': 'active_when_selection',
    },
    {
        'id': 'normalize_width',
        'text': tr('normalize_width'),
        'shortcuts': ['Shift+W'],
        'callback': 'on_action_normalize_width',
        'group': 'active_when_selection',
    },
    {
        'id': 'normalize_size',
        'text': tr('normalize_size'),
        'shortcuts': ['Shift+S'],
        'callback': 'on_action_normalize_size',
        'group': 'active_when_selection',
    },
    {
        'id': 'arrange_optimal',
        'text': tr('arrange_optimal'),
        'shortcuts': ['Shift+O'],
        'callback': 'on_action_arrange_optimal',
        'group': 'active_when_selection',
    },
    {
        'id': 'arrange_horizontal',
        'text': tr('arrange_horizontal'),
        'callback': 'on_action_arrange_horizontal',
        'group': 'active_when_selection',
    },
    {
        'id': 'arrange_vertical',
        'text': tr('arrange_vertical'),
        'callback': 'on_action_arrange_vertical',
        'group': 'active_when_selection',
    },
    {
        'id': 'crop',
        'text': tr('crop'),
        'shortcuts': ['Shift+C'],
        'callback': 'on_action_crop',
        'group': 'active_when_croppable',
    },
    {
        'id': 'flip_horizontally',
        'text': tr('flip_horizontally'),
        'shortcuts': ['H'],
        'callback': 'on_action_flip_horizontally',
        'group': 'active_when_selection',
    },
    {
        'id': 'flip_vertically',
        'text': tr('flip_vertically'),
        'shortcuts': ['V'],
        'callback': 'on_action_flip_vertically',
        'group': 'active_when_selection',
    },
    {
        'id': 'new_scene',
        'text': tr('new_scene'),
        'shortcuts': ['Ctrl+N'],
        'callback': 'clear_scene',
    },
    {
        'id': 'fit_scene',
        'text': tr('fit_scene'),
        'shortcuts': ['1'],
        'callback': 'on_action_fit_scene',
    },
    {
        'id': 'fit_selection',
        'text': tr('fit_selection'),
        'shortcuts': ['2'],
        'callback': 'on_action_fit_selection',
        'group': 'active_when_selection',
    },
    {
        'id': 'reset_scale',
        'text': tr('reset_scale'),
        'callback': 'on_action_reset_scale',
        'group': 'active_when_selection',
    },
    {
        'id': 'reset_rotation',
        'text': tr('reset_rotation'),
        'callback': 'on_action_reset_rotation',
        'group': 'active_when_selection',
    },
    {
        'id': 'reset_flip',
        'text': tr('reset_flip'),
        'callback': 'on_action_reset_flip',
        'group': 'active_when_selection',
    },
    {
        'id': 'reset_crop',
        'text': tr('reset_crop'),
        'callback': 'on_action_reset_crop',
        'group': 'active_when_selection',
    },
    {
        'id': 'reset_transforms',
        'text': tr('reset_transforms'),
        'shortcuts': ['R'],
        'callback': 'on_action_reset_transforms',
        'group': 'active_when_selection',
    },
    {
        'id': 'select_all',
        'text': tr('select_all'),
        'shortcuts': ['Ctrl+A'],
        'callback': 'on_action_select_all',
    },
    {
        'id': 'deselect_all',
        'text': tr('deselect_all'),
        'shortcuts': ['Ctrl+Shift+A'],
        'callback': 'on_action_deselect_all',
    },
    {
        'id': 'help',
        'text': tr('help'),
        'shortcuts': ['F1', 'Ctrl+H'],
        'callback': 'on_action_help',
    },
    {
        'id': 'about',
        'text': tr('about'),
        'callback': 'on_action_about',
    },
    {
        'id': 'debuglog',
        'text': tr('debuglog'),
        'callback': 'on_action_debuglog',
    },
    {
        'id': 'show_scrollbars',
        'text': tr('show_scrollbars'),
        'checkable': True,
        'settings': 'View/show_scrollbars',
        'callback': 'on_action_show_scrollbars',
    },
    {
        'id': 'show_menubar',
        'text': tr('show_menubar'),
        'checkable': True,
        'settings': 'View/show_menubar',
        'callback': 'on_action_show_menubar',
    },
    {
        'id': 'show_titlebar',
        'text': tr('show_titlebar'),
        'checkable': True,
        'checked': True,
        'callback': 'on_action_show_titlebar',
    },
    {
        'id': 'fullscreen',
        'text': tr('fullscreen'),
        'shortcuts': ['F11'],
        'checkable': True,
        'callback': 'on_action_fullscreen',
    },
    {
        'id': 'always_on_top',
        'text': tr('always_on_top'),
        'checkable': True,
        'callback': 'on_action_always_on_top',
    },
    {
        'id': 'open_settings_dir',
        'text': tr('open_settings_dir'),
        'callback': 'on_action_open_settings_dir',
    },
    {
        'id': 'language_english',
        'text': tr('english'),
        'checkable': True,
        'callback': 'on_action_set_language_english',
    },
    {
        'id': 'language_russian',
        'text': tr('russian'),
        'checkable': True,
        'callback': 'on_action_set_language_russian',
    },
]

# For backward compatibility
actions = get_actions()
