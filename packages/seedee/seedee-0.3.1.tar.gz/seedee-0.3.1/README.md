# seedee

A data format for n-dimensional arrays.

> This project is in an early stage of development and should be used with caution


## Installation

### Python

Pre-built Python wheels can be installed via `pip`:

```
python3 -m pip install seedee
```

To build a wheel yourself, e.g., if your platform is not supported by the
pre-built wheels, download the latest release and extract it. Inside the source
directory, run:

```
$ cmake -S . -B build -DBUILD_PYTHON=ON -DCMAKE_BUILD_TYPE=Release
$ cmake --build build --target python-wheel --verbose
```

Building requires `cmake` version  `3.13` or newer.

If everything works, the wheel is created in the `build/python/dist/`
subdirectory and can be installed via `pip`.

### C/C++

To build and install the C/C++ libraries, run:
```
$ cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=path/to/install/dir
$ cmake --build build --target seedee --verbose
$ cmake --install build
```

Building requires `cmake` version  `3.13` or newer.


## Usage example

### Python

```python
import numpy as np
import seedee

# Create a numpy array of some dimension, shape, and dtype
array = np.arange(48).reshape((6, 8)).astype("uint16")

# Serialize the array using the bitshuffle+lz4 compression method
buffer, meta = seedee.serialize(array, seedee.COMPRESSION_BITSHUFFLE)
# buffer is a 1D numpy array of type uint8
# meta is a string

# Send buffer and meta to a remote process using any preferred method,
# e.g., via a ZMQ multi-message
...

# Deserialize the received buffer and meta into a numpy array
new_array = seedee.deserialize(buffer, meta)

# The resulting array is equal to the original array
assert np.all(array == new_array)
```

### C/C++

See `test` directory for some examples. Note that the C/C++ interface will
likely change in the future.

## Limitations

Only arrays up to 1GB are supported.

## Development

Use the following commands to compile `seedee` and run the tests:
```
cmake -S . -B build -DBUILD_PYTHON=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build --target all --verbose
ctest --test-dir build -T test --output-on-failure
```

## Contribution

Please feel free to open issues or pull requests.

## Acknowledgments

`seedee` depends on multiple open source libraries that are included in this
repository under the `thirdparty` directory for convenience. The licenses of
these dependencies can be found in the corresponding subdirectories and in
LICENSE_THIRDPARTY.txt.

The chunk serializer implementations are based on the corresponding HDF5 filter
plugins which are subject to their own licenses:
* LZ4 filter plugin: https://github.com/nexusformat/HDF5-External-Filter-Plugins/blob/master/LZ4/COPYING
* bitshuffle filter plugin: https://github.com/kiyo-masui/bitshuffle/blob/master/LICENSE
* zlib filter plugin: https://github.com/HDFGroup/hdf5/blob/develop/COPYING
