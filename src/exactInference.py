from probBayes import *
from xmlParser import *
import sys


T, F = True, False

# enumerationAsk and enumerationAll****************************************************************************


def enumerationAsk(X, e, bn):
    """
    X: the query variable
    e: observed values for variables E
    bn: a BayesNet with variables {X} ⋃ E ⋃ Y /* Y = hidden variables */

    Return the conditional probability distribution of variable X given evidence e, from BayesNet bn. 
    Examples:
    >>> enumerationAsk('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary)
    'False: 0.716, True: 0.284'

    """
    # assert X not in e, "Query variable must be distinct from evidence"
    Q = ProbDist(X)     # a distribution over X, initially empty
    for xi in bn.variableValues(X):
        Q[xi] = enumerateAll(bn.variables, extend(e, X, xi), bn)
    return Q.normalize()


def enumerateAll(variables, e, bn):
    """
    Returns the sum of those entries in P(variables | e{others})
    consistent with e, where P is the joint distribution represented
    by bn
    
    Parents must precede children in variables.
    """
    if not variables:       # if EMPTY?(vars) then return 1.0
        return 1.0
    Y, rest = variables[0], variables[1:]   # Y ← FIRST(vars)
    Ynode = bn.variable_node(Y)
    if Y in e:
        return Ynode.pX(e[Y], e) * enumerateAll(rest, e, bn)
    else:
        return sum(Ynode.pX(y, e) * enumerateAll(rest, extend(e, Y, y), bn)
                   for y in bn.variableValues(Y))


# util functions ****************************************************************************

# Functions on Sequences and Iterables
def extend(s, var, val):
    """
    Copy the substitution s and extend it by setting var to val; return copy.
    >>> extend({x: 1}, y, 2) == {x: 1, y: 2}
    True
    
    """
    s2 = s.copy()
    s2[var] = val
    return s2

# main functions ****************************************************************************

if __name__ == '__main__':
    xmlDir = sys.argv[1]
    queryVar = sys.argv[2]
    evidenceList = sys.argv[3:]
    evidenceKeyList = [evidenceList[i] for i in range(len(evidenceList)) if i%2 == 0]
    evidenceValueList = [evidenceList[i] for i in range(len(evidenceList)) if i%2 == 1]
    evidenceDict = {}
    for i in range(len(evidenceKeyList)):
        evidenceDict[evidenceKeyList[i]] = bool(evidenceValueList[i])

    xmlBayesNet = bayesNetFromXML(xmlDir)

    result = enumerationAsk(queryVar, evidenceDict, xmlBayesNet)
    print('P(True)=', result[T])
    print('P(False)=', result[F])


