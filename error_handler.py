class ErrorHandler:
    def __init__(self):
        self.errors = []

    def add_error(self, line_number, severity, message):
        self.errors.append({
            'line_number': line_number,
            'severity': severity,
            'message': message
        })

    def get_errors(self):
        return self.errors

    def print_errors(self):
        for error in self.errors:
            print(f"[{error['severity'].upper():<8}] Line {error['line_number']:<4}: {error['message']}")
