# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfpwm']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=2.0.0,<3.0.0']

extras_require = \
{'resample': ['librosa>=0.10.0,<0.11.0']}

setup_kwargs = {
    'name': 'dfpwm',
    'version': '0.2.0',
    'description': 'DFPWM convertor for Python',
    'long_description': '# DFPWM\n\nDFPWM convertor for Python\n\n## Installation\n\n### From PyPI\nYou can get this package from PyPI\nif you are in py311 Linux x86\n\n```shell\npip install dfpwm\n```\n\n### Build from source\n\n## Usage\n\n```python\nfrom pathlib import Path\nimport soundfile as sf  # for reading audio\nimport dfpwm\n\ndata, sample_rate = sf.read(\'./someaudio.mp3\')  # read audio\n\n# If sample rate is not 48000, may get strange result\n# use `dfpwm.resample(...)` to resample\nif sample_rate != dfpwm.SAMPLE_RATE:\n    raise ValueError(f"{sample_rate} != {dfpwm.SAMPLE_RATE}")\n\nif len(data.shape) != 0 and data.shape[1] > 1:\n    data = data[:, 0]  # get channel 0\n\ndfpwm = dfpwm.compressor(data)  # convert\nPath(\'out.dfpwm\').write_bytes(dfpwm)  # write result to file\n```\n\n## Build from source\n\n### Clone\n\n```shell\ngit clone https://github.com/CyanChanges/python-dfpwm.git python-dfpwm\ncd python-dfpwm\n```\n\n### Build\nThis project use `poetry` to build,\nMake sure `poetry` is installed.\n\n```shell\npoetry build\n```\n\n',
    'author': 'cyan',
    'author_email': 'contact@cyans.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
