import io
from concurrent.futures import ThreadPoolExecutor
import json
import h5py
try:
    import hdf5plugin  # noqa
except ImportError:
    pass
import numpy as np
import pytest
import seedee


def example_array(shape, dtype=np.int64, offset=0):
    size = np.prod(shape)
    offset = np.array(offset).astype(dtype)
    a = np.arange(size).astype(dtype).reshape(*shape)
    return a + offset


@pytest.fixture
def threadpool():
    pool = ThreadPoolExecutor(max_workers=4)
    yield pool
    pool.shutdown(wait=True)


@pytest.fixture(
    params=[
        seedee.COMPRESSION_NONE, seedee.COMPRESSION_BITSHUFFLE,
        seedee.COMPRESSION_LZ4, seedee.COMPRESSION_DEFLATE])
def compression(request):
    return request.param


@pytest.fixture(
    params=[
        np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64,
        np.float32, np.float64, np.bool_])
def dtype(request):
    return request.param


def test_version():
    assert seedee.__version__
    assert isinstance(seedee.__version__, str)
    assert seedee.__version__ != "unknown"


def test_wrong_meta():
    with pytest.raises(ValueError, match="Invalid JSON"):
        seedee.deserialize(b"123", "wrong_meta")


def test_no_protocol():
    with pytest.raises(ValueError, match="Invalid protocol"):
        seedee.deserialize(b"123", '{"format": "foo"}')


def test_wrong_protocol():
    with pytest.raises(ValueError, match="Invalid protocol"):
        seedee.deserialize(b"123", '{"protocol": "not_seedee"}')


def test_invalid_stride_serialize():
    a = example_array(shape=(6, 8))
    a_column_major = np.asfortranarray(a)
    with pytest.raises(ValueError, match="Invalid stride"):
        buf, meta = seedee.serialize(a_column_major, seedee.COMPRESSION_NONE)


def test_invalid_stride_deserialize():
    a = example_array(shape=(6, 8))
    buf, meta = seedee.serialize(a, seedee.COMPRESSION_NONE)
    print(meta)
    m = json.loads(meta)
    m["array"]["stride"] = [8, 1]
    meta_with_invalid_stride = json.dumps(m)
    print(meta_with_invalid_stride)
    with pytest.raises(ValueError, match="Invalid stride"):
        seedee.deserialize(buf, meta_with_invalid_stride)


def test_round_trip(dtype, compression):
    a = example_array(shape=(6, 8), dtype=dtype)
    buf, meta = seedee.serialize(a, compression)
    assert len(buf) > 0
    assert meta
    print(meta)
    a2 = seedee.deserialize(buf, meta)
    assert np.all(a == a2)


def test_round_trip_with_bytes(dtype, compression):
    a = example_array(shape=(6, 8), dtype=dtype)
    buf, meta = seedee.serialize(a, compression)
    buf = buf.tobytes()
    a2 = seedee.deserialize(buf, meta)
    assert np.all(a == a2)


def test_round_trip_view_int8(dtype, compression):
    a = example_array(shape=(6, 8), dtype=dtype)
    buf, meta = seedee.serialize(a, compression)
    buf = buf.view("int8")
    a2 = seedee.deserialize(buf, meta)
    assert np.all(a == a2)


def test_round_trip_parallel(dtype, compression, threadpool):
    """Serialize and deserialize in parallel on the same thread"""
    def thread(i):
        a = example_array(shape=(6, 8), dtype=dtype, offset=i)
        buf, meta = seedee.serialize(a, compression)
        a2 = seedee.deserialize(buf, meta)
        assert np.all(a == a2)
        return a2

    futures = [threadpool.submit(thread, i) for i in range(1000)]

    threadpool.shutdown(wait=True)

    # raise errors
    for f in futures:
        f.result()


def test_round_trip_parallel_different_threads(dtype, compression, threadpool):
    """Serialize and deserialize in parallel on different threads"""
    def serialize_thread(i):
        a = example_array(shape=(6, 8), dtype=dtype, offset=i)
        buf, meta = seedee.serialize(a, compression)
        return buf, meta

    def deserialize_thread(i, future):
        buf, meta = future.result()
        a2 = seedee.deserialize(buf, meta)
        a = example_array(shape=(6, 8), dtype=dtype, offset=i)
        assert np.all(a == a2)

    s_futures = [threadpool.submit(serialize_thread, i) for i in range(1000)]

    d_futures = [
        threadpool.submit(deserialize_thread, i, f)
        for i, f in enumerate(s_futures)]

    threadpool.shutdown(wait=True)

    # raise_errors
    for f in s_futures:
        f.result()

    for f in d_futures:
        f.result()


def test_round_trip_parallel_serialize(dtype, compression, threadpool):
    """Only serialize in parallel, deserialize sequentially"""
    def serialize_thread(i):
        a = example_array(shape=(6, 8), dtype=dtype, offset=i)
        buf, meta = seedee.serialize(a, compression)
        return buf, meta

    s_futures = [threadpool.submit(serialize_thread, i) for i in range(1000)]

    # Wait for all serializations to finish
    threadpool.shutdown(wait=True)

    for i, f in enumerate(s_futures):
        buf, meta = f.result()
        a2 = seedee.deserialize(buf, meta)
        a = example_array(shape=(6, 8), dtype=dtype, offset=i)
        assert np.all(a == a2)


def test_round_trip_parallel_deserialize(dtype, compression, threadpool):
    """Only deserialize in parallel, serialize sequentially"""
    def serialize(i):
        a = example_array(shape=(6, 8), dtype=dtype, offset=i)
        buf, meta = seedee.serialize(a, compression)
        return buf, meta

    def deserialize_thread(i, buf, meta):
        a2 = seedee.deserialize(buf, meta)
        a = example_array(shape=(6, 8), dtype=dtype, offset=i)
        assert np.all(a == a2)

    messages = [serialize(i) for i in range(1000)]

    d_futures = [
        threadpool.submit(deserialize_thread, i, buf, meta)
        for i, (buf, meta) in enumerate(messages)]

    threadpool.shutdown(wait=True)

    for f in d_futures:
        f.result()


def test_deserialize_missing_json_key(dtype, compression):
    a = example_array(shape=(6, 8), dtype=dtype)
    buf, meta = seedee.serialize(a, compression)
    m = json.loads(meta)
    keys = list(m.keys())
    for key in keys:
        print(key)
        m = json.loads(meta)
        del m[key]
        meta_without_key = json.dumps(m)
        print(meta_without_key)
        with pytest.raises(ValueError):
            seedee.deserialize(buf, meta_without_key)


def get_compression_args(compression, compression_opts):
    if compression == seedee.COMPRESSION_NONE:
        assert compression_opts is None
        compression_id = None
    elif compression == seedee.COMPRESSION_BITSHUFFLE:
        compression_id = compression
        # h5py expects a tuple instead of a list
        compression_opts = tuple(compression_opts)
    elif compression == seedee.COMPRESSION_LZ4:
        compression_id = compression
        # h5py expects a tuple instead of a list
        compression_opts = tuple(compression_opts)
    elif compression == seedee.COMPRESSION_DEFLATE:
        compression_id = "gzip"
        # h5py expects an int instead of a list for gzip compression options
        assert len(compression_opts) == 1
        compression_opts = compression_opts[0]
    else:
        raise ValueError("Unknown compression: '{}'".format(compression))

    compression_args = {
        "compression": compression_id, "compression_opts": compression_opts}

    return compression_args


def write_chunk(file, chunk, meta_json):
    meta = json.loads(meta_json)
    array = meta["array"]
    shape = tuple(array["shape"])
    format = "{}{}{}".format(
        chr(array["byteorder"]), chr(array["datatype"]), array["itemsize"])
    dtype = np.dtype(format)
    compression = meta["compression"]
    compression_opts = meta["compression_opts"]
    compression_args = get_compression_args(compression, compression_opts)

    d = file.create_dataset(
            "data", dtype=dtype, shape=shape, chunks=shape,
            **compression_args)
    d.id.write_direct_chunk((0,)*len(shape), bytes(chunk))


def test_serialize_hdf5_chunk(compression, dtype):
    a = example_array(shape=(6, 8), dtype=dtype)

    buf, meta = seedee.serialize(a, compression)

    bytes_io = io.BytesIO()
    with h5py.File(bytes_io, "w") as f:
        write_chunk(f, buf, meta)

    bytes_io.seek(0)

    with h5py.File(bytes_io, "r") as f:
        a2 = f["data"][()]

    assert np.all(a == a2)


def test_deserialize_hdf5_chunk(compression, dtype):
    a = example_array(shape=(600, 800), dtype=dtype)

    # Get meta dictionary
    _, meta = seedee.serialize(a, compression)

    compression_opts = {
        seedee.COMPRESSION_NONE: None,  # only supported option
        seedee.COMPRESSION_BITSHUFFLE: (0, 2),  # only supported option
        seedee.COMPRESSION_LZ4: (0,),  # only supported option
        seedee.COMPRESSION_DEFLATE: (2,),  # test a non-default option
    }[compression]

    compression_args = get_compression_args(compression, compression_opts)

    bytes_io = io.BytesIO()
    with h5py.File(bytes_io, "w") as f:
        f.create_dataset(
            "data", data=a, shape=a.shape, chunks=a.shape, **compression_args)

    bytes_io.seek(0)

    with h5py.File(bytes_io, "r") as f:
        _, chunk = f["data"].id.read_direct_chunk((0,)*a.ndim)
        print("header size:", int.from_bytes(chunk[:8], "big"))
        print("header size:", np.frombuffer(chunk[:8], dtype=">u8"))

    a2 = seedee.deserialize(chunk, meta)

    assert np.all(a == a2)
