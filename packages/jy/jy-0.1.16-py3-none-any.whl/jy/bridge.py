"""Python portals to JS"""

from typing import Any, Optional
from functools import partial

from dol.signatures import Sig

from jy.js_parse import dflt_py_to_js_value_trans, func_name_and_params_pairs


# TODO: Add value transformer (routing). For example, booleans, True->true
def _js_func_call(
    *args,
    __sig,
    __func_call_template,
    __value_trans=dflt_py_to_js_value_trans,
    __apply_defaults=True,
    **kwargs,
):
    _kwargs = __sig.map_arguments(args, kwargs, apply_defaults=__apply_defaults)
    inputs = map(__value_trans, _kwargs.values())
    inputs = ", ".join(map(str, inputs))
    return __func_call_template.format(inputs=inputs)


# TODO: value_trans only sees value. Might want to transform according to other
#  contextural information, like the parameter name, or the function name, etc.
def mk_py_binder_func(
    name,
    params,
    *,
    prefix="",
    suffix="",
    doc="",
    value_trans=dflt_py_to_js_value_trans,
    apply_defaults=True,
):
    *_, func_name = name.split(".")  # e.g. object.containing.func --> func
    func_call_template = prefix + name + "({inputs})" + suffix

    sig = Sig.from_params(params)
    js_func_call = partial(
        _js_func_call,
        __sig=sig,
        __func_call_template=func_call_template,
        __value_trans=value_trans,
        __apply_defaults=apply_defaults,
    )
    js_func_call = sig(js_func_call)
    js_func_call.__name__ = func_name
    js_func_call.__doc__ = doc

    return js_func_call


class JsBridge:
    """
    The default class to make instances that will contain methods that mirror JS
    function calls
    """


def add_js_funcs(
    js_code: str,
    *,
    obj: Any = None,
    name: Optional[str] = None,
    encoding: Optional[str] = None,
    forbidden_method_names=(),
    apply_defaults=True,
    value_trans=dflt_py_to_js_value_trans,
):
    '''
    Add js call functions as attributes to an object.

    If object is not given, ``add_js_funcs`` will use a new ``JsBridge`` instance.

    >>> js_code = """
    ... function foo(a, b="hello", c= 3) {
    ...     return a + b.length * c
    ... }
    ... const bar = (y, z = 1) => y * z
    ... func.assigned.to.nested.prop = function (x) {
    ...     return x + 3
    ... }
    ... """
    >>> js = add_js_funcs(js_code)
    >>> from inspect import signature
    >>> list(vars(js))
    ['foo', 'bar', 'prop']
    >>> signature(js.foo)
    <Sig (a, b='hello', c=3)>
    >>> js.foo(1, 'hi')
    'foo(1, "hi", 3)'
    >>> js.prop('up')
    'func.assigned.to.nested.prop("up")'
    '''

    if obj is None:
        obj = JsBridge()

    forbidden_method_names = set(forbidden_method_names)

    for full_func_ref, params in func_name_and_params_pairs(js_code, encoding=encoding):
        *_, func_name = full_func_ref.split(".")  # e.g. object.containing.func --> func
        # TODO: Could specify a recovery function that finds another name instead of
        #  raising an error
        if func_name in forbidden_method_names:
            raise ValueError(
                f"This func name was already used, or mentioned in "
                f"the forbidden_method_names argument: {func_name}"
            )
        setattr(
            obj,
            func_name,
            mk_py_binder_func(
                full_func_ref,
                params,
                value_trans=value_trans,
                apply_defaults=apply_defaults,
            ),
        )

    if name:
        obj.__name__ = name

    return obj
