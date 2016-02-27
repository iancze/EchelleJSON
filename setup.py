#!/usr/bin/env python

import os
import sys
from setuptools import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

# Hackishly synchronize the version.
version = r"0.1.0"

setup(
    name="EchelleJSON",
    version=version,
    author="Ian Czekala",
    author_email="iancze@gmail.com",
    url="https://github.com/iancze/EchelleJSON",
    py_modules=["EchelleJSON"],
    description="A simple JSON format for Echelle spectra",
    long_description=open("README.rst").read(),
    package_data={"": ["LICENSE"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
