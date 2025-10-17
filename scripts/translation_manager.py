#!/usr/bin/env python3
"""
Translation management utility for BeeRef.

This script helps manage translations by:
- Extracting translation keys from the codebase
- Creating translation templates
- Validating translation files
- Generating translation statistics
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path
from typing import Dict, List, Set

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import translator without PyQt6 dependencies
import json
from pathlib import Path

class MockTranslator:
    """Mock translator for script usage without PyQt6."""
    
    def __init__(self):
        self.translations = {}
        self.translations_dir = project_root / 'translations'
        self._load_builtin_translations()
        self._load_external_translations()
    
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
            except Exception as e:
                logger.warning(f"Failed to load translation file {translation_file}: {e}")
    
    def save_translation_template(self, language_code: str = 'template') -> bool:
        """Save a translation template file for a new language."""
        try:
            template_file = self.translations_dir / f'{language_code}.json'
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(self.translations['en'], f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to save translation template: {e}")
            return False
    
    def get_available_languages(self):
        """Get list of available languages."""
        return list(self.translations.keys())

translator = MockTranslator()

logger = logging.getLogger(__name__)


def extract_translation_keys() -> Set[str]:
    """Extract all translation keys used in the codebase."""
    keys = set()
    
    # Pattern to match tr('key') or tr("key") calls
    tr_pattern = re.compile(r'\btr\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)')
    
    # Search in Python files
    for py_file in project_root.rglob('*.py'):
        if py_file.name == 'translation_manager.py':
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = tr_pattern.findall(content)
                keys.update(matches)
        except Exception as e:
            logger.warning(f"Could not read {py_file}: {e}")
    
    return keys


def validate_translation_file(file_path: Path, reference_keys: Set[str]) -> Dict[str, List[str]]:
    """Validate a translation file against reference keys."""
    issues = {
        'missing_keys': [],
        'extra_keys': [],
        'empty_values': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
        
        # Check for missing keys
        for key in reference_keys:
            if key not in translations:
                issues['missing_keys'].append(key)
        
        # Check for extra keys
        for key in translations:
            if key not in reference_keys:
                issues['extra_keys'].append(key)
        
        # Check for empty values
        for key, value in translations.items():
            if not value or value.strip() == '':
                issues['empty_values'].append(key)
                
    except Exception as e:
        logger.error(f"Error validating {file_path}: {e}")
    
    return issues


def generate_translation_template(language_code: str = 'template') -> bool:
    """Generate a translation template file."""
    return translator.save_translation_template(language_code)


def print_translation_stats():
    """Print statistics about available translations."""
    available_languages = translator.get_available_languages()
    reference_keys = extract_translation_keys()
    
    print(f"Available languages: {', '.join(available_languages)}")
    print(f"Total translation keys: {len(reference_keys)}")
    print()
    
    for lang in available_languages:
        lang_translations = translator.translations.get(lang, {})
        translated_count = sum(1 for v in lang_translations.values() if v and v.strip())
        total_count = len(reference_keys)
        coverage = (translated_count / total_count * 100) if total_count > 0 else 0
        
        print(f"{lang}: {translated_count}/{total_count} ({coverage:.1f}%)")
        
        # Show missing keys
        missing = [k for k in reference_keys if k not in lang_translations or not lang_translations[k]]
        if missing:
            print(f"  Missing: {', '.join(missing[:5])}{'...' if len(missing) > 5 else ''}")


def validate_all_translations():
    """Validate all translation files."""
    reference_keys = extract_translation_keys()
    translations_dir = project_root / 'translations'
    
    if not translations_dir.exists():
        print("No translations directory found")
        return
    
    print(f"Validating translations against {len(reference_keys)} reference keys...")
    print()
    
    for translation_file in translations_dir.glob('*.json'):
        if translation_file.name == 'template.json':
            continue
            
        print(f"Validating {translation_file.name}:")
        issues = validate_translation_file(translation_file, reference_keys)
        
        if not any(issues.values()):
            print("  ✓ All good!")
        else:
            if issues['missing_keys']:
                print(f"  ✗ Missing keys: {len(issues['missing_keys'])}")
            if issues['extra_keys']:
                print(f"  ⚠ Extra keys: {len(issues['extra_keys'])}")
            if issues['empty_values']:
                print(f"  ✗ Empty values: {len(issues['empty_values'])}")
        print()


def main():
    parser = argparse.ArgumentParser(description='BeeRef Translation Manager')
    parser.add_argument('command', choices=['extract', 'template', 'validate', 'stats'],
                       help='Command to execute')
    parser.add_argument('--language', '-l', default='template',
                       help='Language code for template generation')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    if args.command == 'extract':
        keys = extract_translation_keys()
        print("Translation keys found in codebase:")
        for key in sorted(keys):
            print(f"  {key}")
        print(f"\nTotal: {len(keys)} keys")
    
    elif args.command == 'template':
        if generate_translation_template(args.language):
            print(f"Translation template saved as {args.language}.json")
        else:
            print("Failed to generate translation template")
            sys.exit(1)
    
    elif args.command == 'validate':
        validate_all_translations()
    
    elif args.command == 'stats':
        print_translation_stats()


if __name__ == '__main__':
    main()
