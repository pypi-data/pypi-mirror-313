import os
import sys
import shutil
from setuptools import setup, find_packages, find_namespace_packages
from setuptools.command.install import install

setup(name='pyrre',
      version='1.0.0',
      description='PyRRE: Python code to run the fortran FERRE package to fit synthetic spectra',
      author='David Nidever',
      author_email='dnidever@montana.edu',
      url='https://github.com/dnidever/pyrre',
      requires=['numpy','astropy(>=4.0)','scipy','ferre'],
      zip_safe = False,
      include_package_data=True,
      packages=find_namespace_packages(where="python"),
      package_dir={"": "python"}
)
