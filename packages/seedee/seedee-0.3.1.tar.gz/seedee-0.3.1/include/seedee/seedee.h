#ifndef SEEDEE_H
#define SEEDEE_H

#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#pragma GCC visibility push(default)


extern const char seedee_version[32];

typedef enum {
    INVALID_PROTOCOL = -1,  // must be seedee
    INVALID_MAJOR_VERSION = -2,  // must be 1
    INVALID_MINOR_VERSION = -3,  // musst be 0
    INVALID_FORMAT = -4,  // musst be hdf5_chunk
    INVALID_COMPRESSION = -5,  // must be none, lz4, bitshuffle, or deflate
    INVALID_COMPRESSION_OPTS = -6, // must be NULL
    BUFFER_TOO_SMALL = -7,  // the supplied buffer is too small to hold the data
    COMPRESSION_FAILED = -8,  // the compression library reported an error
    INVALID_NUMBER_OF_BLOCKS = -9,  // must be 1
    INVALID_BLOCK_SIZE = -10,  // must be positive
    INVALID_STRIDE = -11,  // must be NULL
    INVALID_ARRAY = -12,  // size, shape, stride, and itemsize are inconsistent
    INVALID_JSON = -13,
    INCOMPLETE_METADATA = -14, // at least one key is missing
}  SeedeeError;


// Return descriptive strings for error codes
const char *seedee_errstr(int err);


enum SeedeeDataFormat{
    FORMAT_HDF5_CHUNK,
    FORMAT_INVALID = -1,
};


enum SeedeeCompressionType{
    COMPRESSION_NONE = 0,
    COMPRESSION_BITSHUFFLE = 32008,
    COMPRESSION_LZ4 = 32004,
    COMPRESSION_DEFLATE = 1,
    COMPRESSION_INVALID = -1,
};


struct SeedeeNDArray {
    char *data;  // pointer to uncompressed data
    int size;  // size of data in bytes
    int ndims;  // number of dimensions
    int *shape;  // number of items in each dimension
    int *stride;  // only NULL is supported, indicating C order
    char datatype; // b, i, u, f for bool, integer, unsigned integer, and floating point, respectively
    int itemsize; // number of bytes per item
    char byteorder; // <, > for little and big endian, respectively
};


// Return the size for the buffer that the used needs to allocate
int seedee_get_buffer_size(
    const struct SeedeeNDArray* array, enum SeedeeDataFormat data_format,
    enum SeedeeCompressionType compression, const void* compression_opts, int n_opts);

// Fill the buffer with the serialized data. The meta argument will point to a
// null-terminatated C string with the metadata json. Returns the number of
// actual bytes written
int seedee_serialize_ndarray(
    const struct SeedeeNDArray* array, enum SeedeeDataFormat data_format,
    enum SeedeeCompressionType compression, const void* compression_opts, int n_opts,
    char* buf, int buf_len, char** meta);


// Return the total size of the data array that the user needs to allocate. All
// non-allocating fields in the array argument will be filled. zero_copy
// indicates if copy-free deserialization will be possible.
int seedee_get_data_size(
    const char* meta, const char* buf, int buf_len, bool* zero_copy, struct SeedeeNDArray* array);


// Fill the user allocated fields in array with the deserialized data. Returns
// the number of actual bytes written. In case zero_copy is true, array->data
// will point to the first data byte in buf.
int seedee_deserialize_ndarray(
    const char* meta, const char* buf, int buf_len,
    bool zero_copy, struct SeedeeNDArray* array);


#pragma GCC visibility pop

#ifdef __cplusplus
}
#endif

#endif // HELLOWORLD_H
