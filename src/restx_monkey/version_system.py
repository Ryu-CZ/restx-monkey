from . import tools

DUNDER_VERSION_ATTR = "__version__"


def inject_dunder_version():
    """Set missing `__version__` attribute to flask and werkzeug"""

    if tools.get_version("werkzeug") >= (3, 0, 0):
        import werkzeug

        setattr(werkzeug, DUNDER_VERSION_ATTR, tools.get_version_str("werkzeug"))
    if tools.get_version("flask") >= (3, 0, 0):
        import flask

        setattr(flask, DUNDER_VERSION_ATTR, tools.get_version_str("flask"))
