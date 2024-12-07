# The MIT License (MIT)
# 
# Copyright (c) 2014 Andreas Dewes
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='checkmate5',
    version='4.0.101',
    license='MIT',
    install_requires=[
        'blitzdb5',
        'pyyaml',
        'sqlalchemy'
    ],
    entry_points={
        'console_scripts': [
            'checkmate = checkmate.scripts.manage:main',
        ],
    },
    description='A meta-code checker written in Python.',
    long_description="""\
Checkmate is a cross-language (meta-)tool for static code analysis, written in Python.
Unlike other tools, it provides a global overview of the code quality in a project and aims
to provide clear, actionable insights to the user.

Documentation
=============

The documentation can be found `here <https://github.com/tcosolutions/checkmate>`.

Source Code
===========

The source code can be found on `Github <https://github.com/tcosolutions/checkmate>`.

""",
    long_description_content_type='text/markdown',
)

