import sys
import pandas as pd
import math


def train(data):
    pwl = len(data[0])
    truevalue = {}
    falsevalue = {}
    goodtrue = 0
    goodfalse = 0
    truesubset = []
    falsesubset = []

    for each in data:
        if each[pwl - 1] == 1:
            goodtrue += 1
            truesubset.append(each)
        elif each[pwl - 1] == 0:
            goodfalse += 1
            falsesubset.append(each)

    for each in data:
        for i in range(len(each) - 1):
            if i not in truevalue:
                truevalue[i] = {}
            if i not in falsevalue:
                falsevalue[i] = {}
            if each[i] not in truevalue[i]:
                truevalue[i][each[i]] = 0
            if each[i] not in falsevalue[i]:
                falsevalue[i][each[i]] = 0
          
    for each in truesubset:
        for i in range(len(each) - 1):
            truevalue[i][each[i]] = truevalue[i][each[i]] + 1

    for each in falsesubset:
        for i in range(len(each) - 1):
            falsevalue[i][each[i]] = falsevalue[i][each[i]] + 1
    return goodtrue, goodfalse, truevalue, falsevalue


def predict(numberTrue, numberFalse, trueDictionary, falseDictionary, point):
    tVal = 1
    fVal = 1
    for i in range(len(point) - 1):
        if point[i] in trueDictionary[i]:
            toBeAdded = (trueDictionary[i][point[i]] + 1.0) / (numberTrue + len(trueDictionary[i]))
            tVal *= toBeAdded
        else:
            toBeAdded = (1.0) / (len(trueDictionary[i]))
            tVal *= toBeAdded
        if point[i] in falseDictionary[i]:
            toBeAdded = (falseDictionary[i][point[i]] + 1.0) / (numberFalse + len(falseDictionary[i]))
            fVal *= toBeAdded
        else:
            toBeAdded = (1.0) / (len(falseDictionary[i]))
            fVal *= toBeAdded
    tVal *= float(numberTrue) / (numberTrue + numberFalse)
    fVal *= (float(numberFalse)) / (numberTrue + numberFalse)


    if tVal >= fVal:
        return 1
    else:
        return 0


def calcLoss(numberTrue, numberFalse, trueDictionary, falseDictionary, data):
    pwl = len(data[0])
    count = 0
    for each in data:
        if predict(numberTrue, numberFalse, trueDictionary, falseDictionary, each) != each[pwl - 1]:
            count = count + 1
    return float(count) / len(data)

trainFile = sys.argv[1]
testFile = sys.argv[2]

data = pd.read_csv(trainFile, sep=",", quotechar='"', engine='python')
trainingData = data.as_matrix()

dataTest = pd.read_csv(testFile, sep=",", quotechar='"', engine='python')
testData = dataTest.as_matrix()

trueNum, falseNum, trueDict, falseDict = train(trainingData)
val = calcLoss(trueNum, falseNum, trueDict, falseDict, testData)
#sqloss = squaredLoss(trueNum, falseNum, trueDict, falseDict, testData)

print "ZERO-ONE LOSS=%.4f" % val

#print "ZERO-ONE LOSS=%.4f" % sqloss
