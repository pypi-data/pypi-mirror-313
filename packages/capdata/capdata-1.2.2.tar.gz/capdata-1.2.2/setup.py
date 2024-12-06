# -*- coding: utf-8 -*-

from sys import version_info

from setuptools import setup, find_packages

__version__ = '1.2.2'  # 版本号
requirements = open('requirements.txt').readlines()  # 依赖文件

if version_info < (3, 8, 0):
    raise SystemExit('Sorry! capdata requires python 3.8.0 or later.')

setup(
    name='capdata',
    description='capdata  api',
    long_description='',
    license='',
    version=__version__,
    author='zbz',
    url='',
    py_modules=['capdata'],
    packages=find_packages(exclude=["test"]),
    python_requires='>= 3.8.0',
    install_requires=requirements
)
