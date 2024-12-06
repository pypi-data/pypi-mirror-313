from setuptools import setup, find_packages
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open(os.path.join("rangy", "__version__.py")) as f:
    exec(f.read())

setup(
    name="rangy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sphinx-rtd-theme==3.0.2",
        "sphinxcontrib-applehelp==2.0.0",
        "sphinxcontrib-devhelp==2.0.0",
        "sphinxcontrib-htmlhelp==2.1.0",
        "sphinxcontrib-jquery==4.1",
        "sphinxcontrib-jsmath==1.0.1",
        "sphinxcontrib-qthelp==2.0.0",
        "sphinxcontrib-serializinghtml==2.0.0",
        "rstcheck==6.2.4",
        "rstcheck-core==1.2.1",
        "doc8==1.1.2"
    ],
    extras_require={
        "testing": ["pytest"],
    },
    author="Arthur Debert",
    author_email="arthur@debert.xyz",
    description="A library for distributing items based on flexible count specifications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arthur-debert/rangy",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
