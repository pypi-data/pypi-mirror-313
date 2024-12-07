class Sanitizer:
    @classmethod
    def sanitize_lines(cls, text: list[str]):
        return [cls.santize_str(line) for line in text if line]

    @classmethod
    def santize_str(cls, line: str):
        return line.lstrip()
