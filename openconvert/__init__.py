"""
OpenConvert CLI Tool

A command-line interface for connecting to the OpenConvert OpenAgents network
to discover file conversion services and perform file conversions.
"""

import asyncio
from pathlib import Path
from typing import Optional, List

__version__ = "1.0.0"
__author__ = "OpenAgents Team"
__email__ = "team@openagents.com"

# Import the async convert function
try:
    from .openconvert_cli import convert as _async_convert
except ImportError:
    from openconvert_cli import convert as _async_convert


def convert(
    input_files: List[Path],
    output_path: Path,
    from_format: Optional[str] = None,
    to_format: Optional[str] = None,
    prompt: Optional[str] = None,
    host: str = "localhost",
    port: int = 8765
) -> bool:
    """Convert files using the OpenConvert network.
    
    This is a synchronous wrapper around the async convert function.
    
    Args:
        input_files: List of input file paths
        output_path: Output file or directory path
        from_format: Source MIME type (optional, will be detected)
        to_format: Target MIME type (optional, will be detected from output extension)
        prompt: Optional conversion prompt
        host: Network host to connect to
        port: Network port to connect to
        
    Returns:
        bool: True if conversion succeeded
        
    Example:
        >>> from openconvert import convert
        >>> from pathlib import Path
        >>> success = convert(
        ...     input_files=[Path("document.txt")],
        ...     output_path=Path("document.pdf")
        ... )
    """
    return asyncio.run(_async_convert(
        input_files=input_files,
        output_path=output_path,
        from_format=from_format,
        to_format=to_format,
        prompt=prompt,
        host=host,
        port=port
    ))


def convert_file(
    input_file: str,
    output_file: str,
    from_format: Optional[str] = None,
    to_format: Optional[str] = None,
    prompt: Optional[str] = None,
    host: str = "localhost",
    port: int = 8765
) -> bool:
    """Convert a single file using the OpenConvert network.
    
    Convenience function for single file conversions with string paths.
    
    Args:
        input_file: Input file path (string)
        output_file: Output file path (string)
        from_format: Source MIME type (optional, will be detected)
        to_format: Target MIME type (optional, will be detected from output extension)
        prompt: Optional conversion prompt
        host: Network host to connect to
        port: Network port to connect to
        
    Returns:
        bool: True if conversion succeeded
        
    Example:
        >>> from openconvert import convert_file
        >>> success = convert_file("document.txt", "document.pdf")
        >>> success = convert_file(
        ...     "data.csv", 
        ...     "report.pdf", 
        ...     prompt="Create a professional report"
        ... )
    """
    return convert(
        input_files=[Path(input_file)],
        output_path=Path(output_file),
        from_format=from_format,
        to_format=to_format,
        prompt=prompt,
        host=host,
        port=port
    )


__all__ = ["convert", "convert_file"] 