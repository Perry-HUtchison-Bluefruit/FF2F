import logging

class ErrorHandler:
    def __init__(self):
        logging.debug("Initializing ErrorHandler class")
        self.errors = []

    def add_error(self, line_number, severity, message):
        logging.debug(f"Adding error at line {line_number}: {severity} - {message}")
        if not any(error['line_number'] == line_number and error['message'] == message for error in self.errors):
            self.errors.append({
                'line_number': line_number,
                'severity': severity,
                'message': message
            })

    def get_errors(self):
        logging.debug("Retrieving errors")
        return self.errors

    def print_errors(self):
        logging.debug("Printing errors")
        for error in self.errors:
            print(f"[{error['severity'].upper()}] Line {error['line_number']}: {error['message']}")
