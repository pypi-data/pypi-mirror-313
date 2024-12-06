import sys
import os

from setuptools import setup, find_packages

# Don't import dawnai module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dawnai'))
from version import VERSION

setup(
    name="dawnai",
    version=VERSION,
    description="Dawn (Python SDK)",
    author="Dawn",
    author_email="sdk@dawnai.com",
    long_description="For questions, email us at sdk@dawnai.com",
    long_description_content_type="text/markdown",
    url="https://dawnai.com",
    packages=find_packages(include=["dawnai", "README.md"]),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
