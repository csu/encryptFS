#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
  name='encryptfs',
  version='0.0.1',
  description='A simple file system that encrypts files individually.',
  long_description=open('README').read(),
  author='Christopher Su',
  author_email='gh@christopher.su',
  url='https://github.com/csu/encryptFS',
  packages=find_packages(),
  install_requires=[
    'pycrypto==2.6.1',
    'wheel==0.24.0',
  ],
  entry_points={
    'console_scripts': [
      'encryptfs=encryptfs.cli:cli_entry'
    ],
  }
)
