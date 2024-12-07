import setuptools

from pathlib import Path

setuptools.setup(
    name="nkvpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    # exclude tests and data directory
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
