# standard libraries:
from setuptools import setup, find_packages
from typing import Dict, List, Any

# TODO: pip install twine wheel
# TODO: python setup.py sdist bdist_wheel
# TODO: twine upload dist/*

# setup:
application_packages: List[str] = find_packages()
application_settings: Dict[str, Any] = {
    "name": "TkEnhanced",
    "version": "2.2.2",
    "description": "Enhanced Tkinter widgets for a modern look and additional functionality.",
    "long_description": "This package includes enhanced widgets for Tkinter with a modern appearance and additional features. It aims to improve the aesthetics and functionality of Tkinter applications.",
    "long_description_content_type": "text/markdown",
    "author": "Bunnitown",
    "packages": application_packages,
    "install_requires": ["pillow>=10.4.0", "numpy>=2.1.1"],
    "classifiers": [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]}
setup(**application_settings)
