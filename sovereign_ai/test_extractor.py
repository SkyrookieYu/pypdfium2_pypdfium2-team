#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Sovereign AI Project
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

"""
Test script for sovereign_ai module.

Run from pypdfium2 root directory:
    python -m sovereign_ai.test_extractor

Or from sovereign_ai directory:
    cd sovereign_ai && python test_extractor.py
"""

import sys
import tempfile
from pathlib import Path

# Add parent directory to path if running directly
if __name__ == "__main__":
    parent_dir = Path(__file__).parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

from sovereign_ai import extract_pdf_to_json


def test_extraction():
    """Test PDF extraction with test files."""
    # Find test resources directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    test_resources = project_root / "tests" / "resources"

    if not test_resources.exists():
        print(f"Error: Test resources not found at {test_resources}")
        sys.exit(1)

    # Test files to process
    test_files = [
        "images.pdf",      # Has images
        "render.pdf",      # Text only
        "text.pdf",        # Multi-page text
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        for pdf_name in test_files:
            pdf_path = test_resources / pdf_name
            if not pdf_path.exists():
                print(f"⚠ Skipping {pdf_name} (not found)")
                continue

            print(f"\n{'='*50}")
            print(f"Testing: {pdf_name}")
            print('='*50)

            try:
                result = extract_pdf_to_json(
                    pdf_path=pdf_path,
                    output_dir=output_dir / pdf_path.stem,
                    save_json=True
                )

                # Print summary
                total_images = sum(len(page["images"]) for page in result)
                print(f"✓ Pages: {len(result)}")
                print(f"✓ Images: {total_images}")

                # Show first page preview
                if result:
                    words_preview = result[0]["words"][:100]
                    if len(result[0]["words"]) > 100:
                        words_preview += "..."
                    print(f"✓ Page 1 preview: {words_preview!r}")

            except Exception as e:
                print(f"✗ Error: {e}")
                import traceback
                traceback.print_exc()

    print(f"\n{'='*50}")
    print("All tests completed!")
    print('='*50)


if __name__ == "__main__":
    test_extraction()
