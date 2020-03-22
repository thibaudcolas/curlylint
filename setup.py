#!/usr/bin/env python

import io

from setuptools import find_packages, setup

with io.open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='curlylint',
    version='0.5.0',
    license='MIT',
    description='A linter for Jinja-like templates. Forked from jinjalint',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Thibaud Colas',
    author_email='thibaudcolas@gmail.com',
    url='https://github.com/thibaudcolas/curlylint',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'parsy==1.1.0',
        'attrs==17.2.0',
        'docopt==0.6.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': ['jinjalint=jinjalint.cli:main'],
    },
)
