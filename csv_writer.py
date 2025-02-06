import csv
from collections import OrderedDict

class CSVWriter:
    def __init__(self):
        pass

    def write_to_csv(self, data, output_file):
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Scenarios'])
            scenarios = self.extract_scenarios(data)
            self.write_scenarios(writer, scenarios)
            writer.writerow(['Feature', 'Test Case/Scenario', 'Test Step'])
            self.write_features_and_steps(writer, data)

    def extract_scenarios(self, data):
        seen = OrderedDict()
        scenarios = []
        for row in data:
            scenario = row[1]
            if scenario and scenario not in seen:
                scenarios.append(scenario)
                seen[scenario] = None
        return scenarios

    def write_scenarios(self, writer, scenarios):
        for scenario in scenarios:
            writer.writerow(['', scenario, ''])

    def write_features_and_steps(self, writer, data):
        last_feature = None
        last_scenario = None

        for feature, scenario, step in data:
            if feature == last_feature:
                feature = ''
            else:
                last_feature = feature

            if scenario == last_scenario:
                scenario = ''
            else:
                last_scenario = scenario

            writer.writerow([feature, scenario, step])
