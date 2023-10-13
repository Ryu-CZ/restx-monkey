# copy of original method werkzeug.routing.parse_rule

import re
import typing as t

_rule_re = re.compile(
    r"""
    (?P<static>[^<]*)                           # static rule data
    <
    (?:
        (?P<converter>[a-zA-Z_][a-zA-Z0-9_]*)   # converter name
        (?:\((?P<args>.*?)\))?                  # converter arguments
        \:                                      # variable delimiter
    )?
    (?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)        # variable name
    >
    """,
    re.VERBOSE,
)


def parse_rule(rule: str) -> t.Iterator[t.Tuple[t.Optional[str], t.Optional[str], str]]:
    """Parse a rule and return it as generator. Each iteration yields tuples
    in the form ``(converter, arguments, variable)``. If the converter is
    `None` it's a static url part, otherwise it's a dynamic one.

    :internal:
    """
    pos = 0
    end = len(rule)
    do_match = _rule_re.match
    used_names = set()
    while pos < end:
        m = do_match(rule, pos)
        if m is None:
            break
        data = m.groupdict()
        if data["static"]:
            yield None, None, data["static"]
        variable = data["variable"]
        converter = data["converter"] or "default"
        if variable in used_names:
            raise ValueError(f"variable name {variable!r} used twice.")
        used_names.add(variable)
        yield converter, data["args"] or None, variable
        pos = m.end()
    if pos < end:
        remaining = rule[pos:]
        if ">" in remaining or "<" in remaining:
            raise ValueError(f"malformed url rule: {rule!r}")
        yield None, None, remaining


def add_werkzeug_urls_encode_decode():
    """
    Inject `werkzeug.urls.url_decode`, `werkzeug.urls.url_encode` if these functions are missing.

    Beware!!! - functions used to replace originals does not have the same header
    """
    # fix for flask login
    import urllib.parse
    import werkzeug.urls

    if not hasattr(werkzeug.urls, "url_decode"):
        werkzeug.urls.url_decode = urllib.parse.parse_qs
    if not hasattr(werkzeug.urls, "url_encode"):
        werkzeug.urls.url_encode = urllib.parse.urlencode
