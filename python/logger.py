from time import asctime

class Logger:

    def __init__(self):
        filename = "log/%s.%s" % (asctime(), 'log')
        self.file = open(filename, 'w')
        print("Log file opened.")

    def write(self, message):
        datastring = "%s: %s\n" % (asctime(), message)
        print(datastring.rstrip())
        self.file.write(datastring)

    def __del__(self):
        self.file.close()
        print "Log file closed."
