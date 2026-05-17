#!/usr/bin/env python3
"""
DocBridge - Markdown to Office Document Converter
"""
from setuptools import setup, find_packages

setup(
    name="docbridge",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
)
