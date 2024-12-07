from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name = 'colorich',
    author='Ethan Amar',
    author_email='EthanA120@Gmail.com',
    version = '0.6.1',
    packages = [],
    long_description = description,
    long_description_content_type = "text/markdown",
)