"""Module contains function that satisfies provided tests."""


def new_format(string):
    """
    Format numeric string by inserting dots every three digits from the right.
    E.g. "1000000" -> "1.000.000"
    """
    return f"{int(string):,}".replace(",", ".")


assert new_format("1000000") == "1.000.000"
assert new_format("100") == "100"
assert new_format("1000") == "1.000"
assert new_format("100000") == "100.000"
assert new_format("10000") == "10.000"
assert new_format("0") == "0"
