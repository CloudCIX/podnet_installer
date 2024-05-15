__all__ = [
    'read_interface_file',
]


def read_interface_file(name, file_name):
    """
    :param name: Interface name on host
    :param file_name: The name of the file of the interface to read
    :return: The content of the filename of the interface
    """
    try:
        with open(f'/sys/class/net/{name}/{file_name}') as file:
            content = file.read().strip()
    except FileNotFoundError:
        content = 'Not Found'
    return content
