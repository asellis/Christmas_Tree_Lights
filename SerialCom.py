# Handles all communication to the Arduino
# For the project, items refers to LED color data

from time import sleep
import time
import serial    # Requires pyserial to be installed (pip install pyserial)

class SerialCom:
    def __init__(self, port = None, baudRate = 500000, debug = False):
        # Sets up communication to the Arduino
        # if no port specified common ports will be tested
        portFound = False # Identifier for if a connection has been established
        self.baudRate = baudRate # Transfer rate of data to Arduino
        self.debug = debug # if set to true will print out debug statements

        waitAmount = 1 # Give a little time to establish connection (seconds)
        
        if port != None:
            try:
                # Will try connecting to specified port
                if debug:
                    print("Trying to connect to '" + str(port) + "'")
                self.ser = serial.Serial(port, self.baudRate) # Try to initialize port
                portFound = True  # Only gets set if success
                if debug:
                    print("Port connected")
            except:
                # Unable to connect to specified port
                if debug:
                    print("Unable to connect to '"+ str(port) + "', trying common ports")
        if not portFound:
            # Try common ports
            if self.debug:
                print('Trying to connect to common ports')
            portFound = self.connectCommonPorts()

        if portFound:
            sleep(waitAmount) # Give a little time to establish connection (seconds)
        # TO ADD: raise exception if not connected

    def connectCommonPorts(self):
        # Attempts to connect to common ports
        # Stops affer connecting to one
        # Added common Windows ports
        commonPorts = ['COM1', 'COM2', 'COM3', 'COM4']
        for port in commonPorts:
            try:
                if self.debug:
                    print("Trying to connect to '"+ str(port) + "'")
                self.ser = serial.Serial(port, self.baudRate) # Try to initialize port
                if self.debug:
                    print("Connected to '" + str(port) + "'")
                return True
            except:
                pass
        if self.debug:
            print("Unable to connect to port")
        return False

    def write(self, item):
        # Writes item command or list of all LED colors to serial
        if type(item) == str or type(item) == chr:
            #self.ser.write(bytes(item, 'utf-8'))
            self.ser.write(item.encode())
            if self.debug:
                print('Sent: ', bytes(item, 'utf-8'))
        else:
            self.ser.write(bytes(item))
            if self.debug:
                print('Sent: ', bytes(item))

    def readline(self, p=False):
        # Returns next line of serial input
        # Prints if p is True
        while not self.ser.inWaiting():
            pass
        if self.ser.inWaiting():
            r = self.ser.readline()
            if p:
                print(r)
            return r

    def readlinewait(self, p=False):
        # USED FOR TESTING ONLY
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
        # Only used for flushing input buffer
        # Reads all input and returns as a list
        # p is for printing
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

def testData(ser, iterations):
    # Tests protocol for number of iterations to measure update rate of LEDs
    ser.debug = False
    data = [0 for i in range(300 * 3)]
    timeData = []
    ser.readAll()
    for i in range(iterations):
        t0 = time.time()
        ser.write('S')
        rec = ser.readlinewait()
        if ser.cleanLine(rec) == 'Ready':
            ser.write(data)
        else:
            print("ERROR 1 Iteration",i)
        rec = ser.readlinewait()
        if ser.cleanLine(rec) == 'Done':
            ser.write('W')
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
