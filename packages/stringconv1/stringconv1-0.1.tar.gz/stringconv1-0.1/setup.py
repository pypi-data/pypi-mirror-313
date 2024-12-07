import setuptools
from pathlib import Path

setuptools.setup(
    name="stringconv1",
    version='0.1',
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=['data', 'test'])
)