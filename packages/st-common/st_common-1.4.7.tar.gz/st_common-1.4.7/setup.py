#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re

from setuptools import setup


# Get the version
APP_NAME = "st_common"

version_regex = r'__version__ = ["\']([^"\']*)["\']'
with open("st_common/__init__.py", "r",encoding="utf-8") as f:
    text = f.read()
    match = re.search(version_regex, text)

    if match:
        VERSION = match.group(1)
    else:
        raise RuntimeError("No version number found!")




# Publish Helper.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

def readall(path):
    with open(path,"r",encoding="utf-8") as fp:
        return fp.read()


setup(
    name=APP_NAME,
    version=VERSION,
    description="suitcase in st st_common module",
    long_description=readall("README.md") + "\n\n" + readall("HISTORY.md"),
    long_description_content_type="text/markdown",
    author="St",
    author_email="st@gmail.com",
    url="https://github.com/VinMing/common",
    packages=["st_common"],
    python_requires=">=3.10",  # 指定至少需要 Python 3.10
    install_requires=[ "requests", "SQLAlchemy","redis","pymongo","pandas","python-dotenv","pycryptodome","Pillow","paddlepaddle","paddleocr"],
    test_suite='tests',
    extras_require={},
    license="ISC",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    zip_safe=False,
)