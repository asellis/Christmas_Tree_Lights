# Controls the lights for a christmas tree
from SerialCom import SerialCom  # Serial Communication to the arduino
from LED import LED              # Class to help store LED values

class xLEDController:
    def __init__(self, port='', baudRate = 500000, ledCount = 300):
        self.ser = SerialCom(port, baudRate)
        self.ser.readAll()  # Initiallizing the serial sends some data
                            # read as a command
                            # This flushes it all out
        self.leds = [LED() for i in range(ledCount)]
        self.stopLED = False

        self.layers = [(0,ledCount)]    # Specifies the start led of each layer
                            # of the tree

    def setLayers(self, layers):
        for i in range(len(layers)-1):
            self.layers.insert(len(self.layers)-1,(layers[i], layers[i+1]))
        self.layers.insert(len(self.layers)-1,(layers[len(layers)-1], len(self.leds)))

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
        
    def set(self, ledNum, red, green, blue):
        self.leds[ledNum].set(red, green, blue)

    def setAll(self, red, green, blue, layer = -1):
        for i in range(self.layers[layer][0],self.layers[layer][1]):
            self.leds[i].set(red, green, blue)

    def setPattern(self, leds, layer=-1):
        for i in range(len(self.leds)):
            color = leds[i%len(leds)].values()
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
    ctrl.setPattern([LED(255,0,0),LED(0,255,0)])
    ctrl.update()
    ctrl.setLayers([0,100, 200])
    ctrl.setAll(255,0,0, layer=0)
    ctrl.setAll(0,255,0, layer=1)
    ctrl.setAll(0,0,255, layer=2)
    ctrl.update()
