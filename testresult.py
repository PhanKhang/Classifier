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
        return str(self.counter) + "  " + self.name + "  " + self.derivedclass + "  " + str(self.hamscore) + "  " + str(
            self.spamscore) + "  " + self.actualclass + "  " + self.result
