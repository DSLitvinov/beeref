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

"""Localization support for BeeRef."""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

from PyQt6 import QtCore, QtWidgets

logger = logging.getLogger(__name__)


class BeeRefTranslator:
    """Handles translation and localization for BeeRef."""
    
    def __init__(self):
        self.translator = QtCore.QTranslator()
        self.current_language = 'en'
        self.translations: Dict[str, Dict[str, str]] = {}
        self.translations_dir = self._get_translations_dir()
        self._load_translations()
    
    def _get_translations_dir(self) -> Path:
        """Get the directory containing translation files."""
        # Try to find translations in the package directory first
        package_dir = Path(__file__).parent
        translations_dir = package_dir / 'translations'
        
        if translations_dir.exists():
            return translations_dir
        
        # Fallback to a translations directory in the project root
        project_root = package_dir.parent
        translations_dir = project_root / 'translations'
        
        # Create the directory if it doesn't exist
        translations_dir.mkdir(exist_ok=True)
        return translations_dir
    
    def _load_translations(self):
        """Load all available translation files."""
        self.translations = {}
        
        # Load built-in translations first
        self._load_builtin_translations()
        
        # Load external translation files
        self._load_external_translations()
        
        logger.info(f"Loaded translations for languages: {list(self.translations.keys())}")
    
    def _load_builtin_translations(self):
        """Load built-in translations as fallback."""
        self.translations['en'] = {
            # Welcome screen
            'drag_drop_text': 'Drag and drop images here',
            'or_text': 'or',
            'browse_button': 'Browse',
            'help_link': 'Help',
            'recent_files': 'Recent Files',
            
            # Menu items
            'file_menu': '&File',
            'edit_menu': '&Edit',
            'view_menu': '&View',
            'insert_menu': '&Insert',
            'transform_menu': '&Transform',
            'normalize_menu': '&Normalize',
            'arrange_menu': '&Arrange',
            'settings_menu': '&Settings',
            'help_menu': '&Help',
            
            # File menu
            'new_scene': '&New Scene',
            'open': '&Open',
            'open_recent': 'Open &Recent',
            'save': '&Save',
            'save_as': 'Save &As...',
            'quit': '&Quit',
            
            # Edit menu
            'undo': '&Undo',
            'redo': '&Redo',
            'select_all': '&Select All',
            'deselect_all': 'Deselect &All',
            'cut': 'Cu&t',
            'copy': '&Copy',
            'paste': '&Paste',
            'delete': '&Delete',
            'raise_to_top': '&Raise to Top',
            'lower_to_bottom': 'Lower to Bottom',
            
            # View menu
            'fit_scene': '&Fit Scene',
            'fit_selection': 'Fit &Selection',
            'fullscreen': '&Fullscreen',
            'always_on_top': '&Always On Top',
            'show_scrollbars': 'Show &Scrollbars',
            'show_menubar': 'Show &Menu Bar',
            'show_titlebar': 'Show &Title Bar',
            
            # Insert menu
            'insert_images': '&Images...',
            'insert_text': '&Text',
            
            # Transform menu
            'crop': '&Crop',
            'flip_horizontally': 'Flip &Horizontally',
            'flip_vertically': 'Flip &Vertically',
            'reset_scale': 'Reset &Scale',
            'reset_rotation': 'Reset &Rotation',
            'reset_flip': 'Reset &Flip',
            'reset_crop': 'Reset Cro&p',
            'reset_transforms': 'Reset &All',
            
            # Normalize menu
            'normalize_height': '&Height',
            'normalize_width': '&Width',
            'normalize_size': '&Size',
            
            # Arrange menu
            'arrange_optimal': '&Optimal',
            'arrange_horizontal': '&Horizontal',
            'arrange_vertical': '&Vertical',
            
            # Settings menu
            'open_settings_dir': 'Open Settings Folder',
            'language_settings': '&Language',
            'en': 'English',
            'ru': 'Русский',
            'be': 'Беларуская',
            'es': 'Español',
            'de': 'Deutsch',
            'it': 'Italiano',
            
            # Help menu
            'help': '&Help',
            'about': '&About',
            'debuglog': 'Show &Debug Log',
            
            # Dialog titles
            'about_title': 'About BeeRef',
            'help_title': 'Help',
            'debug_log_title': 'BeeRef Debug Log',
            
            # About dialog
            'about_description': 'A simple reference image viewer',
            'about_website': 'Visit the BeeRef website',
            'close_button': 'Close',
            
            # Help dialog
            'controls_title': 'Controls',
            'controls_intro': 'For more in depth help refer to the handbook.',
            'controls_intro2': "These are BeeRef's most basic controls:",
            'controls_action_header': 'Action',
            'controls_input_header': 'Input',
            'controls_move_window': 'Move window',
            'controls_open_menu': 'Open menu',
            'controls_select_images': 'Select images',
            'controls_focus_images': 'Focus images',
            'controls_zoom_to_pointer': 'Zoom to pointer',
            'controls_pan_scene': 'Pan Scene',
            'controls_input_right_click_drag': 'right click drag',
            'controls_input_right_click': 'right click',
            'controls_input_left_click_drag': 'left click/drag',
            'controls_input_double_left_click': 'double left click',
            'controls_input_scroll_wheel': 'scroll wheel',
            'controls_input_scroll_click_drag': 'scroll click drag',
            'controls_info': 'To see all controls and set them yourself, check out keyboard shortcuts and the default shortcuts web page for more details.',
            'keyboard_shortcuts_title': 'Keyboard Shortcuts',
            'keyboard_shortcuts_intro': 'These are the main keyboard shortcuts:',
            'keyboard_shortcuts_action_header': 'Action',
            'keyboard_shortcuts_shortcut_header': 'Shortcut',
            'support_title': 'Support',
            'support_text': 'For troubleshooting, please consult the FAQ. For additional help, submitting bug reports, suggestions, or anything else you might want to tell us, visit the forums.',
            'about_link': 'About BeeRef',
            
            # Debug log dialog
            'copy_to_clipboard': 'Co&py To Clipboard',
        }
    
    def _load_external_translations(self):
        """Load external translation files from the translations directory."""
        if not self.translations_dir.exists():
            return
        
        for translation_file in self.translations_dir.glob('*.json'):
            try:
                language_code = translation_file.stem
                with open(translation_file, 'r', encoding='utf-8') as f:
                    translations = json.load(f)
                    self.translations[language_code] = translations
                    logger.debug(f"Loaded translations for {language_code}")
            except Exception as e:
                logger.warning(f"Failed to load translation file {translation_file}: {e}")
    
    def get_text(self, key: str, language: Optional[str] = None) -> str:
        """Get translated text for a given key."""
        if language is None:
            language = self.current_language
        
        # Try the requested language first
        if language in self.translations and key in self.translations[language]:
            return self.translations[language][key]
        
        # Fallback to English
        if key in self.translations.get('en', {}):
            return self.translations['en'][key]
        
        # If not found, return the key itself
        logger.warning(f"Translation key '{key}' not found for language '{language}'")
        return key
    
    def set_language(self, language: str) -> bool:
        """Set the current language."""
        if language in self.translations:
            self.current_language = language
            logger.info(f"Language set to: {language}")
            return True
        else:
            logger.warning(f"Language '{language}' not available")
            return False
    
    def get_available_languages(self) -> List[str]:
        """Get list of available languages."""
        return list(self.translations.keys())
    
    def get_language_name(self, language_code: str) -> str:
        """Get the display name for a language code."""
        if language_code in self.translations:
            # Try to get the language name from the translations
            name_key = f'language_name_{language_code}'
            if name_key in self.translations[language_code]:
                return self.translations[language_code][name_key]
            # Fallback to a generic name
            return language_code.title()
        return language_code
    
    def save_translation_template(self, language_code: str = 'template') -> bool:
        """Save a translation template file for a new language."""
        try:
            template_file = self.translations_dir / f'{language_code}.json'
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(self.translations['en'], f, indent=2, ensure_ascii=False)
            logger.info(f"Translation template saved to {template_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save translation template: {e}")
            return False
    
    def reload_translations(self):
        """Reload all translation files."""
        self._load_translations()


# Global translator instance
translator = BeeRefTranslator()


def tr(key: str, language: Optional[str] = None) -> str:
    """Convenience function to get translated text."""
    return translator.get_text(key, language)


def set_language(language: str) -> bool:
    """Convenience function to set the current language."""
    return translator.set_language(language)


def get_available_languages() -> List[str]:
    """Convenience function to get available languages."""
    return translator.get_available_languages()


def get_language_name(language_code: str) -> str:
    """Convenience function to get language display name."""
    return translator.get_language_name(language_code)
