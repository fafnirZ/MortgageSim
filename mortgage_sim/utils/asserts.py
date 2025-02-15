def assert_type(input: any, expected_types: type | tuple[type, ...]) -> None:
    """essentially is instance check wrapper."""

    if not isinstance(expected_types, (type, tuple)):
        raise ValueError(
            "expected_types expected type or tuple[types,...]",
            f"instead got {type(expected_types)}",
        )

    if type(expected_types) is tuple:
        for val in expected_types:
            if not isinstance(val, type):
                raise ValueError(
                    f"expected Types in the provided tupleinstead got: {expected_types}"
                )

    if not isinstance(input, expected_types):
        raise TypeError(
            f"Type Assertion failed:Expected: {expected_types}\n",
            "Instead got: {type(input)}",
        )
