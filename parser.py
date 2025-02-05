import difflib
from corrector import Corrector

class Parser:
    def __init__(self, keywords):
        self.corrector = Corrector(keywords)

    def parse_feature_file(self, file_content):
        lines = file_content.splitlines()

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
