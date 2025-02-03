import csv
import sys
import os


def parse_feature_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    features = []
    current_feature = None
    current_scenario = None

    for line_number, line in enumerate(lines, start=1):
        line = line.lstrip()
        line = line.rstrip()
        if line.startswith('Feature:'):
            current_feature = line[len('Feature:'):].strip()
            features.append([current_feature, '', ''])
        elif (line.startswith('Scenario:') or
              line.startswith('Scenario Outline:') or
              line.startswith('Developer Task:')):
            current_scenario = line.strip()
            if current_feature and not any(f[0] == current_feature for f in features):
                features.append([current_feature, '', ''])
            if current_feature and current_scenario:
                features.append([current_feature, current_scenario, ''])
        elif any(line.startswith(keyword) for keyword in
                 ['Given', 'When', 'Then', 'And', 'Examples', '|']):
            if current_feature and current_scenario:
                features.append([current_feature, current_scenario, line])
        elif line:
            print(f"Invalid Gherkin syntax at line {line_number}: {line}")

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
    return list({row[1] for row in data})


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
                    'When', 'Then']):
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

    formatting_result = check_formatting(feature_file_path)
    if formatting_result != "Formatting Ok":
        print(formatting_result)

    feature_data = parse_feature_file(feature_file_path)
    write_to_csv(feature_data, output_csv_path)

    print(f"Successfully converted Gherkin file to CSV: {output_csv_path}")


def test_parse_feature_file():
    test_file_path = 'test.feature'
    with open(test_file_path, 'w') as file:
        file.write('''Feature: Test Feature
Scenario: Test Scenario
Given a step
When another step
Then a final step
''')

    expected_output = [
        ['Test Feature', '', ''],
        ['Test Feature', 'Scenario: Test Scenario', ''],
        ['Test Feature', 'Scenario: Test Scenario', 'Given a step'],
        ['Test Feature', 'Scenario: Test Scenario', 'When another step'],
        ['Test Feature', 'Scenario: Test Scenario', 'Then a final step']
    ]

    assert parse_feature_file(test_file_path) == expected_output
    os.remove(test_file_path)


def test_write_to_csv():
    test_data = [
        ['Feature 1', 'Scenario: Test Scenario 1', 'Given a step'],
        ['Feature 1', 'Scenario: Test Scenario 1', 'When another step'],
        ['Feature 1', 'Scenario: Test Scenario 1', 'Then a final step'],
        ['Feature 2', 'Scenario: Test Scenario 2', 'Given a step'],
        ['Feature 2', 'Scenario: Test Scenario 2', 'When another step'],
        ['Feature 2', 'Scenario: Test Scenario 2', 'Then a final step']
    ]

    output_file = 'test_output.csv'
    write_to_csv(test_data, output_file)

    with open(output_file, 'r') as file:
        lines = file.readlines()

    expected_lines = [
        'Scenarios\n',
        'Scenario: Test Scenario 1\n',
        'Scenario: Test Scenario 2\n',
        'Feature,Test Case/Scenario,Test Step\n',
        'Feature 1,Scenario: Test Scenario 1,Given a step\n',
        ',,When another step\n',
        ',,Then a final step\n',
        ',,\n',
        'Feature 2,Scenario: Test Scenario 2,Given a step\n',
        ',,When another step\n',
        ',,Then a final step\n',
        ',,\n'
    ]

    assert lines == expected_lines
    os.remove(output_file)


def test_check_formatting():
    test_file_path = 'test_formatting.feature'
    with open(test_file_path, 'w') as file:
        file.write('''Feature: Test Feature
Scenario: Test Scenario
Given a step
When another step
Then a final step
Invalid line
''')

    expected_output = "Formatting error on line 6: Invalid line"
    assert check_formatting(test_file_path) == expected_output
    os.remove(test_file_path)


def test_main():
    test_file_path = 'test_main.feature'
    with open(test_file_path, 'w') as file:
        file.write('''Feature: Test Feature
Scenario: Test Scenario
Given a step
When another step
Then a final step
''')

    sys.argv = ['Gherkin2Fibery.py', test_file_path]
    main()

    output_file = 'test_main.csv'
    with open(output_file, 'r') as file:
        lines = file.readlines()

    expected_lines = [
        'Scenarios\n',
        'Scenario: Test Scenario\n',
        'Feature,Test Case/Scenario,Test Step\n',
        'Test Feature,Scenario: Test Scenario,Given a step\n',
        ',,When another step\n',
        ',,Then a final step\n',
        ',,\n'
    ]

    assert lines == expected_lines
    os.remove(test_file_path)
    os.remove(output_file)


if __name__ == "__main__":
    main()
