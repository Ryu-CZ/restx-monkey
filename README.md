# restx-monkey

Monkey patches for unmaintained [flask-restx](https://github.com/python-restx/flask-restx) python package to keep it
restx compatible with the latest [flask](https://github.com/pallets/flask) and [werkzeug](https://github.com/pallets/werkzeug).

### Usage

Clone repository and copy monkey module to your project or use it as submodule.

```shell
git clone git@github.com:Ryu-CZ/restx-monkey.git  
```

Before importing `flask-restx` apply all patches

```python
from . import monkey

monkey.patch_restx()

...
import flask_restx
...
```

or select which patches you dont want to apply

```python
from . import monkey

monkey.patch_restx(fix_restx_api=False)

...
import flask_restx
...
```

## Goal of project

Keep [flask-restx](https://github.com/python-restx/flask-restx) compatible with the latest [flask](https://github.com/pallets/flask) and [werkzeug](https://github.com/pallets/werkzeug) as long as it is reasonable simple to monkey patch it.

## What this project is not

This project does not solve incompatibilities of other python packages using [flask-restx](https://github.com/python-restx/flask-restx).

