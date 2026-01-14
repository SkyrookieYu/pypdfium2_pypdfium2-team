# SPDX-FileCopyrightText: 2026 Sovereign AI Project
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

"""
Main PDF extraction module.

Provides the primary API for extracting text and images from PDF files.
Text and images are kept separate - no image links are inserted into text.
"""

import json
import logging
from pathlib import Path
from typing import Optional

import pypdfium2 as pdfium

from .text_utils import extract_full_text
from .image_utils import extract_images_from_page

logger = logging.getLogger(__name__)


def extract_page(
    page: pdfium.PdfPage,
    page_index: int,
    output_dir: Path,
    pdf_stem: str,
    image_format: str = "auto",
    save_images: bool = True
) -> dict:
    """
    Extract text and images from a single PDF page.

    Args:
        page: PdfPage object
        page_index: 0-based page index
        output_dir: Base output directory for images
        pdf_stem: PDF filename without extension (for image naming)
        image_format: Image output format - "auto", "png", or "jpg"
        save_images: Whether to extract and save images (default: True)

    Returns:
        Dictionary with page data:
        {
            "pageNo": int,
            "width": float,
            "height": float,
            "words": str,
            "images": [{"index": int, "path": str, "bounds": list}, ...]
        }
    """
    page_num = page_index + 1

    # Get page dimensions
    width = page.get_width()
    height = page.get_height()

    # Extract images (if enabled)
    if save_images:
        images = extract_images_from_page(
            page=page,
            page_index=page_index,
            output_dir=output_dir,
            pdf_stem=pdf_stem,
            image_format=image_format
        )
    else:
        images = []

    # Extract text (pure text, no image links)
    text = extract_full_text(page)

    # Build result
    if save_images:
        return {
            "pageNo": page_num,
            "width": width,
            "height": height,
            "words": text,
            "images": [
                {
                    "index": img.index,
                    "path": img.path,
                    "bounds": list(img.bounds)
                }
                for img in images
            ]
        }
    else:
        return {
            "pageNo": page_num,
            "words": text,
        }


def extract_pdf_to_json(
    pdf_path: Path,
    output_dir: Path,
    image_format: str = "auto",
    pages: Optional[list[int]] = None,
    save_json: bool = True,
    save_images: bool = True
) -> list[dict]:
    """
    Extract text and images from a PDF file and output as JSON.

    Text and images are kept separate. Images are saved to disk and their
    metadata is stored in the 'images' field. No image references are
    inserted into the text.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Output directory for JSON and images
        image_format: Image format - "auto" (preserve original), "png", or "jpg"
        pages: List of page numbers to extract (1-based). None for all pages.
        save_json: Whether to save the JSON file to disk
        save_images: Whether to extract and save images (default: True)

    Returns:
        List of page dictionaries:
        [
            {
                "pageNo": 1,
                "width": 612.0,
                "height": 792.0,
                "words": "Pure text content...",
                "images": [{"index": 0, "path": "images/doc_page1_img1.png", "bounds": [...]}]
            },
            ...
        ]
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Processing PDF: {pdf_path}")

    # Get PDF stem for image naming
    pdf_stem = pdf_path.stem

    # Open PDF
    pdf = pdfium.PdfDocument(pdf_path)
    total_pages = len(pdf)

    # Determine which pages to process
    if pages is None:
        page_indices = range(total_pages)
    else:
        # Convert 1-based page numbers to 0-based indices
        page_indices = [p - 1 for p in pages if 0 < p <= total_pages]

    result = []

    for page_index in page_indices:
        logger.info(f"Processing page {page_index + 1}/{total_pages}")

        page = pdf[page_index]
        page_data = extract_page(
            page=page,
            page_index=page_index,
            output_dir=output_dir,
            pdf_stem=pdf_stem,
            image_format=image_format,
            save_images=save_images
        )
        result.append(page_data)

    # Save JSON
    if save_json:
        suffix = "w-images" if save_images else "wo-images"
        json_filename = f"{pdf_path.stem}-{suffix}.json"
        json_path = output_dir / json_filename

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved JSON to: {json_path}")

    logger.info(f"Extraction complete. Processed {len(result)} pages.")

    return result
