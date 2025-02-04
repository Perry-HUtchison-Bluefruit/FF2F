import csv
import sys
import os
from collections import OrderedDict
import difflib

def parse_feature_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    corrected_lines = correct_syntax(lines)
    features = extract_features(corrected_lines)

    return features


def process_feature_line(features, current_feature, current_scenario, line):
    if current_feature and not any(f[0] == current_feature for f in features):
        features.append([current_feature, '', ''])
    if current_feature and current_scenario:
        features.append([current_feature, current_scenario, ''])
    return features


def process_scenario_line(features, current_feature, current_scenario, line):
    if current_feature and current_scenario:
        features.append([current_feature, current_scenario, line])
    return features


def handle_invalid_syntax(line_number, line):
    print(f"Invalid Gherkin syntax at line {line_number}: {line}")
    return correct_syntax([line])[0]


def extract_features(data):
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
            features = process_feature_line(features, current_feature, current_scenario, line)
        elif any(line.startswith(keyword) for keyword in ['Given', 'When', 'Then', 'And', 'Examples', '|']):
            features = process_scenario_line(features, current_feature, current_scenario, line)
        elif line:
            corrected_line = handle_invalid_syntax(line_number, line)
            if corrected_line:
                data[line_number - 1] = corrected_line
                return extract_features(data)
    return features


def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Scenarios'])
        scenarios = extract_scenarios(data)
        write_scenarios(writer, scenarios)
        writer.writerow(['Feature', 'Test Case/Scenario', 'Test Step'])
        write_features_and_steps(writer, data)


def extract_scenarios(data):
    seen = OrderedDict()
    scenarios = []
    for row in data:
        scenario = row[1]
        if scenario and scenario not in seen:
            scenarios.append(scenario)
            seen[scenario] = None
    return scenarios


def write_scenarios(writer, scenarios):
    for scenario in scenarios:
        writer.writerow([scenario])


def write_features_and_steps(writer, data):
    last_feature = None
    last_scenario = None

    for i, (feature, scenario, step) in enumerate(data):
        if feature == last_feature:
            feature = ''
        else:
            last_feature = feature

        if scenario == last_scenario:
            scenario = ''
        else:
            last_scenario = scenario

        writer.writerow([feature, scenario, step])

        if i + 1 < len(data) and data[i + 1][1] != last_scenario:
            writer.writerow(['', '', ''])
        elif i + 1 == len(data):
            writer.writerow(['', '', ''])


def check_formatting(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    errors = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not any(line.startswith(keyword) for keyword in
                   ['Feature:', ' ', '', '@', 'Scenario:',
                    'Scenario Outline:', 'Developer Task:', 'Given', 'And',
                    'When', 'Then', 'Examples', '|']):
            errors.append(f"Formatting error on line {i + 1}: {line}")

    if errors:
        return "\n".join(errors)
    else:
        return "Formatting Ok"


def correct_syntax(lines):
    valid_keywords = ['Feature:', 'Scenario:', 'Scenario Outline:', 'Given', 'When', 'Then', 'And', 'Examples', '|']
    corrected_lines = []
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            corrected_lines.append(line)
            continue
        
        # Check for multi-word keywords first
        keyword_found = False
        for keyword in valid_keywords:
            if line_stripped.startswith(keyword):
                corrected_lines.append(line)
                keyword_found = True
                break
        
        if not keyword_found:
            # Handle single-word keywords
            first_word = line_stripped.split()[0] if line_stripped.split() else ''
            if first_word not in valid_keywords:
                closest_matches = difflib.get_close_matches(first_word, valid_keywords, n=1, cutoff=0.8)
                if closest_matches:
                    corrected_line = closest_matches[0] + line_stripped[len(first_word):]
                    corrected_lines.append(corrected_line)
                else:
                    corrected_lines.append(line)
            else:
                corrected_lines.append(line)
    return corrected_lines


def main():
    if len(sys.argv) != 2:
        print("Usage: python Gherkin2Fibery.py <feature_file_path>")
        sys.exit(1)

    feature_file_path = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(feature_file_path))[0]
    output_csv_path = f"{base_name}.csv"

    counter = 1
    while os.path.exists(output_csv_path):
        output_csv_path = f"{base_name}_{counter}.csv"
        counter += 1

    feature_data = parse_feature_file(feature_file_path)
    write_to_csv(feature_data, output_csv_path)

    print(f"Successfully converted Gherkin file to CSV: {output_csv_path}")


if __name__ == "__main__":
    main()
