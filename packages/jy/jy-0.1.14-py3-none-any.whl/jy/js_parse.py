"""Utils to parse JS"""

import os
from pathlib import Path
from functools import wraps
from itertools import chain
from typing import Optional
import json

import esprima

AstScript = esprima.nodes.Script
AstNode = esprima.nodes.Node


# TODO: Parse out js docs and add them to py mirror function


class UnknownNodeType(ValueError):
    """To be raised when an AST node type wasn't handled by a function"""

    def __init__(self, node_type, context=""):
        super().__init__(f"Unknown type {context}: {node_type}")


def if_none_output_raise_unknown_type(context=""):
    def _if_none_output_raise_wrapper(func):
        @wraps(func)
        def _func(*args, **kwargs):
            output = func(*args, **kwargs)
            if output is None:
                # Note we only extract from args, if in kwargs won't work
                # For that reason, we should enforce the node to be the first,
                # positional only, argument in func
                node, *_ = args
                raise UnknownNodeType(node.type, context)
            else:
                return output

        return _func

    return _if_none_output_raise_wrapper


def parse_js_code(js_code: str, encoding: Optional[str] = None) -> AstScript:
    if os.path.isfile(js_code):
        js_code = Path(js_code).read_text(encoding=encoding)
    return esprima.parse(js_code)


def extract_function_def_parts(func_def_code: str) -> str:
    """Extract the body of a function definition from its code"""
    body_tree = parse_js_code(func_def_code).body[0].body

    # Find the position of the first opening brace
    start = func_def_code.find("{", body_tree.start)
    # Find the position of the last closing brace
    end = func_def_code.rfind("}", body_tree.start, body_tree.end)

    return (
        func_def_code[:start],
        func_def_code[start + 1 : end],
        func_def_code[end + 1 :],
    )


def append_to_func_body(func_def_code: str, code_to_append: str) -> str:
    """Append code to the body of a function definition"""
    pre, body, post = extract_function_def_parts(func_def_code)
    return pre + "{" + body + code_to_append + "}" + post


@if_none_output_raise_unknown_type("to extract obj name from")
def _extract_obj_name(x: AstNode, /):
    if x.type == "Identifier":
        return x.name
    elif x.type == "MemberExpression":
        object_name = _extract_obj_name(x.object)
        property_name = _extract_obj_name(x.property)
        return f"{object_name}.{property_name}"


@if_none_output_raise_unknown_type("to extract params from")
def _extract_params(x: AstNode, /):
    if x.type == "Identifier":
        return dict(name=x.name)
    elif x.type == "AssignmentPattern":
        return dict(name=x.left.name, default=x.right.value)


def extract_js_func_params(params_list):
    return map(_extract_params, params_list)


def _extract_params_from_function_expression(x):
    return extract_js_func_params(x.params)


def extract_func_name_and_params(ast_node: AstNode):
    """Extract one or several function ``(name, params)`` pair(s) from an AST node"""
    x = ast_node
    if x.type == "FunctionDeclaration":
        yield x.id.name, list(extract_js_func_params(x.params))
    elif x.type == "AssignmentExpression":
        yield (
            _extract_obj_name(x.left),
            list(extract_js_func_params(x.right.params)),
        )
    elif x.type == "VariableDeclarator":
        yield x.id.name, list(extract_js_func_params(x.init.params))
    elif x.type == "VariableDeclaration":
        # Here we may have several declarations, so we use yield from
        yield from chain.from_iterable(
            map(extract_func_name_and_params, x.declarations)
        )
    elif x.type == "ExpressionStatement":
        yield from extract_func_name_and_params(x.expression)


def func_name_and_params_pairs(js_code: str, *, encoding=None):
    """
    Get ``(name, params)`` pairs of function definitions extracted from ``js_code``.

    >>> js_code = '''
    ... function foo(a, b="hello", c= 3) {
    ...     return a + b.length * c
    ... }
    ... const bar = (y, z = 1) => y * z
    ... func.assigned.to.nested.prop = function (x) {
    ...     return x + 3
    ... }'''
    >>> assert list(func_name_and_params_pairs(js_code)) == [
    ...     ('foo', [
    ...         {'name': 'a'},
    ...         {'name': 'b', 'default': 'hello'},
    ...         {'name': 'c', 'default': 3}
    ...     ]),
    ...     ('bar', [
    ...         {'name': 'y'},
    ...         {'name': 'z', 'default': 1}
    ...     ]),
    ...     ('func.assigned.to.nested.prop', [
    ...         {'name': 'x'}
    ...     ])
    ... ]

    """
    ast_script = parse_js_code(js_code, encoding=encoding)
    for ast_node in ast_script.body:
        # TODO: Check for type of ast_node before calling extract_func_name_and_params
        #  For now, just ignoring errors:
        try:
            yield from extract_func_name_and_params(ast_node)
        except Exception as e:
            print(f"Exception while parsing {ast_node}: {e}")


def dflt_py_to_js_value_trans(x):
    if isinstance(x, bool):
        return str(x).lower()
    elif isinstance(x, str):
        return f'"{x}"'  # surround with quotes
    elif isinstance(x, dict):
        return json.dumps(x)
    return x


import re
import uuid
from typing import Tuple

_dflt_patterns_for_html_ids = (
    r'id="([^"]+)"',  # HTML id attributes
    r"#([a-zA-Z][\w\-]*)",  # CSS IDs
    r'document\.getElementById\("([^"]+)"\)',  # JS getElementById
)


def replace_ids_in_code(
    code: str, patterns: Tuple[str] = _dflt_patterns_for_html_ids
) -> (str, dict):
    """
    Replaces IDs in a mixed HTML, CSS, and JS string with unique versions.

    Args:
    - code (str): The input code containing HTML, CSS, and/or JS.
    - patterns (tuple): A tuple of regex patterns to match IDs.

    Returns:
    - tuple: A tuple containing the modified code and a dictionary of old-to-new ID mappings.

    This function is useful to make id-unique copies of HTML/JS components that have IDs.
    This need was noticed and discussed in: https://github.com/i2mint/jy/discussions/3#discussioncomment-6862843

    """
    # Patterns to match IDs
    patterns = [
        r'id="([^"]+)"',  # HTML id attributes
        r"#([a-zA-Z][\w\-]*)",  # CSS IDs
        r'document\.getElementById\("([^"]+)"\)',  # JS getElementById
    ]

    replaced = {}

    # Generate a unique ID
    def unique_id(match):
        old_id = match.group(1)
        new_id = old_id + "_" + str(uuid.uuid4()).replace("-", "")[:8]
        replaced[old_id] = new_id
        return match.group(0).replace(old_id, new_id)

    # Replace all IDs in the code
    for pattern in patterns:
        code = re.sub(pattern, unique_id, code)

    return code, replaced
