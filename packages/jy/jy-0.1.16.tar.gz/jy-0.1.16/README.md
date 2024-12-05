# jy

Tools to control JS from Python.

(``jy`` stands for "Js pY" or "Js python proxY".)

To install:	```pip install jy```

[Documentation](https://i2mint.github.io/jy/)


# Example

Say you have the ``test01.js``
(whose contents are displayed in the next subsection).

    from jy import add_js_funcs
    js = add_js_funcs("./test01.js")

js has two methods called bar and foo

    assert sorted([x for x in dir(js) if not x.startswith('_')]) == [
        'add_one', 'bar', 'foo', 'obj', 'prop', 'with_arrow_func', 'with_let'
    ]

They mirror the signatures of the underlying JS functions

    from inspect import signature
    assert str(signature(js.foo)) == "(a, b='hello', c=3)"
    assert str(signature(js.bar)) == "(green, eggs='food', and=True, ham=4)"

Calling this function returns a string
(the code to call the underlying JS function)

    assert js.foo(1, 'hi', 5) == 'foo(1, "hi", 5)'

Notice that you can use positional or keyword arguments
Also, notice that though "prop" is the name of `js`'s attribute,
the function call string does indeed use the original full reference:
``func.assigned.to.nested.prop``

    assert js.prop('up') == (
        'func.assigned.to.nested.prop("up")'
    )

Notice that the python (signature) defaults are applied before translating to JS

    assert js.bar(42) == 'bar(42, "food", true, 4)'
    alt_js = add_js_funcs(test01_js_code, apply_defaults=False)

You can opt not to do this by specifying `apply_defaults=False`
This will result in only injecting those inputs you specify in the js call string,
which will have the effect of letting JS apply its defaults, what ever they are

    alt_js = add_js_funcs(test01_js_code, apply_defaults=False)
    assert alt_js.bar(42) == 'bar(42)'


# Appendix

## The ``test01.js`` file's contents

```javascript
// "test01.js" file
// Straight function definition
function foo(a, b="hello", c= 3) {
    return a + b.length * c
}

// Straight function definition
function bar(green, eggs = 'food', and= true, ham= 4) {
    if (and) return eggs.length * ham
}

// global callable variable
add_one = function (x) {
    return x + 1
}

// does the presence of a let break the parser?
let with_let = function (x) {
    return x + 2
}

// with arrow func
// (also testing if const breaks the parse)
const with_arrow_func = (y, z= 1) => y * z

// function assigned to a nested property
func.assigned.to.nested.prop = function (x) {
    return x + 3
}

// function nested in some other function, assigned to a variable
var obj = (function (exports) {
    function bar(name) {
        return name + "__"
    }
})

```
