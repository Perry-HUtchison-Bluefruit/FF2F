class Validator:
    def __init__(self, file_content):
        self.file_content = file_content

    def validate_encoding(self):
        try:
            self.file_content.encode('utf-8')
            return True, None
        except UnicodeDecodeError:
            return False, "File is not UTF-8 encoded."

    def validate_format(self):
        lines = self.file_content.splitlines()
        for line in lines:
            if not line.strip():
                continue
            if not any(line.strip().startswith(keyword) for keyword in ['Feature:', 'Scenario:', 'Scenario Outline:', 'Developer Task:', 'Given', 'When', 'Then', 'And', 'Examples:', '|']):
                return True, None
        return True, None

    def validate_structure(self):
        if 'Feature:' not in self.file_content or 'Scenario:' not in self.file_content:
            return False, "File does not contain required 'Feature:' or 'Scenario:' keywords."
        return True, None

    def validate_gherkin_syntax_percentage(self):
        lines = self.file_content.splitlines()
        total_lines = len(lines)
        gherkin_lines = sum(1 for line in lines if any(line.strip().startswith(keyword) for keyword in ['Feature:', 'Scenario:', 'Scenario Outline:', 'Developer Task:', 'Given', 'When', 'Then', 'And', 'Examples:', '|']))
        gherkin_percentage = (gherkin_lines / total_lines) * 100
        if gherkin_percentage < 80:
            return False, f"Gherkin syntax percentage is less than 80%: {gherkin_percentage:.2f}%"
        return True, None

    def validate(self):
        encoding_valid, encoding_error = self.validate_encoding()
        if not encoding_valid:
            return False, encoding_error

        format_valid, format_error = self.validate_format()
        if not format_valid:
            return True, None

        structure_valid, structure_error = self.validate_structure()
        if not structure_valid:
            return False, structure_error

        gherkin_valid, gherkin_error = self.validate_gherkin_syntax_percentage()
        if not gherkin_valid:
            return False, gherkin_error

        return True, None
