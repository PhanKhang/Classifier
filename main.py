from os import listdir
from os.path import isfile, join
#from parser import Parser
from modelbuilder import ModelBuilder
import re

modelBuilder = ModelBuilder()


def parseFile(file):
    f = open(file, "r")
    rawbody = f.read()
    return re.split('[^a-zA-Z]', rawbody)

def train():
    trainPath = (input("Folder with training set (train by default):") or 'train')
    delta = int((input("Smoothing delta (0.5 by default):") or 0.5))
    vocabFile = (input("Vocabulary file name (vocab.txt by default):") or 'vocab.txt')
    modelBuilder.delta = delta
    spamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "spam" in f]
    hamSet = [f for f in listdir(trainPath) if isfile(join(trainPath, f)) and "ham" in f]
    for hamFile in hamSet:
        hamTokenSet = parseFile(trainPath+'/'+hamFile)
        modelBuilder.createWords(hamTokenSet, 'ham')
    for spamFile in spamSet:
        spamTokenSet = parseFile(trainPath+'/'+spamFile)
        modelBuilder.createWords(spamTokenSet, 'spam')

    modelBuilder.caclulateProbabilities()
    va = modelBuilder.getWords()
    vf = open(vocabFile, 'a')
    for line in va:
        vf.write(line)


def classify():
    vocabFile = (input("Vocab file name (vocab.txt by default):"))
    print("STUB: working on "+vocabFile)


def main():
    action = input("what are we doing? (1 - train, 2 - classify):")
    if action == str(1):
        train()
    elif action == str(2):
        classify()


main()