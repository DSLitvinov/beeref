# BeeRef Localization System

This document describes the localization system implemented in BeeRef to support multiple languages and translations.

## Overview

BeeRef now supports a comprehensive localization system that allows the application interface to be translated into multiple languages. The system is designed to be:

- **Extensible**: Easy to add new languages
- **Maintainable**: Clear separation between code and translations
- **Robust**: Fallback mechanisms for missing translations
- **Developer-friendly**: Tools to manage and validate translations

## Architecture

### Core Components

1. **`beeref/localization.py`**: Main localization module
   - `BeeRefTranslator` class: Handles translation loading and management
   - `tr()` function: Convenience function for getting translations
   - Built-in English translations as fallback

2. **`translations/` directory**: External translation files
   - JSON format for easy editing
   - One file per language (e.g., `ru.json` for Russian)
   - Template file for new translations

3. **`scripts/translation_manager.py`**: Management utility
   - Extract translation keys from codebase
   - Generate translation templates
   - Validate translation files
   - Show translation statistics

## Usage

### For Users

Users can change the language through the application settings:
- Go to Settings → Language
- Select desired language
- The interface will update immediately

### For Developers

#### Adding New Translation Keys

1. Add the key to the built-in English translations in `beeref/localization.py`:
   ```python
   'new_key': 'English text',
   ```

2. Use the key in your code:
   ```python
   from beeref.localization import tr
   
   label.setText(tr('new_key'))
   ```

3. Update all existing translation files with the new key

#### Adding a New Language

1. Generate a translation template:
   ```bash
   python3 scripts/translation_manager.py template --language es
   ```

2. Translate all values in the generated `es.json` file

3. Test the translation in the application

#### Managing Translations

Use the translation manager script:

```bash
# Show translation statistics
python3 scripts/translation_manager.py stats

# Validate all translation files
python3 scripts/translation_manager.py validate

# Extract all translation keys from codebase
python3 scripts/translation_manager.py extract

# Generate a new translation template
python3 scripts/translation_manager.py template --language fr
```

## File Structure

```
beeref/
├── localization.py          # Main localization module
├── translations/            # Translation files directory
│   ├── README.md           # Translation guidelines
│   ├── template.json       # Template for new translations
│   └── ru.json            # Russian translations
└── scripts/
    └── translation_manager.py  # Management utility
```

## Translation File Format

Translation files are in JSON format with UTF-8 encoding:

```json
{
  "drag_drop_text": "Drag and drop images here",
  "or_text": "or",
  "browse_button": "Browse",
  "help_link": "Help"
}
```

### Key Naming Convention

- Use descriptive, lowercase names with underscores
- Group related keys with prefixes (e.g., `controls_*`, `menu_*`)
- Keep keys in English for consistency

### Translation Guidelines

- Maintain consistency in terminology
- Consider cultural differences in UI text
- Keep translations concise but clear
- Test translations in the actual application
- Use proper Unicode encoding for special characters

## Implementation Details

### Translation Loading

1. Built-in English translations are loaded first as fallback
2. External translation files are loaded from the `translations/` directory
3. Missing translations fall back to English
4. Missing keys return the key itself (with warning)

### Language Detection

- Language preference is stored in application settings
- Default language is English
- Language can be changed at runtime

### Build System Integration

Translation files are included in the PyInstaller build:
- All `.json` files from the `translations/` directory are bundled
- Translations are available in the packaged application

## Current Status

### Implemented Features

- ✅ Core localization framework
- ✅ JSON-based translation files
- ✅ Built-in English translations
- ✅ Russian translation
- ✅ Translation management tools
- ✅ Build system integration
- ✅ All UI components localized

### Localized Components

- Menu system (all menus and actions)
- Welcome screen
- About dialog
- Help dialog
- Debug log dialog
- Recent files list
- All button and label text

### Available Languages

- **English (en)**: Complete, built-in fallback
- **Russian (ru)**: Complete translation
- **Belarusian (be)**: Complete translation
- **Spanish (es)**: Complete translation
- **German (de)**: Complete translation
- **Italian (it)**: Complete translation

### Dynamic Language Detection

The system now automatically detects and includes new translation files in the language settings menu. When you add a new `.json` translation file to the `translations/` directory, it will automatically appear in the Settings → Language menu without requiring any code changes.

## Future Enhancements

### Planned Features

- [ ] Qt Linguist integration for professional translation tools
- [ ] Plural forms support
- [ ] Context-aware translations
- [ ] Translation memory integration
- [ ] Online translation management

### Additional Languages

The system is ready to support additional languages. To add a new language:

1. Create a new translation file
2. Translate all keys
3. Test thoroughly
4. Submit for inclusion

## Contributing

### For Translators

1. Use the translation template as a starting point
2. Follow the translation guidelines
3. Test your translations in the application
4. Submit translation files for review

### For Developers

1. Always use the `tr()` function for user-visible text
2. Add new keys to the built-in English translations
3. Update all existing translation files
4. Use the validation tools before committing

## Troubleshooting

### Common Issues

1. **Missing translations**: Check that all keys are present in translation files
2. **Encoding issues**: Ensure files are saved with UTF-8 encoding
3. **Invalid JSON**: Use a JSON validator to check file syntax
4. **Build issues**: Verify translation files are included in build configuration

### Validation

Always run validation before committing:
```bash
python3 scripts/translation_manager.py validate
```

This will check for:
- Missing translation keys
- Extra keys not used in code
- Empty translation values
- JSON syntax errors

## Conclusion

The BeeRef localization system provides a solid foundation for supporting multiple languages. It's designed to be maintainable, extensible, and developer-friendly while providing a good user experience for international users.

The system is ready for production use and can easily accommodate new languages and features as the application evolves.
