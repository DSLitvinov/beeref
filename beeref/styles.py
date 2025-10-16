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

"""Centralized styling definitions for BeeRef dialogs and UI components."""


class BeeRefStyles:
    """Centralized styling definitions for BeeRef UI components."""
    
    # Color definitions from constants.py
    COLORS = {
        # Qt:
        'Active:Base': (60, 60, 60),
        'Active:Window': (40, 40, 40),
        'Active:Button': (60, 60, 60),
        'Active:Text': (200, 200, 200),
        'Active:HighlightedText': (255, 255, 255),
        'Active:WindowText': (200, 200, 200),
        'Active:ButtonText': (200, 200, 200),
        'Active:Highlight': (100, 100, 100),
        'Active:Link': (100, 100, 100),
        'Disabled:Light': (0, 0, 0, 0),
        'Disabled:Text': (140, 140, 140),

        # BeeRef specific:
        'Scene:Selection': (100, 100, 100),
        'Scene:Canvas': (60, 60, 60),
        'Scene:Text': (200, 200, 200)
    }
    
    # UI-specific color definitions
    DARK_BACKGROUND = "#2d2d2d"
    WHITE_TEXT = "#ffffff"
    BLUE_LINK = "#0078d4"
    BLUE_LINK_HOVER = "#106ebe"
    BLUE_LINK_PRESSED = "#005a9e"
    GRAY_TEXT = "#888888"
    
    # Base dialog style
    DIALOG_STYLE = f"""
        QDialog {{
            background-color: {DARK_BACKGROUND};
            color: {WHITE_TEXT};
        }}
        QLabel {{
            color: {WHITE_TEXT};
            background-color: transparent;
        }}
    """
    
    # Consolidated button style (used for all buttons)
    BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {DARK_BACKGROUND};
            color: {WHITE_TEXT};
            border: 1px solid #555555;
            border-radius: 6px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #3d3d3d;
            border-color: #666666;
        }}
        QPushButton:pressed {{
            background-color: #1d1d1d;
            border-color: #444444;
        }}
    """
    
    # Table style
    TABLE_STYLE = f"""
        QTableWidget {{
            background-color: transparent;
            border: none;
            gridline-color: transparent;
        }}
        QTableWidget::item {{
            padding: 5px;
            border: none;
        }}
        QHeaderView::section {{
            background-color: transparent;
            border: none;
            padding: 5px;
        }}
    """
    
    # Text styles
    WELCOME_TEXT_STYLE = f"""
        QLabel {{
            color: {GRAY_TEXT};
            font-size: 16px;
            font-weight: normal;
        }}
    """
    
    WELCOME_OR_TEXT_STYLE = f"""
        QLabel {{
            color: {GRAY_TEXT};
            font-size: 14px;
        }}
    """
    
    # Section title styles
    SECTION_TITLE_STYLE = "font-weight: bold; font-size: 16px; margin-bottom: 10px;"
    SECTION_TITLE_WITH_MARGIN_STYLE = "font-weight: bold; font-size: 16px; margin-top: 20px; margin-bottom: 10px;"
    
    # Link styles
    HELP_LINK_STYLE = f"color: {GRAY_TEXT}; text-decoration: underline;"
    HTML_LINK_STYLE = f"color: {GRAY_TEXT}; text-decoration: underline;"
    
    @staticmethod
    def get_dialog_style():
        """Get the base dialog styling."""
        return BeeRefStyles.DIALOG_STYLE
    
    @staticmethod
    def get_button_style():
        """Get the consolidated button styling."""
        return BeeRefStyles.BUTTON_STYLE
    
    @staticmethod
    def get_table_style():
        """Get the table styling."""
        return BeeRefStyles.TABLE_STYLE
    
    @staticmethod
    def get_welcome_text_style():
        """Get the welcome screen text styling."""
        return BeeRefStyles.WELCOME_TEXT_STYLE
    
    @staticmethod
    def get_welcome_or_text_style():
        """Get the welcome screen 'or' text styling."""
        return BeeRefStyles.WELCOME_OR_TEXT_STYLE
    
    @staticmethod
    def get_help_link_style():
        """Get the help link styling."""
        return BeeRefStyles.HELP_LINK_STYLE
    
    @staticmethod
    def get_section_title_style():
        """Get the section title styling."""
        return BeeRefStyles.SECTION_TITLE_STYLE
    
    @staticmethod
    def get_section_title_with_margin_style():
        """Get the section title with margin styling."""
        return BeeRefStyles.SECTION_TITLE_WITH_MARGIN_STYLE
    
    @staticmethod
    def get_html_link_style():
        """Get the HTML link styling."""
        return BeeRefStyles.HTML_LINK_STYLE
    
    @staticmethod
    def get_colors():
        """Get the COLORS dictionary from constants."""
        return BeeRefStyles.COLORS
