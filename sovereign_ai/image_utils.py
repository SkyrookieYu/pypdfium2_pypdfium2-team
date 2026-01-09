# SPDX-FileCopyrightText: 2026 Sovereign AI Project
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

"""
Image extraction utilities for PDF pages.
"""

import logging
from dataclasses import dataclass
from pathlib import Path

import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c

logger = logging.getLogger(__name__)


@dataclass
class ImageInfo:
    """Represents an extracted image with its metadata."""
    index: int           # Image index within the page
    filename: str        # Saved filename (e.g., "page1_img1.png")
    path: str            # Relative path from output dir (e.g., "images/page1_img1.png")
    bounds: tuple        # (left, bottom, right, top) in PDF coordinates
    y_center: float      # Center Y coordinate for positioning


def extract_images_from_page(
    page: pdfium.PdfPage,
    page_index: int,
    output_dir: Path,
    pdf_stem: str,
    max_depth: int = 15,
    image_format: str = "auto"
) -> list[ImageInfo]:
    """
    Extract all images from a PDF page and save them to disk.

    Args:
        page: PdfPage object
        page_index: 0-based page index
        output_dir: Base output directory
        pdf_stem: PDF filename without extension (for image naming)
        max_depth: Maximum recursion depth for nested objects
        image_format: Output format - "auto" (preserve original), "png", or "jpg"

    Returns:
        List of ImageInfo objects with metadata about extracted images
    """
    # Create images subdirectory
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Get all image objects from the page
    image_objects = list(page.get_objects(
        filter=(pdfium_c.FPDF_PAGEOBJ_IMAGE,),
        max_depth=max_depth
    ))

    extracted_images = []
    page_num = page_index + 1  # 1-based for filenames

    for img_index, image_obj in enumerate(image_objects):
        img_num = img_index + 1

        try:
            # Get image bounds (position on page)
            bounds = image_obj.get_bounds()  # (left, bottom, right, top)
            left, bottom, right, top = bounds

            # Calculate center Y for positioning
            y_center = (top + bottom) / 2

            # Determine output filename with PDF stem prefix
            base_name = f"{pdf_stem}_page{page_num}_img{img_num}"

            if image_format == "auto":
                # Use smart extraction which preserves original format
                output_path = images_dir / base_name
                try:
                    image_obj.extract(output_path)
                    # Find the actual saved file (extract adds extension)
                    saved_files = list(images_dir.glob(f"{base_name}.*"))
                    if saved_files:
                        actual_filename = saved_files[0].name
                    else:
                        # Fallback to bitmap extraction
                        actual_filename = _extract_as_bitmap(
                            image_obj, images_dir, base_name, "png"
                        )
                except Exception as e:
                    logger.warning(f"Smart extraction failed for {base_name}: {e}")
                    actual_filename = _extract_as_bitmap(
                        image_obj, images_dir, base_name, "png"
                    )
            else:
                # Force specific format using bitmap
                actual_filename = _extract_as_bitmap(
                    image_obj, images_dir, base_name, image_format
                )

            # Create ImageInfo
            relative_path = f"images/{actual_filename}"
            extracted_images.append(ImageInfo(
                index=img_index,
                filename=actual_filename,
                path=relative_path,
                bounds=bounds,
                y_center=y_center
            ))

            logger.debug(f"Extracted image: {actual_filename} at bounds {bounds}")

        except Exception as e:
            logger.error(f"Failed to extract image {img_index} from page {page_num}: {e}")
            continue
        finally:
            # Close the image object to free resources
            image_obj.close()

    # Sort by Y position (top to bottom in reading order)
    # Higher Y is at top in PDF coordinates, so sort descending
    extracted_images.sort(key=lambda img: -img.y_center)

    return extracted_images


def _extract_as_bitmap(
    image_obj: pdfium.PdfImage,
    output_dir: Path,
    base_name: str,
    format: str
) -> str:
    """
    Extract image as bitmap and save in specified format.

    Args:
        image_obj: PdfImage object
        output_dir: Directory to save the image
        base_name: Base filename without extension
        format: Output format (png, jpg, etc.)

    Returns:
        Actual saved filename with extension
    """
    bitmap = image_obj.get_bitmap(render=False)
    pil_image = bitmap.to_pil()

    filename = f"{base_name}.{format}"
    output_path = output_dir / filename

    # Handle format-specific options
    if format.lower() in ("jpg", "jpeg"):
        # Convert RGBA to RGB for JPEG
        if pil_image.mode == "RGBA":
            pil_image = pil_image.convert("RGB")
        pil_image.save(output_path, format="JPEG", quality=95)
    else:
        pil_image.save(output_path, format=format.upper())

    return filename
