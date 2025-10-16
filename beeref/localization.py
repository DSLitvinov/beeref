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

import os
from PyQt6 import QtCore, QtWidgets


class BeeRefTranslator:
    """Handles translation and localization for BeeRef."""
    
    def __init__(self):
        self.translator = QtCore.QTranslator()
        self.current_language = 'en'
        self.translations = {
            'en': {
                # Welcome screen
                'drag_drop_text': 'Drag and drop images here',
                'or_text': 'or',
                'browse_button': 'Browse',
                'help_link': 'Help',
                
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
                'english': 'English',
                'russian': 'Русский',
                
                # Help menu
                'help': '&Help',
                'about': '&About',
                'debuglog': 'Show &Debug Log',
                
                # Dialog titles
                'about_title': 'About BeeRef',
                'help_title': 'Help',
                
                # About dialog
                'about_description': 'A simple reference image viewer',
                'about_website': 'Website',
                'close_button': 'Close',
                
                # Help dialog
                'controls_title': 'Controls',
                'controls_intro': 'Keyboard shortcuts and mouse controls:',
                'support_title': 'Support',
                'faq_link': 'FAQ',
                'forums_link': 'Forums',
                'about_link': 'About BeeRef',
            },
            'ru': {
                # Welcome screen
                'drag_drop_text': 'Перетащите изображения сюда',
                'or_text': 'или',
                'browse_button': 'Обзор',
                'help_link': 'Справка',
                
                # Menu items
                'file_menu': '&Файл',
                'edit_menu': '&Правка',
                'view_menu': '&Вид',
                'insert_menu': '&Вставка',
                'transform_menu': '&Трансформация',
                'normalize_menu': '&Нормализация',
                'arrange_menu': '&Упорядочить',
                'settings_menu': '&Настройки',
                'help_menu': '&Справка',
                
                # File menu
                'new_scene': '&Новая сцена',
                'open': '&Открыть',
                'open_recent': 'Открыть &недавние',
                'save': '&Сохранить',
                'save_as': 'Сохранить &как...',
                'quit': '&Выход',
                
                # Edit menu
                'undo': '&Отменить',
                'redo': '&Повторить',
                'select_all': 'Выделить &всё',
                'deselect_all': 'Снять выделение',
                'cut': '&Вырезать',
                'copy': '&Копировать',
                'paste': '&Вставить',
                'delete': '&Удалить',
                'raise_to_top': 'На &передний план',
                'lower_to_bottom': 'На задний план',
                
                # View menu
                'fit_scene': '&Вместить сцену',
                'fit_selection': 'Вместить выделенное',
                'fullscreen': '&Полный экран',
                'always_on_top': '&Поверх всех окон',
                'show_scrollbars': 'Показать &полосы прокрутки',
                'show_menubar': 'Показать &строку меню',
                'show_titlebar': 'Показать &заголовок',
                
                # Insert menu
                'insert_images': '&Изображения...',
                'insert_text': '&Текст',
                
                # Transform menu
                'crop': '&Обрезать',
                'flip_horizontally': 'Отразить &горизонтально',
                'flip_vertically': 'Отразить &вертикально',
                'reset_scale': 'Сбросить &масштаб',
                'reset_rotation': 'Сбросить &поворот',
                'reset_flip': 'Сбросить &отражение',
                'reset_crop': 'Сбросить обрезку',
                'reset_transforms': 'Сбросить &всё',
                
                # Normalize menu
                'normalize_height': '&Высота',
                'normalize_width': '&Ширина',
                'normalize_size': '&Размер',
                
                # Arrange menu
                'arrange_optimal': '&Оптимально',
                'arrange_horizontal': '&Горизонтально',
                'arrange_vertical': '&Вертикально',
                
                # Settings menu
                'open_settings_dir': 'Открыть папку настроек',
                'language_settings': '&Язык',
                'english': 'English',
                'russian': 'Русский',
                
                # Help menu
                'help': '&Справка',
                'about': '&О программе',
                'debuglog': 'Показать &журнал отладки',
                
                # Dialog titles
                'about_title': 'О программе BeeRef',
                'help_title': 'Справка',
                
                # About dialog
                'about_description': 'Простой просмотрщик справочных изображений',
                'about_website': 'Веб-сайт',
                'close_button': 'Закрыть',
                
                # Help dialog
                'controls_title': 'Управление',
                'controls_intro': 'Горячие клавиши и управление мышью:',
                'support_title': 'Поддержка',
                'faq_link': 'Часто задаваемые вопросы',
                'forums_link': 'Форумы',
                'about_link': 'О программе BeeRef',
            }
        }
    
    def get_text(self, key, language=None):
        """Get translated text for a given key."""
        if language is None:
            language = self.current_language
        
        if language in self.translations and key in self.translations[language]:
            return self.translations[language][key]
        elif key in self.translations['en']:
            return self.translations['en'][key]
        else:
            return key
    
    def set_language(self, language):
        """Set the current language."""
        if language in self.translations:
            self.current_language = language
            return True
        return False
    
    def get_available_languages(self):
        """Get list of available languages."""
        return list(self.translations.keys())
    
    def get_language_name(self, language_code):
        """Get the display name for a language code."""
        if language_code in self.translations:
            return self.translations[language_code].get('language_name', language_code)
        return language_code


# Global translator instance
translator = BeeRefTranslator()


def tr(key, language=None):
    """Convenience function to get translated text."""
    return translator.get_text(key, language)
