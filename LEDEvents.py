# Used to store event data to be used with LEDPlayer
# Can load events from a file
# Event data include the function (i.e. glow), it's parameters,
#   and the LEDs/layer to be affected

# 2 Classes:
#   ledEvent stores data for a single event
#   ledEvents stores multiple ledEvents in a queue using a list

class ledEvent:
    def __init__(self, time=0, command='', parameters='', layer=''):
        self.time = time
        self.leds = []
        self.layer = layer
        self.command = ''
        self.parameters = parameters
        self.end = False
        
    def setTime(self, time):
        self.time = time

    def setLEDs(self, leds):
        self.leds = leds

    def setLayer(self, layer):
        self.layer = layer

    def setCommand(self, command):
        self.command = command

    def setParameters(self, parameters):
        self.parameters = parameters

    def setEnd(self, bool = True):
        self.end = True

    def end(self):
        return self.end

    def content(self):
        return [self.time, self.command, self.parameters, self.layer]

    def getTime(self):
        return self.time()

    def __str__(self):
        return 'ledEvent: time={} command={} parameters={} layer={}'.format(\
            self.time, self.command, self.parameters, self.layer)


class ledEvents:
    def __init__(self, file = ''):
        self.events = []
        if file!='':
            self.openEvents(file)

    def openEvents(self, file):
        contents = open(file, "r").readlines()
        for line in contents[1:]:
            items = line.strip().split('\t')
            self.events.append(ledEvent(int(items[0]),items[1],items[2],items[3]))

    def time(self):
        # Returns the time of the next event
        return self.events[0].getTime()

    def next(self):
        # Returns the first event and removes it from the list of events
        return self.events.pop(0)

    def printEvents(self):
        for event in self.events:
            print(event)

if __name__ == '__main__':
    ledEvents('Player_Test.txt')
