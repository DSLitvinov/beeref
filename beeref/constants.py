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

APPNAME = 'BeeRef'
APPNAME_FULL = f'{APPNAME} Reference Image Viewer'
VERSION = '0.3.4-dev'
WEBSITE = 'https://github.com/rbreu/beeref'
COPYRIGHT = 'Copyright © 2021-2024 Rebecca Breu'

CHANGED_SYMBOL = '✎'

COLORS = {
    # Qt:
    'Active:Base': (60, 60, 60),
    'Active:AlternateBase': (70, 70, 70),
    'Active:Window': (40, 40, 40),
    'Active:Button': (40, 40, 40),
    'Active:Text': (200, 200, 200),
    'Active:HighlightedText': (255, 255, 255),
    'Active:WindowText': (200, 200, 200),
    'Active:ButtonText': (200, 200, 200),
    'Active:Highlight': (83, 167, 165),
    'Active:Link': (90, 181, 179),

    'Disabled:Base': (40, 40, 40),
    'Disabled:Window': (40, 40, 40, 50),
    'Disabled:WindowText': (120, 120, 120),
    'Disabled:Light': (0, 0, 0, 0),
    'Disabled:Text': (140, 140, 140),

    # BeeRef specific:
    'Scene:Selection': (116, 234, 231),
    'Scene:Canvas': (60, 60, 60),
    'Scene:Text': (200, 200, 200),
}


def get_welcome_overlay_icon_style():
    return 'padding: 12px; margin-bottom: 12px;'


def get_standard_button_style():
    highlight = COLORS['Active:Highlight']
    text = COLORS['Active:ButtonText']
    return (
        'QPushButton {'
        f'color: rgb({text[0]}, {text[1]}, {text[2]});'
        f'background-color: rgba({highlight[0]}, {highlight[1]}, {highlight[2]}, 0.25);'
        'padding: 0.6em 2em;'
        'border: none;'
        'border-radius: 6px;'
        '}'
        'QPushButton:hover {'
        f'background-color: rgba({highlight[0]}, {highlight[1]}, {highlight[2]}, 0.4);'
        '}'
        'QPushButton:pressed {'
        f'background-color: rgba({highlight[0]}, {highlight[1]}, {highlight[2]}, 0.6);'
        '}'
    )


# Floating Menu Styles

def _css_color(color):
    """Return a CSS-compatible rgb/rgba string for the given color tuple."""
    length = len(color)
    if length == 3:
        r, g, b = color
        return f"rgb({r}, {g}, {b})"
    if length == 4:
        r, g, b, a = color
        return f"rgba({r}, {g}, {b}, {a})"
    raise ValueError('Color tuples must have 3 (RGB) or 4 (RGBA) components.')


def get_floating_menu_base_style():
    """Base container style for floating menus."""
    bg = COLORS['Active:Window']
    border = COLORS['Active:Base']
    return f"""
        QWidget#FloatingMenu {{
            background-color: {_css_color(bg)};
            border-radius: 8px;
            border: 1px solid {_css_color(border)};
        }}
    """


def get_floating_menu_button_style():
    """Push button styling for floating menus."""
    background_color = (255, 255, 255, 30)
    border_color = (255, 255, 255, 10)
    inactive = COLORS['Disabled:Text']
    active = COLORS['Active:Text']
    accent = COLORS['Active:Highlight']

    return f"""
        QWidget#FloatingMenu QPushButton[floatingButton="true"] {{
            background-color: {_css_color(background_color)};
            color: {_css_color(inactive)};
            border: 1px solid {_css_color(border_color)};
            border-radius: 4px;
            padding: 4px 10px;
            font-weight: 600;
            min-width: 12px;
            min-height: 28px;
            max-height: 28px;
        }}

        QWidget#FloatingMenu QPushButton[floatingButton="true"]:hover,
        QWidget#FloatingMenu QPushButton[floatingButton="true"]:checked,
        QWidget#FloatingMenu QPushButton[floatingButton="true"][active="true"] {{
            color: {_css_color(active)};
        }}

        QWidget#FloatingMenu QPushButton[floatingButton="true"]:checked,
        QWidget#FloatingMenu QPushButton[floatingButton="true"][active="true"] {{
            border-bottom: 2px solid {_css_color(accent)};
        }}
    """


def get_floating_menu_separator_style():
    """Separator styling for floating menus."""
    border_color = (255, 255, 255, 10)
    r, g, b = border_color[:3]

    return f"""
        QWidget#FloatingMenu QFrame#FloatingMenuSeparator {{
            background-color: rgba({r}, {g}, {b}, 30);
            min-height: 28px;
            max-height: 28px;
        }}
    """


def get_floating_menu_combo_style():
    """Combo-box styling for floating menus."""
    from beeref.assets import BeeAssets
    
    bg = COLORS['Active:Button']
    active_color = COLORS['Active:Text']
    border_color = (255, 255, 255, 10)
    border_r, border_g, border_b = border_color[:3]
    
    # Получаем путь к иконке стрелки
    assets = BeeAssets()
    arrow_icon_path = assets.PATH.joinpath('icons', 'small-down.svg')
    # Используем прямой путь, экранируя обратные слеши для Windows
    arrow_icon_path_str = str(arrow_icon_path).replace('\\', '/')

    return f"""
        QWidget#FloatingMenu QComboBox,
        QWidget#FloatingMenu QFontComboBox {{
            background-color: {_css_color(bg)};
            color: {_css_color(active_color)};
            border: 1px solid rgba({border_r}, {border_g}, {border_b}, 160);
            border-radius: 4px;
            padding: 4px 12px;
            min-width: 40px;
            min-height: 28px;
            max-height: 28px;
        }}

        QWidget#FloatingMenu QComboBox::drop-down,
        QWidget#FloatingMenu QFontComboBox::drop-down {{
            border: none;
            width: 16px;
        }}

        QWidget#FloatingMenu QComboBox::down-arrow,
        QWidget#FloatingMenu QFontComboBox::down-arrow {{
            image: url({arrow_icon_path_str});
            width: 12px;
            height: 12px;
            margin-right: 4px;
        }}

        QWidget#FloatingMenu QComboBox QAbstractItemView,
        QWidget#FloatingMenu QFontComboBox QAbstractItemView {{
            min-width: 152px;
        }}

        QWidget#FloatingMenu QComboBox#FloatingMenuFontSize QAbstractItemView {{
            min-width: 80px;
        }}

        QWidget#FloatingMenu QComboBox#FloatingMenuGifSpeed QAbstractItemView {{
            min-width: 80px;
        }}
    """


def get_floating_menu_style():
    """Aggregate stylesheet for floating menus."""
    return ''.join([
        get_floating_menu_base_style(),
        get_floating_menu_button_style(),
        get_floating_menu_separator_style(),
        get_floating_menu_combo_style(),
    ])
