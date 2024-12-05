from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import BeliefPropagation

def bayesian_network():
    """
    Example:
    >>> bayesian_network()
    Model is valid: True
    +------+----------+
    | C    |   phi(C) |
    +------+----------+
    | C(0) |   0.6000 |
    | C(1) |   0.4000 |
    +------+----------+

    Code:
    ----
    from pgmpy.models import BayesianNetwork
    from pgmpy.factors.discrete import TabularCPD
    from pgmpy.inference import BeliefPropagation

    def bayesian_network():
        model = BayesianNetwork([('A', 'C'), ('B', 'C')])

        model.add_cpds(
            TabularCPD('A', 2, [[0.8], [0.2]]),
            TabularCPD('B', 2, [[0.7], [0.3]]),
            TabularCPD('C', 2, [[0.9, 0.6, 0.7, 0.1], [0.1, 0.4, 0.3, 0.9]], evidence=['A', 'B'], evidence_card=[2, 2])
        )

        print("Model is valid:", model.check_model())

        infer = BeliefPropagation(model)
        result = infer.query(variables=['C'], evidence={'A': 1, 'B': 0})

        print(result)
    """
    
    
    model = BayesianNetwork([('A', 'C'), ('B', 'C')])

    model.add_cpds(
        TabularCPD('A', 2, [[0.8], [0.2]]),
        TabularCPD('B', 2, [[0.7], [0.3]]),
        TabularCPD('C', 2, [[0.9, 0.6, 0.7, 0.1], [0.1, 0.4, 0.3, 0.9]], evidence=['A', 'B'], evidence_card=[2, 2])
    )

    print("Model is valid:", model.check_model())

    infer = BeliefPropagation(model)
    result = infer.query(variables=['C'], evidence={'A': 1, 'B': 0})

    print(result)


