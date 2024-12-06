#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='dfss',
    version='1.7.12',
    author='zetao.zhang',
    author_email='zetao.zhang@sophgo.com',
    description='download_from_sophon_sftp',
    packages=find_packages(),
	package_data={"dfss":["output/*"]},
    include_package_data=True,
)
