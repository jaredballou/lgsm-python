# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='lgsm',
    version='0.0.1',
    description='Linux Game Server Manager for Steam-based games',
    long_description=readme,
    author='Jared Ballou',
    author_email='lgsm@jballou.com',
    url='https://github.com/jaredballou/lgsm-python',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'gamedata')),
    scripts=['bin/lgsm'],
)

