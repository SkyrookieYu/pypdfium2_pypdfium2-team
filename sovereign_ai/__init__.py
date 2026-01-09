# SPDX-FileCopyrightText: 2026 Sovereign AI Project
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

"""
Sovereign AI - PDF Text and Image Extraction Module

This module provides functionality to extract text and images from PDF files,
with position-aware image link insertion in the extracted text.

Usage:
    from sovereign_ai import extract_pdf_to_json

    result = extract_pdf_to_json(
        pdf_path=Path("input.pdf"),
        output_dir=Path("output"),
        include_image_links=True
    )
"""

from .pdf_extractor import extract_pdf_to_json, extract_page

__all__ = ["extract_pdf_to_json", "extract_page"]
__version__ = "0.1.0"
