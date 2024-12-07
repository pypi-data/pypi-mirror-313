import typing
import collections.abc
import typing_extensions

def complete(line: str):
    """Returns a list containing the completion possibilities for an import line.

        :param line: incomplete line which contains an import statement:

    import xml.d
    from xml.dom import
        :type line: str
        :return: list of completion possibilities
    """

def get_root_modules():
    """Returns a list containing the names of all the modules available in the
    folders of the python-path.

        :return: modules
    """

def module_list(path: str):
    """Return the list containing the names of the modules available in
    the given folder.

        :param path: folder path
        :type path: str
        :return: modules
    """
