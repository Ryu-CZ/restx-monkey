import sys
import unittest
import warnings
import shutil
import pathlib

import flask

RESTX_PKG_NAME = "flask_restx"
sys.path.append('../src')


class MonkeyTest(unittest.TestCase):

    def test_get_version(self):
        import restx_monkey
        self.assertIsNotNone(restx_monkey.get_version("pip"))
        self.assertIsNone(restx_monkey.get_version("the-test-mumble_jumble"))

    def test_restx_import(self):
        """check if restx can be import without errors"""
        import restx_monkey
        restx_monkey.patch_restx(replace_parse_rule=True, fix_restx_api=False, fix_restx_parser=False)
        _ = __import__(RESTX_PKG_NAME)
        self.assertIn(RESTX_PKG_NAME, sys.modules)

    def test_fix_restx_api(self):
        """check if flask_restx.api.Api works"""
        import restx_monkey
        restx_monkey.patch_restx(replace_parse_rule=True, fix_restx_api=True, fix_restx_parser=False)
        import flask_restx
        import flask
        warnings.filterwarnings("error")
        api = None
        warn_api = None
        warn_register = None
        bp = flask.Blueprint("test_api", __name__)
        try:
            api = flask_restx.Api(app=bp, title="Test API")
        except Warning as warn:
            warn_api = warn
        self.assertIsNone(warn_api)
        self.assertIsNotNone(api)
        app = flask.Flask(__name__)
        try:
            app.register_blueprint(bp)
        except Warning as warn:
            warn_register = warn
        self.assertIsNone(warn_register)

    def test_parse_rule(self):
        from src.restx_monkey.werkzeug_routing import parse_rule
        self.assertEqual(
            tuple(parse_rule("https://www.google.com/api/<int:version>/index.json?val=3")),
            ((None, None, 'https://www.google.com/api/'), ('int', None, 'version'), (None, None, '/index.json?val=3'))
        )
        with self.assertRaises(ValueError):
            tuple(parse_rule("https://www.google.com/api/<int:version>/<int:version>/index.json?val=3"))
        with self.assertRaises(ValueError):
            tuple(parse_rule("https://www.google.com/api/<int:version>/<string:version>/index.json?val=3"))
        with self.assertRaises(ValueError):
            tuple(parse_rule("https://www.google.com/api/<int:version>>/index.json?val=3")),

    def test_restx_req_parser(self):
        import restx_monkey
        restx_monkey.patch_restx(replace_parse_rule=True, fix_restx_api=True, fix_restx_parser=True)
        import flask_restx
        bp = flask.Blueprint("bp_test", __name__)
        api = flask_restx.Api(bp, title="test parser")

        @api.route("/json_catcher")
        class Catcher(flask_restx.Resource):

            @staticmethod
            def post():
                return {"return": 1}

        app = flask.Flask(__name__)
        app.register_blueprint(bp)
        _ = Catcher

        args_parser = flask_restx.reqparse.RequestParser()
        args_parser.add_argument("test", type=int, location=("json", "args",))
        with app.test_request_context("/json_catcher?test=2", method="POST"):
            args_data = args_parser.parse_args()
        self.assertIn("test", args_data)
        self.assertEqual(args_data["test"], 2)

        json_parser = flask_restx.reqparse.RequestParser()
        json_parser.add_argument("test", type=int, location="json")
        with app.test_request_context("/json_catcher", method="POST", json={"test": 2}):
            json_data = json_parser.parse_args()
        self.assertIn("test", json_data)
        self.assertEqual(json_data["test"], 2)

        multi_location_args_parser = flask_restx.reqparse.RequestParser()
        multi_location_args_parser.add_argument("test", type=int, location=("json",))
        with app.test_request_context("/json_catcher", method="POST"):
            multi_loc_data = multi_location_args_parser.parse_args()
        self.assertIsNone(multi_loc_data.get("test"))

        bad_args_parser = flask_restx.reqparse.RequestParser()
        bad_args_parser.add_argument("test", type=int, location="json")
        with app.test_request_context("/json_catcher?test=2", method="POST"):
            bad_args_data = bad_args_parser.parse_args()
        self.assertIsNone(bad_args_data.get("test"))

        callable_args_parser = flask_restx.reqparse.RequestParser()
        callable_args_parser.add_argument("test", type=int, location="get_json")
        with app.test_request_context("/json_catcher", method="POST", json={"test": 2}):
            json_data = callable_args_parser.parse_args()
        self.assertIn("test", json_data)
        self.assertEqual(json_data["test"], 2)

        callable_args_parser = flask_restx.reqparse.RequestParser()
        callable_args_parser.add_argument("test", type=int, location=("args", "get_json"))
        with app.test_request_context("/json_catcher", method="POST", json={"test": 2}):
            json_data = callable_args_parser.parse_args()
        self.assertIn("test", json_data)
        self.assertEqual(json_data["test"], 2)

        list_parser = flask_restx.reqparse.RequestParser()
        list_parser.add_argument(
            'tag',
            location='args',
            type=flask_restx.inputs.regex('^[-_a-zA-Z0-9]+$'),
            action='append',
            default='',
            help='Filters obj tagged with the provided tags',
        )
        tag_schema = list_parser.args[0].__schema__
        self.assertEqual(tag_schema["items"].get("pattern"), "^[-_a-zA-Z0-9]+$")

    def test_swagger_replace(self):
        import restx_monkey
        from restx_monkey.swagger_ui import is_writable
        self.assertFalse(is_writable("/root"))
        self.assertTrue(is_writable(__file__))
        # optimal scenario works
        os_error = None
        try:
            restx_monkey.patch_restx(replace_parse_rule=True, fix_restx_api=True, update_swagger_ui=True)
        except OSError as e:
            os_error = e
        self.assertIsNone(os_error)
        # skip on no permission
        os_error = None
        try:
            restx_monkey.swagger_ui.replace_static_swagger_files("/root/blabla")
        except OSError as e:
            os_error = e
        self.assertIsNone(os_error)
        os_error = None
        # create missing `file` dir
        tmp_static = pathlib.Path(__file__).parent / "__tmp_static__"
        try:
            tmp_static.mkdir(exist_ok=True)
            restx_monkey.swagger_ui.replace_static_swagger_files(tmp_static)
        except OSError as e:
            os_error = e
        finally:
            shutil.rmtree(str(tmp_static), ignore_errors=True)
        self.assertIsNone(os_error)


if __name__ == '__main__':
    unittest.main()
