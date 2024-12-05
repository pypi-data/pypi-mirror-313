"""Tests for js_bridge"""

from jy.js_parse import func_name_and_params_pairs
from jy.util import js_files

test01_js_code = js_files["test01"]


def test_func_name_and_params_pairs():
    pairs = list(func_name_and_params_pairs(test01_js_code))
    assert pairs == [
        (
            "foo",
            [
                {"name": "a"},
                {"name": "b", "default": "hello"},
                {"name": "c", "default": 3},
            ],
        ),
        (
            "bar",
            [
                {"name": "green"},
                {"name": "eggs", "default": "food"},
                {"name": "and", "default": True},
                {"name": "ham", "default": 4},
            ],
        ),
        ("add_one", [{"name": "x"}]),
        ("with_let", [{"name": "x"}]),
        ("with_arrow_func", [{"name": "y"}, {"name": "z", "default": 1}]),
        # Note that the name here is dot-separated!
        ("func.assigned.to.nested.prop", [{"name": "x"}]),
        ("obj", [{"name": "exports"}]),
    ]


def test_replace_ids_in_code():
    from jy.js_parse import replace_ids_in_code

    # Test with HTML content
    html_code = '<div id="test">Hello</div>'
    new_html, replaced_html = replace_ids_in_code(html_code)
    assert 'id="test_' in new_html
    assert "test" in replaced_html

    # Test with CSS content
    css_code = "#test { color: red; }"
    new_css, replaced_css = replace_ids_in_code(css_code)
    assert "#test_" in new_css
    assert "test" in replaced_css

    # Test with JS content
    js_code = 'document.getElementById("test").style.color = "red";'
    new_js, replaced_js = replace_ids_in_code(js_code)
    assert 'document.getElementById("test_' in new_js
    assert "test" in replaced_js

    # Test with mixed content
    mixed_code = """
    <div id="test">Hello</div>
    <style>#test { color: red; }</style>
    <script>
    document.getElementById("test").style.color = "blue";
    </script>
    """
    new_mixed, replaced_mixed = replace_ids_in_code(mixed_code)
    assert 'id="test_' in new_mixed
    assert "#test_" in new_mixed
    assert 'document.getElementById("test_' in new_mixed
    assert "test" in replaced_mixed

    # Test with custom patterns
    custom_patterns = (r'id="custom_([^"]+)"',)
    custom_code = '<div id="custom_test">Hello</div>'
    new_custom, replaced_custom = replace_ids_in_code(custom_code, custom_patterns)
    assert 'id="custom_test_' in new_custom
    assert "custom_test" in replaced_custom

    # Another test

    js_code = """
    function sendToPython(){
        var data = document.querySelector("#myInput").value;
        var kernel = IPython.notebook.kernel;
        kernel.execute("data_from_js = '" + data + "'");
        kernel.execute("print('Received data from JS: ' + data_from_js)");
    }

    document.querySelector("#myButton").addEventListener("click", function(){
        sendToPython();
    });
    """

    _js_code, _js_replacements = replace_ids_in_code(js_code)

    # Html (with original js_code embedded in it)
    HTML_code = """
    <input type="text" id="myInput" placeholder="Enter some text">
    <button id="myButton">Submit</button>
    <script type="text/Javascript">{}</script>
    """.format(
        js_code
    )

    _html_code, _html_replacements = replace_ids_in_code(HTML_code)

    assert (
        sorted(_js_replacements)
        == sorted(_html_replacements)
        == ["myButton", "myInput"]
    )

    for replacement in _html_replacements.values():
        assert replacement in _html_code
