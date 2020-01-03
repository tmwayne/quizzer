#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

"""
description: Setup tools to create python package
author: Tyler Wayne
data created:
last modified:
"""

######################################################################
### SETUP
######################################################################

import setuptools


######################################################################
### MAIN
######################################################################

if __name__ == '__main__':

    with open("README", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="quizzer-twayne",
        version="0.5.0",
        author="Tyler Wayne",
        author_email="tylerwayne3@gmail.com",
        description="Administer a quiz provided by the user",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="git@github.com:tmwayne/quizzer.git",
        packages=["quizzer"],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
    )

