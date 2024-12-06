

def validate_structure(data, required_structure, data_name="data"):
    """
    Recursively validate the structure and types of a nested dictionary,
    including lists of types and nested dictionaries.

    Parameters:
    - data: dict, the dictionary to validate
    - required_structure: dict, the required structure and types
    - data_name: str, the name of the data (used for error messages)
    """
    for key, subkeys in required_structure.items():
        if key not in data:
            raise ValueError(f"Missing key in {data_name}: {key}")

        if isinstance(subkeys, dict):
            if not isinstance(data[key], (dict, type(None))):
                raise TypeError(
                    f"Incorrect type for {data_name}['{key}']: expected dict or None, got {type(data[key])}")
            if data[key] is not None:
                validate_structure(data[key], subkeys, f"{data_name}['{key}']")
        elif isinstance(subkeys, list):
            if not isinstance(data[key], list):
                raise TypeError(
                    f"Incorrect type for {data_name}['{key}']: expected list, got {type(data[key])}")
            for element in data[key]:
                if isinstance(subkeys[0], dict):
                    validate_structure(
                        element, subkeys[0], f"{data_name}['{key}']")
                else:
                    if not isinstance(element, tuple(subkeys)):
                        raise TypeError(
                            f"Incorrect type for elements in {data_name}['{key}']: expected {subkeys[0]}, got {type(element)}")
        else:
            if not isinstance(data[key], (subkeys, type(None))):
                raise TypeError(
                    f"Incorrect type for {data_name}['{key}']: expected {subkeys} or None, got {type(data[key])}")
