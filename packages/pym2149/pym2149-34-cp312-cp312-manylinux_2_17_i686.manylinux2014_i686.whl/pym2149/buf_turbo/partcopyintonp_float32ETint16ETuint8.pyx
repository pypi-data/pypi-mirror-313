# cython: language_level=3

cimport numpy as np
import cython

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def partcopyintonp_float32(self, np.uint32_t startframe, np.uint32_t endframe, np.ndarray[np.float32_t] py_thatnp):
    cdef np.ndarray[np.float32_t] py_self_buf = self.buf
    cdef np.float32_t* self_buf = &py_self_buf[0]
    cdef np.float32_t* thatnp = &py_thatnp[0]
    cdef np.uint32_t j
    for j in range(endframe - startframe):
        thatnp[j] = self_buf[startframe]
        startframe += 1

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def partcopyintonp_int16(self, np.uint32_t startframe, np.uint32_t endframe, np.ndarray[np.int16_t] py_thatnp):
    cdef np.ndarray[np.int16_t] py_self_buf = self.buf
    cdef np.int16_t* self_buf = &py_self_buf[0]
    cdef np.int16_t* thatnp = &py_thatnp[0]
    cdef np.uint32_t j
    for j in range(endframe - startframe):
        thatnp[j] = self_buf[startframe]
        startframe += 1

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def partcopyintonp_uint8(self, np.uint32_t startframe, np.uint32_t endframe, np.ndarray[np.uint8_t] py_thatnp):
    cdef np.ndarray[np.uint8_t] py_self_buf = self.buf
    cdef np.uint8_t* self_buf = &py_self_buf[0]
    cdef np.uint8_t* thatnp = &py_thatnp[0]
    cdef np.uint32_t j
    for j in range(endframe - startframe):
        thatnp[j] = self_buf[startframe]
        startframe += 1
