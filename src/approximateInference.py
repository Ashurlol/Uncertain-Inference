from probBayes import *
from xmlParser import *
import sys


T, F = True, False

# Prior sampling

def priorSample(bn):
    """
    bn: a Bayesian network
    
    randomly samples from P(Xi | parents(Xi))

    """
    event = {}
    for node in bn.nodes:
        event[node.variable] = node.sample(event)
    return event

def consistentWith(event, evidence):
    """
    Returns if event consistent with the given evidence

    """
    for k,v in evidence.items():
        if event[k] != v:
            return False
    return True

# Rejection sampling

def rejectionSampling(X, e, bn, N):
    """
    X: query
    e: evidence
    bn: Bayesian network
    N: number of samples

    Returns the probability distribution of query X given evidence e in BayesNet bn with N samples.
    
    """
    counts = {x: 0 for x in bn.variableValues(X)}  #count the number of each variable's value
    for j in range(N):
        sample = priorSample(bn) 
        if consistentWith(sample, e):
            counts[sample[X]] += 1
    return ProbDist(X, counts)




# likelihood weighting

def likelihoodWeighting(X, e, bn, N):
    """
    X: query
    e: evidence
    bn: Bayesian network
    N: number of samples

    Returns the weighted probability distribution of query X given evidence e in BayesNet bn with N samples.  

    """
    W = {x: 0 for x in bn.variableValues(X)}   # the dict to count the number of each variable's value
    for j in range(N):
        sample, weight = weightedSample(bn, e)  # boldface x, w in [Figure 14.15]
        W[sample[X]] += weight
    return ProbDist(X, W)

def weightedSample(bn, e):
    """
    Returns the event and its weight
    """
    w = 1
    event = dict(e)  # the event initial with evidence value
    for node in bn.nodes:
        Xi = node.variable
        if Xi in e:
            w *= node.pX(e[Xi], event)     # w ← w × P(Xi = xi | parents(Xi))
        else:
            event[Xi] = node.sample(event)      # x[i] ← a random sample from P(Xi | parents(Xi))
    return event, w


# main functions 
if __name__ == '__main__':
    sampleNum = int(sys.argv[1])
    xmlDir = sys.argv[2]
    queryVar = sys.argv[3]
    evidenceList = sys.argv[4:]
    evidenceKeyList = [evidenceList[i] for i in range(len(evidenceList)) if i%2 == 0]
    evidenceValueList = [evidenceList[i] for i in range(len(evidenceList)) if i%2 == 1]
    evidenceDict = {}
    for i in range(len(evidenceKeyList)):
        evidenceDict[evidenceKeyList[i]] = bool(evidenceValueList[i])

    xmlBayesNet = bayesNetFromXML(xmlDir)

    result1 = rejectionSampling(queryVar, evidenceDict, xmlBayesNet, sampleNum)
    result2 = likelihoodWeighting(queryVar, evidenceDict, xmlBayesNet, sampleNum)

    print('')
    print('With rejection sampling','P(True)=', result1[T],', P(False)=', result1[F])
    print('With likelihood weighting','P(True)=', result2[T],', P(False)=', result2[F])
    print('')


