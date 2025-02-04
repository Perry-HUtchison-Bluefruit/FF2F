import difflib

class Corrector:
    def __init__(self):
        self.valid_keywords = ['Feature:', 'Scenario:', 'Scenario Outline:', 'Given', 'When', 'Then', 'And', 'Examples', '|']

    def correct_syntax(self, lines):
        corrected_lines = []
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                corrected_lines.append(line)
                continue
            keyword = line_stripped.split()[0]
            if keyword not in self.valid_keywords:
                closest_matches = difflib.get_close_matches(keyword, self.valid_keywords, n=1, cutoff=0.8)
                if closest_matches:
                    corrected_line = closest_matches[0] + line_stripped[len(keyword):]
                    corrected_lines.append(corrected_line)
            else:
                corrected_lines.append(line)
        return corrected_lines

    def handle_invalid_syntax(self, line_number, line):
        print(f"Invalid Gherkin syntax at line {line_number}: {line}")
        return self.correct_syntax([line])[0]
