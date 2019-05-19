from math import log
import sys
from scipy.stats import chi2


# from scipy.stats.stats import chisqprob
class Node:
    """
    A simple node class to build our tree with. It has the following:

    children (dictionary<str,Node>): A mapping from attribute value to a child node
    attr (str): The name of the attribute this node classifies by.
    islead (boolean): whether this is a leaf. False.
    """

    def __init__(self, attr):
        self.children = {}
        self.attr = attr
        self.isleaf = False


class LeafNode(Node):
    """
    A basic extension of the Node class with just a value.

    value (str): Since this is a leaf node, a final value for the label.
    islead (boolean): whether this is a leaf. True.
    """

    def __init__(self, value):
        self.value = value
        self.isleaf = True


class Tree:
    """
    A generic tree implementation with which to implement decision tree learning.
    Stores the root Node and nothing more. A nice printing method is provided, and
    the function to classify values is left to fill in.
    """

    def __init__(self, root=None):
        self.root = root

    def prettyPrint(self):
        print str(self)

    def preorder(self, depth, node):
        if node is None:
            return '|---' * depth + str(None) + '\n'
        if node.isleaf:
            return '|---' * depth + str(node.value) + '\n'
        string = ''
        for val in node.children.keys():
            childStr = '|---' * depth
            childStr += '%s = %s' % (str(node.attr), str(val))
            string += str(childStr) + "\n" + self.preorder(depth + 1, node.children[val])
        return string

    def count(self, node=None):
        if node is None:
            node = self.root
        if node.isleaf:
            return 1
        count = 1
        for child in node.children.values():
            if child is not None:
                count += self.count(child)
        return count

    def __str__(self):
        return self.preorder(0, self.root)

    def classify(self, classificationData):
        """
        Uses the classification tree with the passed in classificationData.`

        Args:
            classificationData (dictionary<string,string>): dictionary of attribute values
        Returns:
            str
            The classification made with this tree.
        """
        # YOUR CODE HERE
        root = self.root
        while not root.isleaf:
            attribute = root.attr
            valueOfAttribute = classificationData[attribute]
            root = root.children[valueOfAttribute]
        return root.value


def getPertinentExamples(examples, attrName, attrValue):
    """
    Helper function to get a subset of a set of examples for a particular assignment
    of a single attribute. That is, this gets the list of examples that have the value
    attrValue for the attribute with the name attrName.

    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValue (str): a value of the attribute
    Returns:
        list<dictionary<str,str>>
        The new list of examples.
    """
    # YOUR CODE HERE
    newExamples = []
    for dictionary in examples:
        for key in dictionary.keys():
            if key == attrName and dictionary[key] == attrValue:
                newExamples.append(dictionary)

    return newExamples


def getClassCounts(examples, className):
    """
    Helper function to get a dictionary of counts of different class values
    in a set of examples. That is, this returns a dictionary where each key
    in the list corresponds to a possible value of the class and the value
    at that key corresponds to how many times that value of the class
    occurs.

    Args:
        examples (list<dictionary<str,str>>): list of examples
        className (str): the name of the class
    Returns:
        dictionary<string,int>
        This is a dictionary that for each value of the class has the count
        of that class value in the examples. That is, it maps the class value
        to its count.
    """
    classCounts = {}
    # YOUR CODE HERE
    for dictionary in examples:
        for key in dictionary.keys():
            if key == className:
                attrVal = dictionary[key]
                if attrVal in classCounts.keys():
                    classCounts[attrVal] = classCounts[attrVal] + 1
                else:
                    classCounts[attrVal] = 1

    return classCounts


def getMostCommonClass(examples, className):
    """
    A freebie function useful later in makeSubtrees. Gets the most common class
    in the examples. See parameters in getClassCounts.
    """
    counts = getClassCounts(examples, className)
    return max(counts, key=counts.get) if len(examples) > 0 else None


def getAttributeCounts(examples, attrName, attrValues, className):
    """
    Helper function to get a dictionary of counts of different class values
    corresponding to every possible assignment of the passed in attribute.
	  That is, this returns a dictionary of dictionaries, where each key
	  corresponds to a possible value of the attribute named attrName and holds
 	  the counts of different class values for the subset of the examples
 	  that have that assignment of that attribute.

    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<str>): list of possible values for the attribute
        className (str): the name of the class
    Returns:
        dictionary<str,dictionary<str,int>>
        This is a dictionary that for each value of the attribute has a
        dictionary from class values to class counts, as in getClassCounts
    """
    attributeCounts = {}
    # YOUR CODE HERE
    for possibleValue in attrValues:
        attributeCounts[possibleValue] = getClassCounts(getPertinentExamples(examples, attrName, possibleValue),
                                                        className)
    return attributeCounts


def setEntropy(classCounts):
    """
    Calculates the set entropy value for the given list of class counts.
    This is called H in the book. Note that our labels are not binary,
    so the equations in the book need to be modified accordingly. Note
    that H is written in terms of B, and B is written with the assumption
    of a binary value. B can easily be modified for a non binary class
    by writing it as a summation over a list of ratios, which is what
    you need to implement.

    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The set entropy score of this list of class value counts.
    """
    # YOUR CODE HERE
    totalExamples = sum(classCounts)
    sumProbability = 0
    for number in classCounts:
        probability = float(number) / totalExamples
        logProbablity = log(probability, 2)
        total = probability * logProbablity
        sumProbability += total
    return -1 * sumProbability


def remainder(examples, attrName, attrValues, className):
    """
    Calculates the remainder value for given attribute and set of examples.
    See the book for the meaning of the remainder in the context of info
    gain.

    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The remainder score of this value assignment of the attribute.
    """
    # YOUR CODE HERE
    total = sum(getClassCounts(examples, className).values())
    sum1 = 0.0
    values = getAttributeCounts(examples, attrName, attrValues, className)
    for key in values.keys():
        classes = values[key]
        list = []
        for otherkey in classes.keys():
            list.append(classes[otherkey])
        sumOflist = float(sum(list))
        fraction = sumOflist / total
        # print fraction
        sum1 += float(setEntropy(list) * fraction)
    # print sum1
    return sum1


def infoGain(examples, attrName, attrValues, className):
    """
    Calculates the info gain value for given attribute and set of examples.
    See the book for the equation - it's a combination of setEntropy and
    remainder (setEntropy replaces B as it is used in the book).

    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The gain score of this value assignment of the attribute.
    """
    # YOUR CODE HERE
    secondElementInEquation = remainder(examples, attrName, attrValues, className)

    firstElementInEquation = 0
    classCounts = getClassCounts(examples, className)
    total = sum(classCounts.values())
    for key in classCounts.keys():
        currentCount = classCounts[key]
        probability = float(currentCount) / float(total)
        logprob = log(probability, 2)
        adding = probability * logprob
        firstElementInEquation += adding
    # print firstElementInEquation
    # print secondElementInEquation
    return abs(firstElementInEquation + secondElementInEquation)


def giniIndex(classCounts):
    """
    Calculates the gini value for the given list of class counts.
    See equation in instructions.

    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The gini score of this list of class value counts.
    """
    # YOUR CODE HERE
    sum1 = 0.0
    total = float(sum(classCounts))
    for number in classCounts:
        number = float(number)
        add = float(float(number / total) * float(number / total))
        # print number
        # print total
        # print add
        sum1 += add
    # print (sum1)
    sum1 = 1.0 - sum1
    return sum1


def giniGain(examples, attrName, attrValues, className):
    """
    Return the inverse of the giniD function described in the instructions.
    The inverse is returned so as to have the highest value correspond
    to the highest information gain as in entropyGain. If the sum is 0,
    return sys.maxint.

    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The summed gini index score of this list of class value counts.
    """
    # YOUR CODE HERE
    totalSampleSize = float(len(examples))
    gini = 0.0
    splits = getAttributeCounts(examples, attrName, attrValues, className)
    for key in splits.keys():
        list = []
        for key1 in splits[key].keys():
            list.append(splits[key][key1])
        currentSum = float(sum(list))
        if currentSum != 0.0:
            index = giniIndex(list) * float(currentSum / totalSampleSize)
            gini += index
    if gini == 0.0:
        return sys.maxint
    return (1.0 / gini)


def makeTree(examples, attrValues, className, setScoreFunc, gainFunc):
    """
    Creates the classification tree for the given examples. Note that this is implemented - you
    just need to imeplement makeSubtrees.

    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes = attrValues.keys()
    return Tree(
        makeSubtrees(remainingAttributes, examples, attrValues, className, getMostCommonClass(examples, className),
                     setScoreFunc, gainFunc))


def makeSubtrees(remainingAttributes, examples, attributeValues, className, defaultLabel, setScoreFunc, gainFunc):
    """
    Creates a classification tree Node and all its children. This returns a Node, which is the root
    Node of the tree constructed from the passed in parameters. This should be implemented recursively,
    and handle base cases for zero examples or remainingAttributes as covered in the book.
    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        defaultLabel (string): the default label
        setScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
    Returns:
        Node or LeafNode
        The classification tree node optimal for the remaining set of attributes.
    """
    # YOUR CODE HERE

    if len(examples) == 0:
        return LeafNode(defaultLabel)
    else:
        matching = True
        currentClassification = examples[0][className]
        for dictionary in examples:
            if dictionary[className] != currentClassification:
                matching = False
        if matching:
            return LeafNode(currentClassification)
    if len(remainingAttributes) == 0:
        classCounts = getClassCounts(examples, className)
        currentMax = classCounts[classCounts.keys()[0]]
        currentFeature = classCounts.keys()[0]
        for key in classCounts.keys():
            if classCounts[key] > currentMax:
                currentMax = classCounts[key]
                currentFeature = key
        return LeafNode(currentFeature)
    else:
        maxScore = float(gainFunc(examples, remainingAttributes[0], attributeValues[remainingAttributes[0]], className))
        bestAttribute = remainingAttributes[0]
        for attribute in remainingAttributes:
            currentScore = float((gainFunc(examples, attribute, attributeValues[attribute], className)))
            if abs(currentScore) > abs(maxScore):
                bestAttribute = attribute
                maxScore = currentScore
        node = Node(bestAttribute)

        newRemainingAttributes = []

        # remove bestAttribute from list
        for attribute in remainingAttributes:
            if attribute != bestAttribute:
                newRemainingAttributes.append(attribute)

        for valueOfBest in attributeValues[bestAttribute]:
            newExamples = getPertinentExamples(examples, bestAttribute, valueOfBest)

            classCounts = getClassCounts(examples, className)
            currentMax = classCounts[classCounts.keys()[0]]
            currentFeature = classCounts.keys()[0]
            for key in classCounts.keys():
                if classCounts[key] > currentMax:
                    currentMax = classCounts[key]
                    currentFeature = key
            node.children[valueOfBest] = makeSubtrees(newRemainingAttributes, newExamples, attributeValues, className,
                                                      currentFeature, setScoreFunc, gainFunc)
        return node

        # giniGain(examples,attrName,attrValues,className)


def makePrunedTree(examples, attrValues, className, setScoreFunc, gainFunc, q):
    """
    Creates the classification tree for the given examples. Note that this is implemented - you
    just need to imeplement makeSubtrees.

    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
        q (float): the Chi-Squared pruning parameter
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes = attrValues.keys()
    return Tree(makePrunedSubtrees(remainingAttributes, examples, attrValues, className,
                                   getMostCommonClass(examples, className), setScoreFunc, gainFunc, q))


def makePrunedSubtrees(remainingAttributes, examples, attributeValues, className, defaultLabel, setScoreFunc, gainFunc,
                       q):
    """
    Creates a classification tree Node and all its children. This returns a Node, which is the root
    Node of the tree constructed from the passed in parameters. This should be implemented recursively,
    and handle base cases for zero examples or remainingAttributes as covered in the book.

    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        defaultLabel (string): the default label
        setScoreFunc (func): the function to score classes (ie classEntropy or gini)
        gainFunc (func): the function to score gain of attributes (ie entropyGain or giniGain)
        q (float): the Chi-Squared pruning parameter
    Returns:
        Node or LeafNode
        The classification tree node optimal for the remaining set of attributes.
    """
    # YOUR CODE HERE (Extra Credit)
    if len(examples) == 0:
        return LeafNode(defaultLabel)
    else:
        matching = True
        currentClassification = examples[0][className]
        for dictionary in examples:
            if dictionary[className] != currentClassification:
                matching = False
        if matching:
            return LeafNode(currentClassification)
    if len(remainingAttributes) == 0:
        classCounts = getClassCounts(examples, className)
        currentMax = classCounts[classCounts.keys()[0]]
        currentFeature = classCounts.keys()[0]
        for key in classCounts.keys():
            if classCounts[key] > currentMax:
                currentMax = classCounts[key]
                currentFeature = key
        return LeafNode(currentFeature)
    else:
        maxScore = float(gainFunc(examples, remainingAttributes[0], attributeValues[remainingAttributes[0]], className))
        bestAttribute = remainingAttributes[0]
        for attribute in remainingAttributes:
            currentScore = float((gainFunc(examples, attribute, attributeValues[attribute], className)))
            if abs(currentScore) > abs(maxScore):
                bestAttribute = attribute
                maxScore = currentScore
        node = Node(bestAttribute)

        # a list of all attributesValues we're splitting on
        bestAttributeValues = attributeValues[bestAttribute]

        # make list of class values
        classificationValues = []
        for dictionary in examples:
            for key in dictionary.keys():
                if key == className and not (dictionary[key] in classificationValues):
                    classificationValues.append(dictionary[key])
        classCountsForExamples = getClassCounts(examples, className)
        # chi statistic
        sum = 0.0
        # go through splitValues
        for splitValue in bestAttributeValues:
            # split on values
            subset = getPertinentExamples(examples, bestAttribute, splitValue)
            classCountsForSubset = getClassCounts(subset, className)

            # go through all class values
            for classValue in classificationValues:

                if classValue in classCountsForExamples.keys():
                    numberOfValueInExamples = classCountsForExamples[classValue]
                    # print "number in example ", numberOfValueInExamples
                    probabilityOfValueInExamples = float(numberOfValueInExamples) / float(len(examples))

                else:
                    probabilityOfValueInExamples = 0.0

                if classValue in classCountsForSubset.keys():
                    numberOfValueInSplit = classCountsForSubset[classValue]
                    # print "number in split ", numberOfValueInSplit
                    probabilityOfValueInSplit = float(numberOfValueInSplit)
                else:
                    probabilityOfValueInSplit = 0.0

                p_hat = probabilityOfValueInExamples * float(len(subset))

                if p_hat != 0.0:
                    currentSum = float(((abs(p_hat - probabilityOfValueInSplit)) ** 2) / p_hat)
                    sum += currentSum

        # this is v
        degreesOfFreedom = (len(bestAttributeValues) - 1)  # * (len(classificationValues) - 1)
        p_value_chi = 1 - chi2.cdf(sum, degreesOfFreedom)
        # print p_value_chi
        ##print sum

        # p_value_chi = chisqprob(sum, degreesOfFreedom)
        # print p_value_chi
        # print q

        if p_value_chi > q:  # (0.0028893):
            # print "pruning"
            classCounts = getClassCounts(examples, className)
            # print classCounts
            currentMax = classCounts[classCounts.keys()[0]]
            currentFeature = classCounts.keys()[0]
            for key in classCounts.keys():
                if classCounts[key] > currentMax:
                    currentMax = classCounts[key]
                    currentFeature = key
            return LeafNode(currentFeature)
        else:

            newRemainingAttributes = []

            # remove bestAttribute from list
            for attribute in remainingAttributes:
                if attribute != bestAttribute:
                    newRemainingAttributes.append(attribute)

            for valueOfBest in attributeValues[bestAttribute]:
                newExamples = getPertinentExamples(examples, bestAttribute, valueOfBest)

                classCounts = getClassCounts(examples, className)
                currentMax = classCounts[classCounts.keys()[0]]
                currentFeature = classCounts.keys()[0]
                for key in classCounts.keys():
                    if classCounts[key] > currentMax:
                        currentMax = classCounts[key]
                        currentFeature = key
                node.children[valueOfBest] = makePrunedSubtrees(newRemainingAttributes, newExamples, attributeValues,
                                                                className, currentFeature, setScoreFunc, gainFunc, q)
            return node
