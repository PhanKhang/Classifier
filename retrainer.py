from modelbuilder import ModelBuilder
from uniparser import Uniparser
class Retrainer:

    @classmethod
    def retrainSet(cls, vocabFile, newVocabFile, mode, parameter, delta):
        if mode == 1:
            cls.modeStopWord(vocabFile, newVocabFile, parameter, delta)
        if mode == 2:
            cls.modeWordLength(vocabFile, newVocabFile, delta)
        if mode == 3:
            cls.modeFrequence(vocabFile, newVocabFile, parameter, delta)
        if mode == 4:
            cls.modeDelta(vocabFile,newVocabFile,delta)

    @classmethod
    def modeFrequence(cls, vocabfFile, newVocabFile, input, delta):
        modelBuilder = ModelBuilder()
        modelBuilder.delta = float(delta)
        model = Uniparser.parseModel(vocabfFile)
        wordSet = Uniparser.parseModelArr(vocabfFile)

        hamWordCount = 0
        spamWordCount = 0

        vocabFilePre = newVocabFile.split('.')[0]
        action = input.split(' ')[0]
        frequence = int(input.split(' ')[1])
        if action == '=':
            for word in wordSet:
                if word.hamFreq == frequence or word.spamFreq == frequence:
                    model.pop(word.word, None)
        elif action == '<=':
            for word in wordSet:
                if word.hamFreq <= frequence or word.spamFreq <= frequence:
                    model.pop(word.word, None)
        elif action == 'top':
            sortedModelHam = sorted(wordSet, key=lambda x: x.hamFreq, reverse=True)
            sortedModelSpam = sorted(wordSet, key=lambda x: x.spamFreq, reverse=True)

            size = len(sortedModelSpam)
            cutOff = int(size * frequence / 100)

            for j in range(cutOff):
                model.pop(sortedModelHam[j].word, None)
                model.pop(sortedModelSpam[j].word, None)

        for token, word in model.items():
            hamWordCount += word.hamFreq
            spamWordCount += word.spamFreq

        modelBuilder.hamWordsCount = hamWordCount
        modelBuilder.spamWordsCount = spamWordCount
        modelBuilder.words = model

        modelBuilder.caclulateProbabilities(len(model))
        va = modelBuilder.getWords()
        vf = open(vocabFilePre + action + str(frequence) + '.txt', 'a')
        for line in va:
            vf.write(line)

    @classmethod
    def modeStopWord(cls, vocabFile, newVocabFile, stopFile, delta):
        modelBuilder = ModelBuilder()
        model = Uniparser.parseModel(vocabFile)
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
        modelBuilder.delta = float(delta)

        print(hamWordCount)
        print(modelBuilder.hamWordsCount)

        print(spamWordCount)
        print(modelBuilder.spamWordsCount)

        print(len(model))

        modelBuilder.caclulateProbabilities(len(model))
        va = modelBuilder.getWords()
        vf = open(newVocabFile, 'a')
        for line in va:
            vf.write(line)

    @classmethod
    def modeWordLength(cls, vocabFile, newVocabFile, delta):
        modelBuilder = ModelBuilder()
        model = Uniparser.parseModel(vocabFile)
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
        modelBuilder.delta = float(delta)

        modelBuilder.caclulateProbabilities(len(model))
        va = modelBuilder.getWords()
        vf = open(newVocabFile, 'a')
        for line in va:
            vf.write(line)

    @classmethod
    def modeDelta(cls, vocabFile, newVocabFile, delta):
        modelBuilder = ModelBuilder()
        model = Uniparser.parseModel(vocabFile)
        words = Uniparser.parseModelArr(vocabFile)

        vocabFilePre = newVocabFile.split('.')[0]

        hamWordCount = 0
        spamWordCount = 0

        for word in words:
            hamWordCount += word.hamFreq
            spamWordCount += word.spamFreq

        modelBuilder.hamWordsCount = hamWordCount
        modelBuilder.spamWordsCount = spamWordCount
        modelBuilder.words = model

        modelBuilder.delta = float(delta)
        modelBuilder.caclulateProbabilities(len(words))
        va = modelBuilder.getWords()
        vf = open(vocabFilePre + str(delta).replace('.', '') + '.txt', 'a')
        for line in va:
            vf.write(line)