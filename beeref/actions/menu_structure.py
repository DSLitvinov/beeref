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

from beeref.localization import tr, get_available_languages

MENU_SEPARATOR = 0

def _get_language_menu_items():
    """Generate language menu items dynamically based on available translations."""
    available_languages = get_available_languages()
    
    # Skip template language
    if 'template' in available_languages:
        available_languages.remove('template')
    
    return [f'language_{lang_code}' for lang_code in available_languages]

def get_menu_structure():
    """Get menu structure with current translations."""
    return [
    {
        'menu': tr('file_menu'),
        'items': [
            'new_scene',
            'open',
            {
                'menu': tr('open_recent'),
                'items': '_build_recent_files',
            },
            MENU_SEPARATOR,
            'save',
            'save_as',
            MENU_SEPARATOR,
            'quit',
        ],
    },
    {
        'menu': tr('edit_menu'),
        'items': [
            'undo',
            'redo',
            MENU_SEPARATOR,
            'select_all',
            'deselect_all',
            MENU_SEPARATOR,
            'cut',
            'copy',
            'paste',
            'delete',
            MENU_SEPARATOR,
            'raise_to_top',
            'lower_to_bottom',
        ],
    },
    {
        'menu': tr('view_menu'),
        'items': [
            'fit_scene',
            'fit_selection',
            MENU_SEPARATOR,
            'fullscreen',
            'always_on_top',
            'show_scrollbars',
            'show_menubar',
            'show_titlebar',
        ],
    },
    {
        'menu': tr('insert_menu'),
        'items': [
            'insert_images',
            'insert_text',
        ],
    },
    {
        'menu': tr('transform_menu'),
        'items': [
            'crop',
            'flip_horizontally',
            'flip_vertically',
            MENU_SEPARATOR,
            'reset_scale',
            'reset_rotation',
            'reset_flip',
            'reset_crop',
            'reset_transforms',
        ],
    },
    {
        'menu': tr('normalize_menu'),
        'items': [
            'normalize_height',
            'normalize_width',
            'normalize_size',
        ],
    },
    {
        'menu': tr('arrange_menu'),
        'items': [
            'arrange_optimal',
            'arrange_horizontal',
            'arrange_vertical',
        ],
    },
    {
        'menu': tr('settings_menu'),
        'items': [
            {
                'menu': tr('language_settings'),
                'items': _get_language_menu_items(),
            },
            MENU_SEPARATOR,
            'open_settings_dir',
        ],
    },
    {
        'menu': tr('help_menu'),
        'items': [
            'help',
            'about',
            'debuglog',
        ],
    },
]

# For backward compatibility
menu_structure = get_menu_structure()
