# -*- coding: utf-8 -*-
from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

packages = \
['whill']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'whill',
    'version': '1.4.0',
    'description': 'WHILL Model CR series SDK for Python',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'author': 'Seiya Shimizu',
    'author_email': 'seiya.shimizu@whill.inc',
    'maintainer': 'George Mandokoro',
    'maintainer_email': 'george.mandokoro@whill.inc',
    'url': 'https://whill.inc/jp/model-cr2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
