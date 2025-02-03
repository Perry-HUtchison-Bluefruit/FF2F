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
 
