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
    f = open(file, encoding="ISO-8859-1")
    rawbody = f.read()
    return re.split('[^a-zA-Z]', rawbody)


def train():
    trainPath = (input("Folder with training set (train by default):") or 'train')
    delta = float((input("Smoothing delta (0.5 by default):") or 0.5))
    mode = int(input(
        "Select Mode:\n1-Use stop words\n2-Use word length filtering\n3-Use infrequent word filtering\n0-no mode\n(0 - no mode (default)):") or 0)
    vocabAv = 'no'
    if mode == 1:
        stopFile = (input("Stop file name? (English-Stop-Words.txt by default)") or 'English-Stop-Words.txt')
        vocabFile = (input("Vocabulary file name (stopword-model.txt by default):") or 'stopword-model.txt')
        vocabAv = (input(
            "Is Vocabulary file available if yes provide name? no if not (vocab.txt by default):") or 'vocab.txt')
    elif mode == 2:
        vocabFile = (input("Vocabulary file name (wordlength-model.txt by default):") or 'wordlength-model.txt')
        vocabAv = (input(
            "Is Vocabulary file available if yes provide name? no if not (vocab.txt by default):") or 'vocab.txt')
    elif mode == 3:
        vocabFile = (input("Vocabulary file name (fmodel.txt by default):") or 'fmodel.txt')
        vocabAv = (input(
            "Please provide vocabulary file (vocab.txt by default):") or 'vocab.txt')
    else:
        vocabFile = (input("Vocabulary file name (vocab.txt by default):") or 'vocab.txt')
    modelBuilder.delta = delta

    if vocabAv == 'no':
        spamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "spam" in f]
        hamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "ham" in f]
        progress = 0
        count = 0
        total = len(hamSet) + len(spamSet)
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
    elif mode == 1:
        model = Uniparser.parseModel(vocabAv)
        s = open(stopFile, encoding="ISO-8859-1")
        tokenSet = []

        hamWordCount = 0
        spamWordCount = 0

        for token, word in model.items():
            tokenSet.append(token)
        for w in s:
            for token in tokenSet:
                if w.strip() == token:
                    model.pop(token, None)

        for token, word in model.items():
            hamWordCount += word.hamFreq
            spamWordCount += word.spamFreq

        modelBuilder.hamWordsCount = hamWordCount
        modelBuilder.spamWordsCount = spamWordCount
        modelBuilder.words = model

        modelBuilder.caclulateProbabilities()
        va = modelBuilder.getWords()
        vf = open(vocabFile, 'a')
        for line in va:
            vf.write(line)
    elif mode == 2:
        model = Uniparser.parseModel(vocabAv)
        tokenSet = []

        hamWordCount = 0
        spamWordCount = 0

        for token, word in model.items():
            tokenSet.append(token)
        for token in tokenSet:
            if len(token) <= 2 or len(token) >= 9:
                model.pop(token, None)

        for token, word in model.items():
            hamWordCount += word.hamFreq
            spamWordCount += word.spamFreq

        modelBuilder.hamWordsCount = hamWordCount
        modelBuilder.spamWordsCount = spamWordCount
        modelBuilder.words = model

        modelBuilder.caclulateProbabilities()
        va = modelBuilder.getWords()
        vf = open(vocabFile, 'a')
        for line in va:
            vf.write(line)
    elif mode == 3:
        model = Uniparser.parseModel(vocabAv)
        hamWordCount = 0
        spamWordCount = 0

        vocabFilePre = vocabFile.split('.')[0]

        sortedModelHam = sorted(model.items(), key=lambda x: x[1].hamFreq, reverse=True)
        sortedModelSpam = sorted(model.items(), key=lambda x: x[1].spamFreq, reverse=True)

        for token, word in sortedModelHam:
            if word.hamFreq == 1 or word.spamFreq == 1:
                model.pop(token, None)

        for token, word in model.items():
            hamWordCount += word.hamFreq
            spamWordCount += word.spamFreq

        modelBuilder.hamWordsCount = hamWordCount
        modelBuilder.spamWordsCount = spamWordCount
        modelBuilder.words = model

        modelBuilder.caclulateProbabilities()
        va = modelBuilder.getWords()
        vf = open(vocabFilePre+'1'+'.txt', 'a')
        for line in va:
            vf.write(line)

        #######################################################
        for i in range(1,5):
            hamWordCount = 0
            spamWordCount = 0
            for token, word in sortedModelHam:
                if word.hamFreq <= 5*i or word.spamFreq <= 5*i:
                    model.pop(token, None)

            for token, word in model.items():
                hamWordCount += word.hamFreq
                spamWordCount += word.spamFreq

            modelBuilder.hamWordsCount = hamWordCount
            modelBuilder.spamWordsCount = spamWordCount
            modelBuilder.words = model

            modelBuilder.caclulateProbabilities()
            va = modelBuilder.getWords()
            vf = open(vocabFilePre+str(i*5)+'.txt', 'a')
            for line in va:
                vf.write(line)
        #######################################################
        for i in range(1,6):
            model = model = Uniparser.parseModel(vocabAv)
            sortedModelHam = sorted(model.items(), key=lambda x: x[1].hamFreq, reverse=True)
            sortedModelSpam = sorted(model.items(), key=lambda x: x[1].spamFreq, reverse=True)
            size = len(sortedModelSpam)

            cutOff = size * 0.05 * i

            hamWordCount = 0
            spamWordCount = 0

            count = 0
            for token, word in sortedModelHam:
                model.pop(token, None)
                count += 1
                if count >= cutOff:
                    break
            count = 0
            for token, word in sortedModelSpam:
                model.pop(token, None)
                count += 1
                if count >= cutOff:
                    break

            for token, word in model.items():
                hamWordCount += word.hamFreq
                spamWordCount += word.spamFreq

            modelBuilder.hamWordsCount = hamWordCount
            modelBuilder.spamWordsCount = spamWordCount
            modelBuilder.words = model

            modelBuilder.caclulateProbabilities()
            va = modelBuilder.getWords()
            vf = open(vocabFilePre+str(i*5)+'p.txt', 'a')
            for line in va:
                vf.write(line)





def classify():
    vocabFile = (input("Vocabulary file name (vocab.txt by default):") or 'vocab.txt')
    trainPath = (input("Folder with training set (train by default):") or 'train')
    testPath = (input("Folder with test set (test by default):") or 'test')
    resultFile = (input("Result file name (result.txt by default):") or 'result.txt')
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

    print("Precision Ham = " + str(classifier.precision('ham')))
    print("Recall Ham = " + str(classifier.recall('ham')))
    p = classifier.precision('ham')
    r = classifier.recall('ham')
    b = 1
    print("F1 Ham = " + str((b * b + 1) * p * r / (b * b * p + r)))
    print("__________________________________________")
    print("Precision Spam = " + str(classifier.precision('Spam')))
    print("Recall Spam = " + str(classifier.recall('Spam')))
    p = classifier.precision('Spam')
    r = classifier.recall('Spam')
    b = 1
    print("F1 Spam = " + str((b * b + 1) * p * r / (b * b * p + r)))

    print("Accuracy = " + str(classifier.accuracy()))
    print("Confusion matrix: ")
    print(classifier.conFusionMatrix)

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
