# Changelog

All notable changes to [restx-monkey](https://github.com/Ryu-CZ/restx-monkey) project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2022-08-26

### Added

- Module `monkey` to perform patches of `flask-rest`.
- Patch fatal import error of missing module `werkzeug.routing.parse_rule`.
- Patch deprecated `flask_restx.api.Api` appending of swagger documentation `Api._register_doc` after Api is bound to flask app or blueprint.

## [0.0.0] - 2022-08-26

### Added

- begin of changelog
