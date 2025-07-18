Basic Usage
===========

This guide covers the fundamental concepts and usage patterns of OpenConvert.

Core Concepts
-------------

OpenConvert operates on several key concepts:

**Agents**
  Distributed services that perform specific file conversions. Each agent specializes in certain format conversions (e.g., document agent for text→PDF, image agent for JPEG→PNG).

**Network**
  A collection of connected agents that can discover and communicate with each other. OpenConvert clients connect to networks to find suitable conversion agents.

**MIME Types**
  Standard format identifiers (e.g., ``text/plain``, ``application/pdf``, ``image/jpeg``). OpenConvert uses MIME types to match files with appropriate conversion agents.

**Prompts**
  Natural language instructions that can enhance conversions. Not all agents support prompts, but those that do can perform intelligent transformations.

Basic Command Structure
-----------------------

The basic OpenConvert command follows this pattern:

.. code-block:: bash

   openconvert [OPTIONS] -i INPUT -o OUTPUT

Required Arguments
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   -i, --input    # Input file or directory
   -o, --output   # Output file or directory

Optional Arguments
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   --from         # Source MIME type (auto-detected if not specified)
   --to           # Target MIME type (auto-detected from output extension)
   --prompt       # Natural language conversion instructions
   --host         # Network host (default: localhost)
   --port         # Network port (default: 8765)
   -v, --verbose  # Verbose output
   -q, --quiet    # Quiet mode
   --list-formats # Show available conversions

File and Directory Operations
-----------------------------

Single File Conversion
~~~~~~~~~~~~~~~~~~~~~~

Convert a single file to another format:

.. code-block:: bash

   # Basic conversion (format auto-detected)
   openconvert -i document.txt -o document.pdf

   # Explicit format specification
   openconvert -i data.csv -o report.pdf \\
     --from text/csv --to application/pdf

   # With enhancement prompt
   openconvert -i notes.txt -o presentation.pdf \\
     --prompt "Create slides with bullet points"

Directory Processing
~~~~~~~~~~~~~~~~~~~~

Process entire directories:

.. code-block:: bash

   # Convert all compatible files
   openconvert -i documents/ -o converted/

   # Convert specific format to another
   openconvert -i images/ -o thumbnails/ \\
     --from image/jpeg --to image/webp

   # Apply prompts to all files
   openconvert -i photos/ -o processed/ \\
     --prompt "Resize to 1920x1080 and compress"

Batch File Selection
~~~~~~~~~~~~~~~~~~~~

Use shell patterns for selective processing:

.. code-block:: bash

   # Convert all text files
   openconvert -i *.txt -o pdfs/ --to application/pdf

   # Convert specific files
   openconvert -i "report*.csv" -o charts/ \\
     --to application/pdf --prompt "Create charts"

Format Detection and Specification
----------------------------------

Automatic Detection
~~~~~~~~~~~~~~~~~~~

OpenConvert automatically detects formats when possible:

.. code-block:: bash

   # Input format detected from file content
   # Output format detected from .pdf extension
   openconvert -i document.txt -o document.pdf

Manual Specification
~~~~~~~~~~~~~~~~~~~~

Override automatic detection when needed:

.. code-block:: bash

   # Force specific input format
   openconvert -i data.txt -o chart.png \\
     --from text/csv --to image/png

   # Specify both input and output formats
   openconvert -i file.dat -o output.jpg \\
     --from application/json --to image/jpeg

Common MIME Types
~~~~~~~~~~~~~~~~~

Here are frequently used MIME types:

**Documents**
  - ``text/plain`` - Plain text files
  - ``text/csv`` - CSV data files
  - ``text/markdown`` - Markdown files
  - ``application/pdf`` - PDF documents
  - ``application/vnd.openxmlformats-officedocument.wordprocessingml.document`` - Word documents

**Images**
  - ``image/jpeg`` - JPEG images
  - ``image/png`` - PNG images
  - ``image/gif`` - GIF images
  - ``image/webp`` - WebP images
  - ``image/svg+xml`` - SVG graphics

**Audio/Video**
  - ``audio/mpeg`` - MP3 audio
  - ``audio/wav`` - WAV audio
  - ``video/mp4`` - MP4 video
  - ``video/webm`` - WebM video

Working with Prompts
--------------------

Basic Prompts
~~~~~~~~~~~~~

Simple instructions for enhanced conversion:

.. code-block:: bash

   # Document formatting
   openconvert -i text.txt -o fancy.pdf \\
     --prompt "Use professional formatting with headers"

   # Image processing
   openconvert -i photo.jpg -o thumbnail.jpg \\
     --prompt "Create 200x200 thumbnail"

   # Data visualization
   openconvert -i sales.csv -o chart.png \\
     --prompt "Bar chart showing monthly sales"

Advanced Prompts
~~~~~~~~~~~~~~~~

More detailed instructions for complex transformations:

.. code-block:: bash

   # Complex document creation
   openconvert -i data.csv -o report.pdf \\
     --prompt "Create executive summary with: \\
               1. Title page with company logo \\
               2. Data tables with alternating row colors \\
               3. Charts showing trends \\
               4. Conclusions section"

   # Image enhancement
   openconvert -i old-photo.jpg -o restored.jpg \\
     --prompt "Enhance contrast, reduce noise, sharpen details"

Network Configuration
---------------------

Default Connection
~~~~~~~~~~~~~~~~~~

By default, OpenConvert connects to localhost:

.. code-block:: bash

   # Uses localhost:8765
   openconvert -i file.txt -o file.pdf

Custom Network
~~~~~~~~~~~~~~

Connect to remote networks:

.. code-block:: bash

   # Connect to remote network
   openconvert --host convert.example.com --port 9000 \\
     -i document.txt -o document.pdf

   # Use environment variables
   export OPENCONVERT_HOST=convert.example.com
   export OPENCONVERT_PORT=9000
   openconvert -i file.txt -o file.pdf

Discovery and Exploration
--------------------------

List Available Formats
~~~~~~~~~~~~~~~~~~~~~~

See what conversions are available:

.. code-block:: bash

   # Show all available conversions
   openconvert --list-formats

   # With specific network
   openconvert --host remote.example.com --list-formats

Example output:

.. code-block:: text

   Available conversions:
   
   Document conversions (doc-agent-1):
     text/plain -> application/pdf
     text/markdown -> application/pdf
     text/csv -> application/pdf
   
   Image conversions (image-agent-1):
     image/jpeg -> image/png
     image/jpeg -> image/webp
     image/png -> image/jpeg

Verbose Output
~~~~~~~~~~~~~~

Get detailed information about the conversion process:

.. code-block:: bash

   # Verbose mode shows detailed progress
   openconvert -v -i document.txt -o document.pdf

Example verbose output:

.. code-block:: text

   🔍 Detecting input format...
   📄 Detected: text/plain
   🎯 Target format: application/pdf
   🌐 Connecting to network localhost:8765...
   🤖 Found agent: doc-agent-1
   📤 Sending conversion request...
   ⏳ Converting... (agent: doc-agent-1)
   📥 Receiving result...
   ✅ Conversion completed successfully!
   💾 Saved to: document.pdf

Error Handling
--------------

Common Errors and Solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**No suitable agent found**

.. code-block:: bash

   # Error: No agent supports text/plain -> video/mp4
   # Solution: Check available formats
   openconvert --list-formats

**Connection failed**

.. code-block:: bash

   # Error: Cannot connect to localhost:8765
   # Solution: Check if network is running
   # Start local network or specify different host

**File not found**

.. code-block:: bash

   # Error: Input file 'missing.txt' not found
   # Solution: Check file path and permissions
   ls -la missing.txt

**Format not supported**

.. code-block:: bash

   # Error: Cannot detect format for 'unknown.xyz'
   # Solution: Specify format explicitly
   openconvert -i unknown.xyz -o output.pdf \\
     --from text/plain

Best Practices
--------------

1. **Use explicit formats** when working with unusual file extensions
2. **Test with small files** before batch processing
3. **Use verbose mode** when troubleshooting
4. **Check available formats** before attempting conversions
5. **Start simple** - avoid complex prompts until basic conversion works
6. **Keep prompts clear** - specific instructions work better than vague ones

Next Steps
----------

- Learn about :doc:`../user-guide/advanced-usage` for complex scenarios
- Explore :doc:`../user-guide/python-api` for programmatic usage
- See :doc:`../examples/batch-processing` for real-world examples 