from testresult import Testresult
from math import log10
import numpy as np


class Classifier:
    def __init__(self):
        self.testResults = []
        self.counter = 0
        self.TpHam = 0
        self.FpHam = 0
        self.TpSpam = 0
        self.FpSpam = 0

        self.FnSpam = 0  # false negative
        self.FnHam = 0  # false negativeself.
        self.TnSpam = 0  # true negative
        self.TnHam = 0  # true negative

        self.conFusionMatrix = np.zeros((2, 2))

    def classify(self, name, tokenSet, model, p):
        testresult = Testresult(name)
        actualclass = name.split("-")[1]
        self.counter += 1
        testresult.counter = self.counter
        testresult.hamscore = log10(p)
        testresult.spamscore = log10(p)
        for token in tokenSet:
            if token in model:
                word = model[token]
                ltoken = token.lower()
                testresult.hamscore += log10(word.hamSmoothP)
                testresult.spamscore += log10(word.spamSmoothP)
        testresult.derivedclass = 'ham'
        if testresult.spamscore > testresult.hamscore:
            testresult.derivedclass = 'spam'
        if actualclass == 'ham':
            if actualclass == testresult.derivedclass:
                self.conFusionMatrix[0][0] += 1
            else:
                self.conFusionMatrix[1][0] += 1

        else:
            if actualclass == testresult.derivedclass:
                self.conFusionMatrix[1][1] += 1
            else:
                self.conFusionMatrix[0][1] += 1
        self.testResults.append(testresult.toString())

    def precision(self, label):
        if label == 'ham':
            return self.conFusionMatrix[0][0] / (self.conFusionMatrix[0][0] + self.conFusionMatrix[1][0])
        else:
            return self.conFusionMatrix[1][1] / (self.conFusionMatrix[1][1] + self.conFusionMatrix[0][1])

    def recall(self, label):
        if label == 'ham':
            return self.conFusionMatrix[0][0] / (self.conFusionMatrix[0][0] + self.conFusionMatrix[0][1])
        else:
            return self.conFusionMatrix[1][1] / (self.conFusionMatrix[1][1] + self.conFusionMatrix[1][0])

    def accuracy(self):
        return (self.conFusionMatrix[1][1] + self.conFusionMatrix[0][0]) \
               / (self.conFusionMatrix[0][0] + self.conFusionMatrix[0][1]
                  + self.conFusionMatrix[1][1] + self.conFusionMatrix[1][0])
