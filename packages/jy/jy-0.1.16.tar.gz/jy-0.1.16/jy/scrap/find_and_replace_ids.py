"""
In order to solve this problem: 
https://github.com/i2mint/jy/discussions/3#discussioncomment-6862843
I wrote some code to find and replace ids in html, css, and js strings.

It seems to complex and not very robust. I'm sure there are better ways to do this.
I'm still posting this here in case I want to resurect it.

This code has tests!

"""

# from jy.js_parse import replace_tokens, string_kind, replace_ids, default_token_replacer

import re
from functools import partial
from typing import Callable, Optional, Union


def replace_tokens(string: str, token_extractor: Callable, token_replacer: Callable):
    """
    Replace tokens in a string based on patterns provided in the token_extractor.

    Parameters:
    - string: The input string in which tokens need to be replaced.
    - token_extractor: A dictionary mapping token classes to their regex patterns.
    - token_replacer: A function that determines how a matched token should be replaced.

    Returns:
    - new_string: The string with tokens replaced.
    - replaced: A dictionary mapping old tokens to their replacements.

    >>> new_string, replaced = replace_tokens(
    ...     'Hello, my id="name" is John.',
    ...     {"id": r'id="([^"]+)"'},
    ...     default_token_replacer
    ... )
    >>> list(replaced)
    ['id="name"']
    >>> replaced['id="name"'].startswith('id="name_')
    True
    >>> replaced['id="name"']  # doctest: +SKIP
    'id="name_db72fa7f"'  # random suffix was added
    """

    replaced = {}
    new_string = string

    for token_class, token_pattern in token_extractor.items():
        for match in re.finditer(token_pattern, new_string):
            old_token = match.group(0)
            new_token = token_replacer(old_token, token_class)
            replaced[old_token] = new_token
            new_string = new_string.replace(old_token, new_token)

    return new_string, replaced


import uuid


def default_token_replacer(matched_token: str, token_class: str):
    """
    Default token replacer that appends a unique suffix to the matched token.

    Parameters:
    - matched_token: The token that was matched.
    - token_class: The class of the token (e.g., "id").

    Returns:
    - The replaced token with a unique suffix.

    >>> default_token_replacer('id="test"', 'id')  # doctest: +ELLIPSIS
    'id="test_..."'
    """
    unique_suffix = str(uuid.uuid4()).replace("-", "")[
        :8
    ]  # Taking the first 8 characters for brevity

    # For HTML ids, we want to replace only the value inside the quotes
    if token_class == "id" and matched_token.startswith("id="):
        return 'id="' + matched_token.split('"')[1] + "_" + unique_suffix + '"'

    # For JavaScript getElementById, we want to replace only the value inside the parentheses
    if token_class == "id" and matched_token.startswith("document.getElementById("):
        return (
            'document.getElementById("'
            + matched_token.split('"')[1]
            + "_"
            + unique_suffix
            + '")'
        )

    # For CSS ids, we can append directly
    return matched_token + "_" + unique_suffix


# html_extractor = {"id": r'id="([^"]+)"'}

css_extractor = {"id": r"#([a-zA-Z][\w\-]*)"}

# js_extractor = {"id": r'document\.getElementById\("([^"]+)"\)'}

# Updated extractors
html_extractor = {"id": r'id\s*=\s*["\']([^"\']+?)["\']'}
js_extractor = {"id": r'document\.getElementById\s*\(\s*["\']([^"\']+?)["\']\s*\)'}


replace_html_ids = partial(
    replace_tokens,
    token_extractor=html_extractor,
    token_replacer=default_token_replacer,
)
replace_css_ids = partial(
    replace_tokens, token_extractor=css_extractor, token_replacer=default_token_replacer
)
replace_js_ids = partial(
    replace_tokens, token_extractor=js_extractor, token_replacer=default_token_replacer
)


# Determining the kind of string (html, css, or js)
# TODO: Make the default rules more robust


def _is_html_string(string):
    return "<div" in string or "<a" in string or "<span" in string


def _is_js_string(string):
    return (
        "document.getElementById" in string
        or "function" in string
        or ".addEventListener" in string
    )


def _is_css_string(string):
    return "{" in string and "}" in string and (":" in string or ";" in string)


_dflt_string_kind_rules = tuple(
    {"html": _is_html_string, "js": _is_js_string, "css": _is_css_string}.items()
)


def _string_kind(string, string_kind_rules=_dflt_string_kind_rules):
    string_kind_rules = dict(string_kind_rules)
    for kind, rule in string_kind_rules.items():
        if rule(string):
            return kind


# TODO: Replacer logic is also a mapping. Perhaps could centralize with rules mapping
_dflt_replacer_for_kind = tuple(
    {"html": replace_html_ids, "js": replace_js_ids, "css": replace_css_ids}.items()
)


def replace_ids(
    string,
    kind: Optional[str] = None,
    *,
    replacer_for_kind=_dflt_replacer_for_kind,
    string_to_kind: Optional[Callable] = _string_kind
):
    kind = kind or string_to_kind(string)
    replacer_for_kind = dict(replacer_for_kind)
    replacer = replacer_for_kind.get(kind, None)
    if replacer is not None:
        return replacer(string)
    # if all else fails, just:
    return string, {}


# Tests ----------------------------------------------------------------
def test_replace_tokens():
    test_string = 'Hello, my id="name" is John.'
    extractor = {"id": r'id="([^"]+)"'}
    replacer = default_token_replacer
    new_string, replaced = replace_tokens(test_string, extractor, replacer)
    assert (
        new_string != test_string
    )  # The new string should be different due to the unique ID
    assert 'id="name_' in new_string  # The new ID should start with "name_"


def test_string_kind():
    assert _string_kind('<div class="test">Hello</div>') == "html"
    assert _string_kind("#test { color: red; }") == "css"
    assert _string_kind('function test() { alert("Hello"); }') == "js"
    assert _string_kind("This is a random string.") == None


def test_replace_ids():
    html_test = '<div id="test">Hello</div>'
    css_test = "#test { color: red; }"
    js_test = 'document.getElementById("test").style.color = "red";'

    new_html, replaced_html = replace_ids(html_test)
    new_css, replaced_css = replace_ids(css_test)
    new_js, replaced_js = replace_ids(js_test)

    # Check if the replaced IDs have the unique suffix
    assert 'id="test_' in new_html
    assert "#test_" in new_css
    assert 'document.getElementById("test_' in new_js

    # Check the replaced dictionary
    old_html_id = list(replaced_html.keys())[0]
    old_css_id = list(replaced_css.keys())[0]
    old_js_id = list(replaced_js.keys())[0]

    assert old_html_id == 'id="test"'
    assert old_css_id == "#test"
    assert old_js_id == 'document.getElementById("test")'


## Run the tests
# test_replace_tokens()
# test_string_kind()
# test_replace_ids()

## print("All tests passed!")


# default_token_replacer('id="test"', 'id')
# 'id="test_<some_unique_suffix>"'
