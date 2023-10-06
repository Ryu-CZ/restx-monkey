import warnings
import typing


class FlaskCompatibilityWarning(DeprecationWarning):
    pass


def get_name_strict(view_func: typing.Callable) -> str:
    """Copy of flask internal helper that returns the default endpoint for a given
    function.  This always is the function name.
    """
    assert view_func is not None, "expected view func if endpoint is not provided."
    return view_func.__name__


def move_endpoint_parser():
    """
    Resolve import flask _endpoint_from_view_func.

    Show warning if function cannot be found and provide copy of last known implementation.

    Note: This helper method exists because reoccurring problem with flask function, but
    actual method body remaining the same in each flask version.
    """
    from . import tools

    flask_version = tools.get_version_str("flask").split(".")
    try:
        if flask_version[0] == "1":
            # noinspection PyProtectedMember
            from flask.helpers import _endpoint_from_view_func
        elif flask_version[0] == "2":
            # noinspection PyProtectedMember
            from flask.scaffold import _endpoint_from_view_func
        elif flask_version[0] == "3":
            # noinspection PyProtectedMember
            from flask.sansio.scaffold import _endpoint_from_view_func
        else:
            warnings.simplefilter("once", FlaskCompatibilityWarning)
            _endpoint_from_view_func = None
    except ImportError:
        warnings.simplefilter("once", FlaskCompatibilityWarning)
        _endpoint_from_view_func = None
    if _endpoint_from_view_func is None:
        _endpoint_from_view_func = get_name_strict
    changed = False
    import flask

    if not hasattr(flask.helpers, "_endpoint_from_view_func"):
        flask.helpers._endpoint_from_view_func = _endpoint_from_view_func
        changed = True
    if hasattr(flask, "scaffold"):
        flask.scaffold._endpoint_from_view_func = _endpoint_from_view_func
        changed = True
    return changed
