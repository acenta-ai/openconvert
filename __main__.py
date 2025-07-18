#!/usr/bin/env python3
"""
OpenConvert CLI Module Entry Point

Allows running the OpenConvert CLI as a module:
    python -m openconvert -i input.txt -o output.pdf
"""

import sys
from .openconvert_cli import main

if __name__ == "__main__":
    sys.exit(main()) 