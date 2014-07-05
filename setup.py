# -*- coding: utf-8 *-*
import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="nicepy",
    version="0.0.1",
    author="Mathias Seidler",
    author_email="seishin@gmail.com",
    description=("Nice python tools to stay sane."),
    license="BSD",
    url="https://github.com/katakumpo/nicepy",
    packages=find_packages(exclude=['tests*']),
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
