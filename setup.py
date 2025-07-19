#!/usr/bin/env python3
"""Setup script for openconvert CLI tool."""

from setuptools import setup, find_packages
import os
import re

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "OpenConvert CLI tool for connecting to OpenAgents file conversion network"

# Get version from __init__.py
def get_version():
    init_path = os.path.join(os.path.dirname(__file__), "openconvert", "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        content = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")

setup(
    name="openconvert",
    version=get_version(),
    description="CLI tool for connecting to OpenConvert OpenAgents network for file conversion",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="OpenAgents Team",
    author_email="team@openagents.com",
    maintainer="OpenAgents Team",
    maintainer_email="team@openagents.com",
    url="https://github.com/acenta-ai/openconvert",
    project_urls={
        "Bug Reports": "https://github.com/acenta-ai/openconvert/issues",
        "Source": "https://github.com/acenta-ai/openconvert",
        "Documentation": "https://openconvert.readthedocs.io/",
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyyaml>=5.4.0",
        "openagents>=0.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.17.0",
        ],
        "service": [
            "agconvert",  # Optional for running conversion services
        ],
    },
    entry_points={
        "console_scripts": [
            "openconvert=openconvert.openconvert_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    keywords="file conversion, openagents, cli, network, format conversion, document conversion",
    python_requires=">=3.8",
    zip_safe=False,
) 