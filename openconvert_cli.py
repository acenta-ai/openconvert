#!/usr/bin/env python3
"""
OpenConvert CLI Tool

A command-line interface for connecting to the OpenConvert OpenAgents network
to discover file conversion services and perform file conversions.

Usage:
    openconvert -i input.png -o output.pdf
    openconvert -i input_dir/ -o output.pdf --from image/png --to application/pdf
    openconvert -i input.txt -o output.md --prompt "Add a title and format nicely"
"""

import argparse
import asyncio
import logging
import sys
import os
import mimetypes
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add the openagents src to Python path
current_dir = Path(__file__).resolve().parent
openagents_root = current_dir.parent.parent
sys.path.insert(0, str(openagents_root / "src"))

try:
    from .client import OpenConvertClient
except ImportError:
    from client import OpenConvertClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def detect_mime_type(file_path: Path) -> str:
    """Detect MIME type of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: MIME type string
    """
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type is None:
        # Fall back to common extensions
        ext = file_path.suffix.lower()
        common_types = {
            '.txt': 'text/plain',
            '.md': 'text/markdown', 
            '.html': 'text/html',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.svg': 'image/svg+xml',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.zip': 'application/zip',
            '.rar': 'application/x-rar-compressed',
        }
        mime_type = common_types.get(ext, 'application/octet-stream')
    
    return mime_type


def validate_args(args: argparse.Namespace) -> bool:
    """Validate command-line arguments.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        bool: True if arguments are valid
    """
    # Check input exists
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input path does not exist: {input_path}")
        return False
    
    # Validate output path
    output_path = Path(args.output)
    output_dir = output_path.parent
    if not output_dir.exists():
        logger.error(f"Output directory does not exist: {output_dir}")
        return False
    
    # If input is a directory, require --from and --to
    if input_path.is_dir():
        if not args.from_format or not args.to_format:
            logger.error("When input is a directory, --from and --to formats must be specified")
            return False
    
    return True


def get_input_files(input_path: Path, from_format: Optional[str] = None) -> List[Path]:
    """Get list of input files to process.
    
    Args:
        input_path: Input file or directory path
        from_format: Optional MIME type filter for directory scanning
        
    Returns:
        List of file paths to process
    """
    if input_path.is_file():
        return [input_path]
    
    elif input_path.is_dir():
        files = []
        for file_path in input_path.rglob('*'):
            if file_path.is_file():
                # If from_format is specified, filter by MIME type
                if from_format:
                    file_mime = detect_mime_type(file_path)
                    if file_mime == from_format:
                        files.append(file_path)
                else:
                    files.append(file_path)
        return files
    
    return []


async def convert_files(
    input_files: List[Path],
    output_path: Path,
    from_format: Optional[str] = None,
    to_format: Optional[str] = None,
    prompt: Optional[str] = None,
    host: str = "localhost",
    port: int = 8765
) -> bool:
    """Convert files using the OpenConvert network.
    
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
    """
    client = OpenConvertClient()
    
    try:
        # Connect to the network
        logger.info(f"Connecting to OpenConvert network at {host}:{port}")
        await client.connect(host=host, port=port)
        
        # Process each input file
        success_count = 0
        total_files = len(input_files)
        
        for i, input_file in enumerate(input_files, 1):
            logger.info(f"Processing file {i}/{total_files}: {input_file.name}")
            
            # Detect source format if not specified
            source_format = from_format or detect_mime_type(input_file)
            
            # Detect target format if not specified
            if to_format:
                target_format = to_format
            else:
                target_format = detect_mime_type(output_path)
            
            logger.info(f"Converting {source_format} -> {target_format}")
            
            # Determine output file path
            if len(input_files) == 1:
                # Single file conversion
                output_file = output_path
            else:
                # Multiple files - create output directory if needed
                if output_path.suffix:
                    # Output path has extension, treat as directory name
                    output_dir = output_path.parent / output_path.stem
                else:
                    # Output path is a directory
                    output_dir = output_path
                
                output_dir.mkdir(parents=True, exist_ok=True)
                
                # Generate output filename with target extension
                target_ext = None
                for ext, mime in mimetypes.types_map.items():
                    if mime == target_format:
                        target_ext = ext
                        break
                
                if not target_ext:
                    # Fall back to common extensions
                    ext_map = {
                        'text/plain': '.txt',
                        'text/markdown': '.md',
                        'text/html': '.html',
                        'application/pdf': '.pdf',
                        'image/png': '.png',
                        'image/jpeg': '.jpg',
                        'application/json': '.json',
                    }
                    target_ext = ext_map.get(target_format, '.out')
                
                output_file = output_dir / f"{input_file.stem}{target_ext}"
            
            # Perform conversion
            try:
                success = await client.convert_file(
                    input_file=input_file,
                    output_file=output_file,
                    source_format=source_format,
                    target_format=target_format,
                    prompt=prompt
                )
                
                if success:
                    logger.info(f"✅ Successfully converted to {output_file}")
                    success_count += 1
                else:
                    logger.error(f"❌ Failed to convert {input_file.name}")
                    
            except Exception as e:
                logger.error(f"❌ Error converting {input_file.name}: {e}")
        
        # Report results
        if success_count == total_files:
            logger.info(f"🎉 All {total_files} files converted successfully!")
            return True
        elif success_count > 0:
            logger.info(f"⚠️  {success_count}/{total_files} files converted successfully")
            return True
        else:
            logger.error(f"❌ No files were converted successfully")
            return False
            
    except Exception as e:
        logger.error(f"Error during conversion: {e}")
        return False
        
    finally:
        await client.disconnect()


def main() -> int:
    """Main CLI entry point.
    
    Returns:
        int: Exit code (0 = success, 1 = error)
    """
    parser = argparse.ArgumentParser(
        description="OpenConvert CLI - Connect to OpenAgents network for file conversion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single file (formats auto-detected)
  openconvert -i document.txt -o document.pdf
  
  # Convert directory with specific formats
  openconvert -i images/ -o converted/ --from image/png --to application/pdf
  
  # Convert with custom prompt
  openconvert -i data.csv -o report.pdf --prompt "Create a formatted report with charts"
  
  # Specify network connection
  openconvert -i file.doc -o file.md --host remote.server.com --port 8765

Supported formats include:
  Documents: txt, pdf, docx, html, md, rtf, csv, xlsx
  Images: png, jpg, jpeg, bmp, gif, tiff, svg, webp  
  Audio: mp3, wav, ogg, flac, aac
  Video: mp4, avi, mkv, mov, webm
  Archives: zip, rar, 7z, tar, gz
  Code: json, xml, yaml, html, latex
  Models: stl, obj, fbx, ply
        """
    )
    
    # Required arguments
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input file or directory path"
    )
    parser.add_argument(
        "-o", "--output", 
        required=True,
        help="Output file or directory path"
    )
    
    # Optional format specification
    parser.add_argument(
        "--from", dest="from_format",
        help="Source MIME type (e.g., 'text/plain', 'image/png'). Auto-detected if not specified."
    )
    parser.add_argument(
        "--to", dest="to_format",
        help="Target MIME type (e.g., 'application/pdf', 'text/markdown'). Auto-detected from output extension if not specified."
    )
    
    # Optional conversion prompt
    parser.add_argument(
        "--prompt",
        help="Additional instructions for the conversion (e.g., 'compress by 50%%', 'add a title')"
    )
    
    # Network connection options
    parser.add_argument(
        "--host",
        default="localhost",
        help="OpenConvert network host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="OpenConvert network port (default: 8765)"
    )
    
    # Logging options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true", 
        help="Suppress all output except errors"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Configure logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate arguments
    if not validate_args(args):
        return 1
    
    # Get input files
    input_path = Path(args.input)
    input_files = get_input_files(input_path, args.from_format)
    
    if not input_files:
        logger.error("No input files found to process")
        return 1
    
    logger.info(f"Found {len(input_files)} files to process")
    
    # Run conversion
    try:
        success = asyncio.run(convert_files(
            input_files=input_files,
            output_path=Path(args.output),
            from_format=args.from_format,
            to_format=args.to_format,
            prompt=args.prompt,
            host=args.host,
            port=args.port
        ))
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        logger.info("Conversion cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 