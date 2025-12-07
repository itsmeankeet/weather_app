# to install local package in editable mode

from setuptools import setup, find_packages

setup(
    name='weather_app',
    author='itsmeankeet',
    description='A package for finding weather information',
    author_email='adhikariankit55@gmail.com',
    version='0.0.1',
    packages=find_packages()
)