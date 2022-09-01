# noinspection PyUnresolvedReferences
import typing

import flask
import flask_restx
from werkzeug.datastructures import MultiDict

__all__ = (
    "Argument",
    "RequestParser",
)


class Argument(flask_restx.reqparse.Argument):

    @property
    def __schema__(self):
        param_ = super(Argument, self).__schema__
        if param_ and self.action == "append":
            # fixes badly placed patter of lists
            param_["items"]["pattern"] = param_["pattern"]
            _ = param_.pop("pattern", None)
        return param_

    def source(self, request: flask.Request) -> typing.Any:
        """
        Pulls values off the request in the provided location
        :param request: The flask request object to parse arguments from
        """
        if isinstance(self.location, str):
            if not request.is_json and self.location == "json":
                # fixes problem with new flask.Request json in GET request types
                return MultiDict()
            value = getattr(request, self.location, MultiDict())
            if callable(value):
                value = value()
            return value if value is not None else MultiDict()
        else:
            values = MultiDict()
            locations = list(self.location)
            if not request.is_json and "json" in locations:
                # fixes problem with new flask.Request json in GET request types
                locations.remove("json")
            for _location in locations:
                value = getattr(request, _location, None)
                if callable(value):
                    value = value()
                if value is not None:
                    values.update(value)
            return values


A_ = typing.TypeVar('A_', bound=flask_restx.reqparse.Argument)
PR_ = typing.TypeVar('PR_', bound=flask_restx.reqparse.ParseResult)


class RequestParser(flask_restx.reqparse.RequestParser):
    args: typing.List[typing.Type[A_]]
    argument_class: typing.Type[A_]
    result_class: typing.Type[PR_]
    trim: bool
    bundle_errors: bool

    def __init__(
            self,
            argument_class: typing.Type[A_] = Argument,
            result_class: typing.Type[PR_] = flask_restx.reqparse.ParseResult,
            trim: bool = False,
            bundle_errors: bool = False,
    ) -> None:
        super(RequestParser, self).__init__(argument_class, result_class, trim, bundle_errors)
