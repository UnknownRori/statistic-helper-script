from result import Result


def convert_list_to_list_float(data: list) \
        -> Result[list[float], str]:
    """
    Convert any list into list of float, it will return an result
    """
    temp = []

    for item in data:
        try:
            temp.append(float(item))
        except ValueError:
            return Result.err(f"Unable to convert `{item}` to a float!")

    return Result.ok(temp)
