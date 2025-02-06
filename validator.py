from error_handler import ErrorHandler

class Validator:
    def __init__(self, keywords, error_handler):
        self.valid_keywords = keywords
        self.error_handler = error_handler

    def validate_syntax(self, lines):
        for line_number, line in enumerate(lines, start=1):
            line_stripped = line.strip()
            if not line_stripped:
                continue

            if not any(line_stripped.startswith(valid_keyword) for valid_keyword in self.valid_keywords):
                self.error_handler.add_error(line_number, 'error', f"Invalid Gherkin syntax: {line}")
