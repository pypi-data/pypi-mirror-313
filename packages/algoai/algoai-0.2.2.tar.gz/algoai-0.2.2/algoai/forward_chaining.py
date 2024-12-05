class ForwardKB:
    """
    Example:
   >>> from algoai import ForwardKB
   >>> kb = ForwardKB()
   >>> kb.add_fact("A")
   >>> kb.add_fact("B")
   >>> kb.add_rule({"if": {"A", "B"}, "then": "C"})
   >>> kb.add_rule({"if": {"C"}, "then": "D"})
   >>> kb.forward_chaining()
   >>> print(f"Final facts: {kb.facts}")
    # Output: Inferred: C
    #         Inferred: D
    # Final facts will include: {'A', 'B', 'C', 'D'}
     |
Code:
----
     |
class ForwardKB:
    def __init__(self):
        self.rules = []
        self.facts = set()
     |
    def add_rule(self, rule):
        self.rules.append(rule)
     |
    def add_fact(self, fact):
        self.facts.add(fact)
     |
    def forward_chaining(self):
        while True:
            new_inference = False
            for rule in self.rules:
                if rule["if"].issubset(self.facts) and rule["then"] not in self.facts:
                    self.facts.add(rule["then"])
                    print(f"Inferred: {rule['then']}")
                    new_inference = True
            if not new_inference:
  
    """

    def __init__(self):
        self.rules = []
        self.facts = set()

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_fact(self, fact):
        self.facts.add(fact)

    def forward_chaining(self):
        while True:
            new_inference = False
            for rule in self.rules:
                if set(rule["if"]).issubset(self.facts) and rule["then"] not in self.facts:
                    self.facts.add(rule["then"])
                    print(f"Inferred: {rule['then']}")
                    new_inference = True
            if not new_inference:
                break  # End the loop when no new facts are inferred
