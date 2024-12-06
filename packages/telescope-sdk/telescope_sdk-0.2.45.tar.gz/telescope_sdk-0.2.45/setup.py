# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telescope_sdk']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=5.0,<6.0', 'pycountry>=22.3.5,<23.0.0', 'pydantic>=2.9.2,<3.0.0']

setup_kwargs = {
    'name': 'telescope-sdk',
    'version': '0.2.45',
    'description': 'Telescope Python SDK',
    'long_description': '# Telescope Python SDK\n\nPackage containing Pydantic models representing the entities used in Telescope backend systems. The source of truth\nfor these types lives [here](https://gotelescope.atlassian.net/wiki/spaces/~62cc5da0bb346bdf82fa14f7/pages/32899073/Data+model+changes+move+to+Person).\n\nSee [Deployment](#deployment) for instructions on how to publish a new version of this package.\n\n## Usage\n\n```bash\n$ pip install telescope-sdk\n```\n\nTo construct an entity (e.g. Person) you can use the constructor\n(please note Pydantic only accepts keyword arguments):\n\n```python\nfrom telescope_sdk import Person\nperson = Person(\n    id="123",\n    first_name="John Doe",\n    ...\n    )\n```\n\nOr, to construct from a Python dictionary object:\n\n```python\nperson = Person.model_validate({\n    "id": "123",\n    "first_name": "John Doe",\n    ...\n    })\n```\n\nIf you are mapping from [PDL](https://docs.peopledatalabs.com/docs/fields) types, use the `from_pdl` method:\n\n```python\nperson = Person.from_pdl({\n    "id": "123",\n    "firstName": "John Doe",\n    ...\n    })\n```\n\n- Please note that unless a field is set as "Strict", it will automatically attempt to cast any input,\n  and only throw an error if casting fails\n\n## Development\n\nTo make changes to this package clone the repo and follow the steps below. Please ensure that any changes to the code\nbase are synced with the documentation linked above.\n\n### Installation\n\nFirst set up a virtual environment to isolate dependencies. You can do this in many ways but as an example:\n\n```bash\n$ pyenv virtualenv 3.10.0 <chosen-virtualenv-name>\n$ pyenv activate <chosen-virtualenv-name>\n```\n\nNote this codebase takes advantage of features from Python 3.10+ therefore you may run into errors if you attempt to use\nan earlier Python version.\n\nThis project relies on Poetry for dependency management. To install Poetry follow the instructions\n[here](https://python-poetry.org/docs/#installing-with-pipx) (recommend using [pipx](https://pypa.github.io/pipx/) to\ninstall Poetry globally but manage in virtualenv).\n\nNow ensure you have Make on your machine then run\n\n```bash\n$ make install\n```\n\nThis will install the package and its dependencies in [editable mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html).\n\n### Testing\n\nTo run tests locally, run the following command:\n\n```bash\n$ make test\n```\n\n### Linting\n\nTo run linting locally, run the following command:\n\n```bash\n$ make lint\n```\n\n## Deployment\n\nA new package version is published to PyPI whenever a new release is created on GitHub. To create a new release follow\nthe following steps, from the `master` branch:\n\n1. Update the version number in `pyproject.toml` to the new version number (use semantic versioning).\n2. Create a new release on GitHub with the same version number as the one in `pyproject.toml`.\n3. Draft release notes for the new version. These will be used as the package description on PyPI.\n4. The new version will be published to [PyPI](https://pypi.org/) automatically.\n\nOn pushes to the `master` branch, the `sandbox-deploy` job will run and publish a new version of the package to\n[TestPyPI](https://test.pypi.org/). This is useful for testing changes to the package before publishing to PyPI.\n',
    'author': 'Olivier Ramier',
    'author_email': 'olivier@gotelescope.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/telescope-eng/telescope-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
