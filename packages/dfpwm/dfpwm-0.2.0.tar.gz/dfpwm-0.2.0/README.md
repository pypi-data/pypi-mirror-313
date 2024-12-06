# DFPWM

DFPWM convertor for Python

## Installation

### From PyPI
You can get this package from PyPI
if you are in py311 Linux x86

```shell
pip install dfpwm
```

### Build from source

## Usage

```python
from pathlib import Path
import soundfile as sf  # for reading audio
import dfpwm

data, sample_rate = sf.read('./someaudio.mp3')  # read audio

# If sample rate is not 48000, may get strange result
# use `dfpwm.resample(...)` to resample
if sample_rate != dfpwm.SAMPLE_RATE:
    raise ValueError(f"{sample_rate} != {dfpwm.SAMPLE_RATE}")

if len(data.shape) != 0 and data.shape[1] > 1:
    data = data[:, 0]  # get channel 0

dfpwm = dfpwm.compressor(data)  # convert
Path('out.dfpwm').write_bytes(dfpwm)  # write result to file
```

## Build from source

### Clone

```shell
git clone https://github.com/CyanChanges/python-dfpwm.git python-dfpwm
cd python-dfpwm
```

### Build
This project use `poetry` to build,
Make sure `poetry` is installed.

```shell
poetry build
```

