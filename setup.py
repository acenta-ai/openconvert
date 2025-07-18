#!/usr/bin/env python3
"""Setup script for openconvert CLI tool."""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "OpenConvert CLI tool for connecting to OpenAgents file conversion network"

setup(
    name="openconvert",
    version="1.0.0",
    description="CLI tool for connecting to OpenConvert OpenAgents network for file conversion",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="OpenAgents Team",
    author_email="team@openagents.com",
    url="https://github.com/openagents/openagents",
    packages=find_packages(),
    py_modules=["openconvert_cli"],
    install_requires=[
        "pyyaml",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-asyncio",
            "black",
            "flake8",
        ]
    },
    entry_points={
        "console_scripts": [
            "openconvert=openconvert_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications",
        "Topic :: Internet",
    ],
    python_requires=">=3.8",
) 