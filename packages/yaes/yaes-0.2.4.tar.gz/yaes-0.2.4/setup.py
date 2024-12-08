#!/usr/bin/env python

import os
from setuptools import setup

with open("README.rst", "r") as readme_file:
    long_description = readme_file.read()

version = os.environ.get("BUILD_VERSION")

if version is None:
    with open("VERSION", "r") as version_file:
        version = version_file.read().strip()

setup(
    name="yaes",
    version=version,
    package_dir = {'': 'lib'},
    py_modules = [
        'yaes'
    ],
    install_requires=[
        'Jinja2==3.1.2',
        'overscore==0.1.1',
        'MarkupSafe==2.1.5'
    ],
    url=f"https://yaes.readthedocs.io/en/{version}/",
    download_url="https://github.com/gaf3/yaes",
    author="Gaffer Fitch",
    author_email="yaes@gaf3.com",
    description="Yet Another Expansion Syntax (pronounced 'Yasssss Kweeeeen')",
    long_description=long_description,
    license_files=('LICENSE.txt',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
