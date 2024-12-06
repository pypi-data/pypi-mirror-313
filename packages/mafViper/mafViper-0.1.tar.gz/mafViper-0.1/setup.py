# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:57:31 2024

@author: Joseph Rosen


"""

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description=f.read()

setup(
    name="mafViper",  # Package name
    version="0.1",  # Initial version
    author="Joseph Rosen",
    author_email="joemrosen@gmail.com",
    description="A Python package for processing, analyzing and visualizing MAF files.",
    packages=find_packages(exclude=["tests", "prototypes", "*.pdf", "*.maf", "*.csv", "*.xlsx" ]),
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrosen-code/mafViper",  
    python_requires=">=3.9",  # Minimum Python version
    install_requires=[
        "pandas>=2.2.2",
        "seaborn>=0.13.2",
        "matplotlib>=3.9.2",
    ],
    include_package_data=True,  # Ensures non-code files like README are included
)

