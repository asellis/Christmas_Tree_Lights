# Handles all communication to the Arduino
# This class can be used to send any data over, not just LED data
# For the project, items refers to LED color data

from time import sleep
import time
import serial    # Requires pyserial to be installed (pip install pyserial)

class SerialCom:
    def __init__(self, port = None, baudRate = 500000, debug = False):
        # Sets up communication to the arduino
        # if no port specified common ports will be tested
        self.portFound = False # Identifier for if a connection has been established
        self.baudRate = baudRate
        self.items = [] # Stores items (LED colors) to be sent over to Arduino
        self.debug = debug # if set to true will print out debug statements

        waitAmount = 1 # Give a little time to establish connection (seconds)
        
        if port != None:
            try:
                # Will try connecting to specified port
                if debug:
                    print("Trying to connect to '" + str(port) + "'")
                self.ser = serial.Serial(port, self.baudRate)
                self.portFound = True
                if debug:
                    print("Port connected")
            except:
                # Unable to connect to specified port
                #self.ser.close()
                if debug:
                    print("Unable to connect to '"+ str(port) + "', trying common ports")
        if not self.portFound:
            try:
                # Try common ports
                if self.debug:
                    print('Trying to connect to common ports')
                self.connectCommonPorts()
                self.portFound=True
            except:
                # Failed to connect
                if debug:
                    print("Failed to connect")
        if self.portFound:
            sleep(waitAmount) # seconds

    def connectCommonPorts(self):
        # Attempts to connect to common ports
        # Stops affer connecting to one
        # Added common Windows ports
        commonPorts = ['COM1', 'COM2', 'COM3', 'COM4']
        for port in commonPorts:
            try:
                if self.debug:
                    print("Trying to connect to '"+ str(port) + "'")
                self.ser = serial.Serial(port, self.baudRate)
                self.portFound = True
                if self.debug:
                    print("Connected to '" + str(port) + "'")
                break
            except:
                pass
        if self.debug and self.portFound == False:
            print("Unable to connect to port")

    def write(self, item):
        # Writes item (LED color or other for testing) to serial
        if type(item) == str or type(item) == chr:
            #self.ser.write(bytes(item, 'utf-8'))
            self.ser.write(item.encode())
            if self.debug:
                print('Sent: ', bytes(item, 'utf-8'))
        else:
            self.ser.write(bytes(item))
            if self.debug:
                print('Sent: ', bytes(item))

    def addItems(self, items):
        # Adds items (LED colors) to be sent over
        self.items += items

    def writeItems(self):
        # Writes added items (LEDs) to the serial port
        self.ser.write(bytes(self.items))

    def clearItems(self):
        # Clears everything stored in items
        self.items = []

    def readline(self, p=False):
        # Returns serial input
        # Prints if p is True
        while not self.ser.inWaiting():
            pass
        if self.ser.inWaiting():
            r = self.ser.readline()
            if p:
                print(r)
            return r

    def readlinewait(self, p=False):
        # Waits until there is a line to read
        # Same as readline but without double checking if data
        # is available in buffer
        while not self.ser.inWaiting():
            pass
        r = self.ser.readline()
        if p:
            print(r)
        return r

    def readAll(self, p=False):
        # Reads all input and returns as a list
        data = []
        while self.ser.inWaiting():
            serialIn = self.ser.readline()
            data.append(serialIn)
            if p:
                print(serialIn)
        return data

    def cleanLine(self, line):
        # Returns Arduino read line into a python string
        return line.decode('utf-8').strip()

    def close(self):
        # Closes connection
        self.ser.close()

def testData(ser, times):
    # A test function to ensure that connection has been established
    # and that commands are properly read
    # Also used for getting the update rate of LEDs
    ser.debug = False
    data = [0 for i in range(300 * 3)]
    timeData = []
    ser.readAll()
    for i in range(times):
        t0 = time.time()
        ser.write('S')
        rec = ser.readlinewait()
        if ser.cleanLine(rec) == 'Ready':
            ser.write(data)
        else:
            print("ERROR 1 Iteration",i)
        rec = ser.readlinewait()
        if ser.cleanLine(rec) == 'Done':
            ser.write('s')
        else:
            print("ERROR 2 Iteration",i)
        rec = ser.readlinewait()
        if ser.cleanLine(rec) == 'Done':
            pass
        else:
            print("ERROR 3 Iteration",i)
        t1 = time.time()
        #print(t1-t0)
        timeData.append(t1-t0)
    return timeData
    

if __name__ == '__main__':
    # Tests connection times
    print('Starting')
    ser = SerialCom(baudRate = 500000, debug = True)
    times = testData(ser, 100)
    print("Average Time: {}".format(sum(times)/len(times)))
