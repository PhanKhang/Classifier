from testresult import Testresult
from math import log10


class Classifier:
    def __init__(self):
        self.testResults = []
        self.counter = 0

    def classify(self, name, tokenSet, model, p):
        testresult = Testresult(name)
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
        self.testResults.append(testresult.toString())




