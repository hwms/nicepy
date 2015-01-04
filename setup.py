# -*- coding: utf-8 *-*
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="nicepy",
    version="0.0.2",
    author="Mathias Seidler",
    author_email="seishin@gmail.com",
    description=("Nice python tools for those who want to stay sane."),
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
