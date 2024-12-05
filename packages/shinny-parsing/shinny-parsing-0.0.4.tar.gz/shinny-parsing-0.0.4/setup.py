#!usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'mayanqiong'

import setuptools

setuptools.setup(
    name='shinny-parsing',
    version='0.0.4',
    packages=setuptools.find_packages(),
    url='https://www.shinnytech.com/',
    author='mayanqiong',
    author_email='mayanqiong@shinnytech.com',
    description='parse settlement file',
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=['pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)

