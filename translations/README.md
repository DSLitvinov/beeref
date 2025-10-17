# BeeRef Translations

This directory contains translation files for BeeRef in JSON format.

## File Format

Each translation file is named `{language_code}.json` (e.g., `ru.json` for Russian) and contains a JSON object with translation keys and their corresponding translated text.

Example:
```json
{
  "drag_drop_text": "Drag and drop images here",
  "or_text": "or",
  "browse_button": "Browse"
}
```

## Adding a New Translation

1. Copy the `template.json` file to `{language_code}.json`
2. Translate all the values while keeping the keys unchanged
3. Test the translation by running BeeRef with the new language

## Translation Management

Use the translation manager script to help with translation tasks:

```bash
# Generate a new translation template
python scripts/translation_manager.py template --language es

# Validate all translation files
python scripts/translation_manager.py validate

# Show translation statistics
python scripts/translation_manager.py stats

# Extract all translation keys from the codebase
python scripts/translation_manager.py extract
```

## Guidelines

- Keep translation keys in English and descriptive
- Maintain consistency in terminology
- Test translations in the actual application
- Consider cultural differences in UI text
- Keep translations concise but clear

## Available Languages

- `en` - English (built-in, fallback)
- `ru` - Russian
- `be` - Belarusian
- `es` - Spanish
- `de` - German
- `it` - Italian

## Dynamic Language Detection

The application now automatically detects new translation files and includes them in the language settings menu. Simply add a new `.json` file to this directory and it will appear in the Settings → Language menu without any code changes required.

## Contributing

When adding new translation keys to the codebase:

1. Add the key to the built-in English translations in `beeref/localization.py`
2. Update all existing translation files with the new key
3. Use the translation manager to validate all files
