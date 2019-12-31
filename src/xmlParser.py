from xml.dom.minidom import parse
import xml.dom.minidom
from probBayes import *

T, F = True, False

# XML Parser
def bayesNetFromXML(xmlfile):
    """

    returns a BayesNet from the xml file given

    """

    # use minidom to open the xml
    DOMTree = xml.dom.minidom.parse(xmlfile)
    bif = DOMTree.documentElement   # the root element
    network = bif.getElementsByTagName("NETWORK")[0]
    nodeInfos = network.getElementsByTagName("DEFINITION")

    #rearrange node information so that all are in order
    nodeInfoArrange = []
    #put nodes with no parents first
    for nodeInfo in nodeInfos:
        if len(nodeInfo.getElementsByTagName("GIVEN")) == 0:
            varName = nodeInfo.getElementsByTagName("FOR")[0].childNodes[0].data
            nodeInfoArrange.append([varName, nodeInfo])
            nodeInfos.remove(nodeInfo)

    while len(nodeInfos) > 0:
        varNameList = [node[0] for node in nodeInfoArrange]
        for nodeInfo in nodeInfos:
            varName = nodeInfo.getElementsByTagName("FOR")[0].childNodes[0].data
            allInVarNameList = True
            for givenNode in nodeInfo.getElementsByTagName("GIVEN"):
                if not givenNode.childNodes[0].data in varNameList:
                    allInVarNameList = False
                    break
            if allInVarNameList:
                nodeInfoArrange.append([varName, nodeInfo])
                nodeInfos.remove(nodeInfo)

    nodeInfos = [node[1] for node in nodeInfoArrange]
 
    nodeTupleList = []  

    for nodeInfo in nodeInfos:
        # variable Name
        varName = nodeInfo.getElementsByTagName("FOR")[0].childNodes[0].data
        # parents Name
        parentsName = ""    
        for parent in nodeInfo.getElementsByTagName("GIVEN"):
            parentsName += (" " + parent.childNodes[0].data)
        parentsName = parentsName.strip()

        # conditional probability values in TABLE
        cpValuesStr = ""  
        cpNode = nodeInfo.getElementsByTagName("TABLE")[0]
        for item in cpNode.childNodes:
            if type(item) is xml.dom.minidom.Text:
                cpValuesStr += (" " + item.data.strip())

        # replace all \n and \t by " "
        cpValuesStr.replace("\n", " ")
        cpValuesStr.replace("\t", " ")

        # save all the cp values to a list
        cpValuesList = cpValuesStr.strip().split(" ")
        while " " in cpValuesList:
            cpValuesList.remove(" ")
        while "" in cpValuesList:
            cpValuesList.remove("")

        # only leave the odd index, which is the cp evaluated to True
        cpValuesList = [cpValuesList[i] for i in range(len(cpValuesList)) if i % 2 == 0]

        # cp Dict
        cpDict = {}
        parentNum = len(nodeInfo.getElementsByTagName("GIVEN"))
        cpKeysList = createTFcombo(parentNum)
        for i in range(len(cpKeysList)):
            if len(cpKeysList[i]) == 1:
                cpDict[cpKeysList[i][0]] = float(cpValuesList[i])
            elif len(cpKeysList[i]) > 1:
                cpDict[cpKeysList[i]] = float(cpValuesList[i])

        if parentNum == 0:
            nodeTupleList.append(tuple([varName, parentsName, float(cpValuesList[0])]))
        else:
            nodeTupleList.append(tuple([varName, parentsName, cpDict]))
    return BayesNet(nodeTupleList)




def createTFcombo(num):
    """
    returns a list of True/False tuples for each variable 

    """
    rtList = []

    for i in range(num):
        if len(rtList) == 0:
            rtList.append([T])
            rtList.append([F])
        else:
            rtListToRenew = []
            for item in rtList:
                itemT = item + [T]
                itemF = item + [F]
                rtListToRenew.append(itemT)
                rtListToRenew.append(itemF)
            rtList = rtListToRenew
    rtList = [tuple(iList) for iList in rtList]
    return rtList



  













