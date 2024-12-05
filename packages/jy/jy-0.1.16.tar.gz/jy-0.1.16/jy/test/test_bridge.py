"""Tests for the bridge module"""

from jy.bridge import add_js_funcs

from jy.util import js_files

test01_js_code = js_files["test01"]


def test_add_js_call_attributes_to_obj():
    """
    See test_js_parse.test_func_name_and_params_pairs for intermediate data of this test
    """
    js = add_js_funcs(test01_js_code)

    # js has two methods called bar and foo
    assert sorted([x for x in dir(js) if not x.startswith("_")]) == [
        "add_one",
        "bar",
        "foo",
        "obj",
        "prop",
        "with_arrow_func",
        "with_let",
    ]

    # they mirror the signatures of the underlying JS functions
    from inspect import signature

    assert str(signature(js.foo)) == "(a, b='hello', c=3)"
    assert str(signature(js.bar)) == "(green, eggs='food', and=True, ham=4)"

    # Calling this function returns a string
    # (the code to call the underlying JS function)
    assert js.foo(1, "hi", 5) == 'foo(1, "hi", 5)'

    # Notice that you can use positional or keyword arguments
    # Also, notice that though "prop" is the name of js's attribute,
    # the function call string does indeed use the original full reference:
    # ``func.assigned.to.nested.prop``
    assert js.prop("up") == ('func.assigned.to.nested.prop("up")')

    # Notice that the python (signature) defaults are applied before translating to JS
    assert js.bar(42) == 'bar(42, "food", true, 4)'

    alt_js = add_js_funcs(test01_js_code, apply_defaults=False)
    # You can opt not to do this by specifying apply_defaults=False
    # This will result in only injecting those inputs you specify in the js call string,
    # which will have the effect of letting JS apply it's defaults, what ever they are
    alt_js = add_js_funcs(test01_js_code, apply_defaults=False)
    assert alt_js.bar(42) == "bar(42)"
