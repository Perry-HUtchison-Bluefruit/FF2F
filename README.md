# FF2F
# FeatureFile2Fibery
A tool for extracting Test Cases, and Steps ready to be entered into Fibery 

## Overview

`FF2F.py` is a Python script that parses Gherkin feature files and converts their content into a CSV format. This tool extracts features, scenarios, and steps from Gherkin files and organises them into a structured CSV file ready to be uploaded to Fibery.

An input validation layer has been added to ensure that the feature file is properly encoded, formatted, and structured before parsing.

## Features

- Parses Gherkin feature files to extract features, scenarios, and steps.
- Handles `Feature:`, `Scenario:`, `Scenario Outline:`, and `Developer Task:` lines.
- Includes scenarios and developer tasks even if they don't have steps.
- Generates a CSV file with the extracted data.
- Checks the formatting of the feature file and reports any formatting errors.
- Corrects common syntax errors in the Gherkin file before appending to the CSV.
- `Parser` class handles parsing of feature files.
- `Corrector` class handles syntax correction.
- `CSVWriter` class handles writing data to CSV.
- `Config` class handles keyword configuration.
- `Validator` class handles input validation for file encoding, format, and basic structure.

## Validator Class

The `Validator` class is responsible for validating the input feature file before it is parsed. It checks for the following:

- UTF-8 encoding
- Valid Gherkin format
- Basic structure (presence of `Feature:` and `Scenario:` keywords)

The `Validator` class provides the following methods:

- `validate_encoding()`: Checks if the file is UTF-8 encoded.
- `validate_format()`: Checks if the file has a valid Gherkin format.
- `validate_structure()`: Checks if the file contains the required `Feature:` and `Scenario:` keywords.
- `validate()`: Calls all validation methods and returns the results.

## Usage

### Prerequisites

- Python 3.x

### Running the Script

1. Place your Gherkin feature file in the same directory as `FF2F.py` or provide the full path to the feature file.
2. Open a terminal or command prompt.
3. Navigate to the directory containing `FF2F.py`.
4. Run the script with the following command:

   ```sh
   python FF2F.py <feature_file_path>
   ```

The script will first validate the input feature file. If the file is not valid, an error message will be displayed, and the script will exit. If the file is valid, the script will proceed to parse the file and generate the CSV output.

### Configuration

The script uses a `Config` class to manage keywords used in parsing. You can modify the keywords by editing the `Config` class in `config.py`.

## Example output file

   ```sh

Scenarios
Scenario: scenario 1
Scenario: scenario 2
Scenario: scenario 3
Scenario: scenario 12
Scenario: scenario 13
Feature,Test Case/Scenario,Test Step
feature 1,,
,,
,Scenario: scenario 1,
,,Given step 1
,,When step 2
,,Then step 3
,,
,Scenario: scenario 2,
,,Given step 4
,,When step 5
,,Then step 6
,,
,Scenario: scenario 3,
,,Given step 7
,,When step 8
,,Then step 9
,,
,Scenario: scenario 12,
,,Given step 36
,,When step 37
,,Then step 38
,,
,Scenario: scenario 13,
,,Given step 39
,,When step 40
,,Then step 41
,,And step 42
,,
   ```

## Data Flow Diagram

The `data-flow-diagram.mermaid` file provides a visual representation of the data flow within the FF2F tool. It illustrates the process from reading the feature file to generating the output CSV file, including error handling paths.

## Error Handling

The `ErrorHandler` class in `error_handler.py` is responsible for managing errors encountered during the parsing and correction process. It collects errors, categorizes them by severity, and provides methods to retrieve and print the errors.

To handle errors reported by the `ErrorHandler` class, you can use the following methods:

- `add_error(line_number, severity, message)`: Adds an error with the specified line number, severity, and message.
- `get_errors()`: Returns a list of all collected errors.
- `print_errors()`: Prints all collected errors to the console.

## Example Input File

The `TestFile.feature` file is an example input file that demonstrates various Gherkin syntax elements and scenarios. You can use this file to test the FF2F tool and see how it processes different types of Gherkin syntax.
