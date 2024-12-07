import io
import numpy as np
import time
import zlib


def file(path) -> bytes:
    """
    file serializes a file on disk to binary.

    Parameters
    ----------
    path (str): path to the file.

    Returns
    -------
    bytes object containing serialized data.
    """
    with open(path, "rb") as f:
        return f.read()


def compressed_file(path: str) -> bytes:
    """
    compressed_file compresses and serializes a file on disk to binary.

    Parameters
    ----------
    path (str): path to the file.

    Returns
    -------
    bytes object containing serialized data.
    """
    with open(path, "rb") as f:
        tic = time.perf_counter()
        data = f.read()
        compressed_data = zlib.compress(data)
        compression_factor = float(len(compressed_data)) / float(len(data))
        print(
            f"compressed size: {100*compression_factor:2.0f}% of original in {1000*(time.perf_counter() - tic):2.0f} ms"
        )
        return compressed_data


# Numpy array, no compression
def numpy(array):
    with io.BytesIO() as bytes_buffer:
        np.save(bytes_buffer, array, allow_pickle=True)
        bytes_buffer.seek(0)
        return bytes_buffer.read()


# Numpy array, with compression (use for segmentations/masks)
def compressed_numpy(array):
    with io.BytesIO() as bytes_buffer:
        np.savez_compressed(bytes_buffer, array=array)
        bytes_buffer.seek(0)
        return bytes_buffer.read()
