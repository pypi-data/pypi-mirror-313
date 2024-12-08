from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf8') as f:
    long_description = f.read()


setup(
    name='nixhelloworld',
    version="0.0.1",
    author="Nick Fleming",
    description='Simple hello world script',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
    # Add dependencies here.
    # e.g. 'nump>=1.11.1'
    ],
)
