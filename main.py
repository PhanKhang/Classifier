from os import listdir
import sys
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
    stop = (input("Use stop words? (0 - False by default):") or 0)
    if stop:
        stopFile = (input("Stop file name? (English-Stop-Words.txt by default)") or 'English-Stop-Words.txt')
    vocabFile = (input("Vocabulary file name (vocab.txt by default):") or 'vocab.txt')
    modelBuilder.delta = delta
    spamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "spam" in f]
    hamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "ham" in f]
    progress = 0
    count = 0
    total = len(hamSet)+len(spamSet)
    for hamFile in hamSet:
        count+=1
        progress = count*100/total
        hamTokenSet = Uniparser.parseTrain(trainPath+'/'+hamFile,stop,stopFile)
        modelBuilder.createWords(hamTokenSet, 'ham')
        sys.stdout.flush()
        sys.stdout.write("progress: %d%%   \r" % (progress))

    for spamFile in spamSet:
        count += 1
        progress = count*100/total
        spamTokenSet = Uniparser.parseTrain(trainPath+'/'+spamFile,stop,stopFile)
        modelBuilder.createWords(spamTokenSet, 'spam')
        sys.stdout.flush()
        sys.stdout.write("progress: %d%%   \r" % (progress))


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