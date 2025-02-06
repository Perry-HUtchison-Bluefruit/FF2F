class Config:
    def __init__(self):
        self.keywords = ['Feature:', 'Scenario:', 'Scenario Outline:', 'Given', 'When', 'Then', 'And', 'Examples:', '|']

    def get_keywords(self):
        return self.keywords
