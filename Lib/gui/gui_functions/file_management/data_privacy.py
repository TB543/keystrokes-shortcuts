from cryptography.fernet import Fernet
from compileall import compile_file
from os import remove
from sys import argv


def encrypt(string: str):
    """
    encrypts a string for data protection

    :param string: the string to be encrypted

    :return: an encrypted version of that string
    """

    return cryptography.encrypt(string.encode('UTF-8')).decode('UTF-8')


def decrypt(string: str):
    """
    deciphers an encrypted string to be easily read

    :param string: the string to be encrypted

    :return: the deciphered version of the string
    """

    return cryptography.decrypt(string.encode('UTF-8')).decode('UTF-8')


def get_key():
    """
    gets a key to encrypt and decrypt strings and makes a new one if one isn't found

    :return: encryption key
    """

    # tries to import key from existing file
    try:
        from saves.key import key
    except (ModuleNotFoundError, ImportError):

        # generates new key if fails
        key = Fernet.generate_key()

        # writes new key to file
        with open('saves/key.py', 'w') as file:
            path = argv[0].replace('\\', '/')
            file.write(f'from os import remove\nfrom sys import argv\nif __name__ == \'__main__\':\n    '
                       f'remove(__file__)\nelif \'{path}\' == argv[0].replace(\'\\\\\', \'/\'):\n    '
                       f'key = {key}\nelse:\n    remove(__file__)')

        # compiles file and removes it so it can't be opened and read
        compile_file('saves/key.py', legacy=True)
        remove('saves/key.py')

    # returns generated key
    return key


# creates cryptography object used for encryption and decryption
cryptography = Fernet(get_key())
