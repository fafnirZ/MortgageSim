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
                    f"expected Types in the provided tuple\ninstead got: {expected_types}\n"
                    "make sure you actually provided types in the assert_type fn call."
                )

    if not isinstance(input, expected_types):
        raise TypeError(
            "Type Assertion failed:\n",
            f"Expected: {expected_types}\n",
            f"Instead got: {type(input)}",
        )
