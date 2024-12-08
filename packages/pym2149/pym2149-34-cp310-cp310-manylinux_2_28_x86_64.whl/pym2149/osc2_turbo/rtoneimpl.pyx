# cython: language_level=3

cimport numpy as np
import cython

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def rtoneimpl(self, np.uint32_t prescaler, np.uint32_t etdr):
    cdef np.uint32_t self_block_framecount = self.block.framecount
    cdef np.ndarray[np.uint8_t] py_self_blockbuf_buf = self.blockbuf.buf
    cdef np.uint8_t* self_blockbuf_buf = &py_self_blockbuf_buf[0]
    cdef np.uint64_t self_chipimplclock = self.chipimplclock
    cdef np.int32_t self_index = self.index
    cdef np.int32_t self_maincounter = self.maincounter
    cdef np.int64_t self_mfpclock = self.mfpclock
    cdef np.uint32_t self_precounterxmfp = self.precounterxmfp
    cdef np.uint32_t self_repeat = self.repeat
    cdef np.ndarray[np.uint8_t] py_self_shape_buf = self.shape.buf
    cdef np.uint8_t* self_shape_buf = &py_self_shape_buf[0]
    cdef np.uint32_t self_shape_introlen = self.shape.introlen
    cdef np.uint32_t self_shape_size = self.shape.size
    cdef np.uint64_t chunksizexmfp
    cdef np.uint64_t stepsizexmfp
    cdef np.int64_t nextstepxmfp
    cdef np.uint32_t i
    cdef np.int64_t numerator
    cdef np.uint32_t j
    cdef np.uint8_t val
    chunksizexmfp = self_chipimplclock * prescaler
    stepsizexmfp = chunksizexmfp * etdr
    nextstepxmfp = chunksizexmfp * self_maincounter + self_precounterxmfp - chunksizexmfp
    i = 0
    while True:
        numerator = nextstepxmfp + self_mfpclock - 1
        if numerator >= 0:
            j = min(numerator // self_mfpclock, self_block_framecount)
            val = self_shape_buf[self_index]
            while i < j:
                self_blockbuf_buf[i] = val
                i += 1
            if j == self_block_framecount:
                break
        nextstepxmfp += stepsizexmfp
        self_index += 1
        if self_index == self_shape_size:
            self_repeat += 1
            self_index = self_shape_introlen
    nextstepxmfp -= self_mfpclock * self_block_framecount
    self_maincounter = 1
    while nextstepxmfp < 0:
        nextstepxmfp += chunksizexmfp
        self_maincounter -= 1
    self_maincounter += nextstepxmfp // chunksizexmfp
    return self_repeat, self_index, self_maincounter, nextstepxmfp % chunksizexmfp
