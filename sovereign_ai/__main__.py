# SPDX-FileCopyrightText: 2026 Sovereign AI Project
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

"""
Entry point for running sovereign_ai as a module.

Usage:
    python -m sovereign_ai input.pdf -o output/
"""

from .cli import main

if __name__ == "__main__":
    main()
