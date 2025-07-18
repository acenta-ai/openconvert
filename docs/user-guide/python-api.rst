Python API
==========

OpenConvert provides a Python API for programmatic file conversion. This allows you to integrate file conversion capabilities directly into your Python applications.

Quick Start
-----------

.. code-block:: python

   from openconvert import convert_file

   # Simple conversion
   success = convert_file("document.txt", "document.pdf")
   if success:
       print("Conversion successful!")

Installation
------------

The Python API is included when you install OpenConvert:

.. code-block:: bash

   pip install openconvert

API Reference
-------------

High-Level Functions
~~~~~~~~~~~~~~~~~~~~

convert_file()
^^^^^^^^^^^^^^

.. autofunction:: openconvert.convert_file

**Example Usage:**

.. code-block:: python

   from openconvert import convert_file

   # Basic conversion
   success = convert_file("input.txt", "output.pdf")

   # With format specification
   success = convert_file(
       "data.csv", 
       "chart.png",
       from_format="text/csv",
       to_format="image/png"
   )

   # With enhancement prompt
   success = convert_file(
       "report.txt",
       "report.pdf", 
       prompt="Professional layout with headers"
   )

   # Custom network
   success = convert_file(
       "file.txt",
       "file.pdf",
       host="convert.example.com",
       port=9000
   )

convert()
^^^^^^^^^

.. autofunction:: openconvert.convert

**Example Usage:**

.. code-block:: python

   from openconvert import convert
   from pathlib import Path

   # Multiple input files
   success = convert(
       input_files=[Path("file1.txt"), Path("file2.txt")],
       output_path=Path("merged.pdf"),
       prompt="Merge into single document"
   )

   # Directory processing
   input_dir = Path("documents")
   input_files = list(input_dir.glob("*.txt"))
   success = convert(
       input_files=input_files,
       output_path=Path("converted/"),
       to_format="application/pdf"
   )

Low-Level Client
~~~~~~~~~~~~~~~~

For advanced use cases, you can use the low-level client directly:

.. code-block:: python

   import asyncio
   from pathlib import Path
   from openconvert.client import OpenConvertClient

   async def advanced_conversion():
       client = OpenConvertClient()
       
       try:
           # Connect to network (default address)
           await client.connect("network.openconvert.ai", 8765)
           
           # Discover available agents
           agents = await client.discover_agents()
           print(f"Found {len(agents)} agents")
           
           # Convert file
           result = await client.convert_file(
               input_file=Path("input.txt"),
               output_file=Path("output.pdf"),
               source_format="text/plain",
               target_format="application/pdf",
               prompt="Professional formatting"
           )
           
           return result
           
       finally:
           await client.disconnect()

   # Run the async function
   result = asyncio.run(advanced_conversion())

Client Class
^^^^^^^^^^^^

.. autoclass:: openconvert.client.OpenConvertClient
   :members:

Common Patterns
---------------

Batch Processing
~~~~~~~~~~~~~~~~

Process multiple files efficiently:

.. code-block:: python

   from openconvert import convert_file
   from pathlib import Path
   import logging

   def batch_convert_directory(input_dir, output_dir, target_format="application/pdf"):
       """Convert all compatible files in a directory."""
       input_path = Path(input_dir)
       output_path = Path(output_dir)
       output_path.mkdir(exist_ok=True)
       
       results = []
       
       for file_path in input_path.iterdir():
           if file_path.is_file():
               output_file = output_path / f"{file_path.stem}.pdf"
               
               try:
                   success = convert_file(
                       str(file_path),
                       str(output_file),
                       to_format=target_format
                   )
                   results.append((file_path.name, success))
                   
               except Exception as e:
                   logging.error(f"Failed to convert {file_path}: {e}")
                   results.append((file_path.name, False))
       
       return results

   # Usage
   results = batch_convert_directory("documents/", "pdfs/")
   successful = sum(1 for _, success in results if success)
   print(f"Converted {successful}/{len(results)} files")

Error Handling
~~~~~~~~~~~~~~

Robust error handling for production use:

.. code-block:: python

   from openconvert import convert_file
   import logging

   def safe_convert(input_file, output_file, **kwargs):
       """Convert file with comprehensive error handling."""
       try:
           success = convert_file(input_file, output_file, **kwargs)
           
           if success:
               logging.info(f"Successfully converted {input_file} to {output_file}")
               return True
           else:
               logging.error(f"Conversion failed: {input_file} -> {output_file}")
               return False
               
       except FileNotFoundError:
           logging.error(f"Input file not found: {input_file}")
           return False
           
       except PermissionError:
           logging.error(f"Permission denied: {output_file}")
           return False
           
       except ConnectionError:
           logging.error("Cannot connect to OpenConvert network")
           return False
           
       except Exception as e:
           logging.error(f"Unexpected error: {e}")
           return False

   # Usage with logging
   logging.basicConfig(level=logging.INFO)
   safe_convert("document.txt", "document.pdf")

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

Manage network settings and defaults:

.. code-block:: python

   import os
   from openconvert import convert_file

   class OpenConvertConfig:
       """Configuration manager for OpenConvert."""
       
       def __init__(self):
           self.host = os.getenv('OPENCONVERT_HOST', 'localhost')
           self.port = int(os.getenv('OPENCONVERT_PORT', 8765))
           self.default_prompt = os.getenv('OPENCONVERT_DEFAULT_PROMPT', '')
       
       def convert(self, input_file, output_file, **kwargs):
           """Convert with default configuration."""
           kwargs.setdefault('host', self.host)
           kwargs.setdefault('port', self.port)
           
           if self.default_prompt and 'prompt' not in kwargs:
               kwargs['prompt'] = self.default_prompt
               
           return convert_file(input_file, output_file, **kwargs)

   # Usage
   config = OpenConvertConfig()
   success = config.convert("document.txt", "document.pdf")

Async Usage
~~~~~~~~~~~

For applications that need non-blocking operation:

.. code-block:: python

   import asyncio
   from openconvert.client import OpenConvertClient
   from pathlib import Path

   async def async_batch_convert(file_pairs):
       """Convert multiple files asynchronously."""
       client = OpenConvertClient()
       
       try:
           await client.connect()
           
           # Create conversion tasks
           tasks = []
           for input_file, output_file in file_pairs:
               task = client.convert_file(
                   input_file=Path(input_file),
                   output_file=Path(output_file),
                   source_format=None,  # Auto-detect
                   target_format=None   # Auto-detect
               )
               tasks.append(task)
           
           # Run conversions concurrently
           results = await asyncio.gather(*tasks, return_exceptions=True)
           
           return results
           
       finally:
           await client.disconnect()

   # Usage
   file_pairs = [
       ("doc1.txt", "doc1.pdf"),
       ("doc2.txt", "doc2.pdf"), 
       ("doc3.txt", "doc3.pdf")
   ]
   
   results = asyncio.run(async_batch_convert(file_pairs))

Integration Examples
--------------------

Web Application Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Flask example:

.. code-block:: python

   from flask import Flask, request, send_file, jsonify
   from openconvert import convert_file
   import tempfile
   import os

   app = Flask(__name__)

   @app.route('/convert', methods=['POST'])
   def convert_endpoint():
       """API endpoint for file conversion."""
       if 'file' not in request.files:
           return jsonify({'error': 'No file provided'}), 400
       
       file = request.files['file']
       target_format = request.form.get('format', 'application/pdf')
       prompt = request.form.get('prompt', '')
       
       with tempfile.TemporaryDirectory() as temp_dir:
           # Save uploaded file
           input_path = os.path.join(temp_dir, file.filename)
           file.save(input_path)
           
           # Convert file
           output_path = os.path.join(temp_dir, 'output.pdf')
           success = convert_file(
               input_path,
               output_path,
               to_format=target_format,
               prompt=prompt if prompt else None
           )
           
           if success:
               return send_file(output_path, as_attachment=True)
           else:
               return jsonify({'error': 'Conversion failed'}), 500

   if __name__ == '__main__':
       app.run(debug=True)

Command-Line Tool Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extend OpenConvert with custom tools:

.. code-block:: python

   #!/usr/bin/env python3
   """Custom document processor using OpenConvert."""

   import argparse
   from pathlib import Path
   from openconvert import convert_file

   def process_documents(input_dir, output_dir, template="professional"):
       """Process documents with predefined templates."""
       
       templates = {
           "professional": "Create professional layout with headers and TOC",
           "academic": "Academic paper format with citations and references",
           "presentation": "Convert to presentation slides with bullet points"
       }
       
       prompt = templates.get(template, template)
       input_path = Path(input_dir)
       output_path = Path(output_dir)
       output_path.mkdir(exist_ok=True)
       
       for file_path in input_path.glob("*.txt"):
           output_file = output_path / f"{file_path.stem}.pdf"
           
           success = convert_file(
               str(file_path),
               str(output_file),
               prompt=prompt
           )
           
           if success:
               print(f"✅ {file_path.name} -> {output_file.name}")
           else:
               print(f"❌ Failed: {file_path.name}")

   if __name__ == "__main__":
       parser = argparse.ArgumentParser(description="Process documents with OpenConvert")
       parser.add_argument("input_dir", help="Input directory")
       parser.add_argument("output_dir", help="Output directory") 
       parser.add_argument("--template", default="professional",
                          help="Document template (professional, academic, presentation)")
       
       args = parser.parse_args()
       process_documents(args.input_dir, args.output_dir, args.template)

Type Hints and Typing
---------------------

OpenConvert provides full type hints for better IDE support:

.. code-block:: python

   from typing import Optional, List
   from pathlib import Path
   from openconvert import convert, convert_file

   # Function with type hints
   def batch_convert_with_types(
       input_files: List[str],
       output_dir: str,
       target_format: Optional[str] = None,
       prompt: Optional[str] = None
   ) -> List[bool]:
       """Type-annotated batch conversion function."""
       results: List[bool] = []
       
       for input_file in input_files:
           output_file = Path(output_dir) / f"{Path(input_file).stem}.pdf"
           
           success: bool = convert_file(
               input_file,
               str(output_file),
               to_format=target_format,
               prompt=prompt
           )
           
           results.append(success)
       
       return results

Testing
-------

Example test cases for applications using OpenConvert:

.. code-block:: python

   import unittest
   from unittest.mock import patch, MagicMock
   from openconvert import convert_file

   class TestOpenConvertIntegration(unittest.TestCase):
       """Test OpenConvert integration."""
       
       @patch('openconvert.convert_file')
       def test_successful_conversion(self, mock_convert):
           """Test successful file conversion."""
           mock_convert.return_value = True
           
           result = convert_file("test.txt", "test.pdf")
           
           self.assertTrue(result)
           mock_convert.assert_called_once_with("test.txt", "test.pdf")
       
       @patch('openconvert.convert_file')
       def test_failed_conversion(self, mock_convert):
           """Test failed file conversion."""
           mock_convert.return_value = False
           
           result = convert_file("test.txt", "test.pdf")
           
           self.assertFalse(result)
       
       @patch('openconvert.convert_file')
       def test_conversion_with_prompt(self, mock_convert):
           """Test conversion with custom prompt."""
           mock_convert.return_value = True
           
           result = convert_file(
               "test.txt", 
               "test.pdf", 
               prompt="Professional formatting"
           )
           
           self.assertTrue(result)
           mock_convert.assert_called_once_with(
               "test.txt", 
               "test.pdf", 
               prompt="Professional formatting"
           )

   if __name__ == '__main__':
       unittest.main()

Best Practices
--------------

1. **Always handle errors** - Network operations can fail
2. **Use type hints** - Better IDE support and code clarity
3. **Log operations** - Essential for debugging and monitoring
4. **Test with small files** first before batch processing
5. **Use async patterns** for better performance with multiple files
6. **Configure timeouts** for production environments
7. **Cache agent discovery** when possible
8. **Validate inputs** before conversion attempts

See Also
--------

- :doc:`cli-reference` - Command-line interface reference
- :doc:`advanced-usage` - Advanced usage patterns
- :doc:`../examples/python-integration` - More Python examples
- :doc:`../api/openconvert` - Complete API documentation 