import pathlib
from setuptools import setup, find_packages, Extension


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

version = "0.0.4-10"

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# This call to setup() does all the work
setup(
    name="chronulus-core",
    version=version,
    description="Core components for Chronulus",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Chronulus AI",
    author_email="jeremy@chronulus.com",
    license="Apache",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=False,
    install_requires=requirements,
)