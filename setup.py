#!/usr/bin/env python

import io

from setuptools import find_packages, setup  # type: ignore

from curlylint import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __name__,
    __url__,
    __version__,
)

with io.open("README.md", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name=__name__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    copyright=__copyright__,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    package_data={"curlylint": ["py.typed"]},
    keywords=[
        "curlylint",
        "linter",
        "linting",
        "jinja",
        "jinja2",
        "django templates",
        "twig",
        "nunjucks",
        "liquid",
        "templates",
        "html",
    ],
    python_requires=">=3.6",
    install_requires=[
        "parsy==1.1.0",
        "attrs>=17.2.0",
        "click>=6.5",
        "toml>=0.9.4",
        "pathspec>=0.6, <1",
        "dataclasses>=0.6; python_version < '3.7'",
    ],
    extras_require={
        "dev": [
            "black==19.10b0",
            "isort==4.2.5",
            "flake8==3.7.8",
            "mypy==0.770",
            "pytest==5.4.2",
            "coverage==5.1",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Quality Assurance",
        "Typing :: Typed",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["curlylint=curlylint.cli:patched_main"]},
)
