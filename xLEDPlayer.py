# Used for doing multiple effects on the LEDs
# Stores more information about how the LED is going
# to change such as for a glow
from xLEDController import xLEDController
from LED import LED
from time import sleep
from time import time
import _thread

class xLEDPlayer:
    def __init__(self, port='', baudRate = 500000, ledCount = 300):
        self.ctrl = xLEDController(port, baudRate, ledCount)
        self.leds = dict()  # Stores information about each LED
        for i in range(ledCount):
            self.leds[i] = dict()
        self.commands = []
        self.parameters = []
        self.events = []
        self.pauseLoop = False
        self.stopLoop = False

        self.setupLED()

    def setupLED(self):
        # Adds dictionary values for all possible commands
        for i in range(len(self.leds)):
            self.leds[i]['command'] = None

            # Assign dictionaries for each pattern
            # Each pattern dictionary stores values needed to
            # continuously update the pattern
            
            # Glow
            self.leds[i]['glow']=dict()

            # Spiral
            self.leds[i]['spiral']=dict()

            # Fade
            self.leds[i]['fade']=dict()

    def checkCommands(self):
        # Will check LEDs for their current command and execute
        commands = [self.leds[i]['command'] for i in range(len(self.leds))]
        for i in range(len(self.leds)):
            command = commands[i]
            if command == None:
                continue
            elif command == 'glow':
                # glow
                self.glow(i)
            elif command == 'spiral':
                #spiral
                self.spiral(i)
            elif command == 'fade':
                self.fade(i)

    def checkEvents(self):
        # Will check events and execute if time correct
        pass

    def addCommand(self, command, parameters):
        self.commands.append(command)
        self.parameters.append(parameters)

    def clearCommands(self):
        self.commands=[]
        self.parameters=[]

    def update(self):
        self.ctrl.update()

    def plugParameters(self, command, args):
        # Runs the function 'command' with parameters stored in a list 'args'
        command(*args)

    def setLayers(self, layerStarts):
        self.ctrl.setLayers(layerStarts)

    def getLayer(self, layer):
        return self.ctrl.getLayer(layer)

    def pause(self):
        if self.pauseLoop:
            self.pauseLoop = False
        else:
            self.pauseLoop = True

    def stop(self):
        self.stopLoop = True

    def play(self):
        self.stopLoop = False
        while not self.stopLoop:
            while self.pauseLoop:
                pass
            self.checkCommands()
            #for i in range(len(self.commands)):
            #    self.plugParameters(self.commands[i], self.parameters[i])
            self.update()

    def setPattern(self, pattern, leds):
        self.ctrl.setPattern(pattern, leds)

    def setLED(self, led, R, G, B):
        self.ctrl.set(led,int(R),int(G),int(B))

    def reset(self):
        # Stops player and resets LEDs
        if not self.stopLoop:
            self.stopLoop = True
        sleep(0.1)
        for i in range(len(self.leds)):
            self.ctrl.set(0,0,0,[i])
        self.update()

    def fixRange(self, value):
        # Ensures the value is within range
        if value < 0:
            value = 0
        if value > 255:
            value = 255

    """
    Glow
    """
    
    def setGlow(self, led, amount=-1, minValue=0, maxValue=255, stopAt=-1, duration=-1, cycleDuration=-1, valueStart=-1):
        # Sets the LED to glow

        # Update dictionary
        self.leds[led]['command']='glow'
        self.leds[led]['glow']['amount']=amount                     # The max value change in the glow
                                                                    # don't set if using duration
        self.leds[led]['glow']['ratio']=self.ctrl.ledValues(led)    # The color ratio
        self.leds[led]['glow']['count']=0                           # The number of times going from min to max value
        self.leds[led]['glow']['minValue']=minValue                 # Minimum value of led
        self.leds[led]['glow']['maxValue']=maxValue                 # Maximum value of led
        self.leds[led]['glow']['stopAt']=stopAt                     # Stop at count
        self.leds[led]['glow']['cycleBack']=False                   # Use to go from increasing to decreasing glow

        # Values dealing with time
        self.leds[led]['glow']['startTime']=time()                  # Start time
        self.leds[led]['glow']['duration']=duration                 # Unused
        self.leds[led]['glow']['cycleDuration']=cycleDuration       # The time to complete one cycle
        self.leds[led]['glow']['cycleTime']=0                       # The time spent on current cycle

        if valueStart == 'max':
            ratio = self.leds[led]['glow']['ratio']
            Red = (ratio[0]/max(ratio))*maxValue
            Green = (ratio[1]/max(ratio))*maxValue
            Blue = (ratio[2]/max(ratio))*maxValue
            for color in [Red, Green, Blue]:
                self.fixRange(color)
            self.ctrl.set(int(Red),int(Green),int(Blue),[led])
            if amount>0:
                self.leds[led]['glow']['amount']=-amount
        elif valueStart == 'min':
            ratio = self.leds[led]['glow']['ratio']
            Red = (ratio[0]/max(ratio))*minValue
            Green = (ratio[1]/max(ratio))*minValue
            Blue = (ratio[2]/max(ratio))*minValue
            for color in [Red, Green, Blue]:
                self.fixRange(color)
            self.ctrl.set(int(Red),int(Green),int(Blue),[led])
            if amount<0:
                self.leds[led]['glow']['amount']=-amount

    def glow(self, led):
        glow = self.leds[led]['glow']
        amount = glow['amount']
        count = glow['count']
        if count==0:
            self.leds[i]
        ratio = glow['ratio']
        minValue = glow['minValue']
        maxValue = glow['maxValue']

        stopAt = glow['stopAt']
        currentValues = self.ctrl.leds[led].values()

        startTime = glow['startTime']
        glowTime = time()-startTime
        cycleDuration = glow['cycleDuration']
        cycleTime = glow['cycleTime']


        if cycleDuration<0 and max(currentValues)+amount < minValue or max(currentValues) + amount > maxValue:
            amount = -amount
            self.leds[led]['glow']['amount']=amount

        maxRatio = max(ratio)
        maxIndex = [i for i in range(3) if ratio[i] == maxRatio]

        if cycleDuration>0:
            # d is the percentage to glow
            d = (glowTime%cycleDuration)/(cycleDuration)

            # When the cycle passes the duration
            if glowTime%cycleDuration<cycleTime and amount>0:    
                self.leds[led]['glow']['amount']=-amount
                self.leds[led]['glow']['cycleBack']=True
                amount=-amount
                self.leds[led]['glow']['count']+=1
            elif glowTime%cycleDuration<cycleTime and amount<0:
                self.leds[led]['glow']['amount']=-amount
                self.leds[led]['glow']['cycleBack']=False
                amount=-amount
                self.leds[led]['glow']['count']+=1
        
            self.leds[led]['glow']['cycleTime']=d

            if self.leds[led]['glow']['cycleBack']:
                d = 1-d

            # When d=0 min value, d=1 max value
            #((d*maxValue)+(1-d)*minValue)

            Red = (ratio[0]/maxRatio)*((d*maxValue)+(1-d)*minValue)
            Green = (ratio[1]/maxRatio)*((d*maxValue)+(1-d)*minValue)
            Blue = (ratio[2]/maxRatio)*((d*maxValue)+(1-d)*minValue)
            for color in [Red, Green, Blue]:
                self.fixRange(color)
        else:
            Red = (ratio[0]/maxRatio)*(max(currentValues)+amount)
            Green = (ratio[1]/maxRatio)*(max(currentValues)+amount)
            Blue = (ratio[2]/maxRatio)*(max(currentValues)+amount)
            for color in [Red, Green, Blue]:
                self.fixRange(color)
        self.ctrl.set(int(Red),int(Green),int(Blue),[led])

        # Stop glow
        if (self.leds[led]['glow']['count']>=glow['stopAt'] and glow['stopAt']>0) or (glow['startTime']+glow['duration']>time() and glow['duration']>0):
            self.leds[led]['command']=None



    """
    Spiral
    """

    def setSpiral(self, startLed, endLed, duration=-1, stopAt=-1, pattern=None, fill=True):
        # Changes LEDs sequentially
        # Currently only supports going up tree

        # Set dictionary
        self.leds[startLed]['command']='spiral'
        
        if pattern == None:
            pattern = [self.ctrl.leds[startLed].values()]
        self.leds[startLed]['spiral']['pattern']=pattern        # A pattern to be followed on next iteration of spiral
        self.leds[startLed]['spiral']['color']=pattern[0]       # The current color
        self.leds[startLed]['spiral']['count']=0                # The number of times spiral has completed
        self.leds[startLed]['spiral']['stopAt']=stopAt          # Stop at count
        #self.leds[startLed]['spiral']['stop']=False
        #self.leds[startLed]['spiral']['pos']=0
        self.leds[startLed]['spiral']['start']=startLed         # The initial LED
        self.leds[startLed]['spiral']['end']=endLed             # The last LED
        self.leds[startLed]['spiral']['prev']=startLed          # The previously lit LED
        self.leds[startLed]['spiral']['fill']=fill              # Fills LED colors when skipping multiple LEDs

        # Values dealing with time
        self.leds[startLed]['spiral']['duration']=duration      # How long each spiral takes
        self.leds[startLed]['spiral']['startTime']=time()       # Start time



    def spiral(self, led):
        spiral = self.leds[led]['spiral']
        nextLed = int(spiral['start']+((time()-spiral['startTime'])%spiral['duration'])/(spiral['duration'])*(spiral['end']-spiral['start']))
        
        color = spiral['pattern'][spiral['count']%len(spiral['pattern'])]
        # Setup next led
        if nextLed<led:
            self.leds[led]['spiral']['count']+=1
            self.leds[nextLed]['spiral']['prev']=spiral['start']
            if spiral['fill']:
                self.ctrl.set(color[0],color[1],color[2],[i for i in range(spiral['prev'],spiral['end']+1)])
            if self.leds[led]['spiral']['count']>=spiral['stopAt']:
                self.leds[led]['command']=None
        else:
            self.leds[nextLed]['spiral']['prev']=led
            
        if spiral['stopAt']<=0 or self.leds[led]['spiral']['count']<self.leds[led]['spiral']['stopAt']:
            self.leds[nextLed]['command']='spiral'
            self.leds[nextLed]['spiral']['color']=self.leds[led]['spiral']['pattern']\
                                            [spiral['count']%len(spiral['pattern'])]
            self.leds[nextLed]['spiral']['pattern']=spiral['pattern']
            self.leds[nextLed]['spiral']['count']=self.leds[led]['spiral']['count']
            self.leds[nextLed]['spiral']['stopAt']=spiral['stopAt']
            self.leds[nextLed]['spiral']['start']=spiral['start']
            self.leds[nextLed]['spiral']['end']=spiral['end']
            self.leds[nextLed]['spiral']['duration']=spiral['duration']
            self.leds[nextLed]['spiral']['fill']=spiral['fill']

            self.leds[nextLed]['spiral']['startTime']=spiral['startTime']

        # Set current led to none
        if nextLed!=led or spiral['count']==spiral['stopAt']:
            self.leds[led]['command']=None

        # Set colors
        self.ctrl.set(color[0],color[1],color[2],[led])
        if spiral['fill']:
            self.ctrl.set(color[0],color[1],color[2],[i for i in range(spiral['prev']-1,led+1) if i>=0])
            if nextLed<led:
                for i in range(spiral['prev']-1,spiral['end']+1):
                    if i!=led and i!=nextLed:
                        self.leds[i]['command']=None
            else:
                for i in range(spiral['prev']-1,led):
                    if i>=0 and i!=led and i!=nextLed:
                        self.leds[i]['command']=None

            

    """
    Fade
    """

    def setFade(self, led, duration):
        # Gradually changes led to off over given duration

        # Set dictionary values
        self.leds[led]['command']='fade'
        self.leds[led]['fade']['ratio']=self.ctrl.ledValues(led)    # Color ration
        self.leds[led]['fade']['duration']=duration                 # Duration
        self.leds[led]['fade']['startTime']=time()                  # Start time

    def fade(self, led):
        fade = self.leds[led]['fade']
        ratio = fade['ratio']
        currentTime = time()
        d = 1-((currentTime-fade['startTime'])%fade['duration'])/(fade['duration'])
        #print(currentTime%fade['duration'],fade['duration'],d)
        Red = int((ratio[0]/max(ratio))*(d*max(ratio)))
        Green = int((ratio[1]/max(ratio))*(d*max(ratio)))
        Blue = int((ratio[2]/max(ratio))*(d*max(ratio)))
        if max([Red,Green,Blue])>max(self.ctrl.ledValues(led)):
            Red=0
            Green=0
            Blue=0
        if Red==0 and Green==0 and Blue==0:
            self.leds[led]['command']=None
        self.ctrl.set(Red,Green,Blue,[led])

    """
    Twinkle
    will randomly set led(s) a certain color
    """
    
if __name__ == "__main__":
    player = xLEDPlayer()
    # Testing
    #player.setPattern([LED(100,0,0),LED(0,100,0)], player.getLayer('all'))
    #for i in range(len(player.leds)):
        #player.setFade(i,5)
        #player.setGlow(i, minValue = 20, maxValue = 125, amount = -1, cycleDuration = 5, valueStart='min')
        #player.setGlow(i, minValue = 20, maxValue = 125, amount = -1, )
    player.setSpiral(0,299,duration=12, pattern=[[100,0,0],[0,100,0],[0,0,100]], fill=True, stopAt=9)
    #player.play()
    #'''

    _thread.start_new_thread(player.play,())
    #sleep(.0001)
    #player.stop()
    #player.reset()


