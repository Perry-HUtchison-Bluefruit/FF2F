import difflib

class Corrector:
    def __init__(self, keywords, error_handler):
        self.valid_keywords = keywords
        self.error_handler = error_handler

    def correct_syntax(self, lines):
        corrected_lines = []
        for line_number, line in enumerate(lines, start=1):
            line_stripped = line.strip()
            if not line_stripped:
                corrected_lines.append(line)
                continue

            # Check for multi-word keywords
            keyword = None
            for valid_keyword in self.valid_keywords:
                if line_stripped.startswith(valid_keyword):
                    keyword = valid_keyword
                    break

            if keyword is None:
                words = line_stripped.split()
                if len(words) > 1:
                    first_word, second_word = words[0], words[1]
                else:
                    first_word, second_word = words[0], ''

                # If no valid keyword is found, attempt to correct the first two words first and remove the rest of the line
                closest_matches = difflib.get_close_matches(first_word + ' ' + second_word, self.valid_keywords, n=1, cutoff=0.8)
                if closest_matches:
                    corrected_line = closest_matches[0] + line_stripped[len(first_word + ' ' + second_word):]
                    corrected_lines.append(corrected_line)
                else:
                    # If no valid keyword is found, attempt to correct the first word
                    closest_matches = difflib.get_close_matches(first_word, self.valid_keywords, n=1, cutoff=0.8)
                    if closest_matches:
                        corrected_line = closest_matches[0] + line_stripped[len(first_word):]
                        corrected_lines.append(corrected_line)
                    else:
                        corrected_lines.append(line)
            else:
                corrected_lines.append(line)
        return corrected_lines

    def handle_invalid_syntax(self, line_number, line):
        self.error_handler.add_error(line_number, 'warning', f"Invalid Gherkin syntax: {line}")
        corrected_line = self.correct_syntax([line])[0]
        if corrected_line != line:
            self.error_handler.add_error(line_number, 'update', f"Corrected Gherkin syntax: {corrected_line}")
        return corrected_line
