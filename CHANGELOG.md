# Changelog

All notable changes to [restx-monkey](https://github.com/Ryu-CZ/restx-monkey) project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2022-09-20

### Changed

- Set LICENSE to _BSD-3-Clause_.

## [0.3.1] - 2022-09-07

### Changed

- Use latest droid fonts for Swagger UI.

## [0.3.0] - 2022-09-07

### Added

- Patch to override `static` directory of `flask-restx` with last Swagger UI.

## [0.2.1] - 2022-08-31

### Changed

- Extend `reqparse` patch to [pattern is properly set on list objects](https://github.com/python-restx/flask-restx/pull/453), thanks to
  alexissavin for noticing this.
- Better test coverage to 100%.

## [0.2.0] - 2022-08-31

### Added

- Release project to [pypi](https://pypi.org/project/restx-monkey/)
- Patch `flask_restx.reqparse.Argument` failing on `json` location when there is no `request` json body.

## [0.1.0] - 2022-08-26

### Added

- Module `monkey` to perform patches of `flask-rest`.
- Patch fatal import error of missing module `werkzeug.routing.parse_rule`.
- Patch deprecated `flask_restx.api.Api` appending of swagger documentation `Api._register_doc` after Api is bound to
  flask app or blueprint.

## [0.0.0] - 2022-08-26

### Added

- begin of changelog
