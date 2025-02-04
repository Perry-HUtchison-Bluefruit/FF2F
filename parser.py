import difflib
from corrector import Corrector

class Parser:
    def __init__(self):
        self.corrector = Corrector()

    def parse_feature_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        corrected_lines = self.corrector.correct_syntax(lines)
        features = self.extract_features(corrected_lines)

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
                if corrected_line:
                    data[line_number - 1] = corrected_line
                    return self.extract_features(data)
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
        for line in data[line_number:]:
            if line.startswith('Examples:'):
                examples_found = True
            elif examples_found and line.startswith('|'):
                example_lines += 1
            elif examples_found and not line.startswith('|'):
                break

        if not examples_found or example_lines < 3:
            print(f"Error: 'Scenario Outline:' at line {line_number} is not followed by 'Examples:' and at least three lines starting with '|'")
            exit(1)
