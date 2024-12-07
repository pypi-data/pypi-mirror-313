## Developer Certificate of Origin + License

By contributing to GitLab B.V., You accept and agree to the following terms and
conditions for Your present and future Contributions submitted to GitLab B.V.
Except for the license granted herein to GitLab B.V. and recipients of software
distributed by GitLab B.V., You reserve all right, title, and interest in and to
Your Contributions. All Contributions are subject to the following DCO + License
terms.

[DCO + License](https://gitlab.com/gitlab-org/dco/blob/master/README.md)

_This notice should stay as the first item in the CONTRIBUTING.md file._

## Contributing

Thanks for considering to contribute to the GitLab CIS Scanner project (gitlabcis). Contributions of all forms are always welcome!

## Git Commit Guidelines

This project uses commit messages to automatically determine the type of change.
Messages should adhere to the conventions of [Conventional Commits (v1.0.0-beta.2)](https://www.conventionalcommits.org/en/v1.0.0-beta.2/).

### Commit msg Syntax

```sh
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

#### Examples

```sh
feat(auth): add login functionality  # Correct type, lowercase subject, within 72 characters

fix(api): correct data parsing bug   # Correct type, lowercase subject, within 72 characters

docs(readme): update installation guide  # Correct type, lowercase subject, within 72 characters
```

## Reporting feature requests / bugs

Please [raise an issue](https://gitlab.com/gitlab-org/govern/compliance/engineering/cis/gitlabcis/-/issues) for feature requests or bugs

## Setup Dev Environment

Check out [the docs](https://gitlab.com/gitlab-org/govern/compliance/engineering/cis/gitlabcis/-/blob/main/docs/readme.md?ref_type=heads#for-developers-install) on how to install the dependencies.

```sh
# obtain a copy of the repo
git clone git@gitlab.com:gitlab-org/govern/compliance/engineering/cis/gitlabcis.git
cd gitlabcis

# install the dependencies
make install

# OR without `make`:
python3 -m pip install -q .
python3 -m pip install -q .\[test,build\]

# start working out of a feature branch
git checkout -b feat/idea
```

### Pre-commit hooks

We use pre-commit hooks to ensure that what's committed to the repository has already passed validation checks locally.

Review the `.pre-commit-config.yaml` to see what checks run.

### Run CLI live tests against the source code

When you make a change to the codebase in _your_ branch, run `make install` again, to recieve a _fresh_ copy of `gitlabcis` to run live tests against.

```sh
# gitlabcis should now be added to the PATH:
gitlabcis https://gitlab.example.com/path/to/project

# for CLI arg help see:
gitlabcis --help
```

## Running unit tests

To run all of the pytest tests:

```sh
# inside the gitlabcis dir run:
pytest -s -vv tests/

# or without debug in stdout:
pytest tests
```
