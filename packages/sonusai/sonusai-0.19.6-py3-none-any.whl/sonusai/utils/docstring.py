def trim_docstring(docstring: str) -> str:
    """Trim whitespace from docstring"""
    from sys import maxsize

    if not docstring:
        return ""

    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()

    # Determine minimum indentation (first line doesn't count)
    indent = maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))

    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())

    # Strip off leading blank lines:
    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    # Return a single string
    return "\n".join(trimmed)


def add_commands_to_docstring(docstring: str, plugin_docstrings: list[str]) -> str:
    """Add commands to docstring"""
    import sonusai

    lines = docstring.splitlines()

    start = lines.index("The sonusai commands are:")
    end = lines.index("", start)

    commands = sonusai.commands_doc.splitlines()
    for plugin_docstring in plugin_docstrings:
        commands.extend(plugin_docstring.splitlines())
    commands.sort()
    commands = list(filter(None, commands))

    lines = lines[: start + 1] + commands + lines[end:]

    return "\n".join(lines)
