CLI Reference
=============

This page provides a complete reference for the OpenConvert command-line interface.

Synopsis
--------

.. code-block:: bash

   openconvert [GLOBAL_OPTIONS] -i INPUT -o OUTPUT [OPTIONS]
   openconvert [GLOBAL_OPTIONS] --list-formats
   openconvert --help
   openconvert --version

Global Options
--------------

These options apply to all OpenConvert commands:

``--help``
  Show help message and exit.

``--version``
  Show version information and exit.

``-v, --verbose``
  Enable verbose output. Shows detailed progress information during conversion.

``-q, --quiet``
  Enable quiet mode. Suppress all output except errors.

``--host HOST``
  Specify the network host to connect to.
  
  :Default: ``localhost``
  :Example: ``--host convert.example.com``

``--port PORT``
  Specify the network port to connect to.
  
  :Default: ``8765``
  :Example: ``--port 9000``

Core Commands
-------------

File Conversion
~~~~~~~~~~~~~~~

Convert files between different formats:

.. code-block:: bash

   openconvert -i INPUT -o OUTPUT [OPTIONS]

**Required Arguments:**

``-i INPUT, --input INPUT``
  Input file or directory path. Can be:
  
  - Single file: ``document.txt``
  - Directory: ``documents/``
  - Glob pattern: ``*.txt`` (shell expansion)

``-o OUTPUT, --output OUTPUT``
  Output file or directory path. The output format is usually detected from the file extension.

**Optional Arguments:**

``--from MIME_TYPE``
  Source MIME type. Override automatic format detection.
  
  :Example: ``--from text/csv``

``--to MIME_TYPE``
  Target MIME type. Override automatic format detection from output extension.
  
  :Example: ``--to application/pdf``

``--prompt TEXT``
  Natural language instructions for enhanced conversion. Not all agents support prompts.
  
  :Example: ``--prompt "Create professional layout with charts"``

Format Discovery
~~~~~~~~~~~~~~~~

List available format conversions:

.. code-block:: bash

   openconvert --list-formats

This command connects to the network and displays all available conversion capabilities from connected agents.

Examples
--------

Basic Conversions
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Simple text to PDF conversion
   openconvert -i document.txt -o document.pdf

   # Image format conversion
   openconvert -i photo.jpg -o photo.png

   # Convert with explicit formats
   openconvert -i data.csv -o chart.png \\
     --from text/csv --to image/png

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Convert all files in directory
   openconvert -i documents/ -o converted/

   # Convert specific format across directory
   openconvert -i photos/ -o thumbnails/ \\
     --from image/jpeg --to image/webp

   # Convert multiple files with shell expansion
   openconvert -i *.txt -o pdfs/ --to application/pdf

Enhanced Conversions
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Document with custom formatting
   openconvert -i report.txt -o report.pdf \\
     --prompt "Professional layout with headers and TOC"

   # Image processing with instructions
   openconvert -i large.jpg -o small.jpg \\
     --prompt "Resize to 800px width, optimize for web"

   # Data visualization
   openconvert -i sales.csv -o charts.pdf \\
     --prompt "Create bar charts showing monthly trends"

Network Operations
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Connect to remote network
   openconvert --host remote.example.com --port 9000 \\
     -i file.txt -o file.pdf

   # List formats from specific network
   openconvert --host convert.company.com --list-formats

   # Verbose mode for debugging
   openconvert -v -i document.txt -o document.pdf

MIME Types Reference
--------------------

Common Document Types
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - MIME Type
     - Extension
     - Description
   * - ``text/plain``
     - ``.txt``
     - Plain text files
   * - ``text/csv``
     - ``.csv``
     - Comma-separated values
   * - ``text/markdown``
     - ``.md``
     - Markdown documents
   * - ``application/pdf``
     - ``.pdf``
     - PDF documents
   * - ``application/vnd.openxmlformats-officedocument.wordprocessingml.document``
     - ``.docx``
     - Word documents
   * - ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet``
     - ``.xlsx``
     - Excel spreadsheets

Common Image Types
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - MIME Type
     - Extension
     - Description
   * - ``image/jpeg``
     - ``.jpg, .jpeg``
     - JPEG images
   * - ``image/png``
     - ``.png``
     - PNG images
   * - ``image/gif``
     - ``.gif``
     - GIF images
   * - ``image/webp``
     - ``.webp``
     - WebP images
   * - ``image/svg+xml``
     - ``.svg``
     - SVG graphics
   * - ``image/tiff``
     - ``.tiff, .tif``
     - TIFF images

Audio and Video Types
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - MIME Type
     - Extension
     - Description
   * - ``audio/mpeg``
     - ``.mp3``
     - MP3 audio
   * - ``audio/wav``
     - ``.wav``
     - WAV audio
   * - ``audio/ogg``
     - ``.ogg``
     - OGG audio
   * - ``video/mp4``
     - ``.mp4``
     - MP4 video
   * - ``video/webm``
     - ``.webm``
     - WebM video
   * - ``video/quicktime``
     - ``.mov``
     - QuickTime video

Exit Codes
----------

OpenConvert uses standard exit codes:

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - Code
     - Description
   * - ``0``
     - Success
   * - ``1``
     - General error (conversion failed, invalid arguments, etc.)
   * - ``2``
     - Network error (cannot connect to agents)
   * - ``3``
     - File error (input not found, output not writable, etc.)
   * - ``4``
     - Format error (unsupported format, no suitable agent, etc.)

Environment Variables
---------------------

OpenConvert recognizes these environment variables:

``OPENCONVERT_HOST``
  Default network host. Overrides the built-in default of ``localhost``.

``OPENCONVERT_PORT``
  Default network port. Overrides the built-in default of ``8765``.

``OPENCONVERT_VERBOSE``
  Enable verbose mode if set to ``1``, ``true``, or ``yes``.

``OPENCONVERT_QUIET``
  Enable quiet mode if set to ``1``, ``true``, or ``yes``.

Example:

.. code-block:: bash

   export OPENCONVERT_HOST=convert.company.com
   export OPENCONVERT_PORT=9000
   export OPENCONVERT_VERBOSE=1
   
   # Now all commands use these defaults
   openconvert -i file.txt -o file.pdf

Configuration Files
-------------------

.. note::
   Configuration file support is planned for future releases.

Future versions will support configuration files for default settings:

.. code-block:: yaml

   # ~/.openconvert.yaml (planned)
   network:
     host: convert.company.com
     port: 9000
   
   defaults:
     verbose: true
     prompt_template: "Professional formatting"
   
   agents:
     preferred:
       - doc-agent-premium
       - image-agent-fast

Shell Completion
----------------

.. note::
   Shell completion support is planned for future releases.

Future versions will include shell completion for:

- Command options
- MIME types
- Available agents
- File paths

Usage Patterns
--------------

Workflow Examples
~~~~~~~~~~~~~~~~~

**Document Processing Workflow:**

.. code-block:: bash

   # 1. Check available document conversions
   openconvert --list-formats | grep document

   # 2. Convert with basic formatting
   openconvert -i draft.txt -o draft.pdf

   # 3. Enhanced conversion with custom prompt
   openconvert -i final.txt -o final.pdf \\
     --prompt "Executive summary format with logo"

**Batch Image Processing:**

.. code-block:: bash

   # 1. Test with single image
   openconvert -i sample.jpg -o sample.webp \\
     --prompt "Compress for web"

   # 2. Process entire directory
   openconvert -i photos/ -o web-ready/ \\
     --from image/jpeg --to image/webp \\
     --prompt "Compress for web, maintain quality"

**Data Visualization Pipeline:**

.. code-block:: bash

   # 1. Create basic chart
   openconvert -i data.csv -o preview.png \\
     --prompt "Simple bar chart"

   # 2. Generate final report
   openconvert -i data.csv -o report.pdf \\
     --prompt "Executive dashboard with multiple charts and analysis"

Command Chaining
~~~~~~~~~~~~~~~~

Combine OpenConvert with other tools:

.. code-block:: bash

   # Find and convert all text files
   find . -name "*.txt" -exec openconvert -i {} -o {}.pdf \\;

   # Convert and compress
   openconvert -i large.png -o temp.webp && \\
   openconvert -i temp.webp -o small.webp --prompt "Further compress"

   # Parallel processing with xargs
   ls *.txt | xargs -I {} -P 4 openconvert -i {} -o {}.pdf

Performance Tips
----------------

1. **Use explicit formats** to avoid detection overhead
2. **Test prompts** on small files before batch processing
3. **Connect to local networks** for better performance
4. **Use appropriate agents** - check ``--list-formats`` for capabilities
5. **Monitor verbose output** to identify bottlenecks

Troubleshooting
---------------

For detailed troubleshooting information, see :doc:`troubleshooting`.

Common quick fixes:

.. code-block:: bash

   # Connection issues
   openconvert --host localhost --port 8765 --list-formats

   # Format issues
   openconvert --list-formats | grep "text/plain"

   # Verbose debugging
   openconvert -v -i problem.txt -o output.pdf

See Also
--------

- :doc:`python-api` - Python API reference
- :doc:`advanced-usage` - Advanced usage patterns
- :doc:`../examples/batch-processing` - Batch processing examples
- :doc:`../deployment/network-setup` - Network setup guide 