# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
from libc.math cimport floor
from libc.stdlib cimport malloc, free
import numpy as np
cimport numpy as np

cdef int PREC = 10

cdef short* proc_untracked(const double[:] input_data, const int sz) nogil:
    cdef int charge = 0
    cdef int strength = 0
    cdef short previous_bit = False

    cdef short *out = <short*>malloc(sizeof(short) * sz)

    cdef size_t i = 0
    cdef size_t j = 0

    cdef int this_byte = 0
    cdef float level
    cdef short current_bit
    cdef int next_charge
    cdef int next_strength
    cdef int target
    cdef int v1, v2
    while i < sz:
        j = 0
        while j < 8:
            level = floor(input_data[i * 8 + j] * 127)

            current_bit = level > charge or (level == charge and charge == 127)
            target = (127 if current_bit else -128)

            v1 = ((strength * (target - charge) + (1 << PREC - 1)) >> PREC)

            next_charge = charge + v1
            if v1 == 0 and next_charge != target:
                next_charge += 1 if current_bit else -1

            v2 = this_byte >> 1

            this_byte = v2 + 128 if current_bit else v2

            z = ((1 << PREC) - 1 if current_bit == previous_bit else 0)
            next_strength = strength

            if strength != z:
                next_strength += 1 if current_bit == previous_bit else -1

            v3 = 2 << (PREC - 8)
            if next_strength < v3:
                next_strength = v3

            charge = next_charge
            strength = next_strength
            previous_bit = current_bit

            j+=1

        out[i] = this_byte

        i += 1

    return out

cpdef compressor(
        in_array: np.ndarray[np.float64],
        tracker: "typing.Callable"[["typing.Iterable"], "typing.Iterable"] = None
):
    cdef int charge = 0
    cdef int strength = 0
    cdef char previous_bit = False

    cdef size_t sz = len(in_array) // 8
    cdef const double [:] in_array_view = in_array

    cdef short *out_array = <short*>malloc(sizeof(short) * sz)

    cdef size_t i
    cdef size_t j
    cdef float level
    cdef short this_byte
    cdef char current_bit
    cdef int next_charge
    cdef int next_strength
    cdef int target
    cdef int v1, v2

    if tracker:
        for i in tracker(range(sz)):
            this_byte = 0

            for j in range(8):
                level = floor(in_array_view[i * 8 + j] * 127)

                current_bit = level > charge or (level == charge and charge == 127)
                target = (127 if current_bit else -128)

                v1 = ((strength * (target - charge) + (1 << PREC - 1)) >> PREC)

                next_charge = charge + v1
                if v1 == 0 and next_charge != target:
                    next_charge += 1 if current_bit else -1

                v2 = this_byte >> 1

                this_byte = v2 + 128 if current_bit else v2

                z = ((1 << PREC) - 1 if current_bit == previous_bit else 0)
                next_strength = strength

                if strength != z:
                    next_strength += 1 if current_bit == previous_bit else -1

                v3 = 2 << (PREC - 8)
                if next_strength < v3:
                    next_strength = v3

                charge = next_charge
                strength = next_strength
                previous_bit = current_bit

            out_array[i] = this_byte
    else:
        free(<void*>out_array)
        array = proc_untracked(in_array_view, sz)
        out_array = array

    cdef np.ndarray result = np.asarray(<short[:sz]>out_array).astype('int8')
    free(<void*>out_array)
    return result
