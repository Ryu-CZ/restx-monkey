import unittest

from . import test_restx_monkey


def suite() -> unittest.TestSuite:
    loader = unittest.TestLoader()
    return loader.loadTestsFromModule(test_restx_monkey)


def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())


if __name__ == "__main__":
    main()
