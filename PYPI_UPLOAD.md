# PyPI Upload Guide for OpenConvert

This guide explains how to upload the openconvert package to PyPI (Python Package Index).

## 📋 Prerequisites

### Required Tools
```bash
pip install build twine
```

### PyPI Account Setup
1. Create accounts on both:
   - **TestPyPI**: https://test.pypi.org/account/register/
   - **PyPI**: https://pypi.org/account/register/

2. Enable 2FA (Two-Factor Authentication) for security

3. Create API tokens:
   - **TestPyPI**: https://test.pypi.org/manage/account/token/
   - **PyPI**: https://pypi.org/manage/account/token/

## 🚀 Quick Upload Process

### Automated Upload (Recommended)
Use the provided helper script:

```bash
# 1. Prepare and build package
python scripts/pypi_upload.py all

# 2. Test upload to TestPyPI
python scripts/pypi_upload.py test-upload

# 3. Test installation from TestPyPI
pip install -i https://test.pypi.org/simple/ openconvert

# 4. Upload to production PyPI
python scripts/pypi_upload.py upload
```

### Manual Upload Process

#### Step 1: Clean and Prepare
```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info/

# Validate package structure
python scripts/pypi_upload.py prepare
```

#### Step 2: Build Distribution Files
```bash
# Build source distribution and wheel
python -m build
# or
python setup.py sdist bdist_wheel
```

#### Step 3: Check Package Quality
```bash
# Validate distributions
twine check dist/*
```

#### Step 4: Upload to TestPyPI
```bash
# Upload to TestPyPI for testing
twine upload --repository testpypi dist/*
```

#### Step 5: Test Installation
```bash
# Create new virtual environment
python -m venv test_env
source test_env/bin/activate  # Linux/Mac
# or test_env\Scripts\activate  # Windows

# Install from TestPyPI
pip install -i https://test.pypi.org/simple/ openconvert

# Test the installation
openconvert --help
python -c "import openconvert; print(openconvert.__version__)"
```

#### Step 6: Upload to Production PyPI
```bash
# Upload to production PyPI
twine upload dist/*
```

## 🔐 Authentication Methods

### Method 1: Interactive (Prompted)
When you run upload commands, you'll be prompted for:
- Username: `__token__`
- Password: Your API token (starts with `pypi-`)

### Method 2: Environment Variables
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-AgEIcHlwaSKNF...  # Your API token

# Now uploads won't prompt for credentials
twine upload dist/*
```

### Method 3: Configuration File
Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaSKNF...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaSKNF...
```

## 📦 Package Information

### Current Version: 1.0.0

### Package Details
- **Name**: `openconvert`
- **Homepage**: https://github.com/acenta-ai/openconvert
- **Documentation**: https://openconvert.readthedocs.io/
- **License**: MIT
- **Python Support**: 3.8+

### Installation After Upload
```bash
# Regular installation
pip install openconvert

# Development installation
pip install openconvert[dev]

# Service installation (with agconvert)
pip install openconvert[service]

# Documentation building
pip install openconvert[docs]
```

## 🧪 Testing Your Upload

### Test Commands
```bash
# Test CLI functionality
openconvert --version
openconvert --help

# Test Python API
python -c "
import openconvert
print(f'Version: {openconvert.__version__}')
result = openconvert.convert('test.txt', 'text/plain', 'text/markdown')
print('API working!')
"

# Test module execution
python -m openconvert --help
```

### Verification Checklist
- [ ] Package installs without errors
- [ ] CLI command `openconvert` is available
- [ ] Python import `import openconvert` works
- [ ] Version matches expected: `openconvert.__version__`
- [ ] Entry points work correctly
- [ ] Dependencies are installed automatically

## 🔄 Version Updates

### Before Each Upload
1. **Update version** in `openconvert/__init__.py`:
   ```python
   __version__ = "1.1.0"  # Increment appropriately
   ```

2. **Update changelog** in `README.md`

3. **Test locally**:
   ```bash
   python scripts/pypi_upload.py all
   ```

4. **Commit changes**:
   ```bash
   git add .
   git commit -m "Bump version to 1.1.0"
   git tag v1.1.0
   git push origin master --tags
   ```

### Semantic Versioning
- **Patch** (1.0.1): Bug fixes, no breaking changes
- **Minor** (1.1.0): New features, backwards compatible
- **Major** (2.0.0): Breaking changes

## 🚨 Troubleshooting

### Common Issues

#### 1. Authentication Failed
```
403 Forbidden: Invalid or expired token
```
**Solution**: Check your API token and ensure it's correctly set.

#### 2. Package Already Exists
```
400 Bad Request: File already exists
```
**Solution**: You cannot re-upload the same version. Increment the version number.

#### 3. Package Name Conflict
```
403 Forbidden: The user 'X' isn't allowed to upload to project 'Y'
```
**Solution**: The package name might be taken. Choose a different name.

#### 4. Missing Dependencies
```
error: Microsoft Visual C++ 14.0 is required
```
**Solution**: Install build tools or use a different environment.

#### 5. Large Package Size
```
413 Request Entity Too Large
```
**Solution**: Exclude unnecessary files using `MANIFEST.in` or `.gitignore`.

### Debug Commands
```bash
# Check package contents
python -m zipfile -l dist/openconvert-1.0.0-py3-none-any.whl

# Inspect package metadata
python -m pip show openconvert

# Check installed files
python -c "import openconvert; print(openconvert.__file__)"
```

## 📚 References

- [PyPI Documentation](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)

## 🎯 Production Checklist

Before uploading to production PyPI:

- [ ] Package builds successfully
- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] Version number is incremented
- [ ] Changelog is updated
- [ ] Test upload to TestPyPI successful
- [ ] Test installation from TestPyPI works
- [ ] Git tags created
- [ ] Repository is clean (no uncommitted changes)

## 📈 Post-Upload Steps

1. **Verify listing**: Check https://pypi.org/project/openconvert/
2. **Test installation**: `pip install openconvert`
3. **Update documentation**: Link to PyPI package
4. **Announce release**: GitHub releases, social media, etc.
5. **Monitor downloads**: PyPI provides download statistics

---

**Ready to upload?** Use the automated script:

```bash
python scripts/pypi_upload.py all
python scripts/pypi_upload.py test-upload
python scripts/pypi_upload.py upload
``` 