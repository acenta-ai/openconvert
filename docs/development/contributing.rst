Contributing
============

We welcome contributions to OpenConvert! This guide will help you get started with contributing to the project.

Getting Started
---------------

Development Environment Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Fork and clone the repository:**

   .. code-block:: bash

      # Fork on GitHub, then clone your fork
      git clone https://github.com/yourusername/openconvert.git
      cd openconvert

2. **Set up development environment:**

   .. code-block:: bash

      # Create virtual environment
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\\Scripts\\activate

      # Install in development mode with dev dependencies
      pip install -e ".[dev]"

      # Install pre-commit hooks
      pre-commit install

3. **Verify setup:**

   .. code-block:: bash

      # Run tests
      pytest

      # Check code formatting
      black --check openconvert/
      flake8 openconvert/

      # Verify CLI works
      openconvert --help

Development Workflow
~~~~~~~~~~~~~~~~~~~~

1. **Create a feature branch:**

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make your changes**

3. **Test your changes:**

   .. code-block:: bash

      # Run full test suite
      pytest

      # Run specific tests
      pytest tests/test_client.py

      # Check coverage
      pytest --cov=openconvert --cov-report=html

4. **Format and lint code:**

   .. code-block:: bash

      # Format code
      black openconvert/ tests/

      # Check linting
      flake8 openconvert/ tests/

      # Type checking (if using mypy)
      mypy openconvert/

5. **Commit and push:**

   .. code-block:: bash

      git add .
      git commit -m "Add feature: description of your changes"
      git push origin feature/your-feature-name

6. **Create a Pull Request**

Types of Contributions
---------------------

Bug Reports
~~~~~~~~~~~

Before submitting a bug report:

1. **Check existing issues** - Search for similar issues
2. **Try the latest version** - Bug might already be fixed
3. **Minimal reproduction** - Create the smallest example that reproduces the issue

**Good bug report includes:**

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, OpenConvert version)
- Error messages and logs
- Minimal code example

**Bug report template:**

.. code-block:: text

   **Bug Description**
   A clear description of what the bug is.

   **Steps to Reproduce**
   1. Set up environment with...
   2. Run command...
   3. Observe error...

   **Expected Behavior**
   What you expected to happen.

   **Actual Behavior**
   What actually happened.

   **Environment**
   - OS: Ubuntu 22.04
   - Python: 3.10.8
   - OpenConvert: 1.0.0
   - OpenAgents: (version)

   **Error Output**
   ```
   Paste error messages here
   ```

   **Minimal Example**
   ```python
   # Minimal code that reproduces the issue
   from openconvert import convert_file
   convert_file("test.txt", "test.pdf")
   ```

Feature Requests
~~~~~~~~~~~~~~~~

For feature requests:

1. **Check roadmap** - See if it's already planned
2. **Discuss first** - Open a discussion before implementing
3. **Consider scope** - Start with small, focused features

**Feature request template:**

.. code-block:: text

   **Feature Description**
   Clear description of the proposed feature.

   **Use Case**
   Why is this feature needed? What problem does it solve?

   **Proposed Solution**
   How should this feature work?

   **Alternatives Considered**
   What other approaches did you consider?

   **Additional Context**
   Any other relevant information.

Code Contributions
~~~~~~~~~~~~~~~~~~

**Areas where we need help:**

- **New format support** - Add support for additional file formats
- **Performance improvements** - Optimize conversion speed and memory usage
- **Documentation** - Improve guides, examples, and API docs
- **Testing** - Add test cases and improve coverage
- **CLI enhancements** - Better error messages, progress bars, etc.
- **Agent implementations** - New conversion agents
- **Platform support** - Windows, macOS compatibility improvements

Documentation
~~~~~~~~~~~~~

Documentation improvements are always welcome:

- **Fix typos and grammar**
- **Add examples** - Real-world usage examples
- **Improve clarity** - Make explanations clearer
- **Add translations** - Translate documentation to other languages
- **API documentation** - Improve docstrings and auto-generated docs

Code Style and Standards
------------------------

Python Code Style
~~~~~~~~~~~~~~~~~

We follow PEP 8 with some modifications:

.. code-block:: python

   # Good: Clear function names and docstrings
   def convert_file_to_pdf(input_file: str, output_file: str) -> bool:
       """Convert a file to PDF format.
       
       Args:
           input_file: Path to input file
           output_file: Path to output PDF file
           
       Returns:
           True if conversion succeeded, False otherwise
       """
       # Implementation here
       pass

   # Good: Type hints
   from typing import Optional, List
   
   def batch_convert(
       files: List[str], 
       output_dir: str,
       format: Optional[str] = None
   ) -> List[bool]:
       """Convert multiple files."""
       results = []
       for file in files:
           # Process each file
           pass
       return results

**Formatting tools:**

- **Black** - Code formatter (line length 88)
- **isort** - Import sorting
- **flake8** - Linting

.. code-block:: bash

   # Format code
   black openconvert/ tests/
   isort openconvert/ tests/
   
   # Check style
   flake8 openconvert/ tests/

Documentation Style
~~~~~~~~~~~~~~~~~~~

- **Use reStructuredText** for documentation files
- **Clear headings** - Use proper heading hierarchy
- **Code examples** - Include working examples
- **Cross-references** - Link to related sections

.. code-block:: rst

   Example Function
   ~~~~~~~~~~~~~~~~

   The :func:`convert_file` function converts files:

   .. code-block:: python

      from openconvert import convert_file
      
      success = convert_file("input.txt", "output.pdf")

   See also:
   
   - :doc:`cli-reference` - Command line usage
   - :doc:`../examples/batch-processing` - Batch examples

Commit Message Format
~~~~~~~~~~~~~~~~~~~~~

Use conventional commit format:

.. code-block:: text

   type(scope): description

   Longer explanation if needed.

   Fixes #issue-number

**Types:**

- ``feat:`` New feature
- ``fix:`` Bug fix
- ``docs:`` Documentation changes
- ``style:`` Code style changes (formatting, etc.)
- ``refactor:`` Code refactoring
- ``test:`` Adding or updating tests
- ``chore:`` Maintenance tasks

**Examples:**

.. code-block:: text

   feat(cli): add progress bar for batch conversions
   
   fix(client): handle connection timeout properly
   
   docs(api): add examples for convert_file function
   
   test(client): add unit tests for error handling

Testing Guidelines
------------------

Test Structure
~~~~~~~~~~~~~~

.. code-block:: text

   tests/
   ├── unit/           # Unit tests
   │   ├── test_client.py
   │   ├── test_cli.py
   │   └── test_utils.py
   ├── integration/    # Integration tests
   │   ├── test_conversion.py
   │   └── test_network.py
   ├── fixtures/       # Test data
   │   ├── sample.txt
   │   ├── sample.pdf
   │   └── sample.jpg
   └── conftest.py     # Pytest configuration

Writing Tests
~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from unittest.mock import patch, MagicMock
   from openconvert import convert_file
   from openconvert.client import OpenConvertClient

   class TestConvertFile:
       """Test the convert_file function."""
       
       @patch('openconvert.client.OpenConvertClient')
       def test_successful_conversion(self, mock_client_class):
           """Test successful file conversion."""
           # Setup mock
           mock_client = MagicMock()
           mock_client_class.return_value = mock_client
           mock_client.convert_file.return_value = True
           
           # Test
           result = convert_file("test.txt", "test.pdf")
           
           # Assert
           assert result is True
           mock_client.convert_file.assert_called_once()
       
       def test_file_not_found(self):
           """Test handling of missing input file."""
           with pytest.raises(FileNotFoundError):
               convert_file("missing.txt", "output.pdf")
       
       @pytest.mark.integration
       def test_real_conversion(self, test_network):
           """Integration test with real network."""
           # This test requires a running network
           result = convert_file("fixtures/sample.txt", "output.pdf")
           assert result is True

**Test categories:**

- **Unit tests** - Test individual functions/classes
- **Integration tests** - Test component interactions  
- **End-to-end tests** - Test complete workflows
- **Performance tests** - Test speed and resource usage

Running Tests
~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   pytest

   # Run specific test file
   pytest tests/unit/test_client.py

   # Run tests by marker
   pytest -m "not integration"  # Skip integration tests
   pytest -m integration        # Only integration tests

   # Run with coverage
   pytest --cov=openconvert --cov-report=html

   # Run performance tests
   pytest --benchmark-only

Review Process
--------------

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

**Before submitting:**

1. **Rebase on main** - Keep history clean
2. **Run full test suite** - Ensure all tests pass
3. **Update documentation** - If adding features
4. **Add tests** - For new functionality
5. **Check CI** - Ensure all checks pass

**Pull request template:**

.. code-block:: text

   ## Description
   Brief description of changes.

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature  
   - [ ] Documentation update
   - [ ] Performance improvement
   - [ ] Other (specify)

   ## Testing
   - [ ] Added unit tests
   - [ ] Added integration tests
   - [ ] Manual testing performed
   - [ ] All existing tests pass

   ## Documentation
   - [ ] Updated API documentation
   - [ ] Updated user guides
   - [ ] Added examples

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Tests added/updated
   - [ ] Documentation updated

Review Criteria
~~~~~~~~~~~~~~~

Reviewers check for:

- **Functionality** - Does it work as intended?
- **Code quality** - Is it maintainable and readable?
- **Performance** - Any performance implications?
- **Security** - Any security concerns?
- **Testing** - Adequate test coverage?
- **Documentation** - Clear documentation?
- **Compatibility** - Breaks existing functionality?

Community Guidelines
--------------------

Code of Conduct
~~~~~~~~~~~~~~~

We follow the Contributor Covenant Code of Conduct:

- **Be respectful** - Treat everyone with respect
- **Be inclusive** - Welcome newcomers and diverse perspectives  
- **Be constructive** - Provide helpful feedback
- **Be patient** - Help others learn and grow

Communication Channels
~~~~~~~~~~~~~~~~~~~~~~

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and ideas
- **Discord** - Real-time chat and support
- **Pull Requests** - Code review discussions

Getting Help
~~~~~~~~~~~~

If you need help contributing:

1. **Read the documentation** - Start with this guide
2. **Search existing issues** - Your question might be answered
3. **Ask in discussions** - Post in GitHub Discussions
4. **Join Discord** - Get real-time help from community
5. **Mention maintainers** - Tag maintainers in issues if stuck

Recognition
-----------

Contributors are recognized through:

- **Contributors list** - Added to README and documentation
- **Release notes** - Mentioned in release announcements  
- **Badges** - GitHub profile badges for contributions
- **Maintainer nomination** - Outstanding contributors may be invited as maintainers

Release Process
---------------

For maintainers:

1. **Version bumping** - Update version in setup.py
2. **Changelog** - Update CHANGELOG.md
3. **Documentation** - Update version in docs/conf.py
4. **Testing** - Run full test suite
5. **Tagging** - Create git tag
6. **Release** - Publish to PyPI
7. **Announcement** - Post release notes

.. code-block:: bash

   # Release checklist
   git checkout main
   git pull origin main
   
   # Update version and changelog
   # Run tests
   pytest
   
   # Create tag
   git tag v1.1.0
   git push origin v1.1.0
   
   # Build and publish
   python setup.py sdist bdist_wheel
   twine upload dist/*

Thank You!
----------

Thank you for contributing to OpenConvert! Every contribution, whether it's code, documentation, bug reports, or feature suggestions, helps make the project better for everyone.

See Also
--------

- :doc:`architecture` - Project architecture overview
- :doc:`testing` - Detailed testing guide
- `GitHub Repository <https://github.com/openagents/openconvert>`_
- `Discord Community <https://discord.gg/openagents>`_ 