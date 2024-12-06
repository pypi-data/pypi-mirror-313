import pkgutil


def get_file_contents(file_name):
    return pkgutil.get_data('redbeard_cli', file_name).decode("utf-8")
