import re
from word import Word


class Uniparser:

    @classmethod
    def parseTrain(cls, file):
        f = open(file, "r")
        rawbody = f.read()
        return re.split('[^a-zA-Z]', rawbody)

    @classmethod
    def parseModel(cls, file):
        model = {}
        f = open(file, "r")
        for line in f:
            breakdown = line.split("  ")
            word = Word(breakdown[1])
            word.hamFreq = breakdown[2]
            word.hamSmoothP = breakdown[3]
            word.spamFreq = breakdown[4]
            word.spamSmoothP = breakdown[5]
            model[word.word] = word
        return model
