from typing import Callable, Iterable

from numpy import ndarray, float32


def compressor(
        in_array: ndarray[float32],
        tracker: "Callable"[["Iterable"], "Iterable"] = None
) -> ndarray:
    pass
