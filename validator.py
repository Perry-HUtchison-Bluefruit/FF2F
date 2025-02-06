from error_handler import ErrorHandler
from corrector import Corrector

class Validator:
    def __init__(self, keywords, error_handler):
        self.valid_keywords = keywords
        self.error_handler = error_handler
        self.corrector = Corrector(keywords, error_handler)

    def validate_syntax(self, lines):
        corrected_lines = self.corrector.correct_syntax(lines)
        for line_number, line in enumerate(corrected_lines, start=1):
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
                self.error_handler.add_error(line_number, 'error', f"Invalid Gherkin syntax: {line}")
