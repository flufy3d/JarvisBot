# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('LICENSE') as f:
    license = f.read()

setup(
    name='JarvisBot',
    version='0.1.0',
    description='a telegram bot ,for personal transaction management and chat',
    long_description=readme,
    author='flufy3d',
    author_email='flufy3d@gmail.com',
    url='https://github.com/flufy3d/JarvisBot',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
