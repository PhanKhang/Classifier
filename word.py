class Word:
    def __init__(self, word):
        self.word = word
        self.hamFreq = 0
        self.hamSmoothP = 0
        self.spamFreq = 0
        self.spamSmoothP = 0
