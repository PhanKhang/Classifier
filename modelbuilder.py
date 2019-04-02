from word import Word
from decimal import *
import math

class ModelBuilder:
    def __init__(self):
        self.delta = 0
        self.tokens = []
        self.words = {}
        self.hamWordsCount = 0
        self.spamWordsCount = 0

    def createWords(self, tokenSet, mailtype):
        for token in tokenSet:
            ltoken = token.lower()
            if mailtype == 'ham':
                if ltoken in self.tokens and ltoken != '':
                    self.hamWordsCount += 1
                    self.words[ltoken].hamFreq += 1
                elif ltoken != '':
                    self.tokens.append(ltoken)
                    word = Word(ltoken)
                    word.hamFreq = 1
                    self.hamWordsCount += 1
                    self.words[ltoken] = word
            elif mailtype == 'spam':
                if ltoken in self.tokens and ltoken != '':
                    self.words[ltoken].spamFreq += 1
                    self.spamWordsCount += 1
                elif ltoken != '':
                    self.tokens.append(ltoken)
                    word = Word(ltoken)
                    word.spamFreq = 1
                    self.spamWordsCount += 1
                    self.words[ltoken] = word


    def caclulateProbabilitiesi(self):
        deltav = float(len(self.tokens) * self.delta)
        for token, word in self.words.items():
            word.hamSmoothP = float(word.hamFreq + self.delta) / float(self.hamWordsCount + deltav)
            word.spamSmoothP = float(word.spamFreq + self.delta) / float(self.spamWordsCount + deltav)

    def caclulateProbabilities(self, vSize):
        deltav = float(vSize * self.delta)
        for token, word in self.words.items():
            word.hamSmoothP = float(word.hamFreq + self.delta) / float(self.hamWordsCount + deltav)
            word.spamSmoothP = float(word.spamFreq + self.delta) / float(self.spamWordsCount + deltav)

    def getWords(self):
        result = []
        counter = 1
        for token in sorted(self.words.keys()):
            result.append(str(counter) + "  " + token + "  " + str(self.words[token].hamFreq) + "  " + str(self.words[
                token].hamSmoothP) + "  " + str(self.words[token].spamFreq) + "  " + str(self.words[token].spamSmoothP)+"\n")
            counter += 1
        return result
