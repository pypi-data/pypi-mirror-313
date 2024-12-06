#!/usr/bin/env python

from setuptools import setup,find_packages
import pathlib,os

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

version = os.environ["PYTHON_EIGEN_INGENUITY_VERSION"]

install_requires = (HERE / "requirements.txt").read_text()

pkgname = 'python-eigen-ingenuity'

# Invoke setup
setup(
    name=pkgname,
    version=version,
    author='Murray Callander',
    author_email='info@eigen.co',
    url='https://www.eigen.co/',
    description="A python library used to query data from the Eigen Ingenuity system",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages("."),
    license='Apache License 2.0',
    install_requires=[install_requires],
    entry_points={
        'console_scripts': [
            'assetmodelbuilder=modelbuilder:__cli_entrypoint__',
        ],
    }
)