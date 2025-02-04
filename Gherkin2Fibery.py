import csv
import sys
import os
from collections import OrderedDict
from difflib import get_close_matches


def parse_feature_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    features = extract_features(lines)

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


def handle_invalid_syntax(line_number, line, features, current_feature, current_scenario):
    print(f"Invalid Gherkin syntax at line {line_number}: {line}")
    closest_match = find_closest_match(line)
    if closest_match:
        features.append([current_feature, current_scenario, closest_match])
    return features


def find_closest_match(line):
    keywords = ['Feature:', 'Scenario:', 'Scenario Outline:', 'Developer Task:', 'Given', 'When', 'Then', 'And', 'Examples', '|']
    closest_matches = get_close_matches(line, keywords)
    return closest_matches[0] if closest_matches else None


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
            features = handle_invalid_syntax(line_number, line, features, current_feature, current_scenario)
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
