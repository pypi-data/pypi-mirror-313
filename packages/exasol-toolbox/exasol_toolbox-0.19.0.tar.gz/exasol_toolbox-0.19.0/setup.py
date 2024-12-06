# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exasol',
 'exasol.toolbox',
 'exasol.toolbox.nox',
 'exasol.toolbox.pre_commit_hooks',
 'exasol.toolbox.release',
 'exasol.toolbox.sphinx',
 'exasol.toolbox.sphinx.multiversion',
 'exasol.toolbox.templates',
 'exasol.toolbox.tools']

package_data = \
{'': ['*'],
 'exasol.toolbox.sphinx.multiversion': ['templates/*'],
 'exasol.toolbox.templates': ['github/*',
                              'github/ISSUE_TEMPLATE/*',
                              'github/PULL_REQUEST_TEMPLATE/*',
                              'github/actions/python-environment/*',
                              'github/workflows/*']}

install_requires = \
['bandit[toml]>=1.7.9,<2.0.0',
 'black>=24.1.0',
 'coverage>=6.4.4,<8.0.0',
 'furo>=2022.9.15',
 'import-linter>=2.0,<3.0',
 'importlib-resources>=5.12.0',
 'isort>=5.12.0,<6.0.0',
 'jinja2>=3.1.4,<4.0.0',
 'mypy>=0.971',
 'myst-parser>=2.0.0,<4',
 'nox>=2022.8.7',
 'pluggy>=1.5.0,<2.0.0',
 'pre-commit>=4',
 'prysk[pytest-plugin]>0.17.0,<1',
 'pylint>=2.15.4',
 'pytest>=7.2.2,<9',
 'pyupgrade>=2.38.2,<4.0.0',
 'shibuya>=2024.5.14',
 'sphinx-copybutton>=0.5.0,<0.6.0',
 'sphinx-design>=0.5.0,<1',
 'sphinx-inline-tabs>=2023.4.21,<2024.0.0',
 'sphinx>=5.3,<8',
 'typer[all]>=0.7.0']

entry_points = \
{'console_scripts': ['sphinx-multiversion = '
                     'exasol.toolbox.sphinx.multiversion:main',
                     'tbx = exasol.toolbox.tools.tbx:CLI',
                     'version-check = '
                     'exasol.toolbox.pre_commit_hooks.package_version:main']}

setup_kwargs = {
    'name': 'exasol-toolbox',
    'version': '0.19.0',
    'description': 'Your one-stop solution for managing all standard tasks and core workflows of your Python project.',
    'long_description': '<h1 align="center">Exasol Toolbox</h1>\n\n<p align="center">\nYour one-stop solution for managing all standard tasks and core workflows of your Python project.\n</p>\n\n<p align="center">\n\n<a href="https://github.com/exasol/python-toolbox/actions/workflows/ci.yml">\n    <img src="https://github.com/exasol/python-toolbox/actions/workflows/ci.yml/badge.svg?branch=main" alt="Checks Main">\n</a>\n<a href="https://opensource.org/licenses/MIT">\n    <img src="https://img.shields.io/pypi/l/exasol-toolbox" alt="License">\n</a>\n<a href="https://pypi.org/project/exasol-toolbox/">\n    <img src="https://img.shields.io/pypi/dm/exasol-toolbox" alt="Downloads">\n</a>\n<a href="https://pypi.org/project/exasol-toolbox/">\n    <img src="https://img.shields.io/pypi/pyversions/exasol-toolbox" alt="Supported Python Versions">\n</a>\n<a href="https://pypi.org/project/exasol-toolbox/">\n    <img src="https://img.shields.io/pypi/v/exasol-toolbox" alt="PyPi Package">\n</a>\n</p>\n\n## 🚀 Features\n\n- Centrally managed standard tasks\n  - code formatting & upgrading\n  - linting\n  - type-checking\n  - unit-tests\n  - integration-tests\n  - coverage\n  - documentation\n\n- Centrally manged core workflows\n  - workspace/project verification\n  - build and publish releases\n  - build and publish documentation\n\n- Configurable & Extensible\n  - Project configuration\n  - Event hooks\n\n## 🔌️ Prerequisites\n\n- [Python](https://www.python.org/) >= 3.8\n\n## 💾 Installation\n\n```shell\npip install exasol-toolbox\n```\n\n## 📚 Documentation\n\nFor futher details, checkout the latest [documentation](https://exasol.github.io/python-toolbox/).\n\n',
    'author': 'Nicola Coretti',
    'author_email': 'nicola.coretti@exasol.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
