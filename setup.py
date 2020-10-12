#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 SeatGeek

# This file is part of fuzzywuzzy.

from spacyEntityLinker import __version__
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='spacy-entity-linker',
    version=__version__,
    author='Emanuel Gerber',
    author_email='emanuel.j.gerber@gmail.com',
    packages=['spacyEntityLinker'],
    url='https://github.com/egerber/spacy-entity-linker',
    license="MIT",
    classifiers=["Environment :: Console",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Science/Research",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: POSIX :: Linux",
                 "Programming Language :: Cython",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.4"
                 ],
    description='Linked Entity Pipeline for spaCy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=True,
)
