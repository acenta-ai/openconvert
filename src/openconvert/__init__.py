"""
OpenConvert CLI Tool

A command-line interface for connecting to the OpenConvert OpenAgents network
to discover file conversion services and perform file conversions.
"""

import asyncio
from pathlib import Path
from typing import Optional, List

__version__ = "1.1.1"
__author__ = "OpenAgents Team"
__email__ = "team@openagents.com"

# Import the async convert function
try:
    from openconvert.openconvert_cli import convert as _async_convert
except ImportError:
    from openconvert_cli import convert as _async_convert


def convert(
    input_files: List[Path],
    output_path: Path,
    host: str = "network.openconvert.ai",
    port: int = 8765,
) -> bool:
    """
    Convert files using the OpenConvert network.
    
    Args:
        input_files: List of input file paths to convert
        output_path: Output file path  
        host: OpenConvert network host (default: network.openconvert.ai)
        port: OpenConvert network port (default: 8765)
        
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        result = asyncio.run(_async_convert(
            input_files=input_files,
            output_path=output_path,
            host=host,
            port=port
        ))
        return result
    except Exception as e:
        print(f"Conversion failed: {e}")
        return False


def convert_file(
    input_path: str, 
    output_path: str,
    host: str = "network.openconvert.ai",
    port: int = 8765
) -> bool:
    """
    Convert a single file using the OpenConvert network.
    
    Args:
        input_path: Path to input file
        output_path: Path for output file
        host: OpenConvert network host (default: network.openconvert.ai)
        port: OpenConvert network port (default: 8765)
        
    Returns:
        bool: True if conversion successful, False otherwise
        
    Example:
        >>> from openconvert import convert_file
        >>> success = convert_file("document.txt", "document.pdf")
        >>> if success:
        ...     print("Conversion completed!")
    """
    try:
        input_files = [Path(input_path)]
        output_file = Path(output_path)
        
        return convert(
            input_files=input_files,
            output_path=output_file,
            host=host,
            port=port
        )
    except Exception as e:
        print(f"File conversion failed: {e}")
        return False


# Export main functions
__all__ = [
    "convert",
    "convert_file",
    "__version__",
    "__author__",
    "__email__",
] 