from setuptools import setup, find_packages
setup(
name='bank_calculator',
version='0.1.1',
author='Andrew Rawson',
email='arawson@proton.me',
description='A simple Python package that can calculate loan payments and dividends',
packages=find_packages(),
classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
],
python_requires='>= 3.12'
)
