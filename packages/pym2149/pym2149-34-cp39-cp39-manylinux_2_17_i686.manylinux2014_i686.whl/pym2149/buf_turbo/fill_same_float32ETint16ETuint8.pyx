# cython: language_level=3

cimport numpy as np
import cython

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def fill_same_float32(self, np.float32_t value):
    cdef np.ndarray[np.float32_t] py_self_buf = self.buf
    cdef np.float32_t* self_buf = &py_self_buf[0]
    cdef np.uint32_t i
    for i in range(py_self_buf.size):
        self_buf[i] = value

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def fill_same_int16(self, np.int16_t value):
    cdef np.ndarray[np.int16_t] py_self_buf = self.buf
    cdef np.int16_t* self_buf = &py_self_buf[0]
    cdef np.uint32_t i
    for i in range(py_self_buf.size):
        self_buf[i] = value

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def fill_same_uint8(self, np.uint8_t value):
    cdef np.ndarray[np.uint8_t] py_self_buf = self.buf
    cdef np.uint8_t* self_buf = &py_self_buf[0]
    cdef np.uint32_t i
    for i in range(py_self_buf.size):
        self_buf[i] = value
