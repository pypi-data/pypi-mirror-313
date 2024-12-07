# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sourcesquirrel',
 'sourcesquirrel.classes',
 'sourcesquirrel.constants',
 'sourcesquirrel.integrations',
 'sourcesquirrel.integrations.google',
 'sourcesquirrel.prefabs',
 'sourcesquirrel.utils',
 'sourcesquirrel.validators']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.1.5,<4.0.0', 'pydrive2>=1.21.3,<2.0.0']

setup_kwargs = {
    'name': 'bookio-sourcesquirrel',
    'version': '0.2.0',
    'description': 'Source of truth for book.io and stuff.io data',
    'long_description': '# book.io / sourcesquirrel\n\n---\n\n![source, the squirrel](/img/source.png)\n> source, the squirrel\n\n',
    'author': 'Fede',
    'author_email': 'fede@book.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/book-io/sourcesquirrel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
