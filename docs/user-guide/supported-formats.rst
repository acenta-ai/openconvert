Supported Formats
==================

OpenConvert supports a wide variety of file formats through its distributed agent network. The available formats depend on which agents are running in your network.

Document Formats
----------------

Text Documents
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - Format
     - MIME Type
     - Extensions
     - Typical Conversions
   * - Plain Text
     - ``text/plain``
     - ``.txt``
     - PDF, HTML, Word
   * - Markdown
     - ``text/markdown``
     - ``.md, .markdown``
     - PDF, HTML, Word
   * - Rich Text
     - ``text/rtf``
     - ``.rtf``
     - PDF, Word, HTML
   * - CSV Data
     - ``text/csv``
     - ``.csv``
     - PDF, Excel, Charts

**Example conversions:**

.. code-block:: bash

   # Text to PDF
   openconvert -i document.txt -o document.pdf

   # Markdown to Word
   openconvert -i README.md -o README.docx

   # CSV to formatted report
   openconvert -i data.csv -o report.pdf --prompt "Create charts and analysis"

Office Documents
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 25 25 30

   * - Format
     - MIME Type
     - Extensions
     - Typical Conversions
   * - PDF
     - ``application/pdf``
     - ``.pdf``
     - Word, Images, Text
   * - Word Document
     - ``application/vnd.openxmlformats-officedocument.wordprocessingml.document``
     - ``.docx``
     - PDF, Text, HTML
   * - Excel Spreadsheet
     - ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet``
     - ``.xlsx``
     - PDF, CSV, Charts
   * - PowerPoint
     - ``application/vnd.openxmlformats-officedocument.presentationml.presentation``
     - ``.pptx``
     - PDF, Images

**Example conversions:**

.. code-block:: bash

   # Word to PDF
   openconvert -i document.docx -o document.pdf

   # Excel to chart PDF
   openconvert -i spreadsheet.xlsx -o charts.pdf --prompt "Create visual dashboard"

Web Formats
~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Format
     - MIME Type
     - Extensions
     - Typical Conversions
   * - HTML
     - ``text/html``
     - ``.html, .htm``
     - PDF, Word, Text
   * - XML
     - ``application/xml``
     - ``.xml``
     - JSON, PDF, Text
   * - JSON
     - ``application/json``
     - ``.json``
     - CSV, XML, PDF tables

Image Formats
-------------

Raster Images
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Format
     - MIME Type
     - Extensions
     - Typical Conversions
   * - JPEG
     - ``image/jpeg``
     - ``.jpg, .jpeg``
     - PNG, WebP, PDF, thumbnails
   * - PNG
     - ``image/png``
     - ``.png``
     - JPEG, WebP, PDF, GIF
   * - GIF
     - ``image/gif``
     - ``.gif``
     - PNG, JPEG, MP4 (animated)
   * - WebP
     - ``image/webp``
     - ``.webp``
     - JPEG, PNG, optimized formats
   * - TIFF
     - ``image/tiff``
     - ``.tiff, .tif``
     - JPEG, PNG, PDF
   * - BMP
     - ``image/bmp``
     - ``.bmp``
     - JPEG, PNG, WebP

**Example conversions:**

.. code-block:: bash

   # JPEG to PNG
   openconvert -i photo.jpg -o photo.png

   # Batch resize images
   openconvert -i photos/ -o thumbnails/ --prompt "Resize to 300x300 thumbnails"

   # Convert to web-optimized format
   openconvert -i large-image.png -o optimized.webp --prompt "Compress for web"

Vector Graphics
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Format
     - MIME Type
     - Extensions
     - Typical Conversions
   * - SVG
     - ``image/svg+xml``
     - ``.svg``
     - PNG, JPEG, PDF
   * - PDF (vector)
     - ``application/pdf``
     - ``.pdf``
     - SVG, PNG, JPEG
   * - EPS
     - ``application/postscript``
     - ``.eps``
     - PDF, PNG, JPEG

Audio Formats
-------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Format
     - MIME Type
     - Extensions
     - Typical Conversions
   * - MP3
     - ``audio/mpeg``
     - ``.mp3``
     - WAV, FLAC, OGG
   * - WAV
     - ``audio/wav``
     - ``.wav``
     - MP3, FLAC, OGG
   * - FLAC
     - ``audio/flac``
     - ``.flac``
     - MP3, WAV, OGG
   * - OGG
     - ``audio/ogg``
     - ``.ogg``
     - MP3, WAV, FLAC
   * - AAC
     - ``audio/aac``
     - ``.aac, .m4a``
     - MP3, WAV, OGG

**Example conversions:**

.. code-block:: bash

   # High quality to compressed
   openconvert -i music.wav -o music.mp3 --prompt "High quality encoding"

   # Extract audio from video
   openconvert -i video.mp4 -o audio.mp3

Video Formats
-------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Format
     - MIME Type
     - Extensions
     - Typical Conversions
   * - MP4
     - ``video/mp4``
     - ``.mp4``
     - WebM, AVI, MOV, thumbnails
   * - WebM
     - ``video/webm``
     - ``.webm``
     - MP4, thumbnails, GIF
   * - AVI
     - ``video/x-msvideo``
     - ``.avi``
     - MP4, WebM, MOV
   * - MOV
     - ``video/quicktime``
     - ``.mov``
     - MP4, WebM, AVI
   * - MKV
     - ``video/x-matroska``
     - ``.mkv``
     - MP4, WebM, AVI

**Example conversions:**

.. code-block:: bash

   # Video format conversion
   openconvert -i video.avi -o video.mp4 --prompt "Optimize for web streaming"

   # Extract video thumbnail
   openconvert -i video.mp4 -o thumbnail.jpg --prompt "Extract frame at 30 seconds"

Archive Formats
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Format
     - MIME Type
     - Extensions
     - Typical Conversions
   * - ZIP
     - ``application/zip``
     - ``.zip``
     - TAR, 7Z, extract contents
   * - TAR
     - ``application/x-tar``
     - ``.tar``
     - ZIP, 7Z, extract contents
   * - 7Z
     - ``application/x-7z-compressed``
     - ``.7z``
     - ZIP, TAR, extract contents
   * - RAR
     - ``application/x-rar-compressed``
     - ``.rar``
     - ZIP, 7Z, extract contents

**Example conversions:**

.. code-block:: bash

   # Convert archive formats
   openconvert -i backup.rar -o backup.zip

   # Create archive from directory
   openconvert -i project/ -o project.tar.gz

Code and Data Formats
---------------------

Programming Languages
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Format
     - MIME Type
     - Extensions
     - Typical Conversions
   * - Python
     - ``text/x-python``
     - ``.py``
     - PDF (formatted), HTML
   * - JavaScript
     - ``application/javascript``
     - ``.js``
     - PDF (formatted), HTML
   * - JSON
     - ``application/json``
     - ``.json``
     - CSV, XML, formatted PDF
   * - YAML
     - ``application/x-yaml``
     - ``.yaml, .yml``
     - JSON, XML, formatted PDF
   * - XML
     - ``application/xml``
     - ``.xml``
     - JSON, YAML, formatted PDF

Data Formats
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Format
     - MIME Type
     - Extensions
     - Typical Conversions
   * - CSV
     - ``text/csv``
     - ``.csv``
     - Excel, JSON, charts, reports
   * - TSV
     - ``text/tab-separated-values``
     - ``.tsv``
     - CSV, Excel, JSON
   * - Parquet
     - ``application/octet-stream``
     - ``.parquet``
     - CSV, JSON, Excel
   * - SQLite
     - ``application/x-sqlite3``
     - ``.db, .sqlite``
     - CSV, JSON, reports

3D and CAD Formats
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Format
     - MIME Type
     - Extensions
     - Typical Conversions
   * - STL
     - ``model/stl``
     - ``.stl``
     - OBJ, PLY, images
   * - OBJ
     - ``model/obj``
     - ``.obj``
     - STL, PLY, images
   * - PLY
     - ``model/ply``
     - ``.ply``
     - STL, OBJ, images
   * - GLTF
     - ``model/gltf+json``
     - ``.gltf``
     - OBJ, images, videos

**Example conversions:**

.. code-block:: bash

   # 3D model format conversion
   openconvert -i model.stl -o model.obj

   # Generate preview images
   openconvert -i model.stl -o preview.png --prompt "Generate preview from multiple angles"

Agent-Specific Capabilities
---------------------------

Document Agent
~~~~~~~~~~~~~~

Specializes in text and document processing:

- **Input formats**: text/plain, text/markdown, text/csv, text/rtf
- **Output formats**: application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document
- **Features**: Prompt support, formatting, layout control
- **Prompts**: "Professional layout", "Academic paper format", "Executive summary"

Image Agent
~~~~~~~~~~~

Handles image processing and conversion:

- **Input formats**: image/jpeg, image/png, image/gif, image/webp, image/tiff
- **Output formats**: image/jpeg, image/png, image/webp, application/pdf
- **Features**: Resizing, compression, format optimization
- **Prompts**: "Resize to 800px width", "Compress for web", "Create thumbnail"

Audio Agent
~~~~~~~~~~~

Processes audio files:

- **Input formats**: audio/mpeg, audio/wav, audio/flac, audio/ogg
- **Output formats**: audio/mpeg, audio/wav, audio/flac, audio/ogg
- **Features**: Format conversion, quality adjustment
- **Prompts**: "High quality encoding", "Compress for streaming"

Video Agent
~~~~~~~~~~~

Handles video processing:

- **Input formats**: video/mp4, video/webm, video/avi, video/quicktime
- **Output formats**: video/mp4, video/webm, image/jpeg (thumbnails)
- **Features**: Format conversion, compression, thumbnail extraction
- **Prompts**: "Optimize for web", "Extract thumbnail at 30s"

Format Discovery
----------------

Check Available Formats
~~~~~~~~~~~~~~~~~~~~~~~~

Use the format discovery feature to see what's available in your network:

.. code-block:: bash

   # List all available conversions
   openconvert --list-formats

   # Filter by input format
   openconvert --list-formats | grep "text/plain"

   # Filter by agent type
   openconvert --list-formats | grep "image"

Example output:

.. code-block:: text

   Available conversions:
   
   Document conversions (doc-agent-1):
     text/plain -> application/pdf
     text/markdown -> application/pdf
     text/csv -> application/pdf
     text/csv -> application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
   
   Image conversions (image-agent-1):
     image/jpeg -> image/png
     image/jpeg -> image/webp
     image/png -> image/jpeg
     image/png -> application/pdf
   
   Audio conversions (audio-agent-1):
     audio/wav -> audio/mp3
     audio/mp3 -> audio/wav
     audio/flac -> audio/mp3

Format Detection
~~~~~~~~~~~~~~~~

OpenConvert automatically detects input formats:

.. code-block:: bash

   # Automatic detection (recommended)
   openconvert -i document.txt -o document.pdf

   # Explicit format specification
   openconvert -i data.txt -o chart.png --from text/csv --to image/png

   # Check what format is detected
   openconvert -i unknown_file.dat --list-formats

Custom Format Support
---------------------

Adding New Formats
~~~~~~~~~~~~~~~~~~~

To add support for new formats, you can:

1. **Develop a new agent** that handles the specific format
2. **Extend existing agents** to support additional formats
3. **Use conversion chains** through intermediate formats

Example agent capability configuration:

.. code-block:: yaml

   agent:
     capabilities:
       formats:
         input: ["application/x-custom-format"]
         output: ["application/pdf", "text/plain"]
       features:
         supports_prompts: true
         max_file_size: "100MB"

Format Conversion Chains
~~~~~~~~~~~~~~~~~~~~~~~~

Some conversions may go through intermediate formats:

.. code-block:: text

   # Direct conversion (preferred)
   text/plain -> application/pdf

   # Chain conversion (automatic)
   custom/format -> text/plain -> application/pdf

Limitations and Considerations
------------------------------

File Size Limits
~~~~~~~~~~~~~~~~~

Different agents may have different file size limits:

- **Document agent**: Usually 50MB max
- **Image agent**: Usually 100MB max  
- **Video agent**: Usually 500MB max
- **Audio agent**: Usually 200MB max

Quality and Fidelity
~~~~~~~~~~~~~~~~~~~~

Some conversions may result in quality loss:

- **Lossy image formats**: JPEG compression
- **Audio compression**: MP3 encoding
- **Video compression**: H.264 encoding
- **Document formatting**: Layout approximation

Agent Availability
~~~~~~~~~~~~~~~~~~

Format support depends on which agents are running:

- **Check regularly**: Agent availability can change
- **Start required agents**: Ensure needed agents are running
- **Load balancing**: Multiple agents improve performance
- **Fallback options**: Have alternative conversion paths

See Also
--------

- :doc:`../deployment/network-setup` - Setting up agents
- :doc:`../user-guide/cli-reference` - Format specification options
- :doc:`../examples/batch-processing` - Bulk format conversions 