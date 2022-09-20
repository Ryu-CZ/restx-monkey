import typing

import pkg_resources

VERSION = (0, 4, 0)
__version__ = ".".join(map(str, VERSION))

__all__ = (
    "patch_restx",
)

_original_restx_api = None
_injected_werkzeug_routing = False
_original_argument_cls = None
_original_parser_cls = None
_swagger_ui_is_replaced = False


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
def patch_restx(
        replace_parse_rule: bool = True,
        fix_restx_api: bool = True,
        fix_restx_parser: bool = True,
        update_swagger_ui: bool = True,
) -> None:
    """
    Monkey patch unmaintained `flask-restx`. This has a hidden side effects!!! See params bellow.

    :param replace_parse_rule: Patch werkzeug because `flask-restx` is not compatible with latest `werkzeug`
    :param fix_restx_api: fix deprecated `flask-restx.api.Api` init of `doc` endpoints after blueprint is bound
    :param fix_restx_parser: replace failing `flask_restx.reqparse.Argument` class with fixed one
    :param update_swagger_ui: replace swagger UI source files with new version
    """
    global _original_restx_api, _injected_werkzeug_routing, _original_argument_cls, _original_parser_cls, _swagger_ui_is_replaced

    is_incompatible = get_version("flask") >= (2, 2, 0) and get_version("flask-restx") < (0, 6, 0)
    if replace_parse_rule and is_incompatible and not _injected_werkzeug_routing:
        import werkzeug
        import werkzeug.routing
        from . import werkzeug_routing
        if not hasattr(werkzeug.routing, "parse_rule"):
            werkzeug.routing.parse_rule = werkzeug_routing.parse_rule
        _injected_werkzeug_routing = True
        # noinspection PyUnresolvedReferences
        from werkzeug.routing import parse_rule as test_rule
        _ = test_rule

    if fix_restx_api and _original_restx_api is None and is_incompatible:
        from . import restx_api
        import flask_restx
        _original_restx_api = flask_restx.api.Api
        flask_restx.api.Api = restx_api.ApiWrapper
        flask_restx.Api = restx_api.ApiWrapper

    if fix_restx_parser and is_incompatible and _original_argument_cls is None and _original_parser_cls is None:
        from . import restx_reqparser
        import flask_restx
        _original_argument_cls = flask_restx.reqparse.Argument
        _original_parser_cls = flask_restx.reqparse.RequestParser
        flask_restx.reqparse.Argument = restx_reqparser.Argument
        flask_restx.reqparse.RequestParser = restx_reqparser.RequestParser

    if update_swagger_ui and is_incompatible and not _swagger_ui_is_replaced:
        from . import swagger_ui
        swagger_ui.replace_static_swagger_files()
        _swagger_ui_is_replaced = True
