# adds package to import path
from sys import path
path.insert(0, __file__.strip('__init__.py'))

# imports package functions
from data_privacy import *
from compression import *
from zlib import error as compression_error


def read_file(name: str):
    """
    reads the contents of a file to get the data used for this program, decrypt and decompress if required

    :param name: the file name of the file to be read

    :return: the contents of the file
    """

    # gets data and attempts to convert data to correct data type
    try:
        with open(name, 'rb') as file:
            data = file.read()
        return eval(data)
    except (SyntaxError, ValueError):
        pass

    # attempts to decompress and then convert data
    try:
        with open(name, 'rb') as file:
            data = file.read()
        return eval(decompress(data))
    except (compression_error, SyntaxError):
        pass

    # attempts to decrypt then convert data
    try:
        with open(name, 'rb') as file:
            data = file.read()
        return eval(decrypt(data.decode('UTF-8')))
    except UnicodeDecodeError:
        pass

    # attempts to decrypt then decompress then convert data
    try:
        with open(name, 'rb') as file:
            data = file.read()
        return eval(decrypt(decompress(data)))
    except ModuleNotFoundError:
        pass


def write_file(name: str, data: dict, encrypt_data: bool, compress_data: bool):
    """
    writes program data to a file, encrypts and compresses if settings are selected

    :param name: the name of the file to be written to

    :param data: the data to be written to the file is dict format (primary data type for this program)

    :param encrypt_data: determines if user wants to encrypt their files, yes if true

    :param compress_data: determines if user wants to compress their files, yes if true
    """

    # converts data to string
    data = str(data)

    # encrypts data
    if encrypt_data:
        data = encrypt(data)

    # compresses data
    if compress_data:
        data = compress(data)

    # converts data to bytes
    try:
        data = data.encode('UTF-8')
    except AttributeError:
        pass

    # writes data to file as bytes
    with open(name, 'wb') as file:
        file.write(data)
