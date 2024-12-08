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
    name="overscore",
    version=version,
    package_dir = {'': 'lib'},
    py_modules = [
        'overscore'
    ],
    install_requires=[
    ],
    url=f"https://overscore.readthedocs.io/en/{version}/",
    download_url="https://github.com/gaf3/overscore",
    author="Gaffer Fitch",
    author_email="overscore@gaf3.com",
    description="Double underscore access notation",
    long_description=long_description,
    license_files=('LICENSE.txt',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
