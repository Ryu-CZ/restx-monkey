import sys
import unittest
import warnings

RESTX_PKG_NAME = "flask_restx"


class MonkeyTest(unittest.TestCase):

    def test_get_version(self):
        import monkey
        self.assertIsNotNone(monkey.get_version("pip"))
        self.assertIsNone(monkey.get_version("the-test-mumble_jumble"))

    def test_restx_import(self):
        """check if restx can be import without errors"""
        import monkey
        monkey.patch_restx(replace_parse_rule=True, fix_restx_api=False)
        _ = __import__(RESTX_PKG_NAME)
        self.assertIn(RESTX_PKG_NAME, sys.modules)

    def test_fix_restx_api(self):
        """check if flask_restx.api.Api works"""
        import monkey
        monkey.patch_restx(replace_parse_rule=True, fix_restx_api=True)
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


if __name__ == '__main__':
    unittest.main()
