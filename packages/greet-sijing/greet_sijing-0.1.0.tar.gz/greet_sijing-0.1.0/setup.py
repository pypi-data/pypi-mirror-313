#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 11:29:58 2024

@author: michellel
"""

from setuptools import setup, find_packages

setup(
    name="greet_sijing",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple greeting module.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/greet",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
