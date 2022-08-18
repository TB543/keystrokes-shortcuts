from zlib import compress as comp, decompress as de_comp


def compress(string: str):
    """
    converts a string to bytes and compresses it

    :param string: the string to be compressed

    :return: the compressed data in byte form
    """

    return comp(string.encode('UTF-8'))


def decompress(byte_code: bytes):
    """
    decompressed a compressed string

    :param byte_code: the byte code of the compressed string

    :return: the decompressed string
    """

    return de_comp(byte_code).decode('UTF-8')
