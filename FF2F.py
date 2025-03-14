import sys
import os
from parser import Parser
from csv_writer import CSVWriter
from config import Config
from error_handler import ErrorHandler
from validator import Validator

def main():
    if len(sys.argv) != 2:
        print("Usage: python FF2F.py <feature_file_path>")
        sys.exit(1)

    feature_file_path = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(feature_file_path))[0]
    output_csv_path = os.path.join("GeneratedCSV", f"{base_name}.csv")

    if not os.path.exists("GeneratedCSV"):
        os.makedirs("GeneratedCSV")

    if os.path.exists(output_csv_path):
        counter = 1
        while os.path.exists(output_csv_path):
            output_csv_path = os.path.join("GeneratedCSV", f"{base_name}_{counter}.csv")
            counter += 1

    with open(feature_file_path, 'r') as file:
        file_content = file.read()

    validator = Validator(file_content)
    is_valid, validation_error = validator.validate()
    if not is_valid:
        print(f"Validation Error: {validation_error}")
        sys.exit(1)

    config = Config()
    keywords = config.get_keywords()

    error_handler = ErrorHandler()
    parser = Parser(keywords, error_handler)
    feature_data = parser.parse_feature_file(file_content)

    csv_writer = CSVWriter()
    csv_writer.write_to_csv(feature_data, output_csv_path)

    error_handler.print_errors()

    print(f"Successfully converted Gherkin file to CSV: {output_csv_path}")

if __name__ == "__main__":
    main()
