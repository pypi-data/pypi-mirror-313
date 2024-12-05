# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bitcoin_lite']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=3.0.11,<4.0.0']

setup_kwargs = {
    'name': 'bitcoin-lite',
    'version': '0.1.0',
    'description': 'A lightweight Bitcoin transaction system using Cython',
    'long_description': None,
    'author': 'danymukesha',
    'author_email': 'danymukesha@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
