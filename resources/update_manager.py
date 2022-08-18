from os import system


def v3_1_0_and_up():
    """
    downloads updates for versions 3.1.0 and up
    """

    global version

    version = 'v3.1.0'


# sets variables
latest_version = 'v3.1.0'
versions = {'v3.1.0': v3_1_0_and_up}

# applies every update
while version != latest_version:
    versions[version]()

# updates patch notes

# reruns program
system(f'python {__file__}')
