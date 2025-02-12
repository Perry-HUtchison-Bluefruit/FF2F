import os
from config import Config

def is_file_readable(file_path):
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)

def is_valid_gherkin_file(file_path):
    if not is_file_readable(file_path):
        return False, "File does not exist or is not readable."

    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        if not first_line.startswith("Feature:"):
            return False, "File is not a valid Gherkin file."

    config = Config()
    keywords = config.get_keywords()

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not any(line.startswith(keyword) for keyword in keywords):
                return False, "File contains invalid Gherkin syntax."

    return True, "File is a valid Gherkin file."
