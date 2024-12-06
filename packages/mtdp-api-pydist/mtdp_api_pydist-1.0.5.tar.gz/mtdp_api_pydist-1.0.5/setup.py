#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
  long_description = f.read()


setup(name='mtdp_api_pydist',  # 包名
      version='1.0.5',  # 版本号
      description='A small example package',
      long_description=long_description,
      author='cloudflere',
      author_email='cloudflere@qq.com',
      url='https://cloudflere.com',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      include_package_data= True,
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ],
      )