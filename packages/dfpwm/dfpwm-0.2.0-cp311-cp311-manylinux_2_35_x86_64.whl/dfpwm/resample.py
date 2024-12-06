from typing import BinaryIO, TypeVar

import numpy as np

from .constants import SAMPLE_RATE

T = TypeVar("T", bound=np.dtype)


def resample_from_file(
        io: "BinaryIO",
        to_sample_rate=SAMPLE_RATE,
        dtype: T = np.float32
) -> tuple["np.ndarray", float]:

    import warnings
    try:
        import librosa
    except ImportError as e:
        raise ImportError("resample feature is not available") from e
    warnings.warn("resample_from_file is deprecated, use `dfpwm.resample` instead")
    return librosa.load(io, dtype=dtype, sr=to_sample_rate)


def resample(
        data: np.ndarray,
        source_sample_rate: int,
        to_sample_rate=SAMPLE_RATE,
        dtype: T = np.float32
) -> np.ndarray[T]:

    try:
        import librosa
    except ImportError as e:
        raise ImportError("resample feature is not available") from e
    return librosa.resample(data, orig_sr=source_sample_rate, target_sr=to_sample_rate).astype(dtype)
