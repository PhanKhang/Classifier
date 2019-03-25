import re


class Parser(object):

    def parseFile(file):
        f = open(file, "r")
        rawbody = f.read()
        return re.split('[^a-zA-Z]', rawbody)
