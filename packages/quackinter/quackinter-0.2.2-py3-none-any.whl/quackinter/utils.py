def extract_cmd(string: str) -> tuple[str, str]:
    if not string:
        raise ValueError("When extracting the command, the string was empty.")
    separate = string.split(" ", 1)
    return (separate[0].upper(), separate[1] if len(separate) == 2 else "")
