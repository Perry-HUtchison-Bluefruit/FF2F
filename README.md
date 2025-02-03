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

Scenarios
Scenario: scenario 1
Scenario: scenario 2
Scenario: scenario 3
Scenario Outline: Correct scenario outline: scenario 4
Scenario Outline: Incorret example name: scenario 5
Scenario Outline: Missing examples keyword: scenario 6
Scenario Outline: Missing example table: scenario 7
Scenario Outline: scenario outline should be scenario: scenario 8
Scenario: scenario 9
Scenario: scenario 10
Developer Task: task 1
Developer Task: task 2
Scenario: scenario 11
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
,Scenario Outline: Correct scenario outline: scenario 4,
,,Given step 10 <column 1>
,,When step 11
,,Then step 12
,,Examples:
,,| column 1 |
,,| value 1  |
,,| value 2  |
,,| value 3  |
,,
,Scenario Outline: Incorret example name: scenario 5,
,,Given step 13
,,And step 14 <column 2>
,,When step 15
,,Then step 16
,,Examples:
,,| column 1 |
,,| value 1  |
,,| value 2  |
,,
,Scenario Outline: Missing examples keyword: scenario 6,
,,Given step 17
,,And step 18 <column 1>
,,When step 19
,,Then step 20
,,| column 1 |
,,| value 1  |
,,
,Scenario Outline: Missing example table: scenario 7,
,,Given step 17
,,And step 18 <column 1>
,,When step 19
,,Then step 20
,,Examples:
,,| column 1 |
,,
,Scenario Outline: scenario outline should be scenario: scenario 8,
,,Given step 21
,,When step 22
,,Then step 23
,,
feature 2,,
,,
,Scenario: scenario 9,
,,Given step 24
,,And step 25
,,When step 26
,,Then step 27
,,
,Scenario: scenario 10,
,,Given step 28
,,And step 29
,,When step 30
,,Then step 31
,,And step 32
,,
,Developer Task: task 1,
,,
feature 3,,
,,
,Developer Task: task 2,
,,
,Scenario: scenario 11,
,,When step 34
,,Then step 35
,,Given step 36
,,When step 37
,,Then step 38
,,Given step 39
,,When step 40
,,Then step 41
,,And step 42
,,

 
