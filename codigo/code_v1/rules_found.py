#class for the rules found

class rules_found:
    def __init__(self):
        self.rules = []

    def set_rules(self, rules, sup, conf):
        self.sup = sup
        self.conf = conf
        self.rules = rules

    def get_rules(self):
        return self.rules

    def __str__(self):
        return f"Rules: {self.rules}\n"
