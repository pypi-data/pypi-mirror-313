from os import path
from setuptools import setup, find_packages
import os

# Read the contents of your description file
this_directory = os.path.dirname(__file__)  # Change to the directory of setup.py
description_file_path = path.join(this_directory, "README.md")
with open(description_file_path, encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="whatsapp-flows",
    version="0.1.0",
    description="Opensource python wrapper for Meta Whatsapp Flows Cloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/misingo255/whatsapp-flows",
    author="Wilbert Misingo",
    author_email="wilbertmisingo@gmail.com",
    license="Apache",
    packages=find_packages(),  # Automatically find your packages
    install_requires=["requests>=2.31.0"],  # External dependencies
    keywords=[
        "Whatsapp",
        "Whatsapp Flows",
        "Whatsapp API",
        "Whatsapp Python",
        "Whatsapp Python API",
        "Whatsapp Flows Python API",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
