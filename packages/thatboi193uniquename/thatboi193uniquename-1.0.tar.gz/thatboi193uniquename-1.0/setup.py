import setuptools
from pathlib import Path
setuptools.setup(
    name="thatboi193uniquename",
    version="1.0",
    long_description=Path("readme.md").read_text(),
    packages= setuptools.find_packages(exclude=["data", "tests"])
)