from error_handler import ErrorHandler

class Validator:
    def __init__(self, keywords, error_handler):
        self.valid_keywords = keywords
        self.error_handler = error_handler

    def validate_syntax(self, lines):
        for line_number, line in enumerate(lines, start=1):
            print(f"Validating line {line_number}: {line.strip()}")  # Debug statement
            line_stripped = line.strip()
            if not line_stripped:
                continue

            # Check for multi-word keywords
            keyword = None
            for valid_keyword in self.valid_keywords:
                if line_stripped.startswith(valid_keyword):
                    keyword = valid_keyword
                    break

            if keyword is None:
                # If no valid keyword is found, report an error
                print(f"Invalid Gherkin syntax found at line {line_number}: {line}")  # Debug statement
                self.error_handler.add_error(line_number, 'error', f"Invalid Gherkin syntax: {line}")
