import os
import re
import sys
import platform
import subprocess
import multiprocessing

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

if sys.version_info < (3, 6):
    print('Python 3.6 or higher required, please upgrade.')
    sys.exit(1)

VERSION = '0.1'
REQUIREMENTS = ['numpy', 'numba', 'vtk', 'matplotlib']

setup(name='checkmesh',
    version=VERSION,
    author='Jannick Wolters',
    description='FEM mesh analysis tool',
    long_description='',
    packages=['checkmesh'],
    package_dir={'': 'src'},
    install_requires=REQUIREMENTS,
    zip_safe=False)