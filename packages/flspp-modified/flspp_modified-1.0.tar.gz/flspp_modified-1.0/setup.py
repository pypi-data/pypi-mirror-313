# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flspp']

package_data = \
{'': ['*'], 'flspp': ['cpp/*']}

install_requires = \
['numpy1.23.5', 'scikit-learn0.23.2']

setup_kwargs = {
    'name': 'flspp_modified',
    'version': '1.0',
    'description': 'Implementation of the FLS++ algorithm for K-Means clustering.',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}
from build_extension import *
build(setup_kwargs)

setup(**setup_kwargs)
