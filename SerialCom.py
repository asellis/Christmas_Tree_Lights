# Handles all communication to arduino

from time import sleep
import time
import serial    # Requires pyserial to be installed (pip install pyserial)

class SerialCom:
    def __init__(self, port = None, baudRate = 500000, debug = False):
        # Sets up communication to the arduino
        # if no port specified common ports will be tested
        self.portFound = False
        self.baudRate = baudRate
        self.items = [] # Stores items to send over
        self.debug = debug

        waitAmount = 1 # Give a little time to establish connection
        
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
            sleep(waitAmount)

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
        # Adds items to be sent over
        self.items += items

    def writeItems(self):
        # Sends over added items
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
        # Returns arduino read line into a python string
        return line.decode('utf-8').strip()

    def close(self):
        self.ser.close()

def testData(ser, times):
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
    print('Starting')
    ser = SerialCom(baudRate = 500000, debug = True)
    #sleep(1)
    """
    ser.readAll(True)
    #sleep(.0001)
    times = []
    for i in range(100):
        t0 = time.time()
        ser.write('S')
        a = ser.readAll()
        if a[2].decode('utf-8').strip() == 'Ready for data':
            data = [0 for i in range(300*3)]
            ser.write(data)
            #sleep(.0001)
        b = ser.readAll()
        if b[0].decode('utf-8').strip() == 'Done':
            t1 = time.time()
            ser.write('s')
            #sleep(.0001)
            ser.readAll()
        print(t1-t0)
        times.append(t1-t0)
    """
    times = testData(ser, 100)
    print("Average Time: {}".format(sum(times)/len(times)))
