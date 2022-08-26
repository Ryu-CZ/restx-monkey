import sys
import typing

import pkg_resources

_version = (0, 0, 1)
__version__ = ".".join(map(str, _version))

__all__ = (
    "patch_restx",
)

_original_restx_api = None
_injected_werkzeug_routing = False


def get_version(pkg: str) -> typing.Union[typing.Tuple, None]:
    """
    Parse package version as tuple for easy comparison.

    :param pkg: package name
    :return: version tuple of python package for easy comparison
    """
    packages = pkg_resources.working_set.by_key
    if pkg not in packages:
        return None
    return tuple(map(int, packages[pkg].version.split(".")))


# noinspection PyUnresolvedReferences
def patch_restx(replace_parse_rule: bool = True, fix_restx_api: bool = True) -> None:
    """
    Monkey patch unmaintained `flask-restx`. This has a hidden side effects!!! See params bellow.
    :param replace_parse_rule: Patch werkzeug because `flask-restx` is not compatible with latest `werkzeug`
    :param fix_restx_api: fix deprecated `flask-restx.api.Api` init of `doc` endpoints after blueprint is bound
    """
    global _original_restx_api, _injected_werkzeug_routing
    packages = pkg_resources.working_set.by_key
    if replace_parse_rule and "flask-restx" in packages and not _injected_werkzeug_routing and (
            get_version("werkzeug") > (2, 1, 9) and get_version("flask-restx") <= (0, 6, 0)
    ):
        import werkzeug
        import werkzeug.routing
        from . import werkzeug_routing
        if not hasattr(werkzeug.routing, "parse_rule"):
            werkzeug.routing.parse_rule = werkzeug_routing.parse_rule
        _injected_werkzeug_routing = True
        # noinspection PyUnresolvedReferences
        from werkzeug.routing import parse_rule as test_rule
        _ = test_rule

    if fix_restx_api and "flask" in packages and _original_restx_api is None and (
            get_version("flask") >= (2, 2, 0) and get_version("flask-restx") < (0, 6, 0)
    ):
        from . import restx_api
        import flask_restx
        _original_restx_api = flask_restx.api.Api
        flask_restx.api.Api = restx_api.ApiWrapper
        flask_restx.Api = restx_api.ApiWrapper
