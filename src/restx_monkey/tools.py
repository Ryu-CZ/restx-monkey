import typing
import sys


if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
    import importlib.metadata

    def get_version_str(pkg: str) -> typing.Union[str, None]:
        """
        Parse package version.

        :param pkg: package name
        :return: str version
        """
        try:
            pkg_version: str = importlib.metadata.version(pkg)
        except ModuleNotFoundError:
            return None
        return pkg_version

else:
    # noinspection PyDeprecation
    import pkg_resources

    def get_version_str(pkg: str) -> typing.Union[str, None]:
        """
        Parse package version.

        :param pkg: package name
        :return: str version
        """
        # noinspection PyDeprecation
        packages = pkg_resources.working_set.by_key
        if pkg not in packages:
            return None
        return packages[pkg].version


def get_version(pkg: str) -> typing.Union[typing.Tuple, None]:
    """
    Parse package version as tuple for easy comparison.

    :param pkg: package name
    :return: version tuple of python package for easy comparison
    """
    str_version = get_version_str(pkg)
    if str_version is None:
        return None
    return tuple(map(int, str(str_version).split(".")))
