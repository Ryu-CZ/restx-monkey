# Restx-Monkey

Monkey patches for unmaintained [flask-restx](https://github.com/python-restx/flask-restx) python package to keep
your installation of flask-restx compatible with the latest [flask](https://github.com/pallets/flask)
and [werkzeug](https://github.com/pallets/werkzeug).

![example workflow](https://github.com/Ryu-CZ/restx-monkey/actions/workflows/release/badge.svg?branch=master)

## Installation

To install restx_monkey, use [pip](https://pip.pypa.io/en/stable/):

```shell
pip install -U restx-monkey
```

## Usage

Before importing `flask-restx` apply all patches in your main module:

```python
# app main file
import restx_monkey as monkey

monkey.patch_restx()

# after patch import other modules 
import flask_restx
# your other code
```

or select which patches you do not want to apply

```python
# app main file
import restx_monkey as monkey

monkey.patch_restx(fix_restx_api=False)

# after patch import other modules 
import flask_restx
# your other code
```

### What is patched?

Here is list of patches applied to [flask-restx](https://github.com/python-restx/flask-restx) package by this monkey:

- _replace_parse_rule_ - injects `parse_rule` method into werkzeug because `flask-restx` is using this internal method
- _fix_restx_api_ - fix deprecated `flask-restx.api.Api` init of `doc` endpoints after blueprint is bound
- _fix_restx_parser_ - replace failing `flask_restx.reqparse.Argument` class with child whom can correctly handle `json`
  location of argument in `flask.Request` even in HTTP `GET` callback
- _update_swagger_ui_ - replace content of `flask_restx.static` directory with the latest swagger UI

## Goal of project

Keep [flask-restx](https://github.com/python-restx/flask-restx) compatible with the
latest [flask](https://github.com/pallets/flask) and [werkzeug](https://github.com/pallets/werkzeug) as long as it is
reasonable simple to monkey patch it.

### What this project is not

This project does not solve incompatibilities of other python packages
using [flask-restx](https://github.com/python-restx/flask-restx).

