# FF2F
# FeatureFile2Fibery
A tool for extracting Test Cases, and Steps ready to be entered into Fibery 

## Overview

`Gherkin2Fibery.py` is a Python script that parses Gherkin feature files and converts their content into a CSV format. This tool extracts features, scenarios, and steps from Gherkin files and organises them into a structured CSV file ready to be uploaded to Fibery.

## Features

- Parses Gherkin feature files to extract features, scenarios, and steps.
- Handles `Feature:`, `Scenario:`, `Scenario Outline:`, and `Developer Task:` lines.
- Includes scenarios and developer tasks even if they don't have steps.
- Generates a CSV file with the extracted data.
- Checks the formatting of the feature file and reports any formatting errors.
- Corrects common syntax errors in the Gherkin file before appending to the CSV.

## Usage

### Prerequisites

- Python 3.x

### Running the Script

1. Place your Gherkin feature file in the same directory as `Gherkin2Fibery.py` or provide the full path to the feature file.
2. Open a terminal or command prompt.
3. Navigate to the directory containing `Gherkin2Fibery.py`.
4. Run the script with the following command:

   ```sh
   python Gherkin2Fibery.py <feature_file_path>

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
