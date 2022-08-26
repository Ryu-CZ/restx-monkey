# noinspection PyUnresolvedReferences
import flask_restx


class ApiWrapper(flask_restx.Api):
    """
    Fixes of `_register_doc` after app init of `flask_restx.api.Api`. THis is not deprecated behavior
    in `flask.Blueprint` compatibility in `flask` version 2.2+
    """
    _doc_registered: bool = False

    def init_app(self, app, **kwargs):
        self.app = app
        # noinspection PyAttributeOutsideInit
        self._add_specs = kwargs.get("add_specs", True)
        self._register_doc(app)
        super().init_app(app, **kwargs)

    def _register_doc(self, app_or_blueprint) -> None:
        if getattr(self, "_doc_registered", None):
            return
        super(ApiWrapper, self)._register_doc(app_or_blueprint)
        self._doc_registered = True

