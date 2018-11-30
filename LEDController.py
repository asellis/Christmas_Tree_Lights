# Controls the lights for a christmas tree
from SerialCom import SerialCom     # Serial Communication to the arduino
from LED import LED                 # Class to help store LED values

class LEDController:
    def __init__(self, port='', baudRate = 500000, ledCount = 300):
        self.ser = SerialCom(port, baudRate)
        self.ser.readAll()  # Initiallizing the serial sends some data
                            # read as a command
                            # This flushes it all out
        self.leds = [LED() for i in range(ledCount)]
        self.stopLED = False

        self.layers = dict()   # Each entry will be a layer that contains the
                                # The LED number to light up
        self.layers['all'] = [i for i in range(ledCount)]

    def setLayers(self, layerStarts):
        for i in range(len(layerStarts)-1):
            self.layers[str(i)] = [j for j in range(layerStarts[i], layerStarts[i+1])]
        self.layers[str(len(layerStarts)-1)] = [j for j in range(layerStarts[-1], len(self.leds))]

        # Split into quarters
        q1=[]
        q2=[]
        q3=[]
        q4=[]
        for layer in self.layers:
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
        self.layers['q1'] = q1
        self.layers['q2'] = q2
        self.layers['q3'] = q3
        self.layers['q4'] = q4

    def getLayer(self, layer):
        # Returns the LED indecies of the specified layer
        return self.layers[layer]

    def ledValues(self, led):
        return self.leds[led].values()

    def update(self):
        # Sends data to the arduino to update all LEDs
        # Waits for a response before sending next command/data
        data = []
        for led in self.leds:
            data += led.values()
        self.ser.write('S')          # Command for setting LED
        rec = self.ser.readline()    # Received data from the arduino
        if self.ser.cleanLine(rec) == 'Ready':
            self.ser.write(data)
        rec = self.ser.readline()
        if self.ser.cleanLine(rec) == 'Done':
            self.ser.write('s')      # Command to show all the LEDs
        rec = self.ser.readline()
        if self.ser.cleanLine(rec) == 'Done':
            return
        
    def set(self, red, green, blue, leds):
        for led in leds:
            self.leds[led].set(red, green, blue)

    def setAll(self, red, green, blue, leds):
        for i in leds:
            self.leds[i].set(red, green, blue)

    def setPattern(self, pattern, leds):
        for i in leds:
            color = pattern[i%len(pattern)].values()
            self.leds[i].set(color[0], color[1], color[2])

    def glow(self, count=5, minIntensity=0, maxIntensity=255):
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
        self.stopLED = True

    def start(self):
        self.stopLED = False

if __name__ == '__main__':
    ctrl = xLEDController()
    ctrl.update()
    #ctrl.setPattern([LED(255,0,0),LED(0,255,0)], ctrl.getLayer('all'))
    ctrl.update()
    ctrl.setLayers([0,50,102,143,186,227,255,273,288,299])
    ctrl.setAll(255,0,0, ctrl.getLayer('q1'))
    ctrl.setAll(0,255,0, ctrl.getLayer('q2'))
    ctrl.setAll(0,0,255, ctrl.getLayer('q3'))
    ctrl.update()
