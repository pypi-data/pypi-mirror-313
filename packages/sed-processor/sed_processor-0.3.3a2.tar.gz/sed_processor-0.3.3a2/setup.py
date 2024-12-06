# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sed',
 'sed.binning',
 'sed.calibrator',
 'sed.core',
 'sed.dataset',
 'sed.io',
 'sed.loader',
 'sed.loader.base',
 'sed.loader.flash',
 'sed.loader.generic',
 'sed.loader.mpes',
 'sed.loader.sxp']

package_data = \
{'': ['*'], 'sed': ['config/*']}

install_requires = \
['bokeh>=2.4.2',
 'dask>=2021.12.0,<2023.12.1',
 'docutils<0.21',
 'fastdtw>=0.3.4',
 'h5py>=3.6.0',
 'ipympl>=0.9.1',
 'ipywidgets>=7.7.1,<8.0.0',
 'joblib>=1.2.0',
 'lmfit>=1.0.3',
 'matplotlib>=3.5.1,<3.9.0',
 'natsort>=8.1.0',
 'numba>=0.55.1',
 'numpy>=1.18,<2.0',
 'pandas>=1.4.1',
 'psutil>=5.9.0',
 'pyarrow>=14.0.1,<17.0',
 'pynxtools-mpes>=0.2.0',
 'pynxtools>=0.8.0',
 'pyyaml>=6.0.0',
 'scipy>=1.8.0',
 'symmetrize>=0.5.5',
 'threadpoolctl>=3.1.0',
 'tifffile>=2022.2.9',
 'tqdm>=4.62.3',
 'xarray>=0.20.2']

extras_require = \
{':extra == "notebook"': ['jupyterlab-h5web[full]>=8.0.0,<9.0.0'],
 'all': ['notebook>=6.5.7,<7.0.0'],
 'notebook': ['jupyter>=1.0.0',
              'ipykernel>=6.9.1',
              'jupyterlab>=3.4.0,<4.0.0',
              'notebook>=6.5.7,<7.0.0']}

setup_kwargs = {
    'name': 'sed-processor',
    'version': '0.3.3a2',
    'description': 'Single Event Data Frame Processor: Backend to handle photoelectron resolved datastreams',
    'long_description': '[![Documentation Status](https://github.com/OpenCOMPES/sed/actions/workflows/documentation.yml/badge.svg)]([https://opencompes.github.io/sed/](https://opencompes.github.io/docs/sed/latest/))\n[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)\n![](https://github.com/OpenCOMPES/sed/actions/workflows/linting.yml/badge.svg?branch=main)\n![](https://github.com/OpenCOMPES/sed/actions/workflows/testing_multiversion.yml/badge.svg?branch=main)\n![](https://img.shields.io/pypi/pyversions/sed-processor)\n![](https://img.shields.io/pypi/l/sed-processor)\n[![](https://img.shields.io/pypi/v/sed-processor)](https://pypi.org/project/sed-processor)\n[![Coverage Status](https://coveralls.io/repos/github/OpenCOMPES/sed/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/OpenCOMPES/sed?branch=main)\n\n**sed-processor** is a backend to process and bin multidimensional single-event datastreams, with the intended primary use case in multidimensional photoelectron spectroscopy using time-of-flight instruments.\n\nIt builds on [Dask](https://www.dask.org/) dataframes, where each column represents a multidimensional "coordinate" such as position, time-of-flight, pump-probe delay etc., and each entry represents one electron. The `SedProcessor` class provides a single user entry point, and provides functions for handling various workflows for coordinate transformation, e.g. corrections and calibrations.\n\nFurthermore, "sed-processor" provides fast and parallelized binning routines to compute multidimensional histograms from the processed dataframes in a delayed fashion, thus reducing requirements on cpu power and memory consumption.\n\nFinally, in contains several export routines, including export into the [NeXus](https://www.nexusformat.org/) format with rich and standardized metadata annotation.\n\n# Installation\n\n## Prerequisites\n- Python 3.8+\n- pip\n\n## Steps\n- Create a new virtual environment using either venv, pyenv, conda, etc. See below for an example.\n\n```bash\npython -m venv .sed-venv\n```\n\n- Activate your environment:\n\n```bash\n# On macOS/Linux\nsource .sed-venv/bin/activate\n\n# On Windows\n.sed-venv\\Scripts\\activate\n```\n\n- Install `sed`, distributed as `sed-processor` on PyPI:\n\n```bash\npip install sed-processor[all]\n```\n\n- If you intend to work with Jupyter notebooks, it is helpful to install a Jupyter kernel for your environment. This can be done, once your environment is activated, by typing:\n\n```bash\npython -m ipykernel install --user --name=sed_kernel\n```\n\n- If you do not use Jupyter Notebook or Jupyter Lab, you can skip the installing those dependencies\n\n```bash\npip install sed-processor\n```\n\n# Documentation\nComprehensive documentation including several workflow examples can be found here:\nhttps://opencompes.github.io/docs/sed/latest/\n\n\n# Contributing\nUsers are welcome to contribute to the development of **sed-processor**. Information how to contribute, including how to install developer versions can be found in the [documentation](https://opencompes.github.io/docs/sed/latest/misc/contribution.html)\n\nWe would like to thank our contributors!\n\n[![Contributors](https://contrib.rocks/image?repo=OpenCOMPES/sed)](https://github.com/OpenCOMPES/sed/graphs/contributors)\n\n\n## License\n\nsed-processor is licenced under the MIT license\n\nCopyright (c) 2022-2024 OpenCOMPES\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'OpenCOMPES team',
    'author_email': 'sed-processor@mpes.science',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/OpenCOMPES/sed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11.9',
}


setup(**setup_kwargs)
