# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pypdfium2 is an ABI-level Python 3 binding to PDFium, a powerful PDF rendering, inspection, manipulation and creation library. It is built with ctypesgen (pypdfium2-team fork) and external PDFium binaries from pdfium-binaries.

## Commands

Uses the `just` command runner (modern alternative to make). Run `just -l` to list all commands.

### Testing
```bash
just test                              # Run all tests
just test -sv                          # Verbose with stdout
just test tests/test_document.py       # Single module
just test tests/test_document.py::test_open_path  # Single test
just test -k "test_open"               # Pattern matching
just coverage                          # Tests with coverage report
```

Set `DEBUG_AUTOCLOSE=1` for debugging automatic object finalization.

### Code Quality
```bash
just check      # autoflake (unused imports), codespell, reuse lint (SPDX)
just distcheck  # twine check + check-wheel-contents on dist/*
```

### Build/Packaging
```bash
just build-native [args]      # Build PDFium natively (lean, system deps)
just build-toolchained [args] # Build PDFium with Google toolchain
just update [args]            # Download binaries from pdfium-binaries
just emplace [args]           # Stage files for packaging
just craft [args]             # Create wheel packages
just packaging-pypi           # Full release: clean, check, update-verify, craft, distcheck
just clean                    # Clean build artifacts
```

### Documentation
```bash
just docs-build   # Build HTML docs with Sphinx
just docs-open    # Open docs in browser
just docs-clean   # Clean docs build
```

## Architecture

### Two-Level API Design

1. **High-level helpers** (`src/pypdfium2/_helpers/`) - User-friendly Python classes:
   - `PdfDocument` - Main entry point for opening/creating PDFs
   - `PdfPage` - Page operations (rendering, text extraction)
   - `PdfBitmap` - Image rendering and conversion
   - `PdfTextPage` - Text extraction and search
   - `PdfObject` - Page object handling
   - `PdfMatrix` - Transformation matrices

2. **Raw ctypes API** (`src/pypdfium2_raw/`) - Direct C API access via auto-generated bindings

```python
import pypdfium2 as pdfium           # Helper API
import pypdfium2.raw as pdfium_c     # Raw ctypes API
import pypdfium2.internal as pdfium_i  # Internal utilities
```

### Key Directories

- `src/pypdfium2/_helpers/` - High-level wrapper classes
- `src/pypdfium2/_cli/` - Command-line interface subcommands
- `src/pypdfium2/internal/` - Base classes (`AutoCloseable`, `AutoCastable`), constants, utilities
- `src/pypdfium2_raw/` - Auto-generated ctypes bindings
- `setupsrc/` - Build infrastructure (update.py, build_native.py, build_toolchained.py, craft.py, autorelease.py)
- `tests/resources/` - Test PDF files
- `tests/expectations/` - Expected test outputs

### Resource Management

Uses `AutoCloseable` base class with `weakref.finalize()` for automatic cleanup. Context manager (`with` statements) supported. Helpers expose their underlying raw objects via `.raw` attribute and auto-resolve when passed to raw API functions.

## Build System

Controlled via `PDFIUM_PLATFORM` environment variable:
- `auto` - Auto-detect platform, use prebuilt binary (default)
- `system-search` - Use system-installed PDFium
- `sourcebuild` - Use pre-staged files from `data/sourcebuild/`
- `sourcebuild-native` / `sourcebuild-toolchained` - Trigger build scripts

Other key env vars: `BUILD_PARAMS` (native build options), `PYPDFIUM_MODULES` (modules to include), `PDFIUM_BINDINGS=reference` (use reference bindings).

## Development Environment

Conda/virtual environment name: `pypdfium2`

## Development Notes

- **No hard line wrapping**: The codebase does not hard wrap long lines. Use editor word wrap (recommended: 100 columns)
- **Thread safety**: PDFium is not thread-safe
- **Optional deps**: Pillow, NumPy, opencv-python for image operations (deferred imports)
