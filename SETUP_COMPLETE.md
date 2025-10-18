# BeeRef Development Environment Setup Complete! 🎉

## What's Been Installed

✅ **Python 3.13.7** - Already installed on your system  
✅ **PDM 2.26.0** - Modern Python package manager  
✅ **PyQt6 6.9.1** - GUI framework for BeeRef  
✅ **EXIF 1.6.1** - Image metadata handling  
✅ **Rectangle Packer 2.0.4** - Image arrangement algorithm  
✅ **Development Tools** - pytest, flake8, coverage, etc.

## How to Use

### Running BeeRef
```bash
# Method 1: Using the development script
./run_beeref_dev.sh

# Method 2: Using PDM directly
pdm run python -m beeref

# Method 3: With command line arguments
pdm run python -m beeref --help
```

### Running Tests
```bash
# Run all tests
pdm run pytest

# Run specific test file
pdm run pytest tests/test_main.py -v

# Run with coverage
pdm run pytest --cov=beeref
```

### Code Quality Checks
```bash
# Run linting
pdm run flake8

# Run all checks
pdm run pytest && pdm run flake8
```

## Project Structure

- `beeref/` - Main application code
- `tests/` - Test files
- `translations/` - Internationalization files
- `beeref.desktop` - Linux desktop file
- `BeeRef.spec` - PyInstaller spec file
- `pyproject.toml` - Project configuration
- `pdm.lock` - Dependency lock file

## Development Notes

- **Virtual Environment**: Located at `.venv/`
- **Dependencies**: Managed by PDM
- **Python Version**: 3.13.7 (compatible with >=3.9 requirement)
- **GUI Framework**: PyQt6
- **File Format**: SQLite-based `.bee` files

## Troubleshooting

If you encounter issues:

1. **Missing dependencies**: Run `pdm install`
2. **Python version issues**: The project requires Python >=3.9
3. **PyQt6 issues**: Make sure you have the correct Qt libraries installed
4. **Rectangle packer issues**: This was manually installed due to Python 3.13 compatibility

## Next Steps

1. **Run the application**: `./run_beeref_dev.sh`
2. **Explore the code**: Start with `beeref/__main__.py`
3. **Run tests**: `pdm run pytest`
4. **Check code quality**: `pdm run flake8`

Happy coding! 🚀
