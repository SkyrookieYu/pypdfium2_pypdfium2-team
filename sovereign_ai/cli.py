# SPDX-FileCopyrightText: 2026 Sovereign AI Project
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

"""
Command-line interface for Sovereign AI PDF extraction.
"""

import argparse
import logging
import sys
from pathlib import Path

from .pdf_extractor import extract_pdf_to_json


def setup_logging(verbose: bool = False):
    """Configure logging for CLI."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="sovereign_ai",
        description="Extract text and images from PDF files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic extraction
  python -m sovereign_ai.cli input.pdf -o output/

  # Force PNG format for all images
  python -m sovereign_ai.cli input.pdf -o output/ --image-format png

  # Extract specific pages only
  python -m sovereign_ai.cli input.pdf -o output/ --pages 1,3,5
"""
    )

    parser.add_argument(
        "pdf",
        type=Path,
        help="Input PDF file path"
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        required=True,
        help="Output directory for JSON and images"
    )

    parser.add_argument(
        "--image-format",
        choices=["auto", "png", "jpg"],
        default="auto",
        help="Output format for images (default: auto - preserve original)"
    )

    parser.add_argument(
        "--pages",
        type=str,
        default=None,
        help="Comma-separated list of page numbers to extract (1-based). Default: all pages"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    return parser.parse_args()


def parse_pages(pages_str: str) -> list[int]:
    """Parse comma-separated page numbers."""
    if not pages_str:
        return None

    pages = []
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            # Range: "1-5"
            start, end = part.split("-", 1)
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))

    return sorted(set(pages))


def main():
    """Main entry point for CLI."""
    args = parse_args()
    setup_logging(args.verbose)

    # Validate input
    if not args.pdf.exists():
        print(f"Error: PDF file not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    if not args.pdf.suffix.lower() == ".pdf":
        print(f"Warning: File does not have .pdf extension: {args.pdf}", file=sys.stderr)

    # Parse pages
    pages = parse_pages(args.pages)

    # Run extraction
    try:
        result = extract_pdf_to_json(
            pdf_path=args.pdf,
            output_dir=args.output,
            image_format=args.image_format,
            pages=pages
        )

        # Print summary
        total_images = sum(len(page["images"]) for page in result)
        print(f"\nExtraction complete:")
        print(f"  Pages processed: {len(result)}")
        print(f"  Images extracted: {total_images}")
        print(f"  Output directory: {args.output}")
        print(f"  JSON file: {args.output / (args.pdf.stem + '.json')}")

    except Exception as e:
        logging.error(f"Extraction failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
