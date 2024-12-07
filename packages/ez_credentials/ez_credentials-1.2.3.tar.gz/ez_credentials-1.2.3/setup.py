# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ez_credentials']

package_data = \
{'': ['*']}

install_requires = \
['keyring>=25.2.1,<26.0.0',
 'loguru>=0.7.2,<0.8.0',
 'pyjwt>=2.8.0,<3.0.0',
 'python-dotenv>=1.0.1,<2.0.0',
 'requests>=2.32.3,<3.0.0',
 'validators>=0.33.0,<0.34.0',
 'yarl>=1.9.4,<2.0.0']

setup_kwargs = {
    'name': 'ez_credentials',
    'version': '1.2.3',
    'description': 'Easy credentials management using keyring',
    'long_description': "# Easy credentials\n\nSimple set of classes to manage credentials (user/pwd, token...)\n\n## Installation\n\nClassic through pip or your favourite package manager:\n\n```shell\npip install ez-credentials\n```\n\n## Usage\n\nInstantiate a credential manager. The instance is callable and returns the credentials. You can also get the credentials as a dictionnary or as a tuple.\n\n```python\nfrom ez_credentials import CredentialManager\n\ncred = CredentialManager('test')\n\ncred()\n```\n\nYou'll be prompted for your credentials. They will be stored in your keyring. \n\n'test' is the name of the service. You can define several credential managers with different service names.\n\nOptionally, you cat set how long the credentials should be stored, i.e. how frequently the password is asked for.\nThis is defined in seconds, and default to 30 days.\n\n```python\nfrom time import sleep\nfrom ez_credentials import CredentialManager\n\ncred = CredentialManager('test', expires_in=1)\n\ncred()\nsleep(1)\ncred()\n```\n\nThere are other classes (TokenManager, TokenCredentialManager, WebServiceTokenManager and WebServiceTorkenManager; and some aliases).\n",
    'author': 'Christophe Druet',
    'author_email': 'christophe@stoachup.com',
    'maintainer': 'Christophe Druet',
    'maintainer_email': 'christophe@stoachup.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.13',
}


setup(**setup_kwargs)
