# pyexportvba

[![PyPi Badge](https://img.shields.io/pypi/v/pyexportvba)](https://pypi.org/project/pyexportvba/)
![Publish](https://github.com/pyexportvba/pyexportvba/workflows/Publish/badge.svg)
![Test](https://github.com/pyexportvba/pyexportvba/workflows/Test/badge.svg)
[![Downloads](https://static.pepy.tech/personalized-badge/pyexportvba?period=week&units=international_system&left_color=black&right_color=orange&left_text=Last%20Week)](https://pepy.tech/project/pyexportvba)
[![Downloads](https://static.pepy.tech/personalized-badge/pyexportvba?period=month&units=international_system&left_color=black&right_color=orange&left_text=Month)](https://pepy.tech/project/pyexportvba)
[![Downloads](https://static.pepy.tech/personalized-badge/pyexportvba?period=total&units=international_system&left_color=black&right_color=orange&left_text=Total)](https://pepy.tech/project/pyexportvba)

A python package to export VBA code embedded in Excel files to separate BAS files.
`pyexportvba` is available on PyPI and can be installed with:

    pip install pyexportvba

## Features

The latest development version is always available at the project git
[repository](https://github.com/pyexportvba/pyexportvba).

## Development

To clone the library for development:

    git clone git@github.com:pyexportvba/pyexportvba.git

or

    git clone https://github.com/pyexportvba/pyexportvba.git

### Build The Virtual Environment

The current earliest Python version supported is `3.9`.
You need to be able to create a virtual environment at this version to make sure any changes you make is compatible.

If you are using `conda`:

    conda create --prefix=.venv python=3.9 --yes

If you are using `venv`, make sure you have the right base package:

    >> python --version
    Python 3.9.x

Once you verify your base Python, you can then create a virtual environment using:

    virtualenv -p py3.9 .venv

### Setup

Once you have created your virtual environment and made sure it is active in your current command line:

    pip install -e .[dev]

This should all the dependencies you need for developing into the library and also allow you to run the unit tests:

    pytest
