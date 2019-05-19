from DataInterface import getExtraCreditDataset
from DecisionTree import makeTree, setEntropy, infoGain, makePrunedTree
import random
import time


def getAverageClassificaionRate(dataset, runs=20, testSize=200, setFunc=setEntropy, infoFunc=infoGain):
    """
    Randomly selects a test set and removes it from the training set.
    """
    scores = []
    examples, attrValues, labelName, labelValues = dataset
    l = len(examples) - 1
    print 'Starting test for average error for %d runs with test size %d' % (runs, testSize)
    for r in xrange(runs):
        runExamples = examples[:]
        test = []
        for i in xrange(testSize):
            test.append(runExamples.pop(random.randint(0, l - i)))
        tree = makeTree(runExamples, attrValues, labelName, setFunc, infoFunc)
        score = evaluateTree(tree, test, labelName)[0]
        print 'Score for run %d is %f' % (r + 1, score)
        scores.append(score)
    average = sum(scores) / float(runs)
    print 'Average classification rate over all runs: %f' % (average)
    return (scores, average)

def getAverageClassificaionRateWithPruning(dataset, runs=20, testSize=200, setFunc=setEntropy, infoFunc=infoGain):
    """
    Randomly selects a test set and removes it from the training set.
    """
    scores = []
    examples, attrValues, labelName, labelValues = dataset
    l = len(examples) - 1
    print 'Starting test for average error for %d runs with test size %d' % (runs, testSize)
    for r in xrange(runs):
        runExamples = examples[:]
        test = []
        for i in xrange(testSize):
            test.append(runExamples.pop(random.randint(0, l - i)))
        tree = makePrunedTree(runExamples, attrValues, labelName, setFunc, infoFunc, 0.9)
        score = evaluateTree(tree, test, labelName)[0]
        print 'Score for run %d is %f' % (r + 1, score)
        scores.append(score)
    average = sum(scores) / float(runs)
    print 'Average classification rate over all runs: %f' % (average)
    return (scores, average)


def evaluateTree(tree, testExamples, labelName):
    """
    Simple function to get the correct classification ratio for a given DTree
    and a set of testing examples.

    Args:
        testExamples (list<dictionary<str,str>>): list of examples to test with
        labelName (str): the name of the label
    Returns:
        tuple<float,
        list<tuple<str,str>>>
        Tuple
    """
    confusion = []
    f = 0.0
    for example in testExamples:
        z = tree.classify(example)
        if example[labelName] == z:
            f += 1.0
        else:
            confusion.append((example[labelName], z))
    return (f / len(testExamples), confusion)


def printDemarcation():
    print 'Done\n____________________________________________________________________\n'

def testAdultSetWithPruning(setFunc=setEntropy, infoFunc=infoGain):
    """Correct classification averate rate is about 0.95"""
    examples, attrValues, labelName, labelValues = getExtraCreditDataset()
    print 'Testing Adult dataset. Number of examples %d.' % len(examples)
    start = time.time()
    tree = makePrunedTree(examples, attrValues, labelName, setFunc, infoFunc, 0.9)
    end = time.time()
    print "Training time: ", (end - start)
    f = open('adult.out', 'w')
    f.write(str(tree))
    f.close()
    print 'Tree size: %d.\n' % tree.count()
    print 'Entire tree written out to adult.out in local directory\n'
    dataset = getExtraCreditDataset()
    evaluation = getAverageClassificaionRateWithPruning((examples, attrValues, labelName, labelValues))
    print 'Results for training set:\n%s\n' % str(evaluation)
    printDemarcation()
    return (tree, evaluation)

def testAdultSet(setFunc=setEntropy, infoFunc=infoGain):
    """Correct classification averate rate is about 0.95"""
    examples, attrValues, labelName, labelValues = getExtraCreditDataset()
    print 'Testing Adult dataset. Number of examples %d.' % len(examples)
    start = time.time()
    tree = makeTree(examples, attrValues, labelName, setFunc, infoFunc)
    end = time.time()
    print "Training time: ", (end - start)
    f = open('adult.out', 'w')
    f.write(str(tree))
    f.close()
    print 'Tree size: %d.\n' % tree.count()
    print 'Entire tree written out to adult.out in local directory\n'
    dataset = getExtraCreditDataset()
    evaluation = getAverageClassificaionRate((examples, attrValues, labelName, labelValues))
    print 'Results for training set:\n%s\n' % str(evaluation)
    printDemarcation()
    return (tree, evaluation)


if __name__ == '__main__':
    testAdultSet()