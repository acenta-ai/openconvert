Quick Start
===========

This guide will get you up and running with OpenConvert in just a few minutes.

Prerequisites
-------------

Before starting, make sure you have:

1. ✅ Installed OpenConvert (see :doc:`installation`)
2. ✅ Python 3.8+ available
3. ✅ Access to an OpenAgents network (or set up your own)

Your First Conversion
---------------------

Step 1: Set Up Network
~~~~~~~~~~~~~~~~~~~~~~

First, you need access to an OpenConvert network. You can either:

**Option A: Use an existing network** (if available)

.. code-block:: bash

   # Test connection to existing network
   openconvert --host example.com --port 8765 --list-formats

**Option B: Set up your own local network**

.. code-block:: bash

   # Clone OpenAgents repository
   git clone https://github.com/openagents/openagents.git
   cd openagents

   # Start the network
   openagents launch-network demos/openconvert/network_config.yaml

   # In separate terminals, launch some agents
   python demos/openconvert/run_agent.py doc &
   python demos/openconvert/run_agent.py image &

Step 2: Simple File Conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now let's convert your first file:

.. code-block:: bash

   # Create a test file
   echo "Hello, OpenConvert!" > test.txt

   # Convert text to PDF
   openconvert -i test.txt -o test.pdf

   # Success! Your PDF is ready
   ls -la test.pdf

Step 3: Explore Available Formats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See what conversions are available:

.. code-block:: bash

   # List all available format conversions
   openconvert --list-formats

   # Output example:
   # Available conversions:
   # text/plain -> application/pdf (via doc-agent)
   # image/jpeg -> image/png (via image-agent)
   # ...

Common Use Cases
----------------

Document Conversion
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Text to PDF
   openconvert -i document.txt -o document.pdf

   # Markdown to Word
   openconvert -i README.md -o README.docx

   # CSV to Excel with formatting
   openconvert -i data.csv -o data.xlsx --prompt "Add charts and formatting"

Image Processing
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Convert image format
   openconvert -i photo.jpg -o photo.png

   # Batch convert directory
   openconvert -i photos/ -o converted/ --from image/jpeg --to image/webp

   # Resize images
   openconvert -i large.jpg -o small.jpg --prompt "Resize to 800px width"

Batch Operations
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Convert all files in a directory
   openconvert -i documents/ -o pdfs/ --to application/pdf

   # Convert specific file types
   openconvert -i *.txt -o converted/ --to application/pdf

Using Prompts
~~~~~~~~~~~~~

OpenConvert supports natural language prompts for enhanced conversions:

.. code-block:: bash

   # Enhanced document conversion
   openconvert -i report.txt -o report.pdf \\
     --prompt "Create professional layout with headers and table of contents"

   # Image optimization
   openconvert -i image.png -o optimized.webp \\
     --prompt "Compress for web, maintain quality"

   # Data visualization
   openconvert -i sales.csv -o report.pdf \\
     --prompt "Create charts showing monthly trends"

Python API Quick Start
-----------------------

You can also use OpenConvert from Python:

.. code-block:: python

   from openconvert import convert_file

   # Simple conversion
   success = convert_file("document.txt", "document.pdf")
   if success:
       print("✅ Conversion successful!")

   # With prompt
   success = convert_file(
       "data.csv", 
       "report.pdf",
       prompt="Create a professional report with charts"
   )

Next Steps
----------

Now that you've completed your first conversion, explore more:

📖 **Learn More**
  - :doc:`basic-usage` - Detailed usage guide
  - :doc:`../user-guide/cli-reference` - Complete CLI reference
  - :doc:`../user-guide/python-api` - Python API documentation

🔧 **Advanced Features**
  - :doc:`../user-guide/advanced-usage` - Batch processing, custom prompts
  - :doc:`../deployment/network-setup` - Set up your own network
  - :doc:`../examples/batch-processing` - Real-world examples

🤝 **Get Involved**
  - :doc:`../development/contributing` - Contribute to OpenConvert
  - `GitHub Issues <https://github.com/openagents/openconvert/issues>`_ - Report bugs or request features
  - `Discord Community <https://discord.gg/openagents>`_ - Chat with other users

Troubleshooting
---------------

**Connection Issues**

If you can't connect to the network:

.. code-block:: bash

   # Check if network is running
   openconvert --host localhost --port 8765 --list-formats

   # Try different host/port
   openconvert --host 127.0.0.1 --port 8765 --list-formats

**Conversion Failures**

If conversions fail:

1. Check if the format is supported: ``openconvert --list-formats``
2. Verify input file exists and is readable
3. Try without prompts first
4. Check the verbose output: ``openconvert -v -i input.txt -o output.pdf``

**Need Help?**

- See :doc:`../user-guide/troubleshooting` for detailed troubleshooting
- Join our `Discord server <https://discord.gg/openagents>`_ for community support 