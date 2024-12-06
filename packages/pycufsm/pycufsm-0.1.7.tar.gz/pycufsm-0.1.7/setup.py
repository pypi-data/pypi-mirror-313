# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycufsm', 'pycufsm.Jupyter_Notebooks', 'pycufsm.examples']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5', 'scipy>=1.10.0']

extras_require = \
{'jupyter': ['ipywidgets>=8.0.0', 'matplotlib>=3.2'],
 'plot': ['matplotlib>=3.2']}

setup_kwargs = {
    'name': 'pycufsm',
    'version': '0.1.7',
    'description': 'Python CUFSM (Constrained and Unconstrained Finite Strip Method)',
    'long_description': "# pyCUFSM\n[![Python tests](https://github.com/ClearCalcs/pyCUFSM/actions/workflows/test.yaml/badge.svg)](https://github.com/ClearCalcs/pyCUFSM/actions/workflows/test.yaml)\n[![Documentation Status](https://readthedocs.org/projects/pycufsm/badge/?version=latest)](http://anastruct.readthedocs.io/en/latest/?badge=latest)\n![PyPI - Version](https://img.shields.io/pypi/v/pycufsm)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/pycufsm)\n![Latest Release](https://img.shields.io/github/release-date/ClearCalcs/pyCUFSM)\n![Commits since latest release](https://img.shields.io/github/commits-since/ClearCalcs/pyCUFSM/latest)\n\n## Description\n\nThis package is primarily a port of CUFSM v5.01, written by Benjamin Schafer PhD et al at Johns Hopkins University, from its original MATLAB language to Python v3, using the Numpy and Scipy packages for matrix manipulation and other advanced mathematics functionality. The goal of this project is to create a derivative of CUFSM which can be used either in Jupyter Notebooks or in headless (library) applications. This project is not affiliated with Benjamin Schafer PhD or Johns Hopkins University in any way.\n\nThe original MATLAB CUFSM program may be accessed at the following address: https://www.ce.jhu.edu/cufsm/\n\n### Installation\n\nThis package is still under heavy development, but it may be installed in several different possible forms, as described below:\n1. Minimal (headless) installation: `pip install pycufsm`\n2. Installation with plotting capabilities: `pip install pycufsm[plot]`\n3. Installation with Jupyter Notebooks: `pip install pycufsm[jupyter]`\n4. Installation with full development dependencies: `pip install pycufsm[dev]`\n\n### Contributing\n\nIf you would like to contribute to the pyCUFSM project, then please do - all productive contributions are welcome! However, please make sure that you're working off of the most recent development version of the pyCUFSM code, by cloning the [GitHub repository](https://github.com/ClearCalcs/pyCUFSM), and please review our wiki article on [Contributing to the Code](https://github.com/ClearCalcs/pyCUFSM/wiki/Contributing-to-the-Code).\n\n## Current Status\n\n#### Complete and Generally Tested\n\n-   [x] Unconstrained FSM (signature curve generation)\n-   [x] Constrained FSM\n-   [x] Added template_path() function to define a complete arbitrary cross-section by simple paths\n-   [x] Add automated validation testing of FSM calculations via pytest\n-   [x] Various efficiency and readability improvements:\n    -   [x] Cythonise a few computation-heavy functions in analysis.py, including klocal(), kglocal(), and assemble()\n    -   [x] Moved computation-heavy cFSM functions to analysis.py and cythonised them\n    -   [x] Review code for places where matrices can be preallocated rather than concatenated together\n\n#### Complete But Untested\n\n-   [x] Equation constraints\n-   [x] Spring constraints\n-   [x] General boundary conditions\n\n#### Planned Further Work\n\n-   [ ] Handle holes in cross-sections in some meaningful way\n-   [ ] Various efficiency and readability improvements:\n    -   [ ] Make use of scipy.sparse for sparse matrices where possible\n    -   [ ] Convert some numerical inputs and data to dictionaries with strings\n    -   [ ] Eliminate matrix columns which are nothing more than the index number of the row\n    -   [ ] Review code for function calls that are unnecessarily repeated (a couple of these have already been addressed, e.g. `base_properties()` did not need to be re-run for every half wavelength)\n-   [ ] Write API-style documentation (for now, generally refer to MATLAB CUFSM documentation and/or comments)\n\n## Disclaimer\n\nWhile the original MATLAB CUFSM has been extensively tested, and best efforts have been made to check accuracy of this package against the original MATLAB CUFSM program, including via automated validation testing, no warrant is made as to the accuracy of this package. The developers accept no liability for any errors or inaccuracies in this package, including, but not limited to, any problems which may stem from such errors or inaccuracies in this package such as under-conservative engineering designs or structural failures.\n\nAlways check your designs and never blindly trust any engineering program, including this one.\n",
    'author': 'Brooks Smith',
    'author_email': 'smith120bh@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ClearCalcs/pyCUFSM',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10',
}
from build_cython_ext import *
build(setup_kwargs)

setup(**setup_kwargs)
