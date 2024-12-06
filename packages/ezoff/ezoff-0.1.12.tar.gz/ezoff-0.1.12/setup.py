from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ezoff",
    version="0.1.12",
    description="Python package that acts as a wrapper for the EZOffice API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jordan Maynor",
    author_email="jmaynor@pepsimidamerica.com",
    url="https://github.com/pepsimidamerica/ezoff",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=required,
)
