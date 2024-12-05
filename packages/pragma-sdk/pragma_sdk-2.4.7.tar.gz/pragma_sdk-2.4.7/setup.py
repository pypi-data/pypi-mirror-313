# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pragma_sdk',
 'pragma_sdk.common',
 'pragma_sdk.common.configs',
 'pragma_sdk.common.fetchers',
 'pragma_sdk.common.fetchers.fetchers',
 'pragma_sdk.common.fetchers.future_fetchers',
 'pragma_sdk.common.fetchers.generic_fetchers',
 'pragma_sdk.common.fetchers.generic_fetchers.deribit',
 'pragma_sdk.common.fetchers.generic_fetchers.lp_fetcher',
 'pragma_sdk.common.fetchers.handlers',
 'pragma_sdk.common.randomness',
 'pragma_sdk.common.types',
 'pragma_sdk.offchain',
 'pragma_sdk.onchain',
 'pragma_sdk.onchain.abis',
 'pragma_sdk.onchain.mixins',
 'pragma_sdk.onchain.types']

package_data = \
{'': ['*']}

install_requires = \
['aioresponses>=0.7.4,<0.8.0',
 'deprecated>=1.2.14,<2.0.0',
 'pydantic>=2.7.4,<3.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'pyyaml>=6.0.1,<7.0.0',
 'redis[hiredis]>=5.0.7,<6.0.0',
 'requests-mock>=1.11.0,<2.0.0',
 'starknet.py==0.23.0',
 'typer==0.6.1']

setup_kwargs = {
    'name': 'pragma-sdk',
    'version': '2.4.7',
    'description': 'Core package for rollup-native Pragma Oracle',
    'long_description': '# Pragma SDK\n\nMain repository containing our SDK code.\n\nFor more information, please check the documentation:\n\nhttps://pragma-docs.readthedocs.io/en/latest/index.html\n',
    'author': '0xevolve',
    'author_email': 'matthias@pragma.build',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pragma.build',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<3.13',
}


setup(**setup_kwargs)
