import sys
import os
from parser import Parser
from corrector import Corrector
from csv_writer import CSVWriter

def main():
    if len(sys.argv) != 2:
        print("Usage: python FF2F.py <feature_file_path>")
        sys.exit(1)

    feature_file_path = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(feature_file_path))[0]
    output_csv_path = f"{base_name}.csv"

    counter = 1
    while os.path.exists(output_csv_path):
        output_csv_path = f"{base_name}_{counter}.csv"
        counter += 1

    parser = Parser()
    feature_data = parser.parse_feature_file(feature_file_path)

    csv_writer = CSVWriter()
    csv_writer.write_to_csv(feature_data, output_csv_path)

    print(f"Successfully converted Gherkin file to CSV: {output_csv_path}")

if __name__ == "__main__":
    main()
