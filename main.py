from os import listdir
from os.path import isfile, join
from modelbuilder import ModelBuilder
from classifier import Classifier
from uniparser import Uniparser
import re

modelBuilder = ModelBuilder()
classifier = Classifier()


def parseFile(file):
    f = open(file, encoding = "ISO-8859-1")
    rawbody = f.read()
    return re.split('[^a-zA-Z]', rawbody)

def train():
    trainPath = (input("Folder with training set (train by default):") or 'train')
    delta = float((input("Smoothing delta (0.5 by default):") or 0.5))
    vocabFile = (input("Vocabulary file name (vocab.txt by default):") or 'vocab.txt')
    modelBuilder.delta = delta
    spamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "spam" in f]
    hamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "ham" in f]
    for hamFile in hamSet:
        hamTokenSet = Uniparser.parseTrain(trainPath+'/'+hamFile)
        modelBuilder.createWords(hamTokenSet, 'ham')
    for spamFile in spamSet:
        spamTokenSet = Uniparser.parseTrain(trainPath+'/'+spamFile)
        modelBuilder.createWords(spamTokenSet, 'spam')

    modelBuilder.caclulateProbabilities()
    va = modelBuilder.getWords()
    vf = open(vocabFile, 'a')
    for line in va:
        vf.write(line)


def classify():
    vocabFile = (input("Vocabulary file name (vocab.txt by default):") or 'vocab.txt')
    trainPath = (input("Folder with training set (train by default):") or 'train')
    testPath = (input("Folder with test set (test by default):") or 'test')
    resultFile = (input("Result file name (result.txt by default):") or 'result.txt')
    spamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "spam" in f]
    hamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "ham" in f]
    pHam = float(len(hamSet)/(len(hamSet)+len(spamSet)))
    pSpam = float(len(spamSet) / (len(hamSet) + len(spamSet)))

    model = Uniparser.parseModel(vocabFile)
    testSpamSet = [f for f in listdir(testPath) if isfile(join(testPath, f)) and "spam" in f]
    testHamSet = [f for f in listdir(testPath) if isfile(join(testPath, f)) and "ham" in f]
    for hamTestFile in testHamSet:
        hamTestTokenSet = Uniparser.parseTrain(testPath+'/'+hamTestFile)
        classifier.classify(hamTestFile, hamTestTokenSet, model, pHam)
    for spamTestFile in testSpamSet:
        spamTestTokenSet = Uniparser.parseTrain(testPath+'/'+spamTestFile)
        classifier.classify(spamTestFile, spamTestTokenSet, model, pSpam)

    va = classifier.testResults
    vf = open(resultFile, 'a')
    for line in va:
        vf.write(line)


def main():
    action = input("what are we doing? (1 - train, 2 - classify):")
    if action == str(1):
        train()
    elif action == str(2):
        classify()


main()