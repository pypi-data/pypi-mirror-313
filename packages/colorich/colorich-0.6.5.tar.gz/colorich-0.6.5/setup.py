from setuptools import setup, find_packages

with open("README.md", "r") as f:
    ldescription = f.read()

setup(
    name = 'colorich',
    author='Ethan Amar',
    author_email='EthanA120@Gmail.com',
    version = '0.6.5',
    packages = find_packages(),
    install_requires = [
        "requests>=2.32.3",
        ],
    description = "Replace the classic print function with several colorful functions",
    long_description = ldescription,
    long_description_content_type = "text/markdown",
)