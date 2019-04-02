# Stores all the LED color values and sends data over to an Arduino
# through use of SerialCom class
from SerialCom import SerialCom     # Serial Communication to the Arduino
from LED import LED                 # Class for storing single LED values

class LEDController:
    def __init__(self, port='', baudRate = 500000, ledCount = 300):
        self.ser = SerialCom(port, baudRate)
        self.ser.readAll()  # Flush serial port
        self.leds = [LED() for i in range(ledCount)] # Create LED objects for all
                                                     # the LEDs to store their colors
        self.stopLED = False   # FOR TESTING ONLY: Used to stop glowing effect

        self.layers = dict()   # Contains all layer definitions for partitioning the tree.
                               # Each definition contains all the LED indices
                               # for a given layer

        self.layers['all'] = [i for i in range(ledCount)] # add a definition for all LEDs

    def setLayers(self, layerStarts):
        # Partitions the tree into sections, called layers, for performing effects
        # Layers are sections of the tree, both horizontal like stacked plates,
        # and vertical quarters.

        # Partition horizontal layers
        for i in range(len(layerStarts)-1):
            self.layers[str(i)] = [j for j in range(layerStarts[i], layerStarts[i+1])]
        self.layers[str(len(layerStarts)-1)] = [j for j in range(layerStarts[-1], len(self.leds))]

        # Partition quarters
        q1=[]
        q2=[]
        q3=[]
        q4=[]
        for layer in self.layers: # Split the horizontal layers into quarters
            if layer!='all':
                length = len(self.layers[layer])
                for led in range(len(self.layers[layer])):
                    if led/length <= 1/4:
                        q1.append(self.layers[layer][led])
                    elif led/length > 1/4 and led/length <= 1/2:
                        q2.append(self.layers[layer][led])
                    elif led/length > 1/2 and led/length <=3/4:
                        q3.append(self.layers[layer][led])
                    elif led/length > 3/4 and led/length <=1:
                        q4.append(self.layers[layer][led])
        # Assign LED indices for each quarter’s layer definition
        self.layers['q1'] = q1
        self.layers['q2'] = q2
        self.layers['q3'] = q3
        self.layers['q4'] = q4

    def getLayer(self, layer):
        # Returns the LED indices of the specified layer
        return self.layers[layer]

    def ledValues(self, led):
        # Returns the RGB colors for an LED of a specified index (led)
        return self.leds[led].values()

    def update(self):
        # Sends data to the Arduino to update all LEDs
        # Waits for a response before sending next command/data
        data = []
        for led in self.leds:
            data += led.values()     # Create single list of all RGB values
        self.ser.write('S')          # Command for sending LED values
        rec = self.ser.readline()    # Receive acknowledge from the Arduino
        if self.ser.cleanLine(rec) == 'Ready': # Arduino is ready to receive the data
            self.ser.write(data)
        rec = self.ser.readline()
        if self.ser.cleanLine(rec) == 'Done': # Arduino has finished reading the data
            self.ser.write('W')      # Command to turn on the LEDs with the new data
        rec = self.ser.readline()
        if self.ser.cleanLine(rec) == 'Done': # Arduino has finished writing LED values
            return
        
    def set(self, red, green, blue, leds):
        # Sets the given LEDs a specified color
        for led in leds:
            self.leds[led].set(red, green, blue)

    def setAll(self, red, green, blue, leds):
        # Same as set
        # Unnecessary after changing set to include multiple LEDs,
        # but kept for compatibility
        for i in leds:
            self.leds[i].set(red, green, blue)

    def setPattern(self, pattern, leds):
        # Sets the LEDs a specified repeating pattern
        # e.g. LED 1 Red, LED 2 Green, LED 3 Red, LED 4 Green, etc.
        # Pattern input is of the form [(R,G,B),(R,G,B),...]
        for i in leds:
            color = pattern[i%len(pattern)].values()
            self.leds[i].set(color[0], color[1], color[2])

    # THIS FUNCTION IS ONLY FOR TESTING
    # FORMAL GLOW FUNCTION IN PLAYER FILE
    def glow(self, count=5, minIntensity=0, maxIntensity=255):
        # Maxes the LEDs glow (increase then decrease in intensity and repeat)
        nums = []
        level = maxIntensity
        while not self.stopLED:
            if count+level > maxIntensity or count+level < minIntensity:
                count = -count
            for i in range(len(self.leds)):
                if i%5==0:
                    self.leds[i].set(level,0,0) # Red
                elif i%5==1:
                    self.leds[i].set(0,level,0) # Green
                elif i%5==2:
                    self.leds[i].set(0,0,level) # Blue
                elif i%5==3:
                    self.leds[i].set(level,level,0) # Yellow
                elif i%5==4:
                    self.leds[i].set(level,0,level) # Purple
            level+=count
            self.update()
            
    def stop(self):
        # FOR TESTING ONLY Stops glowing
        self.stopLED = True

    def start(self):
        # FOR TESTING ONLY Resume glowing
        self.stopLED = False
