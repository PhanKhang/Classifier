from os import listdir
import sys
from os.path import isfile, join
from modelbuilder import ModelBuilder
from classifier import Classifier
from uniparser import Uniparser
from retrainer import Retrainer
import re

modelBuilder = ModelBuilder()
classifier = Classifier()


def parseFile(file):
    f = open(file, encoding="ISO-8859-1")
    rawbody = f.read()
    return re.split('[^a-zA-Z]', rawbody)


def train():
    trainPath = (input("Folder with training set (train by default):") or 'train')
    mode = int(input(
        "Select Mode:"
        "\n1-Use stop words"
        "\n2-Use word length filtering"
        "\n3-Use infrequent word filtering"
        "\n4-Use retrain model with different delta"
        "\n0-no mode, regenerate model"
        "\n0 - no mode (default):") or 0)
    vocabAv = 'no'
    inputParameter = ''
    if mode == 1:
        vocabFile = (input("New Vocabulary file name (stopword-model.txt by default):") or 'stopword-model.txt')
        vocabAv = (input(
            "Please provide vocabulary file (baseline.txt by default):") or 'baseline.txt')
        inputParameter = (input("Stop file name? (English-Stop-Words.txt by default)") or 'English-Stop-Words.txt')
        delta = float((input("Smoothing delta (0.5 by default):") or 0.5))
    elif mode == 2:
        vocabFile = (input("New Vocabulary file name (wordlength-model.txt by default):") or 'wordlength-model.txt')
        vocabAv = (input(
            "Please provide vocabulary file (baseline.txt by default):") or 'baseline.txt')
        delta = float((input("Smoothing delta (0.5 by default):") or 0.5))
    elif mode == 3:
        vocabFile = (input("New Vocabulary file name (frequency-model.txt by default):") or 'frequency-model.txt')
        vocabAv = (input(
            "Please provide vocabulary file (baseline.txt by default):") or 'baseline.txt')
        inputParameter = (input(
            "Please indicate action and filtering frequency (i.e = 1 or <= 1 ) or if it is top percentage "
            "filtering then input percentage wihtout % sign (i.e top 5 -- as top 5 %) (default <= 1):") or '<= 1')
        delta = float((input("Smoothing delta (0.5 by default):") or 0.5))
    elif mode == 4:
        vocabFile = (input("New Vocabulary file name (delta-model.txt by default):") or 'delta-model.txt')
        vocabAv = (input(
            "Please provide vocabulary file (baseline.txt by default):") or 'baseline.txt')
        delta = float((input("Smoothing delta (0.5 by default):") or 0.5))
    else:
        vocabFile = (input("Vocabulary file name (baseline.txt by default):") or 'baseline.txt')
    modelBuilder.delta = float(delta)

    if vocabAv == 'no':
        spamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "spam" in f]
        hamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "ham" in f]
        progress = 0
        count = 0
        total = len(hamSet) + len(spamSet)
        mode = 0
        stopFile = ''
        for hamFile in hamSet:
            count += 1
            progress = count * 100 / total
            hamTokenSet = Uniparser.parseTrain(trainPath + '/' + hamFile, mode, stopFile)
            modelBuilder.createWords(hamTokenSet, 'ham')
            sys.stdout.flush()
            sys.stdout.write("progress: %d%%   \r" % (progress))

        for spamFile in spamSet:
            count += 1
            progress = count * 100 / total
            spamTokenSet = Uniparser.parseTrain(trainPath + '/' + spamFile, mode, stopFile)
            modelBuilder.createWords(spamTokenSet, 'spam')
            sys.stdout.flush()
            sys.stdout.write("progress: %d%%   \r" % (progress))

        modelBuilder.caclulateProbabilities()
        va = modelBuilder.getWords()
        vf = open(vocabFile, 'a')
        for line in va:
            vf.write(line)

    else:
        Retrainer().retrainSet(vocabAv, vocabFile, mode, inputParameter, delta)


def classify():
    vocabFile = (input("Vocabulary file name (baseline.txt by default):") or 'baseline.txt')
    trainPath = (input("Folder with training set (train by default):") or 'train')
    testPath = (input("Folder with test set (test by default):") or 'test')
    resultFile = (input("Result file name (result-" + vocabFile.split('.')[0] + ".txt by default):")
                  or 'result-' + vocabFile.split('.')[0] + '.txt')
    spamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "spam" in f]
    hamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "ham" in f]
    pHam = float(len(hamSet) / (len(hamSet) + len(spamSet)))
    pSpam = float(len(spamSet) / (len(hamSet) + len(spamSet)))

    model = Uniparser.parseModel(vocabFile)
    testSpamSet = [f for f in listdir(testPath) if isfile(join(testPath, f)) and "spam" in f]
    testHamSet = [f for f in listdir(testPath) if isfile(join(testPath, f)) and "ham" in f]

    for hamTestFile in testHamSet:
        hamTestTokenSet = Uniparser.parseTrain(testPath + '/' + hamTestFile, 0, '')
        classifier.classify(hamTestFile, hamTestTokenSet, model, pHam)
    for spamTestFile in testSpamSet:
        spamTestTokenSet = Uniparser.parseTrain(testPath + '/' + spamTestFile, 0, '')
        classifier.classify(spamTestFile, spamTestTokenSet, model, pSpam)

    va = classifier.testResults
    vf = open(resultFile, 'a')
    for line in va:
        vf.write(line)

    print("__________________________________________")
    print("Precision Spam = " + str(round(classifier.precision('Spam'), 6)))
    print("Recall Spam = " + str(round(classifier.recall('Spam'), 6)))
    p = classifier.precision('Spam')
    r = classifier.recall('Spam')
    b = 1
    print("F1 Spam = " + str(round((b * b + 1) * p * r / (b * b * p + r), 6)))
    print("__________________________________________")
    print("Precision Ham = " + str(round(classifier.precision('ham'), 6)))
    print("Recall Ham = " + str(round(classifier.recall('ham'), 6)))
    p = classifier.precision('ham')
    r = classifier.recall('ham')
    b = 1
    print("F1 Ham = " + str(round((b * b + 1) * p * r / (b * b * p + r), 6)))
    print("__________________________________________")
    print("Accuracy = " + str(classifier.accuracy()))
    print("Confusion matrix: ")
    print(classifier.conFusionMatrix)


def main():
    action = input("what are we doing? (1 - train, 2 - classify):")
    if action == str(1):
        train()
    elif action == str(2):
        classify()


main()
