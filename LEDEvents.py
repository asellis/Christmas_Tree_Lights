# Used to store event data to be used with LEDPlayer
# An event is a specified time in which some effect is played
# Can load events from a file
# Event data include the function (i.e. glow), it's parameters,
#   and the LEDs/layer to be affected

# 2 Classes:
#   ledEvent stores data for a single event
#   ledEvents stores multiple ledEvents in a queue using a list

class ledEvent:
    # Specifies a time, effect, and LEDs to act upon
    # Command is the effect function name (such as glow)
    # while paramaters are specific to the effect function and include
    # items such as pattern and duration
    def __init__(self, time=0, command='', parameters='', layer=''):
        self.time = time                # Delay time from initial event
                                        #  before executing effect
        self.leds = []                  # LEDs to execute effect on
        self.layer = layer              # LED layer to execute effect on
        self.command = command          # LED effect name
        self.parameters = parameters    # LED effect parameters
        
    def setTime(self, time):
        # Sets the delay time to execute the event in seconds
        self.time = time

    def setLEDs(self, leds):
        # Sets the LED indices
        self.leds = leds

    def setLayer(self, layer):
        # Sets the LED layer
        self.layer = layer

    def setCommand(self, command):
        # Sets the LED effect function name
        self.command = command

    def setParameters(self, parameters):
        # Sets the LED effect parameters (specific to each effect)
        self.parameters = parameters

    def content(self):
        # Returns the information stored in the event
        return [self.time, self.command, self.parameters, self.layer]

    def getTime(self):
        # Returns the delay time
        return self.time

    def __str__(self):
        # Returns a string of the data in the event
        # Used for printing event data
        return 'ledEvent: time={} command={} parameters:{} layer={}'.format(\
            self.time, self.command, self.parameters, self.layer)


class ledEvents:
    # Contains multiple events for sequential execution
    def __init__(self, file = ''):
        self.events = []
        self.songFile=''
        if file!='':
            self.openEvents(file)

    def openEvents(self, file):
        # Opens events from a file
        contents = open(file, "r").readlines()
        startLine=1

        # Checks if there is a song associated with the file
        if contents[0].strip().split('\t')[0]=='song':
            self.songFile=contents[0].strip().split('\t')[1]
            startLine+=1

        # Processes the line containins time, effect name, parameters
        #  and LED layer
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
                    # if '+' then multiple layers are specified
                    leds=items[2].split('+')
                    for led in leds:
                        led.strip()
                else:
                    leds = items[2]
                    leds.strip()
                    leds=[leds] # makes leds iterable (only 1 element though)

            # Setting effect parameters
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
        # Returns the song associated with the events, if specified
        return self.songFile

    def print(self):
        # Prints all the stored events
        for event in self.events:
            print(event)

    def __len__(self):
        # Returns how many events are stored
        return len(self.events)
