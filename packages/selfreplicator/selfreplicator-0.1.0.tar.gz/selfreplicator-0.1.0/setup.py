# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selfreplicator']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=2.1.3,<3.0.0',
 'pandas>=2.2.3,<3.0.0',
 'plotly>=5.24.1,<6.0.0',
 'ray>=2.39.0,<3.0.0',
 'torch>=2.5.1,<3.0.0']

entry_points = \
{'console_scripts': ['selfreplicator = selfreplicator.__main__:main']}

setup_kwargs = {
    'name': 'selfreplicator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ParsaGhadermazi',
    'author_email': '54489047+ParsaGhadermazi@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
