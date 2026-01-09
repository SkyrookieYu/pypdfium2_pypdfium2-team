# SPDX-FileCopyrightText: 2026 Sovereign AI Project
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

"""
Text extraction utilities for PDF pages.
"""

import pypdfium2 as pdfium


def extract_full_text(page: pdfium.PdfPage) -> str:
    """
    Extract full text from a page.

    Args:
        page: PdfPage object

    Returns:
        Full text content of the page
    """
    textpage = page.get_textpage()
    text = textpage.get_text_bounded()
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text
