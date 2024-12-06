from setuptools import setup, find_packages
import os
# Reading the long description from README.md
if os.path.exists("readme.md"):
    with open("readme.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = ""  # Fallback if the README doesn't exist

setup(
    name="kurumii_events",  # Replace with your package name
    version="0.0.3.7",  # Semantic versioning
    description="A Module containing a basic Event System",  # Short description
    long_description=long_description,  # Detailed description from README
    long_description_content_type="text/markdown",  # Use Markdown for the long description
    packages=find_packages(),  # Automatically discover all sub-packages
    install_requires=[],  # List dependencies here, if any
    extras_require={},  # Optional dependencies can be added here
    classifiers=[  # Metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version requirement
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
)