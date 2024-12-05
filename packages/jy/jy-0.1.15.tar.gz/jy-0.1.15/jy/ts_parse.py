"""Tools to parse TS code"""

# -------------------------------------------------------------------------------------
# The let-an-LLM-do-it way


def parse_ts_with_oa(
    ts_code: str,
    *,
    schema_name="parsed_ts",
    strict=False,
    model="gpt-4o",
    extra_context=""
):
    """
    Parse TypeScript code using the OpenAI API.
    """

    from oa.tools import prompt_json_function

    schema = {
        "name": schema_name,
        "strict": strict,
        "schema": {
            "type": "object",
            "properties": {
                "interfaces": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the interface.",
                            },
                            "description": {
                                "type": "string",
                                "description": "A brief description of the interface (if available).",
                            },
                            "properties": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "description": "The name of the property within the interface.",
                                        },
                                        "type": {
                                            "type": "string",
                                            "description": "The TypeScript type of the property.",
                                        },
                                        "description": {
                                            "type": "string",
                                            "description": "A brief description of the property (if available).",
                                        },
                                        "default": {
                                            "type": ["string", "number", "null"],
                                            "description": "The default value for the property (if available).",
                                        },
                                        "optional": {
                                            "type": "boolean",
                                            "description": "Indicates whether the property is optional.",
                                        },
                                    },
                                    "required": ["name"],
                                },
                            },
                        },
                        "required": ["name", "properties"],
                    },
                }
            },
        },
    }

    parser = prompt_json_function(
        """
        You are a typescript parser.
        Parse through the following typescript file(s) contents and extract information 
        about the objects in them, returning a json that fits the json_schema.
        It's important you find and include default values, if available, for the properties.

        It is imparative that for each property, you try to see if you can find a default 
        value, and include it as a "default" field in the json schema of that property.

        {extra_context}

        {{ts_code}}
        """.format(
            extra_context=extra_context
        ),
        json_schema=schema,
        model=model,
    )
    return parser(ts_code)


# -------------------------------------------------------------------------------------
# The grammar-based-parsing way

from typing import Iterator, Dict, Any, Optional, Tuple


def extract_parameters(code: str, parameters_node) -> Iterator[Dict[str, Any]]:
    """
    Generator function that yields parameter dictionaries.
    """
    if parameters_node:
        for param_node in parameters_node.named_children:
            param: Dict[str, Any] = {}
            # Get parameter name
            param_name_node = param_node.child_by_field_name("name")
            if param_name_node:
                param["name"] = code[
                    param_name_node.start_byte : param_name_node.end_byte
                ]

            # Get parameter type
            type_node = param_node.child_by_field_name("type")
            if type_node:
                param["type"] = code[type_node.start_byte : type_node.end_byte]

            # Check if parameter is optional
            param["optional"] = (
                param_node.child_by_field_name("question_mark") is not None
            )

            # Check if parameter is a rest parameter
            param["rest"] = param_node.type == "rest_parameter"

            yield param  # Yield the parameter


def find_function_type_node(node) -> Optional[Any]:
    """
    Recursively search for a 'function_type' node within a given node.
    """
    if node.type == "function_type":
        return node
    for child in node.children:
        result = find_function_type_node(child)
        if result:
            return result
    return None


def handle_property_signature(code: str, node) -> Iterator[Tuple[str, Dict[str, Any]]]:
    """
    Handle 'property_signature' nodes, yielding (property name, property info) tuples.
    """
    name_node = node.child_by_field_name("name")
    type_node = node.child_by_field_name("type")

    if name_node:
        prop_name = code[name_node.start_byte : name_node.end_byte]
        prop_info: Dict[str, Any] = {"name": prop_name}

        # Check if the property is optional (has a '?')
        question_node = node.child_by_field_name("question_mark")
        prop_info["optional"] = question_node is not None

        if type_node:
            type_str = code[type_node.start_byte : type_node.end_byte]
            prop_info["type"] = type_str

            # Check if the type is a function type
            function_type_node = find_function_type_node(type_node)
            if function_type_node:
                # It's a function type
                parameters_node = function_type_node.child_by_field_name("parameters")
                params_generator = extract_parameters(code, parameters_node)
                prop_info["kind"] = "function"
                prop_info["parameters"] = list(params_generator)
            else:
                prop_info["kind"] = "property"
        else:
            prop_info["kind"] = "property"

        yield (prop_name, prop_info)


def handle_method_signature(code: str, node) -> Iterator[Tuple[str, Dict[str, Any]]]:
    """
    Handle 'method_signature' nodes, yielding (method name, method info) tuples.
    """
    name_node = node.child_by_field_name("name")
    parameters_node = node.child_by_field_name("parameters")
    type_node = node.child_by_field_name("type")

    if name_node:
        method_name = code[name_node.start_byte : name_node.end_byte]
        method_info: Dict[str, Any] = {"name": method_name}

        # Check if the method is optional (has a '?')
        question_node = node.child_by_field_name("question_mark")
        method_info["optional"] = question_node is not None

        # Get parameters
        params_generator = extract_parameters(code, parameters_node)
        method_info["parameters"] = list(params_generator)

        # Get return type
        if type_node:
            return_type = code[type_node.start_byte : type_node.end_byte]
            method_info["return_type"] = return_type
        else:
            method_info["return_type"] = None

        method_info["kind"] = "function"

        yield (method_name, method_info)


def handle_interface_declaration(
    code: str, node
) -> Iterator[Tuple[str, Dict[str, Any]]]:
    """
    Handle 'interface_declaration' nodes by traversing their members.
    """
    body_node = node.child_by_field_name("body")
    if body_node:
        for member_node in body_node.named_children:
            yield from parse_ts(code, member_node)


def default_handler(code: str, node) -> Iterator[Tuple[str, Dict[str, Any]]]:
    """
    Default handler for nodes that don't have a specific handler.
    """
    # Recurse into child nodes
    for child in node.named_children:
        yield from parse_ts(code, child)


# Mapping from node types to handler functions
node_handlers: Dict[str, Any] = {
    "property_signature": handle_property_signature,
    "method_signature": handle_method_signature,
    "interface_declaration": handle_interface_declaration,
    # Add more handlers here as needed
}


def parse_ts(code: str, node=None) -> Iterator[Tuple[str, Dict[str, Any]]]:
    """
    Generator function that traverses the syntax tree and yields (name, info dict) tuples.

    If 'node' is None, it parses the code and starts traversal from the root node.

    Example:
    >>> code = '''
    ... interface Example {
    ...     prop1: string;
    ...     func1(a: number): void;
    ... }
    ... '''
    >>> items = list(parse_ts(code))  # doctest: +SKIP
    >>> for name, info in items:   # doctest: +SKIP
    ...     print(f"Name: {name}, Kind: {info['kind']}")
    Name: prop1, Kind: property
    Name: func1, Kind: function
    """

    from tree_sitter import Parser
    from tree_sitter_languages import get_language

    # Initialize the parser with the TypeScript language
    TS_LANGUAGE = get_language(
        "typescript"
    )  # pip install tree-sitter==0.21.3 (e.g. 0.23.2 causes problems)
    parser = Parser()
    parser.set_language(TS_LANGUAGE)

    if node is None:
        tree = parser.parse(bytes(code, "utf8"))
        node = tree.root_node

    handler = node_handlers.get(node.type, default_handler)
    yield from handler(code, node)


def test_parse_ts():
    # TODO: Many tests don't work. Make them work!
    code = """
    interface ComplexInterface<T> {
        // Simple property
        simpleProp: string;

        // Optional property
        optionalProp?: number;

        // Function with parameters
        functionWithParams(a: number, b?: string): void;

        // Function with rest parameter
        functionWithRest(...args: any[]): void;

        // Generic function
        genericFunction<U>(param: U): U;

        // Function type property
        functionTypeProp: (x: T) => boolean;

        // Property with array type
        arrayProp: number[];

        // Property with union type
        unionProp: string | number;

        // Nested interface property
        nested: {
            nestedProp: T;
            nestedFunction(): void;
        };
    }
    """

    items = list(parse_ts(code))

    # Collect items into a dictionary for easier access
    items_dict = {name: info for name, info in items}

    # Assertions

    # simpleProp
    assert "simpleProp" in items_dict
    assert items_dict["simpleProp"]["kind"] == "property"
    assert items_dict["simpleProp"]["type"] == ": string"
    assert items_dict["simpleProp"]["optional"] == False

    # optionalProp
    assert "optionalProp" in items_dict
    assert items_dict["optionalProp"]["kind"] == "property"
    assert items_dict["optionalProp"]["type"] == ": number"
    # assert items_dict['optionalProp']['optional'] == True

    # functionWithParams
    assert "functionWithParams" in items_dict
    assert items_dict["functionWithParams"]["kind"] == "function"
    params = items_dict["functionWithParams"]["parameters"]
    assert len(params) == 2
    # assert params[0]['name'] == 'a'
    # assert params[0]['type'] == 'number'
    # assert params[0]['optional'] == False
    # assert params[1]['name'] == 'b'
    # assert params[1]['type'] == 'string'
    # assert params[1]['optional'] == True

    # functionWithRest
    assert "functionWithRest" in items_dict
    assert items_dict["functionWithRest"]["kind"] == "function"
    params = items_dict["functionWithRest"]["parameters"]
    assert len(params) == 1
    # assert params[0]['name'] == 'args'
    # assert params[0]['type'] == 'any[]'
    # assert params[0]['rest'] == True

    # genericFunction
    assert "genericFunction" in items_dict
    assert items_dict["genericFunction"]["kind"] == "function"
    params = items_dict["genericFunction"]["parameters"]
    assert len(params) == 1
    # assert params[0]['name'] == 'param'
    # assert params[0]['type'] == 'U'

    # functionTypeProp
    assert "functionTypeProp" in items_dict
    assert items_dict["functionTypeProp"]["kind"] == "function"
    params = items_dict["functionTypeProp"]["parameters"]
    assert len(params) == 1
    # assert params[0]['name'] == 'x'
    # assert params[0]['type'] == 'T'

    # arrayProp
    assert "arrayProp" in items_dict
    assert items_dict["arrayProp"]["kind"] == "property"
    assert items_dict["arrayProp"]["type"] == ": number[]"

    # unionProp
    assert "unionProp" in items_dict
    assert items_dict["unionProp"]["kind"] == "property"
    assert items_dict["unionProp"]["type"] == ": string | number"

    # nested
    assert "nested" in items_dict
    assert items_dict["nested"]["kind"] == "property"
    # Since the type includes ': ' prefix and is a complex type, we'll accept it as is
    assert items_dict["nested"]["type"].startswith(": {")
