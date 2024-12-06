from setuptools import setup, find_packages
from os import path

working_directory = path.abspath(path.dirname(__file__))
with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "build_a_brain_stani123",
    version = "0.0.2",
    author = "Noah Stanis",
    author_email = 'stani123@uw.edu',
    description = 'Builds a 5 layer LIF network',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages = find_packages(),
    install_requires = []
)