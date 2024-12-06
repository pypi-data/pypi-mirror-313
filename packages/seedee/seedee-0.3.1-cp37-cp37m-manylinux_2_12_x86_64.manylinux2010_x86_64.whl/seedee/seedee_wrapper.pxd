# cython: language_level=3
# cython: infer_types=True

from libcpp cimport bool

cdef extern from "seedee/seedee.h":
    const char seedee_version[32]

    cdef char *seedee_errstr(int err)

    cdef enum SeedeeDataFormat:
        FORMAT_HDF5_CHUNK

    cpdef enum SeedeeCompressionType:
        COMPRESSION_NONE = 0,
        COMPRESSION_BITSHUFFLE = 32008,
        COMPRESSION_LZ4 = 32004
        COMPRESSION_DEFLATE = 1


    cdef struct SeedeeNDArray:
        char *data
        int size
        int ndims
        int *shape
        int *stride
        char datatype
        int itemsize
        char byteorder


    cdef int seedee_get_buffer_size(
        SeedeeNDArray* array, SeedeeDataFormat data_format,
        SeedeeCompressionType compression, void* compression_opts, int n_opts)

    cdef int seedee_serialize_ndarray(
        SeedeeNDArray* array, SeedeeDataFormat data_format,
        SeedeeCompressionType compression, void* compression_opts, int n_opts,
        char* buf, size_t buf_len, char** meta) nogil

    cdef int seedee_get_data_size(
        char* meta, char* buf, int buf_len, bool* zero_copy, SeedeeNDArray* array)

    cdef int seedee_deserialize_ndarray(
        char* meta, char* buf, int buf_len, bool zero_copy,
        SeedeeNDArray* array) nogil
