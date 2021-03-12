# Contribution Guidelines

[![Netlify Status](https://api.netlify.com/api/v1/badges/6830546d-b21d-4067-9ca2-7288b4aedbaa/deploy-status)](https://app.netlify.com/sites/curlylint/deploys)

Thank you for considering to help this project.

We welcome all support, whether on bug reports, code, design, reviews, tests, documentation, and more.

Please note that this project is released with a [Contributor Code of Conduct](docs/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Development

### Installation

> Requirements: `virtualenv`, `pyenv`

```bash
git clone git@github.com:thibaudcolas/curlylint.git
cd curlylint/
# Install required Python versions
pyenv install --skip-existing 3.6.8
# Make required Python versions available globally.
pyenv global system 3.6.8
# Install the Python environment.
virtualenv .venv -p python3.6
source ./.venv/bin/activate
make init
```

### Commands

```bash
make help           # See what commands are available.
make init           # Install dependencies and initialise for development.
make lint           # Lint the project.
make format         # Format project files.
make test           # Test the project.
make benchmark       # Runs a one-off performance (speed, memory) benchmark.
make clean-pyc      # Remove Python file artifacts.
make sdist          # Builds package version
make publish        # Publishes a new version to pypi.
make publish-test   # Publishes a new version to test pypi.
```

## Hacking

Curlylint is powered by [Parsy](https://github.com/python-parsy/parsy). Parsy is an extremely powerful library and curlylint’s parser relies heavily on it. You have to read
Parsy’s documentation in order to understand what’s going on in
`parse.py`.

## Releases

- Make a new branch for the release of the new version.
- Update the [CHANGELOG](https://github.com/thibaudcolas/curlylint/CHANGELOG.md).
- Update the version number in `curlylint/__init__.py`, following semver.
- Make a PR and squash merge it.
- Back on the `main` branch with the PR merged, use `make publish-test` (confirm, and enter your password, confirm everything good on test.pypi.org).
- Back on the `main` branch with the PR merged, use `make publish` (confirm, and enter your password).
- Finally, go to GitHub and create a release and a tag for the new version.
- Done!
