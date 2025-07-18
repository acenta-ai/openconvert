Installation
============

Requirements
------------

OpenConvert requires Python 3.8 or higher. Make sure you have the following installed on your system:

- Python 3.8+
- pip (Python package installer)
- Git (for installation from source)

System Requirements
~~~~~~~~~~~~~~~~~~~

**Supported Operating Systems:**

- Linux (Ubuntu 18.04+, CentOS 7+, etc.)
- macOS 10.14+
- Windows 10+

**Hardware Requirements:**

- Minimum: 512MB RAM, 100MB disk space
- Recommended: 1GB RAM, 500MB disk space

Installation Methods
--------------------

From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~

Install OpenConvert from PyPI using pip:

.. code-block:: bash

   # Install OpenConvert
   pip install openconvert

   # Verify installation
   openconvert --help

   # Check version
   openconvert --version

From Source (Development)
~~~~~~~~~~~~~~~~~~~~~~~~~

If you plan to contribute to OpenConvert or need the latest development version:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/openagents/openconvert.git
   cd openconvert

   # Install in development mode
   pip install -e .

   # Verify installation
   openconvert --help

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For contributors who need development dependencies:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/openagents/openconvert.git
   cd openconvert

   # Install with development dependencies
   pip install -e ".[dev]"

   # Install pre-commit hooks
   pre-commit install

Alternative Installation Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Using pipx (for isolated installation):**

.. code-block:: bash

   # Install with pipx for isolated environment
   pipx install openconvert

**Using conda (if available):**

.. code-block:: bash

   # Future conda installation
   conda install -c conda-forge openconvert

Docker Installation (Planned)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Docker support is planned for future releases:

.. code-block:: bash

   # Future Docker installation
   docker pull openagents/openconvert
   docker run -it openagents/openconvert openconvert --help

Verification
------------

Test your installation by running:

.. code-block:: bash

   # Check version
   openconvert --version

   # Show help
   openconvert --help

   # Test connection (requires network setup)
   openconvert --list-formats

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Permission Errors**

If you encounter permission errors during installation:

.. code-block:: bash

   # Use --user flag
   pip install --user -e .

**Python Version Issues**

Check your Python version:

.. code-block:: bash

   python --version
   # Should show Python 3.8 or higher

**Missing Dependencies**

If you get import errors, try reinstalling:

.. code-block:: bash

   pip uninstall openconvert
   pip install -e .

Getting Help
~~~~~~~~~~~~

If you encounter issues:

1. Check the `troubleshooting guide <../user-guide/troubleshooting.html>`_
2. Search `GitHub Issues <https://github.com/openagents/openconvert/issues>`_
3. Join our `Discord server <https://discord.gg/openagents>`_
4. Open a `new issue <https://github.com/openagents/openconvert/issues/new>`_ 