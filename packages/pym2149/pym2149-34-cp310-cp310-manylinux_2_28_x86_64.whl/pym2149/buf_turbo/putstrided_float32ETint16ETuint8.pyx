# cython: language_level=3

cimport numpy as np
import cython

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def putstrided_float32(self, np.uint32_t start, np.uint32_t end, np.uint32_t step, np.ndarray[np.float32_t] py_data):
    cdef np.ndarray[np.float32_t] py_self_buf = self.buf
    cdef np.float32_t* self_buf = &py_self_buf[0]
    cdef np.float32_t* data = &py_data[0]
    cdef np.uint32_t j
    j = 0
    while start < end:
        self_buf[start] = data[j]
        start += step
        j += 1

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def putstrided_int16(self, np.uint32_t start, np.uint32_t end, np.uint32_t step, np.ndarray[np.int16_t] py_data):
    cdef np.ndarray[np.int16_t] py_self_buf = self.buf
    cdef np.int16_t* self_buf = &py_self_buf[0]
    cdef np.int16_t* data = &py_data[0]
    cdef np.uint32_t j
    j = 0
    while start < end:
        self_buf[start] = data[j]
        start += step
        j += 1

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def putstrided_uint8(self, np.uint32_t start, np.uint32_t end, np.uint32_t step, np.ndarray[np.uint8_t] py_data):
    cdef np.ndarray[np.uint8_t] py_self_buf = self.buf
    cdef np.uint8_t* self_buf = &py_self_buf[0]
    cdef np.uint8_t* data = &py_data[0]
    cdef np.uint32_t j
    j = 0
    while start < end:
        self_buf[start] = data[j]
        start += step
        j += 1
