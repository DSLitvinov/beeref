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
    
    # Color definitions
    DARK_BACKGROUND = "#2d2d2d"
    WHITE_TEXT = "#ffffff"
    BLUE_LINK = "#0078d4"
    BLUE_LINK_HOVER = "#106ebe"
    BLUE_LINK_PRESSED = "#005a9e"
    GRAY_TEXT = "#888888"
    
    # Dialog styles
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
    
    # Button styles
    BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {BLUE_LINK};
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {BLUE_LINK_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {BLUE_LINK_PRESSED};
        }}
    """
    
    # Link button styles (transparent background)
    LINK_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: transparent;
            color: {BLUE_LINK};
            text-decoration: underline;
            border: none;
            padding: 0px;
            text-align: left;
        }}
        QPushButton:hover {{
            color: {BLUE_LINK_HOVER};
        }}
    """
    
    # Table styles
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
    
    # Welcome screen text styles
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
    
    # Browse button style (specific to welcome screen)
    BROWSE_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {BLUE_LINK};
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {BLUE_LINK_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {BLUE_LINK_PRESSED};
        }}
    """
    
    # Help link style
    HELP_LINK_STYLE = f"color: {GRAY_TEXT}; text-decoration: underline;"
    
    # Section title styles
    SECTION_TITLE_STYLE = "font-weight: bold; font-size: 16px; margin-bottom: 10px;"
    SECTION_TITLE_WITH_MARGIN_STYLE = "font-weight: bold; font-size: 16px; margin-top: 20px; margin-bottom: 10px;"
    
    # Link styles for HTML content
    HTML_LINK_STYLE = f"color: {BLUE_LINK}; text-decoration: underline;"
    
    @staticmethod
    def get_dialog_style():
        """Get the base dialog styling."""
        return BeeRefStyles.DIALOG_STYLE
    
    @staticmethod
    def get_button_style():
        """Get the standard button styling."""
        return BeeRefStyles.BUTTON_STYLE
    
    @staticmethod
    def get_link_button_style():
        """Get the link button styling."""
        return BeeRefStyles.LINK_BUTTON_STYLE
    
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
    def get_browse_button_style():
        """Get the browse button styling."""
        return BeeRefStyles.BROWSE_BUTTON_STYLE
    
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
