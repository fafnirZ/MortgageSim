
def assert_type(input: any, expected_types: type | tuple[type,...]) -> None:
    """essentially is instance check wrapper."""
    
    if not isinstance(expected_types, (type, tuple)):
        raise ValueError("expected_types expected type or tuple[types,...]",
                         f"instead got {type(expected_types)}")

    if type(expected_types) is tuple:
        _expected = list(lambda x: type(x), expected_types)
        for val in expected_types:
            if not isinstance(val, type):
                raise ValueError("expected Types in the provided tuple"
                                 f"instead got: {_expected}")

    if not isinstance(input, expected_types):
        _expected = expected_types
        if isinstance(_expected, tuple):
            _expected = list(lambda x: type(x), expected_types)
        raise TypeError(
            "Type Assertion failed:"
            f"Expected: {_expected}\n"
            f"Instead got: {type(input)}"
        )
