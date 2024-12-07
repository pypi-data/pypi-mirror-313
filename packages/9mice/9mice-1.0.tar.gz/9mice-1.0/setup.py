import setuptools
from pathlib import Path

setuptools.setup(
    name = "9mice",
    version = "1.0",
    long_descriptiong= Path("README.md").read_text(),
    packages = setuptools.find_packages(exclude=['data', 'test'])
)