#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'LICENSE.rst'), encoding='utf-8') as f:
    license = f.read()

version = __import__('visualsnoop').__version__

setup(
    name='visualsnoop',
    version=version,

    description='VisualSnoop client module for Python',
    long_description=long_description,

    url='https://github.com/visualsnoop/visualsnoop-client-python',

    author='Janoš Guljaš',
    author_email='janos@visualsnoop.com',

    license=license,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='visualsnoop',

    packages=find_packages(exclude=['docs', 'tests*']),

    install_requires=[
        'six>=1.9.0',
        'requests>=2.5.1',
    ],

    extras_require={
        'docs': [
            'sphinx',
            'sphinx_rtd_theme',
        ],
    },
)
