# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taskshooter']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2023.1,<2024.0']

setup_kwargs = {
    'name': 'taskshooter',
    'version': '0.2.0',
    'description': 'Library to schedule tasks with custom triggers.',
    'long_description': '# taskshooter\n',
    'author': 'Fede Calendino',
    'author_email': 'fede@calendino.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fedecalendino/taskshooter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
