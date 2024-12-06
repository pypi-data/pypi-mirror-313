# Telescope Python SDK

Package containing Pydantic models representing the entities used in Telescope backend systems. The source of truth
for these types lives [here](https://gotelescope.atlassian.net/wiki/spaces/~62cc5da0bb346bdf82fa14f7/pages/32899073/Data+model+changes+move+to+Person).

See [Deployment](#deployment) for instructions on how to publish a new version of this package.

## Usage

```bash
$ pip install telescope-sdk
```

To construct an entity (e.g. Person) you can use the constructor
(please note Pydantic only accepts keyword arguments):

```python
from telescope_sdk import Person
person = Person(
    id="123",
    first_name="John Doe",
    ...
    )
```

Or, to construct from a Python dictionary object:

```python
person = Person.model_validate({
    "id": "123",
    "first_name": "John Doe",
    ...
    })
```

If you are mapping from [PDL](https://docs.peopledatalabs.com/docs/fields) types, use the `from_pdl` method:

```python
person = Person.from_pdl({
    "id": "123",
    "firstName": "John Doe",
    ...
    })
```

- Please note that unless a field is set as "Strict", it will automatically attempt to cast any input,
  and only throw an error if casting fails

## Development

To make changes to this package clone the repo and follow the steps below. Please ensure that any changes to the code
base are synced with the documentation linked above.

### Installation

First set up a virtual environment to isolate dependencies. You can do this in many ways but as an example:

```bash
$ pyenv virtualenv 3.10.0 <chosen-virtualenv-name>
$ pyenv activate <chosen-virtualenv-name>
```

Note this codebase takes advantage of features from Python 3.10+ therefore you may run into errors if you attempt to use
an earlier Python version.

This project relies on Poetry for dependency management. To install Poetry follow the instructions
[here](https://python-poetry.org/docs/#installing-with-pipx) (recommend using [pipx](https://pypa.github.io/pipx/) to
install Poetry globally but manage in virtualenv).

Now ensure you have Make on your machine then run

```bash
$ make install
```

This will install the package and its dependencies in [editable mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html).

### Testing

To run tests locally, run the following command:

```bash
$ make test
```

### Linting

To run linting locally, run the following command:

```bash
$ make lint
```

## Deployment

A new package version is published to PyPI whenever a new release is created on GitHub. To create a new release follow
the following steps, from the `master` branch:

1. Update the version number in `pyproject.toml` to the new version number (use semantic versioning).
2. Create a new release on GitHub with the same version number as the one in `pyproject.toml`.
3. Draft release notes for the new version. These will be used as the package description on PyPI.
4. The new version will be published to [PyPI](https://pypi.org/) automatically.

On pushes to the `master` branch, the `sandbox-deploy` job will run and publish a new version of the package to
[TestPyPI](https://test.pypi.org/). This is useful for testing changes to the package before publishing to PyPI.
