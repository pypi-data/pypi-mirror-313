def convert_string_to_number(string: str) -> float | int | str:
    try:
        result = float(string)
        return int(result) if result == int(result) else result
    except ValueError:
        return string
