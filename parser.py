import difflib
from corrector import Corrector

class Parser:
    def __init__(self, keywords, error_handler):
        self.error_handler = error_handler
        self.corrector = Corrector(keywords, error_handler)

    def parse_feature_file(self, file_content):
        lines = file_content.splitlines()

        features = self.extract_features(lines)

        return features

    def extract_features(self, data):
        features = []
        current_feature = None
        current_scenario = None
        scenario_outline_detected = False
        for line_number, line in enumerate(data, start=1):
            line = line.strip()
            if line.startswith('Feature:'):
                current_feature = line[len('Feature:'):].strip()
                current_scenario = None
                scenario_outline_detected = False
            elif line.startswith('Scenario Outline:'):
                current_scenario = line.strip()
                scenario_outline_detected = True
                features = self.process_feature_line(features, current_feature, current_scenario, line)
            elif line.startswith('Examples:'):
                scenario_outline_detected = False
                features = self.process_scenario_line(features, current_feature, current_scenario, line)
            elif (line.startswith('Scenario:') or
                  line.startswith('Developer Task:')):
                current_scenario = line.strip()
                scenario_outline_detected = False
                features = self.process_feature_line(features, current_feature, current_scenario, line)
            elif any(line.startswith(keyword) for keyword in ['Given', 'When', 'Then', 'And', '|']):
                features = self.process_scenario_line(features, current_feature, current_scenario, line)
            elif line:
                corrected_line = self.corrector.handle_invalid_syntax(line_number, line)
                if corrected_line != line:
                    # If the line was corrected, reprocess it as a new line
                    if corrected_line.startswith('Scenario:') or corrected_line.startswith('Scenario Outline:') or corrected_line.startswith('Developer Task:'):
                        current_scenario = corrected_line.strip()
                        features = self.process_feature_line(features, current_feature, current_scenario, corrected_line)
                    else:
                        data[line_number - 1] = corrected_line
                        if current_feature and current_scenario:
                            features.append([current_feature, current_scenario, corrected_line])
                else:
                    if current_feature and current_scenario:
                        features.append([current_feature, current_scenario, corrected_line])
            if scenario_outline_detected and not line.startswith('Examples:') and not any(line.startswith(keyword) for keyword in ['Given', 'When', 'Then', 'And', '|']):
                self.error_handler.add_error(line_number, 'error', f"Missing examples table after 'Scenario Outline:' at line {line_number}")
                scenario_outline_detected = False
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
