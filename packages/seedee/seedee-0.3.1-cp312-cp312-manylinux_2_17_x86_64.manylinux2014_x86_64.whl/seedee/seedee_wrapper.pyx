# cython: language_level=3
# cython: infer_types=True

from libc.stdlib cimport malloc, free
from libc.string cimport strcpy
from cython.operator cimport dereference
import seedee.seedee_wrapper
cimport seedee.seedee_wrapper
import numpy as np
cimport numpy as np

np.import_array()

__version__ = (<bytes>seedee_version).decode()


cdef raise_from_error_code(int err):
    cdef const char *msg = seedee_errstr(err)
    cdef bytes msg_bytes = msg
    raise ValueError(msg_bytes.decode())


cdef SeedeeNDArray ndarray_from_numpy(np.ndarray a):
    cdef SeedeeNDArray ndarray
    ndarray.data = np.PyArray_BYTES(a)
    ndarray.size = a.nbytes
    ndarray.ndims = np.PyArray_NDIM(a)
    ndarray.shape = <int*>malloc(ndarray.ndims*sizeof(dereference(ndarray.shape)))
    for i in range(ndarray.ndims):
        ndarray.shape[i] = np.PyArray_DIMS(a)[i]
    if a.flags["C_CONTIGUOUS"]:
        # NULL means C order, so that we can skip the allocation and copy in the common case
        ndarray.stride = NULL
    else:
        ndarray.stride = <int*>malloc(ndarray.ndims*sizeof(dereference(ndarray.stride)))
        for i in range(ndarray.ndims):
            ndarray.stride[i] = np.PyArray_STRIDES(a)[i]
    # for some reason dtype.kind is a str
    ndarray.datatype = a.dtype.kind.encode()[0]
    ndarray.itemsize = a.itemsize
    # for some reason dtype.byteorder is a str
    ndarray.byteorder = a.dtype.byteorder.encode()[0]
    if ndarray.byteorder == 61 or ndarray.byteorder == 124:
        # builtin types have byteorder '=' or '|' (native)
        # TODO: check if using '<' is ok in this case
        ndarray.byteorder = 60
    return ndarray


cdef numpy_from_ndarray(SeedeeNDArray ndarray, const unsigned char[::1] data):
    format = "{}{}{}".format(chr(ndarray.byteorder), chr(ndarray.datatype), ndarray.itemsize)
    # print("format =", format)
    # dtype = np.dtype(format)
    shape = [0]*ndarray.ndims
    for i in range(ndarray.ndims):
        shape[i] = ndarray.shape[i]
    a = np.asarray(data, dtype=np.uint8)
    return a.view(format).reshape(shape)



def serialize(np.ndarray a, SeedeeCompressionType compression):
    cdef SeedeeNDArray ndarray
    cdef char* meta
    cdef bytes meta_bytes
    cdef int buf_len = -1
    ndarray = ndarray_from_numpy(a)

    #print("datatype", ndarray.datatype)
    #print("itemsize", ndarray.itemsize)
    #print("byteorder", ndarray.byteorder)

    try:
        buf_len = seedee_get_buffer_size(
            &ndarray, FORMAT_HDF5_CHUNK, compression, NULL, 0)

        if buf_len < 0:
            raise_from_error_code(buf_len)

        buf = np.empty(buf_len, dtype=np.uint8)

        buf_pointer = np.PyArray_BYTES(buf)
        with nogil:
            buf_len = seedee_serialize_ndarray(
                &ndarray, FORMAT_HDF5_CHUNK, compression, NULL, 0,
                buf_pointer, buf_len, &meta)

        if buf_len < 0:
            raise_from_error_code(buf_len)

    finally:
        free(ndarray.shape)
        if ndarray.stride != NULL:
            free(ndarray.stride)

    try:
        meta_bytes = meta
    finally:
        free(meta)

    return buf[:buf_len], meta_bytes.decode()


def deserialize(buffer, str meta):
    return _deserialize(np.frombuffer(buffer, dtype="uint8"), meta)


cdef _deserialize(const unsigned char[::1] buf, str meta):
    cdef SeedeeNDArray ndarray
    cdef bytes meta_bytes
    cdef char * meta_chars
    cdef char* buf_ptr = <char*>&buf[0]
    cdef int data_size = -1
    cdef bool zero_copy = False;
    cdef int begin = -1
    cdef int status = -1

    meta_bytes = meta.encode()
    meta_chars = meta_bytes

    data_size = seedee_get_data_size(
        meta_chars, buf_ptr, len(buf), &zero_copy, &ndarray)

    # print("data_size", data_size)

    if data_size < 0:
        raise_from_error_code(data_size)

    if zero_copy:
        ndarray.data = NULL
    else:
        data = np.empty(data_size, dtype=np.uint8)
        ndarray.data = np.PyArray_BYTES(data)

    ndarray.shape = <int*>malloc(ndarray.ndims * sizeof(ndarray.shape))

    # print("ndarray.size", ndarray.size)

    try:
        buf_len = len(buf)
        with nogil:
            status = seedee_deserialize_ndarray(
                meta_chars , buf_ptr, buf_len, zero_copy,
                &ndarray)

        if status < 0:
            raise_from_error_code(status)

        # print("status", status)

        # print("datatype", ndarray.datatype)
        # print("itemsize", ndarray.itemsize)
        # print("byteorder", ndarray.byteorder)

        if zero_copy:
            begin = ndarray.data - buf_ptr
            out = numpy_from_ndarray(
                ndarray, buf[begin:begin + data_size])
        else:
            out = numpy_from_ndarray(ndarray, data)

    finally:
        free(ndarray.shape)

    # print("out", out)
    return out
