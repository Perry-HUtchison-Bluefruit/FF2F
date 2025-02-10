import difflib
from validator import Validator
from error_handler import ErrorHandler
from corrector import Corrector

class Parser:
    def __init__(self, keywords, error_handler):
        self.validator = Validator(keywords, error_handler)
        self.error_handler = error_handler
        self.corrector = Corrector(keywords, error_handler)

    def parse_feature_file(self, file_content):
        lines = file_content.splitlines()

        self.validator.validate_syntax(lines)
        features = self.extract_features(lines)

        return features

    def extract_features(self, data):
        features = []
        current_feature = None
        current_scenario = None
        for line_number, line in enumerate(data, start=1):
            line = line.lstrip()
            line = line.rstrip()
            if line.startswith('Feature:'):
                current_feature = line[len('Feature:'):].strip()
                current_scenario = None
            elif (line.startswith('Scenario:') or
                  line.startswith('Scenario Outline:') or
                  line.startswith('Developer Task:')):
                current_scenario = line.strip()
                features = self.process_feature_line(features, current_feature, current_scenario, line)
                if line.startswith('Scenario Outline:'):
                    self.check_scenario_outline(data, line_number)
            elif any(line.startswith(keyword) for keyword in ['Given', 'When', 'Then', 'And', 'Examples', '|']):
                features = self.process_scenario_line(features, current_feature, current_scenario, line)
            elif line:
                corrected_line = self.corrector.handle_invalid_syntax(line_number, line)
                if corrected_line != line:
                    # If the line was corrected, reprocess it as a new line
                    if corrected_line.startswith('Scenario:') or corrected_line.startswith('Scenario Outline:') or corrected_line.startswith('Developer Task:'):
                        current_scenario = corrected_line.strip()
                        features = self.process_feature_line(features, current_feature, current_scenario, corrected_line)
                        if corrected_line.startswith('Scenario Outline:'):
                            self.check_scenario_outline(data, line_number)
                    else:
                        data[line_number - 1] = corrected_line
                        if current_feature and current_scenario:
                            features.append([current_feature, current_scenario, corrected_line])
                else:
                    data[line_number - 1] = corrected_line
                    if current_feature and current_scenario:
                        features.append([current_feature, current_scenario, corrected_line])
        return features

    def process_feature_line(self, features, current_feature, current_scenario, line):
        if current_feature and not any(f[0] == current_feature for f in features):
            features.append([current_feature, '', ''])
        if current_feature and current_scenario:
            features.append([current_feature, current_scenario, ''])
        return features

    def process_scenario_line(self, features, current_feature, current_scenario, line):
        if current_feature and current_scenario:
            features.append([current_feature, current_scenario, line])
        return features

    def check_scenario_outline(self, data, line_number):
        examples_found = False
        example_lines = 0
        invalid_scenario_outlines = []
        for line in data[line_number:]:
            if line.startswith('Examples:'):
                examples_found = True
            elif examples_found and line.startswith('|'):
                example_lines += 1
            elif examples_found and not line.startswith('|'):
                break

        if not examples_found or example_lines < 3:
            invalid_scenario_outlines.append(line_number)

        if invalid_scenario_outlines:
            for invalid_line in invalid_scenario_outlines:
                self.error_handler.add_error(invalid_line, 'error', "'Scenario Outline:' is not followed by 'Examples:' and at least three lines starting with '|'")
