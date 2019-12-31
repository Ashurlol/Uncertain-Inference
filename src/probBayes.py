from math import isclose
import random

# BayesNet and BayesNode

class BayesNet:
    """
    Bayesian network structure

    """

    def __init__(self, node_infos=None):
        """
        Nodes must be ordered with parents before children.

        """
        self.nodes = []
        self.variables = []
        node_infos = node_infos or []
        for node_info in node_infos:
            self.add(node_info)

    def add(self, node_info):
        """
        Add a node to the net. 
        # Its parents must already be in the net, and its variable must not.

        """
        node = BayesNode(*node_info)
        self.nodes.append(node)
        self.variables.append(node.variable)
        for parent in node.parents:
            self.variable_node(parent).children.append(node)

    def variable_node(self, var):
        """
        Return the node for the variable named var.
        >>> burglary.variable_node('Burglary').variable
        'Burglary'

        """
        for n in self.nodes:
            if n.variable == var:
                return n
        raise Exception("No such variable: {}".format(var))

    def variableValues(self, var):
        """
        Return the domain of var.

        """
        return [True, False]

    def __repr__(self):
        return 'BayesNet({0!r})'.format(self.nodes)

class BayesNode:
    """
    The node structure of Bayesian Network
    P(X | parents). 

    """

    def __init__(self, X, parents, cp):
        """
        X:          a variable name
        parents:    a sequence of variable names or a space-separated string.  
        cp:        the conditional probability
        
        Examples:
        >>> X = BayesNode('B', '', 0.001)
        >>> Y = BayesNode('J', 'A', {T: 0.9, F: 0.05})
        >>> Z = BayesNode('A', 'B E',
        ...    {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001})

        """
        # parents: sometimes more than one parent
        if isinstance(parents, str):
            parents = parents.split()

        # cp
        if isinstance(cp, (float, int)):  # no parents
            cp = {(): cp}
        elif isinstance(cp, dict): # one parent
            if cp and isinstance(list(cp.keys())[0], bool):
                cp = {(v,): p for v, p in cp.items()}

        # components of the BayesNode
        self.variable = X
        self.parents = parents
        self.cp = cp
        self.children = []

    def pX(self, value, event):
        """
        Returns the conditional probability of X equals to value when parents' value equal to event
        Examples:
        >>> bn = BayesNode('X', 'B', {T: 0.2, F: 0.625})
        >>> bn.pX(False, {'B': False, 'E': True})
        0.375

        """
        assert isinstance(value, bool)
        pTrue = self.cp[eventValues(event, self.parents)]
        return pTrue if value else 1 - pTrue

    def sample(self, event):
        """
        Returns True/False randomly according to the conditional probability

        """
        return self.pX(True, event) > random.uniform(0.0, 1.0)


    def __repr__(self):
        return repr((self.variable, ' | '.join(self.parents)))


def eventValues(event, variables):
    """
    Returns values in event
    >>> eventValues ({'A': 0.1, 'B': 0.9, 'X': 0.8}, ['X', 'A'])
    (0.8, 0.1)
    >>> eventValues ((0.1, 0.2), ['C', 'A'])
    (0.1, 0.2)
    
    """
    if isinstance(event, tuple) and len(event) == len(variables):
        return event
    else:
        return tuple([event[var] for var in variables])

class ProbDist:
    """
    A discrete probability distribution.
    >>> P = ProbDist('Flip'); P['H'], P['T'] = 0.25, 0.75; 
    >>> P['H']
    0.25
    >>> P = ProbDist('X', {'a': 125, 'b': 375, 'c': 500})
    >>> P['a'], P['b'], P['c']
    (0.125, 0.375, 0.5)
    
    """

    def __init__(self, varName='*', freqs=None):
        """
        Components:
        prob: the probability of each variables' value
        varName: the name of the variable
        values: the values of the variable
        If freqs is given, make it normalized.

        """
        self.prob = {}
        self.varName = varName
        self.values = []
        if freqs != None:
            for (v, p) in freqs.items():
                self[v] = p
            self.normalize()

    def __getitem__(self, val):
        """
        Given a value using [], return P(value).

        """

        return self.prob[val]

    def __setitem__(self, val, p):
        """
        Set P(val) = p using [].

        """
        if val not in self.values:
            self.values.append(val)
        self.prob[val] = p

    def normalize(self):
        """
        All values sum to 1.

        """
        total = sum(self.prob.values())
        if not isclose(total, 1.0):
            for val in self.prob:
                self.prob[val] /= total
        return self


    def __repr__(self):
        return "P({})".format(self.varName)
