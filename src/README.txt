
This program contains 4 python files including xmlParser.py, probBayes.py, exactInference.py and approximateInference.py.

1.xmlParser.py reads an xml file returns a BayesNet
2.probBayes.py contains the class BayesNet, BayesNode and ProbDist to use in other files
3.exactInference.py implemented inference by enumeration algorithm
4.approximateInference.py implemented approximate inference including Rejection sampling and      Likelihood weighting
5.examples contains xml files
6.README is this file

To test out exactInference.py and approximateInference.py, use commands like follows:

python exactInference.py examples/aima-alarm.xml B J true M true

or 

python approximateInference.py 10000 examples/aima-wet-grass.xml R S true

or 

python exactInference.py examples/dog-problem.xml family-out hear-bark true light-on false

The general format is as follows
For exact inference:
python exactInference.py [xml file] [query] [evidence] 
For approximate inference:
python approximateInference.py [xml file] [Number of samples] [query] [evidence] 
where attributes in [] are free to change 

There are three [xml file] to test out:
1. examples/aima-alarm.xml
2. examples/aima-wet-grass.xml
3. examples/dog-problem.xml

Variables in each xml file are as follows: 
1. examples/aima-alarm.xml: B E A J M
2. examples/aima-wet-grass.xml: C S R W
3. examples/dog-problem.xml: light-on bowel-problem dog-out hear-bark family-out
where variables can be used for [query] and [evidence] for each file
a true or false statement needs to follow a variable if it's given in the [evidence]

[Number of samples] needs to be a positive integer