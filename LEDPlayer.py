# Used for doing multiple effects on the LEDs
# Stores information for each LED describing the current effect
# and how it is updating
from LEDController import LEDController # This stores all the actual colors
from LED import LED
from time import sleep
from time import time
from LEDEvents import ledEvents
#import _thread      # Currently used in interface to allow playing of events while reading user inpuit
                     #  May change at a later date to where the entire play function is run in a thread
                     #  from this class instead
import random
import vlc # Player for music

class LEDPlayer:
    def __init__(self, port='', baudRate = 500000, ledCount = 300):
        # Starts connection to serial and sets up LEDs
        self.ctrl = LEDController(port, baudRate, ledCount) # LEDController for storring colors and communicating to Arduino
        self.leds = dict()  # Stores effect information about each LED in dictionaries
        for i in range(ledCount):
            self.leds[i] = dict()

        self.events = ledEvents()       # LED effect events to execute
        self.pauseLoop = False          # Tells the player to pause on next iteration
        self.stopLoop = True            # Stops playing events (no resume)
        self.paused = False             # Confirmation that the player is paused
                                        #  This is for making changes to player safely while playing
        self.startTime = 0              # The time the player starts
        self.media = vlc.MediaPlayer()  # Player for music
        self.setupLED()                 # Sets up dictionaries for every LED to store effect data
        self.pauseTime = 0              # Time in which pause occurred

    def setupLED(self):
        # Adds dictionary values for all possible commands
        for i in range(len(self.leds)):
            self.leds[i]['command'] = None

            # Assign dictionaries for each effect
            # Each pattern dictionary stores values needed to
            # continuously update the pattern
            
            # Glow
            self.leds[i]['glow']=dict()

            # Spiral
            self.leds[i]['spiral']=dict()

            # Fade
            self.leds[i]['fade']=dict()

            # Twinkle
            self.leds[i]['twinkle']=dict()
            self.leds[i]['twinkle']['color']=[0,0,0]    # Stores the previous color
            self.leds[i]['twinkle']['on']=False         # Indicates if the led has changed
            
        self.twinkleInfo = dict()
        self.twinkleInfo['on']=False

    def loadEvents(self, file=''):
        # Loads an events file
        self.events = ledEvents(file)

    def checkCommands(self):
        # Will check LEDs for their current command and execute accordingly
        commands = [self.leds[i]['command'] for i in range(len(self.leds))]
        for i in range(len(self.leds)):
            command = commands[i]

            # Commands per LED
            if command == None:
                continue
            elif command == 'glow':
                # glow
                self.glow(i)
            elif command == 'spiral':
                # spiral
                self.spiral(i)
                pass
            elif command == 'fade':
                # fade
                self.fade(i)
        # Commands on sets of LEDs
        if self.twinkleInfo['on']==True:
            self.twinkle()

    def checkEvents(self):
        # Will check events and execute if the time for event to play has passed
        while len(self.events)>0 and self.events.time()+self.startTime<=time() and not self.stopLoop:
            event = self.events.next()
            self.playEvent(event)

    def playEvent(self, event):
        # Executes the event

        # Get LED indices
        leds = []
        for layer in event.layer:
            leds+=self.getLayer(layer)

        # Check event command and execute accordingly
        if event.command=='setPattern' or event.command=='set':
            pattern = event.parameters
            newPattern = []
            for p in pattern:
                values=p.strip('()').split(',')
                for i in range(len(values)):
                    values[i]=int(values[i])
                newPattern.append(values)
            self.setPattern(newPattern, leds)
        elif event.command=='glow':
            parameters = self.getParameters(event)
            for led in leds:
                exec('self.setGlow({},{})'.format(led, parameters))
        elif event.command=='spiral':
            parameters = self.getParameters(event)
            leds = sorted(leds)
            exec('self.setSpiral({},{},{})'.format(leds[0],leds[-1], parameters))
        elif event.command=='fade':
            parameters = self.getParameters(event)
            for led in leds:
                exec('self.setFade({},{})'.format(led, parameters))
        elif event.command=='twinkle':
            parameters = self.getParameters(event)
            #for param in event.parameters:
            #    parameters+=param[0]+'='+param[1]+','
            #parameters=parameters.strip(',')
            exec('self.setTwinkle({},{})'.format(leds, parameters))
        elif event.command=='stopTwinkle':
            self.twinkleInfo['on']=False
        elif event.command=='clear':
            self.clear()
        elif event.command=='reset':
            self.reset()
        elif event.command=='stop':
            self.stop()

    def getParameters(self, event):
        # Gets the command parameters from an event
        parameters = ''
        for param in event.parameters:
            parameters+=param[0]+'='+param[1]+','
        parameters=parameters.strip(',')
        return parameters

    def update(self):
        # Updates the LEDs to the given colors
        # Sends LED info to the Arduino
        self.ctrl.update()

    def plugParameters(self, command, args):
        # Runs the function 'command' with parameters stored in a list 'args'
        # Used for filling the parameters in for an effect function call
        command(*args)

    def setLayers(self, layerStarts):
        # Sets layers in the tree
        # Input is the beginning LED index of every horizontal layer
        self.ctrl.setLayers(layerStarts)

    def getLayer(self, layer):
        # Returns all the LED indices of the given layer name
        return self.ctrl.getLayer(layer)

    def pause(self):
        # Pauses playing events
        if self.pauseLoop:
            self.pauseLoop = False
        else:
            self.pauseLoop = True

    def stop(self):
        # Stops playing events
        self.stopLoop = True

    def play(self):
        # Plays stored events
        if self.events.song()!='':
            # If there is a song, play it
            self.media = vlc.MediaPlayer(self.events.song())
            self.media.play()
            waitTime=time()
            while self.media.get_time()<=0 and (time()-waitTime)<1:
                # Wait until song starts
                pass
        self.startTime = time()
        self.stopLoop = False
        while not self.stopLoop:
            while self.pauseLoop:
                # Stay in while loop if pauised
                self.paused = True
            self.paused=False
            self.checkEvents()      # Checks if there is any new events and if so update LEDs accordingly
            self.checkCommands()    # Checks currently stored effect in the LED and executes accordingly
            #for i in range(len(self.commands)):
            #    self.plugParameters(self.commands[i], self.parameters[i])
            self.update()           # Sends the data to the Arduino and writes to the LEDs
        self.media.stop()           # Stop playing song


    def reset(self):
        # Stops player and resets LED colors
        if not self.stopLoop:
            self.stopLoop = True
        sleep(0.1)
        for i in range(len(self.leds)):
            self.leds[i]['command']=None
            self.leds[i]['twinkle']['on']=False
            self.ctrl.set(0,0,0,[i])
        self.twinkleInfo['on']=False
        self.update()

    def clear(self):
        # Resets all led commands and colors
        # Does not stop playing
        for i in range(len(self.leds)):
            self.leds[i]['command']=None
            self.leds[i]['twinkle']['on']=False
            self.ctrl.set(0,0,0,[i])
        self.twinkleInfo['on']=False


    """
    Setting LEDs
    """
    def setLED(self, led, R, G, B):
        # Sets LED of index led the specified color
        self.ctrl.set(led,int(R),int(G),int(B))

    def setPattern(self, pattern, leds):
        # Sets the given LED indices the specified repeating pattern
        # Pattern is of the form [(R,G,B),(R,G,B),...]
        p=[]
        for item in pattern:
            p.append(LED(item[0],item[1],item[2]))
        self.ctrl.setPattern(p, leds)

    def fixRange(self, value):
        # Ensures the value is within 8-bit range
        if value < 0:
            value = 0
        if value > 255:
            value = 255

    """
    Glow
    """
    # Incrementally increases and then decreases LED intensity
    
    def setGlow(self, led, amount=-1, minValue=0, maxValue=255, stopAt=-1, duration=-1, cycleDuration=-1, valueStart=-1):
        # Sets up the LED to glow on LED index led
        
        # Update dictionary
        self.leds[led]['command']='glow'
        self.leds[led]['glow']['amount']=amount                     # The max value change in the glow
                                                                    #  don't set if using duration
        self.leds[led]['glow']['ratio']=self.ctrl.ledValues(led)    # The color ratio between Red Green Blue
        self.leds[led]['glow']['count']=0                           # The number of times going from min to max value
        self.leds[led]['glow']['minValue']=minValue                 # Minimum value of LED intensity
        self.leds[led]['glow']['maxValue']=maxValue                 # Maximum value of LED intensity
        self.leds[led]['glow']['stopAt']=stopAt                     # Stop at count
        self.leds[led]['glow']['cycleBack']=False                   # Use to go from increasing to decreasing glow

        # Values dealing with time
        self.leds[led]['glow']['startTime']=time()                  # Start time
        self.leds[led]['glow']['duration']=duration                 # Total time to glow for (unused)
        self.leds[led]['glow']['cycleDuration']=cycleDuration       # The time to complete one cycle (increase in intensity and then decrease)
        self.leds[led]['glow']['cycleTime']=0                       # The time spent on current cycle

        # Sets up whether to start the glow from max intensity (1), off (0), or current intensity (-1)
        if valueStart == 1:
            ratio = self.leds[led]['glow']['ratio']
            Red = (ratio[0]/max(ratio))*maxValue
            Green = (ratio[1]/max(ratio))*maxValue
            Blue = (ratio[2]/max(ratio))*maxValue
            for color in [Red, Green, Blue]:
                self.fixRange(color)
            self.ctrl.set(int(Red),int(Green),int(Blue),[led])
            if amount>0:
                self.leds[led]['glow']['amount']=-amount
        elif valueStart == 0:
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
        # Executes the glow on LED index led

        # Assign local variables from effect dictionaries for easier access
        glow = self.leds[led]['glow']
        amount = glow['amount']
        count = glow['count']
        #if count==0:
        #    self.leds[i]
        ratio = glow['ratio']
        minValue = glow['minValue']
        maxValue = glow['maxValue']

        stopAt = glow['stopAt']
        currentValues = self.ctrl.leds[led].values()

        startTime = glow['startTime']
        glowTime = time()-startTime
        cycleDuration = glow['cycleDuration']
        cycleTime = glow['cycleTime']

        if (cycleDuration<0 and max(currentValues)+amount < minValue) or max(currentValues) + amount > maxValue:
            # If cycleDuration is not specified then change intensity by given amount each cycle
            # ensuring that the change stays withing  the given bounds
            amount = -amount # Change from increasing to decreasing or from decreasing to increasing intensity
            self.leds[led]['glow']['amount']=amount

        maxRatio = max(ratio)
        maxIndex = [i for i in range(3) if ratio[i] == maxRatio]

        if cycleDuration>0:
            # If cycle duration is specified, ensure that the change in glow is proportional to
            #  the given cycle time
            glowPercentage = (glowTime%cycleDuration)/(cycleDuration)

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
        
            self.leds[led]['glow']['cycleTime']=glowPercentage

            if self.leds[led]['glow']['cycleBack']:
                # Change direction of glow (increasing to decreasing)
                glowPercentage = 1-glowPercentage

            # When glowPercentage=0 min value, glowPercentage=1 max value
            #((glowPercentage*maxValue)+(1-glowPercentage)*minValue)
            Red = (ratio[0]/maxRatio)*((glowPercentage*maxValue)+(1-glowPercentage)*minValue)
            Green = (ratio[1]/maxRatio)*((glowPercentage*maxValue)+(1-glowPercentage)*minValue)
            Blue = (ratio[2]/maxRatio)*((glowPercentage*maxValue)+(1-glowPercentage)*minValue)
            for color in [Red, Green, Blue]:
                self.fixRange(color)
        else:
            # If cycle duration is not specified, change by amount
            Red = (ratio[0]/maxRatio)*(max(currentValues)+amount)
            Green = (ratio[1]/maxRatio)*(max(currentValues)+amount)
            Blue = (ratio[2]/maxRatio)*(max(currentValues)+amount)
            for color in [Red, Green, Blue]:
                self.fixRange(color)
        self.ctrl.set(int(Red),int(Green),int(Blue),[led])

        # Stop glow
        if (self.leds[led]['glow']['count']>=glow['stopAt'] and glow['stopAt']>0) or (glow['startTime']+glow['duration']>time() and glow['duration']>0):
            # If one of the set conditions (duration or count) have been fulfilled then stop glow
            self.leds[led]['command']=None



    """
    Spiral
    """
    # New color grows along strand of LEDs

    def setSpiral(self, startLed, endLed, duration=-1, stopAt=-1, pattern=None, fill=True, reverse=False):
        # Changes LEDs sequentially
        # Sets up the LED range to spiral

        # Check if reverse is specified
        # Will change LEDs starting from the top of the tree instead of the bottom
        if reverse and startLed<endLed:
            start = endLed
            end = startLed
            startLed = start
            endLed = end
            
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
                                                                #  Used primarily with duration and typically want to keep
                                                                #  this as true

        if startLed>endLed:
            reverse=True
        self.leds[startLed]['spiral']['reverse']=reverse

        # Values dealing with time
        self.leds[startLed]['spiral']['duration']=duration      # How long each spiral takes
        self.leds[startLed]['spiral']['startTime']=time()       # Start time



    def spiral(self, led):
        # Executes the spiral
        # led is the LED index to execute
        # There should only be one LED that executes this in a cycle

        # Gets spiral dictionary from LED
        spiral = self.leds[led]['spiral']

        # Configures what the next LED should be in the cycle
        nextLed = int(spiral['start']+((time()-spiral['startTime'])%spiral['duration'])/(spiral['duration'])\
                      *(spiral['end']-spiral['start']))
        if spiral['reverse']:
            nextLed = int(spiral['end']+(1-((time()-spiral['startTime'])%spiral['duration'])/(spiral['duration']))\
                          *(spiral['start']-spiral['end']))
            
        color = spiral['pattern'][spiral['count']%len(spiral['pattern'])]
        
        # Setup next led and change color for current LED
        if not spiral['reverse'] and nextLed<led:
            self.leds[led]['spiral']['count']+=1
            self.leds[nextLed]['spiral']['prev']=spiral['start']
            if spiral['fill']:
                # Fill in color to current LED
                self.ctrl.set(color[0],color[1],color[2],[i for i in range(spiral['prev'],spiral['end']+1)])
            if self.leds[led]['spiral']['count']>=spiral['stopAt']:
                self.leds[led]['command']=None
        elif not spiral['reverse']:
            self.leds[nextLed]['spiral']['prev']=led
            
        # Reverse setup and change color for current LED
        if spiral['reverse'] and nextLed>led:
            self.leds[led]['spiral']['count']+=1
            self.leds[nextLed]['spiral']['prev']=spiral['start']
            if spiral['fill']:
                # Fill in color to current LED
                self.ctrl.set(color[0],color[1],color[2],[i for i in range(spiral['prev'],spiral['end']-1,-1)])
            if self.leds[led]['spiral']['count']>=spiral['stopAt']:
                self.leds[led]['command']=None
        elif spiral['reverse']:
            self.leds[nextLed]['spiral']['prev']=led

        # Copies over the data for the spiral into the next LED
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
            self.leds[nextLed]['spiral']['reverse']=spiral['reverse']

            self.leds[nextLed]['spiral']['startTime']=spiral['startTime']

        # Set current LED command to none
        if nextLed!=led or spiral['count']==spiral['stopAt']:
            self.leds[led]['command']=None

        # Set colors
        self.ctrl.set(color[0],color[1],color[2],[led])
        if not spiral['reverse'] and spiral['fill']:
            self.ctrl.set(color[0],color[1],color[2],[i for i in range(spiral['prev']-1,led+1) if i>=0])
            if nextLed<led:
                for i in range(spiral['prev']-1,spiral['end']+1):
                    if i!=led and i!=nextLed:
                        self.leds[i]['command']=None
            else:
                for i in range(spiral['prev']-1,led):
                    if i>=0 and i!=led and i!=nextLed:
                        self.leds[i]['command']=None

        elif spiral['reverse'] and spiral['fill']:
            self.ctrl.set(color[0],color[1],color[2],\
                          [i for i in range(spiral['prev'],led,-1) if i>=0 and i<len(self.leds)])
            if nextLed>led:
                for i in range(spiral['prev'],spiral['end'],-1):
                    if i!=led and i!=nextLed:
                        self.leds[i]['command']=None
            else:
                for i in range(spiral['prev'],led, -1):
                    if i>=0 and i!=led and i!=nextLed:
                        self.leds[i]['command']=None

        #if self.leds[led]['spiral']['count']==self.leds[led]['spiral']['stopAt']:
        #    print(self.leds[led],self.leds[nextLed])
                        
    """
    Fade
    """

    def setFade(self, led, duration=1):
        # Gradually changes led to off over given duration
        # Setup for LED with index led to fade

        # Set dictionary values
        self.leds[led]['command']='fade'
        self.leds[led]['fade']['ratio']=self.ctrl.ledValues(led)    # Color ratio of Red Green Blue
        self.leds[led]['fade']['duration']=duration                 # Duration
        self.leds[led]['fade']['startTime']=time()                  # Start time

    def fade(self, led):
        # Executes the fade for LED index led

        # Gets fade dictionary for LED
        fade = self.leds[led]['fade']
        
        ratio = fade['ratio']
        currentTime = time()
        glowPercentage = 1-((currentTime-fade['startTime'])%fade['duration'])/(fade['duration'])
        #print(currentTime%fade['duration'],fade['duration'],glowPercentage)
        Red = int((ratio[0]/max(ratio))*(glowPercentage*max(ratio)))
        Green = int((ratio[1]/max(ratio))*(glowPercentage*max(ratio)))
        Blue = int((ratio[2]/max(ratio))*(glowPercentage*max(ratio)))
        if max([Red,Green,Blue])>max(self.ctrl.ledValues(led)):
            # If the LED values have not decreased then set them to 0
            # The LEDs are only suppose to fade to 0
            # This if is just to ensure that they reach 0
            Red=0
            Green=0
            Blue=0
        if Red==0 and Green==0 and Blue==0:
            self.leds[led]['command']=None  # Fade has finished
        self.ctrl.set(Red,Green,Blue,[led])

    """
    Twinkle
    will randomly set led(s) a certain color
    """
    def setTwinkle(self, leds, color=None, amount=None, number=0, duration=-1, twinkleDuration=0.5):
        # Sets a number of leds to randomly twinkle
        self.twinkleInfo['on']=True
        self.twinkleInfo['color']=color                         # LED color of twinkle
        self.twinkleInfo['amount']=amount                       # Amount to change current LED color intensity by
                                                                #  (as a percentage), do not use if a color was selected
        self.twinkleInfo['leds']=leds                           # LED indices that can twinkle
        self.twinkleInfo['number']=number                       # How many LEDs will twinkle with each cycle
        self.twinkleInfo['duration']=duration                   # How long to keep cycling
        self.twinkleInfo['twinkleDuration']=twinkleDuration     # How long before moving to next cycle
        self.twinkleInfo['count']=0                             # How manu cycles to perform befor stopping
        self.twinkleInfo['lastUpdate']=time()                   # When the last cycle occurred
        self.twinkleInfo['startTime']=time()                    # Start time

    def twinkle(self):
        # Executes the twinkle effect
        info = self.twinkleInfo
        currentTime = time()
        self.twinkleInfo['lastUpdate']=currentTime
        # If time reached to update
        if currentTime-info['startTime']>info['count']*info['twinkleDuration']:
            # Reset LEDs to original color
            for led in info['leds']:
                if self.leds[led]['twinkle']['on']:
                    self.leds[led]['twinkle']['on']=False
                    color = self.leds[led]['twinkle']['color']
                    self.ctrl.set(color[0],color[1],color[2],[led])

            # Choose random leds to change color
            leds = info['leds']
            random.shuffle(leds)
            chosenLeds = leds[0:info['number']]

            for led in chosenLeds:
                self.leds[led]['twinkle']['color']=self.ctrl.ledValues(led)  # Save previous color
                if info['color']!=None:
                    color = info['color']
                    self.ctrl.set(color[0],color[1],color[2],[led])
                elif info['amount']!=None:
                    amount = info['amount']
                    color = self.leds[led]['twinkle']['color']
                    color = [color[i]*amount for i in range(len(color))]

                    # Ensures propper range of color values
                    for i in range(len(color)):
                        if color[i]>255:
                            color[i]=255
                        if color[i]<0:
                            color[i]=0
                            
                    self.ctrl.set(int(color[0]),int(color[1]),int(color[2]),[led])
                    
                self.leds[led]['twinkle']['on']=True

            self.twinkleInfo['count']+=1
