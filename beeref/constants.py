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
    
    # CSD:
    'CSD:Text': (200, 200, 200),
    'CSD:HoverBg': (255, 255, 255, 20),
    'CSD:PressedBg': (255, 255, 255, 30),
    'CSD:CloseHoverBg': (255, 255, 255, 20),
    'CSD:ClosePressedBg': (255, 255, 255, 30),
}

# CSD Stylesheet functions
def get_csd_button_style() -> str:
    """Get stylesheet for CSD title bar buttons.
    
    :return: CSS stylesheet string
    """
    text_color = COLORS['CSD:Text']
    hover_bg = COLORS['CSD:HoverBg']
    pressed_bg = COLORS['CSD:PressedBg']
    
    return f"""
        QPushButton {{
            border: none;
            background-color: transparent;
            color: rgb({text_color[0]}, {text_color[1]}, {text_color[2]});
            font-size: 16px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: rgba({hover_bg[0]}, {hover_bg[1]}, {hover_bg[2]}, {hover_bg[3]});
        }}
        QPushButton:pressed {{
            background-color: rgba({pressed_bg[0]}, {pressed_bg[1]}, {pressed_bg[2]}, {pressed_bg[3]});
        }}
    """


def get_csd_close_button_style() -> str:
    """Get stylesheet for CSD close button.
    
    :return: CSS stylesheet string
    """
    text_color = COLORS['CSD:Text']
    close_hover = COLORS['CSD:CloseHoverBg']
    close_pressed = COLORS['CSD:ClosePressedBg']
    
    return f"""
        QPushButton {{
            border: none;
            background-color: transparent;
            color: rgb({text_color[0]}, {text_color[1]}, {text_color[2]});
            font-size: 16px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: rgba({close_hover[0]}, {close_hover[1]}, {close_hover[2]}, {close_hover[3]});
            color: white;
        }}
        QPushButton:pressed {{
            background-color: rgba({close_pressed[0]}, {close_pressed[1]}, {close_pressed[2]}, {close_pressed[3]});
        }}
    """


def get_csd_title_style() -> str:
    """Get stylesheet for CSD title label.
    
    :return: CSS stylesheet string
    """
    text_color = COLORS['CSD:Text']
    
    return f"""
        QLabel {{
            color: rgb({text_color[0]}, {text_color[1]}, {text_color[2]});
            background-color: transparent;
            border: none;
        }}
    """
