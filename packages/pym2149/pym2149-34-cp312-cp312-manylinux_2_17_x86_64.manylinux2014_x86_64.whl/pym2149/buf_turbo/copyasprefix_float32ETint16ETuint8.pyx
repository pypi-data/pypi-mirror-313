# cython: language_level=3

cimport numpy as np
import cython

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def copyasprefix_float32(self, np.uint32_t endframe, that):
    cdef np.ndarray[np.float32_t] py_self_buf = self.buf
    cdef np.float32_t* self_buf = &py_self_buf[0]
    cdef np.ndarray[np.float32_t] py_that_buf = that.buf
    cdef np.float32_t* that_buf = &py_that_buf[0]
    cdef np.uint32_t i
    for i in range(endframe):
        self_buf[i] = that_buf[i]

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def copyasprefix_int16(self, np.uint32_t endframe, that):
    cdef np.ndarray[np.int16_t] py_self_buf = self.buf
    cdef np.int16_t* self_buf = &py_self_buf[0]
    cdef np.ndarray[np.int16_t] py_that_buf = that.buf
    cdef np.int16_t* that_buf = &py_that_buf[0]
    cdef np.uint32_t i
    for i in range(endframe):
        self_buf[i] = that_buf[i]

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def copyasprefix_uint8(self, np.uint32_t endframe, that):
    cdef np.ndarray[np.uint8_t] py_self_buf = self.buf
    cdef np.uint8_t* self_buf = &py_self_buf[0]
    cdef np.ndarray[np.uint8_t] py_that_buf = that.buf
    cdef np.uint8_t* that_buf = &py_that_buf[0]
    cdef np.uint32_t i
    for i in range(endframe):
        self_buf[i] = that_buf[i]
