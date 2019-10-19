import sys
import math
import pandas as pd


class Root(object):
    left = None
    right = None
    attr = None

    def __init__(self, left, right, attr):
        self.left = left
        self.right = right
        self.attr = attr


class Leaf(object):
    label = None

    def __init__(self, label):
        self.label = label


def singleL(dataSet):
    labels = []
    for i in range (len(dataSet)):
        if dataSet[i][8] not in labels:
            labels.append(dataSet[i][8])

    return len(labels) == 1


def attribute(dataSet, attributeSet):
    maxInformationGain = -1
    maxInformationGainAttribute = attributeSet[0]
    for i in range(len(attributeSet)):
        informationGain = information(dataSet, attributeSet[i])
        if informationGain > maxInformationGain:
            maxInformationGain = informationGain
            maxInformationGainAttribute = attributeSet[i]
    if maxInformationGain==0:
        return None
    return maxInformationGainAttribute


def information(dataSet, attribute):
    oldEntropy = entropy(dataSet)
    # Create new sets based on attribute
    positives = []
    negatives = []
    for i in range(len(dataSet)):
        positive = False
        for j in range(8):
            if attribute == dataSet[i][j]:
                positive = True
        if positive == True:
            positives.append(dataSet[i])
        else:
            negatives.append(dataSet[i])
    positiveEntropy = entropy(positives)
    proportionOfPositiveData = float(len(positives)) / len(dataSet)
    negativeEntropy = entropy(negatives)
    proportionOfNegativeData = float(len(negatives)) / len(dataSet)
    newEntropy = positiveEntropy * proportionOfPositiveData + negativeEntropy *proportionOfNegativeData
    return oldEntropy - newEntropy


def entropy(dataSet):
    if len(dataSet) == 0:
        return 0
    positives = []
    negatives = []
    for i in range(len(dataSet)):
        if dataSet[i][8] == ">50K":
            positives.append(dataSet[i])
        else:
            negatives.append(dataSet[i])

    positiveProportion = float(len(positives) ) /len(dataSet)
    negativeProportion = float(len(negatives) ) /len(dataSet)
    entropy = 0
    if positiveProportion != 0:
        entropy = entropy + (-1) * (positiveProportion) * math.log(positiveProportion, 2)
    if negativeProportion != 0:
        entropy = entropy + (-1) * (negativeProportion) * math.log(negativeProportion, 2)

    return entropy


def majority(dataSet):
    dictionary = {}
    for i in range(len(dataSet)):
        if dictionary.has_key(dataSet[i][8]):
            dictionary[dataSet[i][8]] = dictionary.get(dataSet[i][8]) + 1
        else:
            dictionary[dataSet[i][8]] = 1
    keys = dictionary.keys()
    maxNum = 0
    maxKey = keys[0]
    for i in range(len(keys)):
        if (dictionary[keys[i]] > maxNum):
            maxNum = dictionary[keys[i]]
            maxKey = keys[i]
    return maxKey


def containsAttribute(dp, attribute):
    for i in range(0, 8):
        if dp[i] == attribute:
            return True
    return False


def calculateLabel(dp, root):
    if type(root) == Root:
        if containsAttribute(dp, root.attr):
            return calculateLabel(dp, root.left)
        else:
            return calculateLabel(dp, root.right)
    else:
        return root.label


def calculateAccuracy(root, dataSet):
    num = 0
    for i in range(len(dataSet)):
        actualLabel = dataSet[i][8]
        predictedLabel = calculateLabel(dataSet[i], root)
        if actualLabel != predictedLabel:
            num += 1

    return 1 - (float(num) / len(dataSet))


def sameAttributes(dataSet):
    prev = dataSet[0]
    for i in range(len(dataSet)):
        curr = dataSet[i]
        for j in range(8):
            if prev[j] != curr[j]:
                return False
        prev = curr
    return True


def numberNodes(root):
    if type(root) == Leaf:
        return 1

    count = 1 + numberNodes(root.left) + numberNodes(root.right)
    return count


def createPrune(node):
    if type(node) == Leaf:
        return None
    else:
        label = majority(node.dataSet)
        return Leaf(label)


def pruner(root, node, dataSet):
    if type(node) == Leaf:
        return
    pruner(root, node.left, dataSet)
    pruner(root, node.right, dataSet)
    originalLeft = node.left
    originalRight = node.right
    prunedLeft = createPrune(node.left)
    prunedRight = createPrune(node.right)
    originalAccuracy = calculateAccuracy(root, dataSet)
    if prunedRight != None:
        node.right = prunedRight
        newAccuracy = calculateAccuracy(root, dataSet)
        if newAccuracy < originalAccuracy:
            node.right = originalRight
    if prunedLeft != None:
        node.left = prunedLeft
        newAccuracy = calculateAccuracy(root, dataSet)
        if newAccuracy < originalAccuracy:
            node.left = originalLeft


def prune(root, validationSet):
    prevAccuracy = -1
    currAccuracy = calculateAccuracy(root, validationSet)
    while (currAccuracy > prevAccuracy):
        prevAccuracy = currAccuracy
        pruner(root, root, validationSet)
        currAccuracy = calculateAccuracy(root, validationSet)


def initVanilla(dataSet, attributeSet):
    if (singleL(dataSet)):
        return Leaf(dataSet[0][8])

    elif len(attributeSet) == 0 or sameAttributes(dataSet):
        majorityLabel = majority(dataSet)
        return Leaf(majorityLabel)

    else:
        A = attribute(dataSet, attributeSet)
        if A == None:
            majorityLabel = majority(dataSet)
            return Leaf(majorityLabel)
        attributeSet.remove(A)
        positiveSet = []
        negativeSet = []
        for i in range(len(dataSet)):
            if containsAttribute(dataSet[i], A):
                positiveSet.append(dataSet[i])
            else:
                negativeSet.append(dataSet[i])

        if len(positiveSet) > 0:
            leftBranch = initVanilla(positiveSet, list(attributeSet))
        else:
            majorityLabel = majority(dataSet)
            leftBranch = Leaf(majorityLabel)

        if len(negativeSet) > 0:
            rightBranch = initVanilla(negativeSet, list(attributeSet))
        else:
            majorityLabel = majority(dataSet)
            rightBranch = Leaf(majorityLabel)
        rootNode = Root(leftBranch, rightBranch, A)
        return rootNode


def initDepth(dataSet, attributeSet, maxDepth, currentDepth):
    if currentDepth >= maxDepth:
        majorityLabel = majority(dataSet)
        return Leaf(majorityLabel)

    if (singleL(dataSet)):
        return Leaf(dataSet[0][8])

    elif len(attributeSet) == 0 or sameAttributes(dataSet):
        majorityLabel = majority(dataSet)
        return Leaf(majorityLabel)

    else:
        A = attribute(dataSet, attributeSet)
        if A == None:
            majorityLabel = majority(dataSet)
            return Leaf(majorityLabel)
        attributeSet.remove(A)
        positiveSet = []
        negativeSet = []
        for i in range(len(dataSet)):
            if containsAttribute(dataSet[i], A):
                positiveSet.append(dataSet[i])
            else:
                negativeSet.append(dataSet[i])

        if len(positiveSet) > 0 and currentDepth < maxDepth:
            leftBranch = initDepth(positiveSet, list(attributeSet), maxDepth, currentDepth + 1)
        else:
            majorityLabel = majority(dataSet)
            leftBranch = Leaf(majorityLabel)

        if len(negativeSet) > 0 and currentDepth < maxDepth:
            rightBranch = initDepth(negativeSet, list(attributeSet), maxDepth, currentDepth + 1)
        else:
            majorityLabel = majority(dataSet)
            rightBranch = Leaf(majorityLabel)
        rootNode = Root(leftBranch, rightBranch, A)
        return rootNode


def initPrune(dataSet, attributeSet):
    if (singleL(dataSet)):
        leafNode = Leaf(dataSet[0][8])
        return leafNode

    elif len(attributeSet) == 0 or sameAttributes(dataSet):
        majorityLabel = majority(dataSet)
        leafNode = Leaf(majorityLabel)
        return leafNode

    else:
        A = attribute(dataSet, attributeSet)
        if A == None:
            majorityLabel = majority(dataSet)
            return Leaf(majorityLabel)
        attributeSet.remove(A)
        positiveSet = []
        negativeSet = []
        for i in range(len(dataSet)):
            if containsAttribute(dataSet[i], A):
                positiveSet.append(dataSet[i])
            else:
                negativeSet.append(dataSet[i])

        if len(positiveSet) <= 0:
            majorityLabel = majority(dataSet)
            leftBranch = Leaf(majorityLabel)
        else:
            leftBranch = initPrune(positiveSet, list(attributeSet))

        if len(negativeSet) <= 0:
            majorityLabel = majority(dataSet)
            rightBranch = Leaf(majorityLabel)
        else:
            rightBranch = initPrune(negativeSet, list(attributeSet))

        rootNode = Root(leftBranch, rightBranch, A)
        rootNode.dataSet = dataSet
        return rootNode


file1 = sys.argv[1]
file2 = sys.argv[2]
model = sys.argv[3]
size = sys.argv[4]

data = pd.read_csv(file1, sep=", ", quotechar="\"", header=None, engine="python")
X = data.as_matrix()

data = pd.read_csv(file2, sep=", ", quotechar="\"", header=None, engine="python")
testData = data.as_matrix()

size = float(size)

validationSetSize = 0
validationSet = []

if len(sys.argv) > 5 and sys.argv[5].isdigit():
    validationSetSize = float(sys.argv[5])
    validationDataNumber = int(math.floor(len(X) * (validationSetSize * .01)))
    validationSet = X[len(X) - validationDataNumber:]

trainingSetNumber = int(math.floor(len(X) * (size * .01)))
trainingSet = X[:trainingSetNumber]


attributes = []
for i in range(8):
    for j in range(len(X)):
        if X[j][i] not in attributes:
            attributes.append(X[j][i])

if model == "vanilla":
    root = initVanilla(trainingSet, attributes)
    trainingAccuracy = calculateAccuracy(root, trainingSet)
    testAccuracy = calculateAccuracy(root, testData)

    print "Training set accuracy: %0.4f " % trainingAccuracy
    print "Test set accuracy: %0.4f" % testAccuracy

elif model == "depth":
    depth = int(sys.argv[6])
    root = initDepth(trainingSet, attributes, depth, 0)

    trainingAccuracy = calculateAccuracy(root, trainingSet)
    validationAccuracy = calculateAccuracy(root, validationSet)
    testAccuracy = calculateAccuracy(root, testData)

    print "Training set accuracy: %0.4f " % trainingAccuracy
    print "Validation set accuracy: %0.4f" % validationAccuracy
    print "Test set accuracy: %0.4f" % testAccuracy


elif model == "prune":
    root = initPrune(trainingSet, attributes)
    prune(root, validationSet)
    trainingAccuracy = calculateAccuracy(root, trainingSet)
    testAccuracy = calculateAccuracy(root, testData)

    print "Training set accuracy: %0.4f " % trainingAccuracy
    print "Test set accuracy: %0.4f" % testAccuracy


