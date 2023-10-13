from . import tools

VERSION = (0, 6, 0)
__version__ = ".".join(map(str, VERSION))

__all__ = ("patch_restx",)

_original_restx_api = None
_injected_werkzeug_routing = False
_original_argument_cls = None
_original_parser_cls = None
_swagger_ui_is_replaced = False
_versions_injected = False
_endpoint_from_view_func__is_moved = False
_werkzeug_coders_injected = False


# noinspection PyUnresolvedReferences
def patch_restx(
    replace_parse_rule: bool = True,
    fix_restx_api: bool = True,
    fix_restx_parser: bool = True,
    update_swagger_ui: bool = True,
    fix_endpoint_from_view: bool = True,
    inject_versions: bool = True,
    fix_werkzeug_url_coders: bool = False,
) -> None:
    """
    Monkey patch unmaintained `flask-restx`. This has a hidden side effects!!! See params bellow.

    :param replace_parse_rule: Patch werkzeug because `flask-restx` is not compatible with latest `werkzeug`
    :param fix_restx_api: fix deprecated `flask-restx.api.Api` init of `doc` endpoints after blueprint is bound
    :param fix_restx_parser: replace failing `flask_restx.reqparse.Argument` class with fixed one
    :param update_swagger_ui: replace swagger UI source files with new version
    :param fix_endpoint_from_view: inject `_endpoint_from_view_func` to `flask.helpers` because `flask` 3.0 moved it to `sansio`
    :param inject_versions: flaks and werkzeug stopped using __version__attribute, put it back
    :param fix_werkzeug_url_coders: inject `werkzeug.urls.url_decode`, `werkzeug.urls.url_encode` if these functions are missing (disabled by default because it is not required by restx)
    """
    global _original_restx_api, _injected_werkzeug_routing, _original_argument_cls, _original_parser_cls, _swagger_ui_is_replaced, _endpoint_from_view_func__is_moved, _versions_injected, _werkzeug_coders_injected
    flask_version = tools.get_version("flask")
    restx_version = tools.get_version("flask-restx")
    werkzeug_version = tools.get_version("werkzeug")

    if fix_endpoint_from_view and not _endpoint_from_view_func__is_moved:
        import flask
        from . import endpoint_from_view

        _endpoint_from_view_func__is_moved = endpoint_from_view.move_endpoint_parser()

    big_three_brake = flask_version >= (3, 0, 0) and restx_version < (1, 2, 0)
    if inject_versions and big_three_brake and not _versions_injected:
        from . import version_system

        version_system.inject_dunder_version()
        _versions_injected = True

    is_incompatible = flask_version >= (2, 2, 0) and restx_version < (0, 6, 0)
    if not is_incompatible:
        return
    if replace_parse_rule and not _injected_werkzeug_routing:
        import werkzeug
        import werkzeug.routing
        from . import werkzeug_routing

        if not hasattr(werkzeug.routing, "parse_rule"):
            werkzeug.routing.parse_rule = werkzeug_routing.parse_rule
        _injected_werkzeug_routing = True
        # noinspection PyUnresolvedReferences
        from werkzeug.routing import parse_rule as test_rule

        _ = test_rule

    if fix_restx_api and _original_restx_api is None:
        from . import restx_api
        import flask_restx

        _original_restx_api = flask_restx.api.Api
        flask_restx.api.Api = restx_api.ApiWrapper
        flask_restx.Api = restx_api.ApiWrapper

    if fix_restx_parser and _original_argument_cls is None and _original_parser_cls is None:
        from . import restx_reqparser
        import flask_restx

        _original_argument_cls = flask_restx.reqparse.Argument
        _original_parser_cls = flask_restx.reqparse.RequestParser
        flask_restx.reqparse.Argument = restx_reqparser.Argument
        flask_restx.reqparse.RequestParser = restx_reqparser.RequestParser

    if update_swagger_ui and not _swagger_ui_is_replaced:
        from . import swagger_ui

        swagger_ui.replace_static_swagger_files()
        _swagger_ui_is_replaced = True

    if fix_werkzeug_url_coders and werkzeug_version > (2, 3, 0) and not _werkzeug_coders_injected:
        from . import werkzeug_routing

        werkzeug_routing.add_werkzeug_urls_encode_decode()
        _werkzeug_coders_injected = True
