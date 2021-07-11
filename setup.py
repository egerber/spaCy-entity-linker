#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
    version='1.0.1',
    author='Emanuel Gerber',
    author_email='emanuel.j.gerber@gmail.com',
    packages=['spacy_entity_linker'],
    url='https://github.com/egerber/spacy-entity-linker',
    license="MIT",
    classifiers=["Environment :: Console",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Science/Research",
                 "License :: OSI Approved :: MIT License",
                 "Programming Language :: Cython",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 3.6"
                 ],
    description='Linked Entity Pipeline for spaCy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=True,
    install_requires=[
        'spacy>=3.0.0',
        'numpy>=1.0.0'
    ],
    entry_points={
        'spacy_factories': 'entityLinker = spacy_entity_linker.EntityLinker:EntityLinker'
    }
)
