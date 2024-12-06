#!/usr/bin/env python
from __future__ import division, absolute_import, print_function,\
    unicode_literals
import sys
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()


if sys.version_info < (2, 6):
    print("Sorry, this module only works on 2.6+, 3+")
    sys.exit(1)


setup(name='sas7bdatx',
      version='2.2.3.3',
      author='Jared Hobbs, Yao Xiao',
      author_email='kaellwen@gmail.com',
      license='MIT',
      url='https://github.com/kaellwen/sas7bdat.git',
      description='A sas7bdat file reader for Python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      py_modules=['sas7bdat'],
      scripts=['scripts/sas7bdat_to_csv'],
      install_requires=['six>=1.8.0'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Text Processing',
          'Topic :: Utilities',
      ],
      keywords=['sas', 'sas7bdat', 'csv', 'converter'])
