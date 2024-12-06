"""String utilities."""

# Python Modules

# 3rd Party Modules

# Project Modules


def camel_to_snake_case(s: str) -> str:
    """Convert the string from CamelCase to snake_case.

    This method uses a simple regular expression to convert a string
    in CamelCase to one in snake_case. Strings with 2 or fewer
    are simply lowercased and returned.

    Parameters
    ----------
    s : str
        The string to convert.

    Returns
    -------
    str
        The string in snake case.
    """
    # There are a number of approaches for converting CamelCase to snake_case
    # enumerated at
    # https://www.geeksforgeeks.org/python-program-to-convert-camel-case-string-to-snake-case/
    # However, the only one that passes all my unit tests is method #4 (regex).
    # The "naive" approach below also passes all the unit tests, is also
    # faster than any of the other listed methods (while #4 is the slowest).
    # See this post for some additional regex approaches:
    # https://stackoverflow.com/a/1176023
    if not s:
        return s

    if len(s) <= 2:
        return s.lower()

    # What will be the previous and next character
    p, c = s[0], s[1]

    # The array to store the result in.
    snake = [p]

    # The iterated variable represents the next character
    for n in s[2:]:
        # If the current character is uppercase and the next character
        # is not, then we'll start a new "word"
        if p.isalpha() and c.isupper() and not n.isupper():
            snake.append("_")

        snake.append(c)

        # Update the previous and next characters
        p, c = c, n

    snake.append(c)

    return "".join(snake).lower()
