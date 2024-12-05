class BackwardKB:
    """
    Example:
    >>> from algoai import BackwardKB
    >>> kb = BackwardKB()
    >>> kb.add_fact("A")
    >>> kb.add_fact("B")
    >>> kb.add_rule({"if": {"A", "B"}, "then": "C"})
    >>> kb.add_rule({"if": {"C"}, "then": "D"})
    >>> goal = "D"
    >>> print(f"Goal {goal} is {'achieved' if kb.backward_chaining(goal) else 'not achievable'}.")
    Goal D is achieved.

    Code:
    class BackwardKB:
        def __init__(self):
            self.rules = []
            self.facts = set()

        def add_rule(self, rule):
        self.rules.append(rule)

        def add_fact(self, fact):
            self.facts.add(fact)

        def backward_chaining(self, goal):
            if goal in self.facts:
                return True
            for rule in self.rules:
                if rule["then"] == goal and all(self.backward_chaining(g) for g in rule["if"]):
                    self.facts.add(goal)
                    return True
            return False
        
    """

    def __init__(self):
        self.rules = []
        self.facts = set()

    def add_rule(self, rule):
       self.rules.append(rule)

    def add_fact(self, fact):
        self.facts.add(fact)

    def backward_chaining(self, goal):
        if goal in self.facts:
            return True
        for rule in self.rules:
            if rule["then"] == goal and all(self.backward_chaining(g) for g in rule["if"]):
                self.facts.add(goal)
                return True
        return False


