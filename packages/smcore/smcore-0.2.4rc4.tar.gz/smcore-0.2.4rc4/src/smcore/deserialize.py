import io
import numpy as np
import zlib


def file(data: bytes, save_path: str):
    """
    file writes binary data to disk. File-based deserialization
    can be useful if a library doesn't present memory-level interface.

    Parameters
    ----------
    data (bytes): serialized data to write to a file
    save_path (str): path to write the file to.
    """
    with open(save_path, "wb") as f:
        f.write(data)


def compressed_file(data: bytes, save_path: str):
    """
    compressed_file decompresses binary data using zlib and saves
    it to disk.

    Parameters
    ----------
    data (bytes): serialized data to write to a file.
    save_path (str): path to write the file to.
    """
    data = zlib.decompress(data)
    with open(save_path, "wb") as f:
        f.write(data)


def compressed_memory_file(data: bytes):
    """
    compressed_memory_file decompresses binary data using zlib and
    saves it to memory as an io.BytesIO object.

    Parameters
    ----------
    data (bytes): serialized data to decompress and write to memory.

    Returns
    -------
    Decompressed,
    """
    return io.BytesIO(zlib.decompress(data))


def memory_file(data: bytes) -> io.BytesIO:
    """
    memory_file saves binary data to memory. BytesIO behaves like
    file, but exists in memory. This is more efficient and recommended
    if it works in your use case.

    Parameters
    ----------
    data (bytes): serialized data to write to memory.

    Returns
    -------
    BytesIO-encoded data.
    """
    return io.BytesIO(data)


def numpy(data: bytes) -> np.ndarray[float]:
    """
    numpy deserializes binary data to a numpy array.

    Parameters
    ----------
    data (bytes): serialized data to write to an array.

    Returns
    -------
    np.ndarray[float] object with deserialized data.
    """
    buff = io.BytesIO(data)
    return np.load(buff, allow_pickle=True)


def compressed_numpy(data: bytes):
    """
    compressed_numpy deserializes binary data to a numpy array.
    It is the same function as numpy, but we include it to maintain
    a consistent interface.

    Parameters
    ----------
    data (bytes): serialized data to write to an array.

    Returns
    -------
    np.ndarray[float] object with deserialized data.
    """
    buff = io.BytesIO(data)
    loaded = np.load(buff, allow_pickle=True)
    return loaded["array"]
