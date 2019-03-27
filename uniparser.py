import re
from word import Word


class Uniparser:

    @classmethod
    def parseTrain(cls, file):
        f = open(file, encoding = "ISO-8859-1")
        rawbody = f.read()
        return re.split('[^a-zA-Z]', rawbody)

    @classmethod
    def parseModel(cls, file):
        model = {}
        f = open(file, "r")
        for line in f:
            breakdown = line.split("  ")
            word = Word(breakdown[1])
            word.hamFreq = float(breakdown[2])
            word.hamSmoothP = float(breakdown[3])
            word.spamFreq = float(breakdown[4])
            word.spamSmoothP = float(breakdown[5])
            model[word.word] = word
        return model
