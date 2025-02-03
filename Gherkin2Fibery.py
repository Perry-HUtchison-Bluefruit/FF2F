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
