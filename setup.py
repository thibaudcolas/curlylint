from setuptools import setup
from pathlib import Path
import versioneer


here = Path(__file__).parent

with (here / 'README.md').open('r') as f:
    long_description = '\n' + f.read()

with open('requirements.txt') as f:
    lines = f.read().split('\n')
    install_requires = [line.split()[0] for line in lines if line]

setup(
    name='jinjalint',
    author='Antoine Motet',
    author_email='antoine.motet@gmail.com',
    url='https://github.com/motet-a/jinjalint',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='A linter for Jinja-like templates',
    long_description=long_description,
    packages=['jinjalint'],
    include_package_data=True,
    license='MIT',
    install_requires=install_requires,
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
