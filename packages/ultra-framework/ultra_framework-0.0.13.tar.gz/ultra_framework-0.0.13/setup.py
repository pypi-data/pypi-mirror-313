from setuptools import setup, find_packages
from pathlib import Path


setup(
    name="",
    version="0.0.2",
    author="Giorgio Ripani",
    author_email="g.ripani93@gmail.com",
    description="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Indipendent"
    ],
    python_requires=">=3.12",
    long_description=(Path(__name__).parent / "README.md").read_text()
)
