# Enhanced caching for improved performance on repetitive parsing tasks
import ast


def kwarg_as_dict(kwarg_str: str) -> dict:
    """
    Parses a string representation of a keyword argument into a dictionary with the value
    appropriately typed.

    Args:
        kwarg_str: A string representing a keyword argument, e.g., "change_prop='True'".

    Returns:
        A dictionary with the keyword as the key and the evaluated Python literal as the value.

    Raises:
        ValueError: If the input string cannot be parsed into a valid keyword argument.
    """
    # Attempt to split the input string into a key and value part
    try:
        key, value_str = kwarg_str.split('=', 1)
        key = key.strip()
        # Using ast.literal_eval to safely evaluate the value string to a Python literal
        value = ast.literal_eval(value_str.strip())
    except ValueError as e:
        raise ValueError(f"Invalid kwarg string '{kwarg_str}': {e}")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in value for '{kwarg_str}': {e}")

    return {key: value}

def pascal_to_snake(s):
    """
    Convert a PascalCase string to snake_case.

    :param s: String in PascalCase format
    :return: String converted to snake_case format
    """
    if not s:
        return ""

    snake_case = [s[0].lower()]
    for char in s[1:]:
        if char.isupper():
            snake_case.append('_')
            snake_case.append(char.lower())
        else:
            snake_case.append(char)

    return ''.join(snake_case)