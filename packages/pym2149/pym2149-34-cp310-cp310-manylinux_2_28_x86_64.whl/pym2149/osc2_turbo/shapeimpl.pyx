# cython: language_level=3

cimport numpy as np
import cython

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def shapeimpl(self):
    cdef np.uint32_t self_block_framecount = self.block.framecount
    cdef np.ndarray[np.uint8_t] py_self_blockbuf_buf = self.blockbuf.buf
    cdef np.uint8_t* self_blockbuf_buf = &py_self_blockbuf_buf[0]
    cdef np.uint8_t self_eager = self.eager
    cdef np.int32_t self_index = self.index
    cdef np.uint32_t self_periodreg_value = self.periodreg.value
    cdef np.uint32_t self_progress = self.progress
    cdef np.uint32_t self_scale = self.scale
    cdef np.ndarray[np.uint8_t] py_self_shape_buf = self.shape.buf
    cdef np.uint8_t* self_shape_buf = &py_self_shape_buf[0]
    cdef np.uint32_t self_shape_introlen = self.shape.introlen
    cdef np.uint32_t self_shape_size = self.shape.size
    cdef np.uint32_t self_stepsize = self.stepsize
    cdef np.uint32_t i
    cdef np.uint8_t val
    cdef np.uint32_t j
    cdef np.uint32_t n
    if self_eager:
        self_stepsize = self_periodreg_value * self_scale
    i = 0
    if self_progress < self_stepsize:
        val = self_shape_buf[self_index]
        j = min(self_stepsize - self_progress, self_block_framecount)
        while i < j:
            self_blockbuf_buf[i] = val
            i += 1
    if i == self_block_framecount:
        self_progress += self_block_framecount
    else:
        if not self_eager:
            self_stepsize = self_periodreg_value * self_scale
        n = (self_block_framecount - i) // self_stepsize
        while n:
            self_index += 1
            if self_index == self_shape_size:
                self_index = self_shape_introlen
            val = self_shape_buf[self_index]
            j = i + self_stepsize
            while i < j:
                self_blockbuf_buf[i] = val
                i += 1
            n -= 1
        if i == self_block_framecount:
            self_progress = self_stepsize
        else:
            self_index += 1
            if self_index == self_shape_size:
                self_index = self_shape_introlen
            val = self_shape_buf[self_index]
            self_progress = self_block_framecount - i
            while i < self_block_framecount:
                self_blockbuf_buf[i] = val
                i += 1
    return self_index, self_progress, self_stepsize
