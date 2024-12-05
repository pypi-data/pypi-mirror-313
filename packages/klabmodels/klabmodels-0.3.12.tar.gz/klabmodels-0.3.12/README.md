# klabmodels

Kodelab data models for AI product suite

### Build Instructions

#### Install Required tools

`pip install setuptools wheel`

#### Build the Package

```
pip install build
python -m build
```

#### Create a GitHub Personal Access Token

1. Go to GitHub > Settings > Developer settings > Personal access tokens.
2. Generate a new token with write:packages and read:packages scopes.

#### Upload package

```
pip install twine
twine upload --skip-existing --repository-url https://upload.pypi.org/legacy/ dist/*
```

### Usage

#### Configure pip to Use GitHub Packages

Create or edit ~/.pip/pip.conf to include your GitHub Packages URL:

```
[global]
extra-index-url = https://<GITHUB_USERNAME>:<GITHUB_TOKEN>@pypi.github.com/<GITHUB_USERNAME>

```

https://github.com/kodelabio/klabmodels.git

git@github.com:kodelabio/klabmodels.git

### Import the package

` pip install klabmodels`
