# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['debiased_spatial_whittle']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.0,<4.0.0',
 'numpy>=1.21.5,<2.0.0',
 'param>=2.1.1,<3.0.0',
 'pre-commit>=4.0.1,<5.0.0',
 'progressbar2>=4.2.0,<5.0.0',
 'ruff>=0.8.2,<0.9.0',
 'scipy>=1.7.3,<2.0.0']

extras_require = \
{':extra == "others"': ['autograd>=1.5,<2.0',
                        'seaborn>=0.12.2,<0.13.0',
                        'numdifftools>=0.9.41,<0.10.0'],
 'gpu': ['cupy-cuda12x>=13.0.0,<14.0.0', 'torch>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'debiased-spatial-whittle',
    'version': '0.3.5',
    'description': 'Spatial Debiased Whittle likelihood for fast inference of spatio-temporal covariance models from gridded data',
    'long_description': '# Spatial Debiased Whittle Likelihood\n\n![Image](logo.png)\n\n[![Documentation Status](https://readthedocs.org/projects/debiased-spatial-whittle/badge/?version=latest)](https://debiased-spatial-whittle.readthedocs.io/en/latest/?badge=latest)\n[![.github/workflows/run_tests_on_push.yaml](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/run_tests_on_push.yaml/badge.svg)](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/run_tests_on_push.yaml)\n[![Pypi](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/pypi.yml/badge.svg)](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/pypi.yml)\n\n## Introduction\n\nThis package implements the Spatial Debiased Whittle Likelihood (SDW) as presented in the article of the same name, by the following authors:\n\n- Arthur P. Guillaumin\n- Adam M. Sykulski\n- Sofia C. Olhede\n- Frederik J. Simons\n\nThe SDW extends ideas from the Whittle likelihood and Debiased Whittle Likelihood to random fields and spatio-temporal data. In particular, it directly addresses the bias issue of the Whittle likelihood for observation domains with dimension greater than 2. It also allows us to work with rectangular domains (i.e., rather than square), missing observations, and complex shapes of data.\n\n## Installation instructions\n\nThe package can be installed via one of the following methods.\n\n1. Via the use of Poetry ([https://python-poetry.org/](https://python-poetry.org/)), by running the following command:\n\n   ```bash\n   poetry add debiased-spatial-whittle\n   ```\n\n2. Otherwise, you can directly install via pip:\n\n    ```bash\n    pip install debiased-spatial-whittle\n    ```\n\n## Development\n\nFirstly, you need to install poetry. Then, git clone this repository, ad run the following command from\nthe directory corresponding to the package.\n\n   ```bash\n   poetry install\n   ```\n\nIf you run into some issue regarding the Python version, you can run\n   ```bash\n   poetry env use <path_to_python>\n   ```\nwhere <path_to_python> is the path to a Python version compatible with the requirements in pyproject.toml.\n\n### Unit tests\nUnit tests are run with pytest. On Pull-requests, the unit tests will be\nrun.\n\n## Documentation\nThe documentation is hosted on readthedocs. It is based on docstrings.\nCurrently, it points to the joss_paper branch and is updated on any push to that branch.\n\n## Versioning\nCurrently, versioning is handled manuallyusing poetry, e.g.\n\n   ```bash\n   poetry version patch\n   ```\nor\n   ```bash\n   poetry version minor\n   ```\n\nWhen creating a release in Github, the version tag should be set to match\nthe version in th pyproject.toml. Creating a release in Github will trigger\na Github workflow that will publish to Pypi (see Pypi section).\n\n## PyPi\nThe package is updated on PyPi automatically on creation of a new\nrelease in Github. Note that currently the version in pyproject.toml\nneeds to be manually updated. This should be fixed by adding\na step in the workflow used for publication to Pypi.\n',
    'author': 'arthur',
    'author_email': 'ahw795@qmul.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://arthurpgb.pythonanywhere.com/sdw',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
