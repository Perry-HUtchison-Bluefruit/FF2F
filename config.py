import logging

class Config:
    def __init__(self):
        logging.debug("Initializing Config class")
        self.keywords = ['Feature:', 'Scenario:', 'Scenario Outline:', 'Given', 'When', 'Then', 'And', 'Examples:', '|']

    def get_keywords(self):
        logging.debug("Retrieving keywords")
        return self.keywords
