# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os
import sys
import pathlib

from invoke import task

ROOT = os.path.dirname(__file__)

CLEAN_PATTERNS = [
    "build",
    "dist",
    "cover",
    "docs/_build",
    "**/*.pyc",
    ".tox",
    "**/__pycache__",
    "reports",
    "*.egg-info",
    "src/*.egg-info",
]


def color(code):
    """A simple ANSI color wrapper factory"""
    return lambda t: "\033[{0}{1}\033[0;m".format(code, t)


blue = color("1;30m")
cyan = color("1;36m")
purple = color("1;35m")


def header(text):
    """Display a header"""
    print(" ".join((blue(">>"), cyan(text))))
    sys.stdout.flush()


def info(text, *args, **kwargs):
    """Display info text"""
    text = text.format(*args, **kwargs)
    print(" ".join((purple(">>>"), text)))
    sys.stdout.flush()


@task
def clean(ctx):
    """Cleanup all build artifacts"""
    header(clean.__doc__)
    with ctx.cd(ROOT):
        for pattern in CLEAN_PATTERNS:
            info("Removing {0}", pattern)
            ctx.run("rm -rf {0}".format(pattern))


@task
def assets(ctx):
    """Fetch web assets"""
    header(assets.__doc__)
    static_folder = "./src/restx_monkey/static"
    with ctx.cd(ROOT):
        ctx.run("npm install")
        ctx.run(f"rm -rf {static_folder}")
        ctx.run(f"mkdir -p {static_folder}")
        ctx.run(
            "cp node_modules/swagger-ui-dist/{swagger-ui*.{css,js}{,.map},favicon*.png,oauth2-redirect.html} "
            + static_folder
        )
        # Until next release we need to install droid sans separately
        ctx.run(f"cp node_modules/typeface-droid-sans/index.css {static_folder}/droid-sans.css")
        if pathlib.Path("./node_modules/typeface-droid-sans/files").exists():
            ctx.run(f"cp -R node_modules/typeface-droid-sans/files {static_folder}")


@task(clean, assets, default=True)
def all(ctx):
    """Run tests, reports and packaging"""
    pass
