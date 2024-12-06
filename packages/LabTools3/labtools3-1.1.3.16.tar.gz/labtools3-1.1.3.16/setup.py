from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "LabTools3",
    version = "1.1.3.16",
    packages = find_packages(),
    # add additional files
    package_data = {'':['*.bat','*.command']},
    # meta data about package
    # metadata for upload to PyPI
    author = "Werner Boeglin",
    author_email = "boeglinw@fiu.edu",
    description = "Python 3 Package of modules for typical analysis tasks analyzing physics data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = "MIT",
    keywords = "Data Analysis",
    url = "http://wanda.fiu.edu/LabTools3",   # project home page, if any
    classifiers=[
        "Programming Language :: Python :: 3.8",
        ],
    python_requires='>=3.8'
)
