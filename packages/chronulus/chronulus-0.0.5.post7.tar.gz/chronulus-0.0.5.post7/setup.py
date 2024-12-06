import pathlib
from setuptools import setup, find_packages, Extension

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "PUBLIC_PACKAGE_README.md").read_text()

version = "0.0.5-7"

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# This call to setup() does all the work
setup(
    name="chronulus",
    version=version,
    description="Chronulus AI Python SDK",
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
    packages=find_packages(where="src"),
    package_data={
        "chronulus": [
            "etc/*.env",  # Include all .env files in etc directory
        ],
    },
    include_package_data=False,
    install_requires=requirements,
)