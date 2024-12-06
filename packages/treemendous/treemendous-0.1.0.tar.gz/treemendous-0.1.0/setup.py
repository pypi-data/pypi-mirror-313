# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['treemendous', 'treemendous.basic', 'treemendous.cpp']

package_data = \
{'': ['*']}

install_requires = \
['sortedcollections>=2.1.0,<3.0.0', 'sortedcontainers>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'treemendous',
    'version': '0.1.0',
    'description': 'Exploring a diverse collection of interval tree implementations across multiple programming languages to identify the most efficient configurations for varied use cases, such as optimizing for query speed, memory usage, or dynamic updates.',
    'long_description': '# Tree-Mendous\nExploring a diverse collection of interval tree implementations across multiple programming languages to identify the most efficient configurations for varied use cases, such as optimizing for query speed, memory usage, or dynamic updates.\n',
    'author': 'Joseph Cox',
    'author_email': 'joseph@codensity.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
