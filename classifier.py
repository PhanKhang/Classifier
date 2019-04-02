from testresult import Testresult
from math import log10
from math import inf
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
                if testresult.hamscore > 0.0:
                    testresult.hamscore += log10(word.hamSmoothP)
                else:
                    testresult.hamscore = - inf
                if testresult.spamscore > 0.0:
                    testresult.spamscore += log10(word.spamSmoothP)
                else:
                    testresult.spamscore = - inf
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
            if float(self.conFusionMatrix[0][0] + self.conFusionMatrix[1][0]) > 0:
                return float(self.conFusionMatrix[0][0]) / float(self.conFusionMatrix[0][0] + self.conFusionMatrix[1][0])
            return inf
        else:
            if float(self.conFusionMatrix[1][1] + self.conFusionMatrix[0][1]) > 0:
                return float(self.conFusionMatrix[1][1]) / float(self.conFusionMatrix[1][1] + self.conFusionMatrix[0][1])
            return inf

    def recall(self, label):
        if label == 'ham':
            if float(self.conFusionMatrix[0][0] + self.conFusionMatrix[0][1]) > 0:
                return float(self.conFusionMatrix[0][0]) / float(self.conFusionMatrix[0][0] + self.conFusionMatrix[0][1])
            return inf
        else:
            if float(self.conFusionMatrix[1][1] + self.conFusionMatrix[1][0]) > 0:
                return float(self.conFusionMatrix[1][1]) / float(self.conFusionMatrix[1][1] + self.conFusionMatrix[1][0])
            return inf

    def accuracy(self):
        return float(self.conFusionMatrix[1][1] + self.conFusionMatrix[0][0]) \
               / float(self.conFusionMatrix[0][0] + self.conFusionMatrix[0][1]
                  + self.conFusionMatrix[1][1] + self.conFusionMatrix[1][0])
