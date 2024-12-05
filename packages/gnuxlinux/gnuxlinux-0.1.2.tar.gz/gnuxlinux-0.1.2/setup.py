# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gnuxlinux', 'gnuxlinux.api', 'gnuxlinux.features']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0', 'rich>=13.9.4,<14.0.0', 'setuptools>=75.6.0,<76.0.0']

entry_points = \
{'console_scripts': ['gnuxlinux = gnuxlinux.__main__:main']}

setup_kwargs = {
    'name': 'gnuxlinux',
    'version': '0.1.2',
    'description': 'gnu utilities eXtended',
    'long_description': '# gnux\n\n<a id="readme-top"></a> \n\n<div align="center">  \n  <p align="center">\n    gnu utilities eXtended\n    <br />\n    <a href="./docs/en/index.md"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="#key-features">Key Features</a>\n    ·\n    <a href="#getting-started">Getting Started</a>\n    ·\n    <a href="#usage">Usage</a>\n    .\n    <a href="#c-specifications">C Specification</a>\n    ·\n    <a href="https://github.com/alexeev-prog/gnux/blob/main/LICENSE">License</a>\n  </p>\n</div>\n<br>\n<p align="center">\n    <img src="https://img.shields.io/github/languages/top/alexeev-prog/gnux?style=for-the-badge">\n    <img src="https://img.shields.io/github/languages/count/alexeev-prog/gnux?style=for-the-badge">\n    <img src="https://img.shields.io/github/license/alexeev-prog/gnux?style=for-the-badge">\n    <img src="https://img.shields.io/github/stars/alexeev-prog/gnux?style=for-the-badge">\n    <img src="https://img.shields.io/github/issues/alexeev-prog/gnux?style=for-the-badge">\n    <img src="https://img.shields.io/github/last-commit/alexeev-prog/gnux?style=for-the-badge">\n</p>\n\nNew, expanded, smart and modernized utilities. Written in C, wrapped in Python.\n\n## Check Other My Projects\n\n + [SQLSymphony](https://github.com/alexeev-prog/SQLSymphony) - simple and fast ORM in sqlite (and you can add other DBMS)\n + [Burn-Build](https://github.com/alexeev-prog/burn-build) - simple and fast build system written in python for C/C++ and other projects. With multiprocessing, project creation and caches!\n + [OptiArch](https://github.com/alexeev-prog/optiarch) - shell script for fast optimization of Arch Linux\n + [libnumerixpp](https://github.com/alexeev-prog/libnumerixpp) - a Powerful C++ Library for High-Performance Numerical Computing\n + [pycolor-palette](https://github.com/alexeev-prog/pycolor-palette) - display beautiful log messages, logging, debugging.\n + [shegang](https://github.com/alexeev-prog/shegang) - powerful command interpreter (shell) for linux written in C\n + [carbonpkg](https://github.com/alexeev-prog/carbonpkg) - powerful and blazing fast package manager written in go\n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n\n## Key Features\n\n + Fast and performance\n + Universal and integrated\n + Human-designed\n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n\n## Getting Started\nGNUXLINUX is available on [PyPI](https://pypi.org/project/gnuxlinux). Simply install the package into your project environment with PIP:\n\n```bash\npip install gnuxlinux\n```\n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n\n## Usage\nExecute any command:\n\n```bash\ngnuxlinux --help\n```\n\n### pkg\nGet info about GNUXLINUX package:\n\n```bash\ngnuxlinux pkg <package_name>\n```\n\n### exec\n\n```bash\ngnuxlinux execute <command>\n```\n\n### mkdir\n\n```bash\ngnuxlinux mkdir <dir_name> <--ignore-exists> <--slug-enable> <--slug-symbol "_">\n```\n\n### cat\n\n```bash\ngnuxlinux cat <filename>\n```\n\n## C Specifications\nGNUX C PyExtensions architecture:\n\n```\next\n└── src\n    ├── gnuxmkdir.c\n    └── gnuxmodule.c\n```\n\n### gnuxmodule.c\n\n + `exec_shell_command(command)` - execute a shell command.\n\n### gnuxmkdir.c\n\n + `gnux_mkdir(dir_name, ignore_exists)` - create directory.\n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n\n## License\nGNUX is a lightweight, fast and scalable web framework for Python\nCopyright (C) 2024  Alexeev Bronislav (C) 2024\n\nThis library is free software; you can redistribute it and/or\nmodify it under the terms of the GNU Lesser General Public\nLicense as published by the Free Software Foundation; either\nversion 2.1 of the License, or (at your option) any later version.\n\nThis library is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU\nLesser General Public License for more details.\n\nYou should have received a copy of the GNU Lesser General Public\nLicense along with this library; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301\nUSA\n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n',
    'author': 'alexeev-prog',
    'author_email': 'alexeev.dev@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
