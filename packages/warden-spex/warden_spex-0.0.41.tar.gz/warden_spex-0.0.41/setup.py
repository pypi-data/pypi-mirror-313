# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['warden_spex']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.10.0',
 'numpy>=2.1.3,<3.0.0',
 'pydantic>=2.10.3,<3.0.0',
 'pytest>=8.2.2,<9.0.0',
 'rbloom>=1.5.1,<2.0.0',
 'ruff>=0.0.128']

setup_kwargs = {
    'name': 'warden-spex',
    'version': '0.0.41',
    'description': 'Statistical Proof of Execution (SPEX) by Warden Protocol',
    'long_description': '# Statistical Proof of Execution (SPEX) by Warden Protocol\n\nWork in progress.\n\n# LICENSE\n\n```\nCopyright 2024 Warden Protocol <https://wardenprotocol.org/>\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n   http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n```',
    'author': 'Michele Dallachiesa',
    'author_email': 'michele@wardenprotocol.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<4.0',
}


setup(**setup_kwargs)
