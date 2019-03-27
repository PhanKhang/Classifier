class Testresult:
    def __init__(self, name):
        self.counter = 0
        self.name = name
        self.actualclass = name.split("-")[1]
        self.derivedclass = ''
        self.hamscore = 0.0
        self.spamscore = 0.0
        self.result = ''

    def toString(self):
        if self.derivedclass == self.actualclass:
            return str(self.counter) + "\t" + self.name + "\t" + self.derivedclass + "\t" + str(self.hamscore) + "\t" + str(
                self.spamscore) + "\t" + self.actualclass + "\t" + self.result + "\tright" + "\n"
        else:
            return str(self.counter) + "\t" + self.name + "\t" + self.derivedclass + "\t" + str(
                self.hamscore) + "\t" + str(
                self.spamscore) + "\t" + self.actualclass + "\t" + self.result + "\twrong" + "\n"
