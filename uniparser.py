import re
from word import Word


class Uniparser:

    @classmethod
    def parseTrain(cls, file, mode, stopFile):
        if mode == 0:
            f = open(file, encoding="ISO-8859-1")
            rawbody = f.read()
            return re.split('[^a-zA-Z]', rawbody)

        elif mode == 1:
            s = open(stopFile, encoding="ISO-8859-1")
            f = open(file, encoding="ISO-8859-1")
            rawbody = f.read()
            tokenSet = re.split('[^a-zA-Z]', rawbody)
            for stopWord in s:
                if stopWord.strip() in tokenSet:
                   tokenSet = tokenSet.remove(stopWord)
            return tokenSet

        elif mode == 2:
            f = open(file, encoding="ISO-8859-1")
            rawbody = f.read()
            tokenSet = re.split('[^a-zA-Z]', rawbody)
            for token in tokenSet:
                if len(token) <= 2 or len(token) >= 9:
                    tokenSet = tokenSet.remove(token)
            return tokenSet



    @classmethod
    def parseModel(cls, file):
        model = {}
        f = open(file, encoding="ISO-8859-1")
        for line in f:
            breakdown = line.split("  ")
            word = Word(breakdown[1])
            word.hamFreq = float(breakdown[2])
            word.hamSmoothP = float(breakdown[3])
            word.spamFreq = float(breakdown[4])
            word.spamSmoothP = float(breakdown[5])
            model[word.word] = word
        return model

    @classmethod
    def parseModelArr(cls, file):
        model = []
        f = open(file, encoding="ISO-8859-1")
        for line in f:
            breakdown = line.split("  ")
            word = Word(breakdown[1])
            word.hamFreq = float(breakdown[2])
            word.hamSmoothP = float(breakdown[3])
            word.spamFreq = float(breakdown[4])
            word.spamSmoothP = float(breakdown[5])
            model.append(word)
        return model
