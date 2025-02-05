import difflib
from corrector import Corrector

class Parser:
    def __init__(self, keywords):
        self.corrector = Corrector(keywords)
        self.keywords = keywords

    def parse_feature_file(self, file_content):
        lines = file_content.splitlines()

        corrected_lines = self.corrector.correct_syntax(lines)
        features = self.extract_features(corrected_lines)

        return features

    def extract_features(self, data):
        features = []
        current_feature = None
        current_scenario = None
        state = 'initial'
        example_lines = 0
        examples_found = False

        for line_number, line in enumerate(data, start=1):
            line = line.lstrip()
            line = line.rstrip()

            if state == 'initial':
                if line.startswith('Feature:'):
                    current_feature = line[len('Feature:'):].strip()
                    current_scenario = None
                    state = 'feature'
                elif line.startswith('Scenario:') or line.startswith('Scenario Outline:') or line.startswith('Developer Task:'):
                    current_scenario = line.strip()
                    features = self.process_feature_line(features, current_feature, current_scenario, line)
                    if line.startswith('Scenario Outline:'):
                        state = 'scenario_outline'
                        examples_found = False
                        example_lines = 0
                    else:
                        state = 'scenario'
                elif any(line.startswith(keyword) for keyword in self.keywords):
                    features = self.process_scenario_line(features, current_feature, current_scenario, line)
                elif line:
                    corrected_line = self.corrector.handle_invalid_syntax(line_number, line)
                    if corrected_line:
                        data[line_number - 1] = corrected_line

            elif state == 'feature':
                if line.startswith('Scenario:') or line.startswith('Scenario Outline:') or line.startswith('Developer Task:'):
                    current_scenario = line.strip()
                    features = self.process_feature_line(features, current_feature, current_scenario, line)
                    if line.startswith('Scenario Outline:'):
                        state = 'scenario_outline'
                        examples_found = False
                        example_lines = 0
                    else:
                        state = 'scenario'
                elif any(line.startswith(keyword) for keyword in self.keywords):
                    features = self.process_scenario_line(features, current_feature, current_scenario, line)
                elif line:
                    corrected_line = self.corrector.handle_invalid_syntax(line_number, line)
                    if corrected_line:
                        data[line_number - 1] = corrected_line

            elif state == 'scenario':
                if any(line.startswith(keyword) for keyword in self.keywords):
                    features = self.process_scenario_line(features, current_feature, current_scenario, line)
                elif line.startswith('Scenario:') or line.startswith('Scenario Outline:') or line.startswith('Developer Task:'):
                    current_scenario = line.strip()
                    features = self.process_feature_line(features, current_feature, current_scenario, line)
                    if line.startswith('Scenario Outline:'):
                        state = 'scenario_outline'
                        examples_found = False
                        example_lines = 0
                    else:
                        state = 'scenario'
                elif line.startswith('Feature:'):
                    current_feature = line[len('Feature:'):].strip()
                    current_scenario = None
                    state = 'feature'
                elif line:
                    corrected_line = self.corrector.handle_invalid_syntax(line_number, line)
                    if corrected_line:
                        data[line_number - 1] = corrected_line

            elif state == 'scenario_outline':
                if line.startswith('Examples:'):
                    examples_found = True
                elif examples_found and line.startswith('|'):
                    example_lines += 1
                elif examples_found and not line.startswith('|'):
                    if example_lines < 3:
                        print(f"Error: 'Scenario Outline:' at line {line_number} is not followed by 'Examples:' and at least three lines starting with '|'")
                    state = 'scenario'
                    if any(line.startswith(keyword) for keyword in self.keywords):
                        features = self.process_scenario_line(features, current_feature, current_scenario, line)
                    elif line.startswith('Scenario:') or line.startswith('Scenario Outline:') or line.startswith('Developer Task:'):
                        current_scenario = line.strip()
                        features = self.process_feature_line(features, current_feature, current_scenario, line)
                        if line.startswith('Scenario Outline:'):
                            state = 'scenario_outline'
                            examples_found = False
                            example_lines = 0
                        else:
                            state = 'scenario'
                    elif line.startswith('Feature:'):
                        current_feature = line[len('Feature:'):].strip()
                        current_scenario = None
                        state = 'feature'
                    elif line:
                        corrected_line = self.corrector.handle_invalid_syntax(line_number, line)
                        if corrected_line:
                            data[line_number - 1] = corrected_line

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
