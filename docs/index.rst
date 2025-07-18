OpenConvert Documentation
=========================

.. image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.8+

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

**Intelligent File Conversion for the Distributed Age**

OpenConvert CLI is a command-line tool that connects to distributed OpenAgents networks to discover and utilize file conversion services. Instead of installing multiple conversion tools, OpenConvert leverages distributed agents to handle various file conversion tasks.

✨ Key Features
---------------

🔗 **Network-Powered**
   Connect to OpenAgents conversion networks

🤖 **Prompt Support**
   Use natural language prompts (agent-dependent)

📁 **Batch Processing**
   Convert files and directories

🔍 **Auto-Detection**
   Automatic MIME type detection

🛡️ **Error Handling**
   Comprehensive error reporting

⚡ **Async Operations**
   Non-blocking network operations

🔧 **Python API**
   Import and use ``from openconvert import convert``

📊 **Format Discovery**
   ``--list-formats`` to see available conversions  

🚀 Quick Start
--------------

.. code-block:: bash

   # Install OpenConvert
   pip install openconvert

   # Convert your first file!
   openconvert -i document.txt -o document.pdf

📚 Documentation Sections
-------------------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting-started/installation
   getting-started/quickstart
   getting-started/basic-usage

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   user-guide/cli-reference
   user-guide/python-api
   user-guide/advanced-usage
   user-guide/supported-formats
   user-guide/troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: Network Setup

   deployment/network-setup
   deployment/agent-configuration
   deployment/docker-deployment

.. toctree::
   :maxdepth: 2
   :caption: Development

   development/contributing
   development/architecture
   development/testing

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/openconvert
   api/client
   api/cli

.. toctree::
   :maxdepth: 1
   :caption: Examples

   examples/batch-processing
   examples/python-integration
   examples/custom-prompts

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 