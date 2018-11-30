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
        self.command = command
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
        return self.time

    def __str__(self):
        return 'ledEvent: time={} command={} parameters:{} layer={}'.format(\
            self.time, self.command, self.parameters, self.layer)


class ledEvents:
    def __init__(self, file = ''):
        self.events = []
        self.songFile=''
        if file!='':
            self.openEvents(file)

    def openEvents(self, file):
        contents = open(file, "r").readlines()
        startLine=1
        
        if contents[0].strip().split('\t')[0]=='song':
            self.songFile=contents[0].strip().split('\t')[1]
            startLine+=1
            
        for line in contents[startLine:]:
            items = line.strip().split('\t')
            if len(items)<=1:
                continue
            items = [item for item in items if item!='']

            time = items[0]
            command = items[1]
            parameters = []
            leds = []
            # Setting layer(s)
            if len(items)>=3:
                if '+' in items[2]:
                    leds=items[2].split('+')
                    for led in leds:
                        led.strip()
                else:
                    leds = items[2]
                    leds.strip()
                    leds=[leds]

            # Setting parameters
            if len(items)>=4:
                parameters = items[3].split(' ')
                for i,item in enumerate(parameters):
                    if '=' in item:
                        p=item.split('=')
                        parameters[i]=(p[0],p[1])
                
            self.events.append(ledEvent(time=float(time),command=command,parameters=parameters,layer=leds))

    def time(self):
        # Returns the time of the next event
        return self.events[0].getTime()

    def next(self):
        # Returns the first event and removes it from the list of events
        return self.events.pop(0)

    def song(self):
        return self.songFile

    def print(self):
        for event in self.events:
            print(event)

    def __len__(self):
        return len(self.events)

if __name__ == '__main__':
    events = ledEvents('Player_Test.txt')
    events.print()
    print(events.song())
