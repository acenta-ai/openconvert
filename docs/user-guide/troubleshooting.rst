Troubleshooting
===============

This guide helps you diagnose and resolve common issues with OpenConvert.

Connection Issues
-----------------

Cannot Connect to Network
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** ``ConnectionError: Cannot connect to localhost:8765``

**Causes and Solutions:**

1. **Network not running**
   
   Check if the OpenAgents network is running:
   
   .. code-block:: bash
   
      # Test connection
      telnet localhost 8765
      # Or use netstat to check if port is open
      netstat -an | grep 8765

   **Solution:** Start the network:
   
   .. code-block:: bash
   
      cd openagents
      openagents launch-network demos/openconvert/network_config.yaml

2. **Wrong host/port**
   
   **Solution:** Verify the correct host and port:
   
   .. code-block:: bash
   
      # Try different combinations
      openconvert --host 127.0.0.1 --port 8765 --list-formats
      openconvert --host localhost --port 8765 --list-formats

3. **Firewall blocking connection**
   
   **Solution:** Check firewall settings or try a different port.

Connection Timeout
~~~~~~~~~~~~~~~~~~

**Problem:** Connection attempts timeout

**Solution:**

.. code-block:: bash

   # Increase timeout (if supported in future versions)
   export OPENCONVERT_TIMEOUT=30
   
   # Check network connectivity
   ping [host]
   
   # Use verbose mode to see where it's hanging
   openconvert -v --host [host] --port [port] --list-formats

Format and Conversion Issues
----------------------------

No Suitable Agent Found
~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** ``No agent found for conversion: text/plain -> video/mp4``

**Solution:**

1. **Check available formats:**
   
   .. code-block:: bash
   
      openconvert --list-formats

2. **Verify format specifications:**
   
   .. code-block:: bash
   
      # Check if you're using correct MIME types
      openconvert --list-formats | grep "text/plain"
      openconvert --list-formats | grep "video"

3. **Start additional agents:**
   
   .. code-block:: bash
   
      # In OpenAgents directory
      python demos/openconvert/run_agent.py video &

Format Detection Failed
~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** ``Cannot detect format for file 'unknown.xyz'``

**Solution:**

.. code-block:: bash

   # Specify format explicitly
   openconvert -i unknown.xyz -o output.pdf --from text/plain
   
   # Check file content
   file unknown.xyz
   head unknown.xyz

Conversion Failed
~~~~~~~~~~~~~~~~~

**Problem:** Conversion starts but fails

**Debugging steps:**

1. **Use verbose mode:**
   
   .. code-block:: bash
   
      openconvert -v -i input.txt -o output.pdf

2. **Try without prompts:**
   
   .. code-block:: bash
   
      # Remove custom prompts to isolate the issue
      openconvert -i input.txt -o output.pdf

3. **Test with smaller files:**
   
   .. code-block:: bash
   
      # Create a minimal test file
      echo "Hello World" > test.txt
      openconvert -i test.txt -o test.pdf

4. **Check agent logs:**
   
   Check the agent terminal for error messages.

File and Permission Issues
--------------------------

Input File Not Found
~~~~~~~~~~~~~~~~~~~~

**Problem:** ``FileNotFoundError: Input file 'missing.txt' not found``

**Solution:**

.. code-block:: bash

   # Check file exists and is readable
   ls -la missing.txt
   
   # Check current directory
   pwd
   
   # Use absolute paths
   openconvert -i /full/path/to/file.txt -o output.pdf

Permission Denied
~~~~~~~~~~~~~~~~~

**Problem:** ``PermissionError: Permission denied: 'output.pdf'``

**Solution:**

.. code-block:: bash

   # Check output directory permissions
   ls -la /path/to/output/directory/
   
   # Create output directory if needed
   mkdir -p /path/to/output/
   
   # Use a writable location
   openconvert -i input.txt -o ~/output.pdf

Output Directory Doesn't Exist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Cannot write to output location

**Solution:**

.. code-block:: bash

   # Create output directory
   mkdir -p /path/to/output/directory/
   
   # Or specify an existing directory
   openconvert -i input.txt -o ~/Documents/output.pdf

Installation Issues
-------------------

Import Errors
~~~~~~~~~~~~~

**Problem:** ``ModuleNotFoundError: No module named 'openconvert'``

**Solution:**

.. code-block:: bash

   # For regular installation
   pip uninstall openconvert
   pip install openconvert
   
   # For development installation
   cd openconvert
   pip install -e .
   
   # Check Python path
   python -c "import sys; print(sys.path)"
   
   # Check if package is installed
   pip list | grep openconvert

Missing Dependencies
~~~~~~~~~~~~~~~~~~~~

**Problem:** ``ImportError: No module named 'yaml'``

**Solution:**

.. code-block:: bash

   # Install missing dependencies
   pip install pyyaml
   
   # Or reinstall OpenConvert (regular installation)
   pip install --upgrade openconvert
   
   # Or reinstall with dependencies (development)
   pip install -e .

Performance Issues
------------------

Slow Conversions
~~~~~~~~~~~~~~~~

**Causes and Solutions:**

1. **Network latency:**
   
   Use local network when possible:
   
   .. code-block:: bash
   
      # Local network is faster
      openconvert --host localhost -i file.txt -o file.pdf

2. **Large files:**
   
   Test with smaller files first:
   
   .. code-block:: bash
   
      # Split large files
      split -l 1000 large_file.txt chunk_
      
      # Process chunks separately
      for chunk in chunk_*; do
          openconvert -i "$chunk" -o "${chunk}.pdf"
      done

3. **Complex prompts:**
   
   Simplify prompts or remove them:
   
   .. code-block:: bash
   
      # Simple conversion first
      openconvert -i file.txt -o file.pdf
      
      # Then try with prompts
      openconvert -i file.txt -o file_enhanced.pdf --prompt "Simple formatting"

Agent Issues
~~~~~~~~~~~~

**Problem:** Agents become unresponsive

**Solution:**

.. code-block:: bash

   # Restart agents
   pkill -f "run_agent.py"
   
   # Start fresh agents
   python demos/openconvert/run_agent.py doc &
   python demos/openconvert/run_agent.py image &

Debugging Techniques
--------------------

Verbose Logging
~~~~~~~~~~~~~~~

Enable detailed logging to understand what's happening:

.. code-block:: bash

   # Maximum verbosity
   openconvert -v -i input.txt -o output.pdf

Check Process Status
~~~~~~~~~~~~~~~~~~~~

Monitor system resources:

.. code-block:: bash

   # Check running processes
   ps aux | grep openconvert
   ps aux | grep openagents
   
   # Monitor network connections
   netstat -an | grep 8765
   
   # Check system resources
   top
   htop

Network Diagnostics
~~~~~~~~~~~~~~~~~~~

Test network connectivity:

.. code-block:: bash

   # Test port connectivity
   telnet localhost 8765
   
   # Check what's listening on the port
   lsof -i :8765
   
   # Test with curl (if agents support HTTP)
   curl -v http://localhost:8765/

Log Files
~~~~~~~~~

Check log files for detailed error information:

.. code-block:: bash

   # OpenAgents logs (if configured)
   tail -f ~/.openagents/logs/network.log
   tail -f ~/.openagents/logs/agent.log
   
   # System logs
   journalctl -f | grep openconvert

Environment Debugging
~~~~~~~~~~~~~~~~~~~~~

Check environment configuration:

.. code-block:: bash

   # Check environment variables
   env | grep OPENCONVERT
   
   # Check Python environment
   which python
   python --version
   pip list | grep -E "(openconvert|openagents|yaml)"

Common Error Messages
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Error Message
     - Solution
   * - ``Connection refused``
     - Start the OpenAgents network
   * - ``No module named 'openagents'``
     - Install OpenAgents or check Python path
   * - ``YAML parse error``
     - Check network configuration file syntax
   * - ``Agent timeout``
     - Restart agents or increase timeout
   * - ``Format not supported``
     - Check available formats with ``--list-formats``
   * - ``File too large``
     - Split file or use streaming (if supported)

Getting Help
------------

If you can't resolve the issue:

1. **Search existing issues:**
   
   `GitHub Issues <https://github.com/openagents/openconvert/issues>`_

2. **Create a bug report:**
   
   Include:
   
   - Operating system and version
   - Python version
   - OpenConvert version
   - Command that failed
   - Complete error message
   - Output of ``openconvert -v --list-formats``

3. **Join the community:**
   
   - `Discord Server <https://discord.gg/openagents>`_
   - `GitHub Discussions <https://github.com/openagents/openconvert/discussions>`_

4. **Minimal reproduction case:**
   
   Create the smallest possible example that reproduces the issue:
   
   .. code-block:: bash
   
      # Minimal test case
      echo "test" > minimal.txt
      openconvert -v -i minimal.txt -o minimal.pdf

Quick Diagnostic Script
-----------------------

Here's a script to gather diagnostic information:

.. code-block:: bash

   #!/bin/bash
   # diagnostic.sh - OpenConvert diagnostic script
   
   echo "=== OpenConvert Diagnostics ==="
   echo "Date: $(date)"
   echo "OS: $(uname -a)"
   echo "Python: $(python --version 2>&1)"
   echo
   
   echo "=== Python Packages ==="
   pip list | grep -E "(openconvert|openagents|yaml)" || echo "None found"
   echo
   
   echo "=== Environment Variables ==="
   env | grep OPENCONVERT || echo "None set"
   echo
   
   echo "=== Network Test ==="
   openconvert --list-formats 2>&1 || echo "Network test failed"
   echo
   
   echo "=== Port Check ==="
   netstat -an | grep 8765 || echo "Port 8765 not listening"
   echo
   
   echo "=== File Test ==="
   echo "Hello World" > diagnostic_test.txt
   openconvert -v -i diagnostic_test.txt -o diagnostic_test.pdf 2>&1
   rm -f diagnostic_test.txt diagnostic_test.pdf

Run this script and include its output when reporting issues.

Prevention Tips
---------------

1. **Always test with simple cases first**
2. **Use version control for configuration files**
3. **Monitor system resources during batch operations**
4. **Keep agents updated**
5. **Use explicit format specifications for reliability**
6. **Implement proper error handling in scripts**
7. **Test network connectivity before large operations** 