import typing
import importlib.metadata


def get_version(pkg: str) -> typing.Union[typing.Tuple, None]:
    """
    Parse package version as tuple for easy comparison.

    :param pkg: package name
    :return: version tuple of python package for easy comparison
    """
    try:
        pkg_version: str = importlib.metadata.version(pkg)
    except ModuleNotFoundError:
        return None
    return tuple(map(int, pkg_version.split(".")))
