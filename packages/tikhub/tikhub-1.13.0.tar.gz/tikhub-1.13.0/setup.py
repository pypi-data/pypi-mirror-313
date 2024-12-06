#! /usr/bin/env python
# -*- coding: utf-8 -*-
# RUN Command Line:
# 1.Build-check dist folder
# python setup.py sdist bdist_wheel
# 2.Upload to PyPi
# twine upload dist/*

from setuptools import setup, find_packages
from tikhub import version

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name="tikhub",
    version=version,
    author="TikHub.io",
    author_email="tikhub.io@proton.me",
    description="A Python SDK for TikHub RESTful API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TikHubIO/TikHub-API-Python-SDK",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "httpx>=0.27.0",
        "rich~=13.7.1",
        "websockets~=12.0",
    ],
)
