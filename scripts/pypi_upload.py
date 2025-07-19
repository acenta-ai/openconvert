#!/usr/bin/env python3
"""
PyPI Upload Helper Script

Automates the process of preparing and uploading the openconvert package to PyPI.
Includes validation, building, and uploading steps.

Usage:
    python scripts/pypi_upload.py prepare     # Prepare package for upload
    python scripts/pypi_upload.py build       # Build distribution files
    python scripts/pypi_upload.py check       # Check distribution files
    python scripts/pypi_upload.py upload      # Upload to PyPI
    python scripts/pypi_upload.py test-upload # Upload to TestPyPI
    python scripts/pypi_upload.py clean       # Clean build artifacts
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_color(color: str, message: str):
    """Print colored output."""
    print(f"{color}{message}{Colors.NC}")

def run_command(cmd: List[str], description: str, check: bool = True) -> bool:
    """Run a command and print the result."""
    print_color(Colors.BLUE, f"🔄 {description}...")
    print(f"   Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print_color(Colors.GREEN, f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print_color(Colors.RED, f"❌ {description} failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except subprocess.CalledProcessError as e:
        print_color(Colors.RED, f"❌ {description} failed with exit code {e.returncode}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False
    except Exception as e:
        print_color(Colors.RED, f"❌ {description} failed: {e}")
        return False

def check_requirements() -> bool:
    """Check if required tools are installed."""
    print_color(Colors.BLUE, "🔍 Checking requirements...")
    
    required_tools = [
        ("python", "Python interpreter"),
        ("pip", "Python package installer"),
    ]
    
    optional_tools = [
        ("twine", "PyPI upload tool (install with: pip install twine)"),
        ("build", "Build tool (install with: pip install build)"),
    ]
    
    all_good = True
    
    # Check required tools
    for tool, description in required_tools:
        if not shutil.which(tool):
            print_color(Colors.RED, f"❌ Missing required tool: {tool} ({description})")
            all_good = False
        else:
            print_color(Colors.GREEN, f"✅ Found: {tool}")
    
    # Check optional tools
    for tool, description in optional_tools:
        if not shutil.which(tool):
            print_color(Colors.YELLOW, f"⚠️  Missing optional tool: {tool} ({description})")
        else:
            print_color(Colors.GREEN, f"✅ Found: {tool}")
    
    return all_good

def clean_build_artifacts():
    """Clean build artifacts."""
    print_color(Colors.BLUE, "🧹 Cleaning build artifacts...")
    
    artifacts = [
        "build/",
        "dist/",
        "*.egg-info/",
        "**/__pycache__/",
        "**/*.pyc",
        "**/*.pyo",
    ]
    
    project_root = Path(__file__).parent.parent
    
    for pattern in artifacts:
        if pattern.endswith("/"):
            # Directory pattern
            for path in project_root.glob(pattern):
                if path.is_dir():
                    print(f"   Removing directory: {path}")
                    shutil.rmtree(path)
        else:
            # File pattern
            for path in project_root.rglob(pattern):
                if path.is_file():
                    print(f"   Removing file: {path}")
                    path.unlink()
    
    print_color(Colors.GREEN, "✅ Build artifacts cleaned")

def prepare_package() -> bool:
    """Prepare the package for upload."""
    print_color(Colors.BLUE, "📦 Preparing package for PyPI...")
    
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Check if required files exist
    required_files = [
        "LICENSE",
        "README.md",
        "setup.py",
        "pyproject.toml",
        "MANIFEST.in",
        "openconvert/__init__.py",
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print_color(Colors.RED, f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print_color(Colors.GREEN, "✅ All required files present")
    
    # Validate package structure
    if not Path("openconvert/__init__.py").exists():
        print_color(Colors.RED, "❌ Package structure invalid: missing openconvert/__init__.py")
        return False
    
    print_color(Colors.GREEN, "✅ Package structure validated")
    return True

def build_package() -> bool:
    """Build the package distribution files."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Clean first
    clean_build_artifacts()
    
    # Try using build tool first, fall back to setup.py
    if shutil.which("python") and shutil.which("build"):
        success = run_command([
            sys.executable, "-m", "build"
        ], "Building package with build tool")
    else:
        # Fallback to setup.py
        print_color(Colors.YELLOW, "⚠️  build tool not found, using setup.py")
        success = run_command([
            sys.executable, "setup.py", "sdist", "bdist_wheel"
        ], "Building package with setup.py")
    
    if success:
        # List built files
        dist_dir = Path("dist")
        if dist_dir.exists():
            files = list(dist_dir.glob("*"))
            print_color(Colors.GREEN, f"✅ Built {len(files)} distribution files:")
            for file_path in files:
                print(f"   - {file_path}")
    
    return success

def check_package() -> bool:
    """Check the built package using twine."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    if not shutil.which("twine"):
        print_color(Colors.YELLOW, "⚠️  twine not found, skipping package check")
        print("   Install with: pip install twine")
        return True
    
    dist_dir = Path("dist")
    if not dist_dir.exists() or not list(dist_dir.glob("*")):
        print_color(Colors.RED, "❌ No distribution files found. Run build first.")
        return False
    
    return run_command([
        "twine", "check", "dist/*"
    ], "Checking package with twine")

def upload_to_testpypi() -> bool:
    """Upload package to TestPyPI."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    if not shutil.which("twine"):
        print_color(Colors.RED, "❌ twine not found. Install with: pip install twine")
        return False
    
    print_color(Colors.YELLOW, "📤 Uploading to TestPyPI...")
    print("   You will be prompted for your TestPyPI credentials")
    print("   Or set TWINE_USERNAME and TWINE_PASSWORD environment variables")
    
    return run_command([
        "twine", "upload", "--repository", "testpypi", "dist/*"
    ], "Uploading to TestPyPI", check=False)

def upload_to_pypi() -> bool:
    """Upload package to PyPI."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    if not shutil.which("twine"):
        print_color(Colors.RED, "❌ twine not found. Install with: pip install twine")
        return False
    
    print_color(Colors.YELLOW, "📤 Uploading to PyPI...")
    print("   ⚠️  WARNING: This will upload to the production PyPI!")
    print("   You will be prompted for your PyPI credentials")
    print("   Or set TWINE_USERNAME and TWINE_PASSWORD environment variables")
    
    # Ask for confirmation
    response = input("   Are you sure you want to upload to PyPI? (yes/no): ")
    if response.lower() != "yes":
        print_color(Colors.YELLOW, "⚠️  Upload cancelled")
        return False
    
    return run_command([
        "twine", "upload", "dist/*"
    ], "Uploading to PyPI", check=False)

def show_help():
    """Show help information."""
    print("PyPI Upload Helper for openconvert")
    print("")
    print("Commands:")
    print("  prepare     - Check requirements and validate package structure")
    print("  build       - Build source and wheel distributions")
    print("  check       - Check distributions with twine")
    print("  test-upload - Upload to TestPyPI for testing")
    print("  upload      - Upload to production PyPI")
    print("  clean       - Clean build artifacts")
    print("  all         - Run prepare, build, and check steps")
    print("")
    print("Installation requirements:")
    print("  pip install build twine")
    print("")
    print("Environment variables (optional):")
    print("  TWINE_USERNAME  - PyPI username")
    print("  TWINE_PASSWORD  - PyPI password")
    print("")
    print("Example workflow:")
    print("  python scripts/pypi_upload.py all")
    print("  python scripts/pypi_upload.py test-upload")
    print("  python scripts/pypi_upload.py upload")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="PyPI Upload Helper for openconvert",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "command",
        choices=["prepare", "build", "check", "test-upload", "upload", "clean", "all", "help"],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    if args.command == "help":
        show_help()
        return
    
    print_color(Colors.BLUE, "🚀 OpenConvert PyPI Upload Helper")
    print()
    
    success = True
    
    if args.command in ["prepare", "all"]:
        if not check_requirements():
            print_color(Colors.RED, "❌ Requirements check failed")
            success = False
        if success and not prepare_package():
            print_color(Colors.RED, "❌ Package preparation failed")
            success = False
    
    if args.command in ["build", "all"] and success:
        if not build_package():
            print_color(Colors.RED, "❌ Package build failed")
            success = False
    
    if args.command in ["check", "all"] and success:
        if not check_package():
            print_color(Colors.RED, "❌ Package check failed")
            success = False
    
    if args.command == "test-upload":
        if not upload_to_testpypi():
            print_color(Colors.RED, "❌ TestPyPI upload failed")
            success = False
    
    if args.command == "upload":
        if not upload_to_pypi():
            print_color(Colors.RED, "❌ PyPI upload failed")
            success = False
    
    if args.command == "clean":
        clean_build_artifacts()
    
    if success:
        print()
        print_color(Colors.GREEN, "🎉 All operations completed successfully!")
        if args.command == "all":
            print()
            print("Next steps:")
            print("1. Test upload: python scripts/pypi_upload.py test-upload")
            print("2. Test install: pip install -i https://test.pypi.org/simple/ openconvert")
            print("3. Production upload: python scripts/pypi_upload.py upload")
    else:
        print()
        print_color(Colors.RED, "❌ Some operations failed. Check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 