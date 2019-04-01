# A console text interface to execute commands for xmas LED controller
# NOTES: directory is hard coded to project directory

from LEDPlayer import LEDPlayer
from time import sleep
import _thread
import sys
import os
currentDir = os.getcwd()
demoDir = currentDir+'/PremadeEvents/'

loadFile='loadInfo.txt'


# Comments for console interface text
notes = """
This is a text based interface for controlling LEDs
Will automatically try to load presets from file {}
""".format(loadFile)

setCommands = """
--- Set Commands ---
PATTERN     set layer [(pattern1),(pattern2),...]
GLOW        glow layer parameter1=value1 parameter2=value2 ...
SPIRAL      spiral layer parameter1=value1 parameter2=value2 ...
"""

playerCommands = """
--- Player Commands ---
START       start
PLAY SONG   play preset
PREMADE     demo preset
RESET       r
STOP        s
QUIT        q
"""

# Dictionaries to hold predefined event files from loadInfo.txt
info=dict()
info['play']=dict() # Used to store music synchronization file
info['demo']=dict() # Used to store predefined effect lighting playlist
info['port']=''
info['baudRate']=500000

def connect(port,baudRate):
    # Establishes connection with LEDPlayer for playing events
    return LEDPlayer(port=port,baudRate=baudRate)

def loadInfo(file):
    # Loads the info file with predefined event files
    # Builds info dictionaries
    contents = open(file,'r').readlines()
    for line in contents:
        items=line.strip().split('\t')
        items = [item for item in items if item!='']
        if len(items)<=1:
            continue
        if items[0]=='play':
            info['play'][items[1]]=items[2]
        elif items[0]=='demo':
            info['demo'][items[1]]=demoDir+items[2]
        elif items[0]=='layers':
            layer=[int(i) for i in items[1].split(',')]
            info['layers']=layer
        elif items[0]=='baudRate':
            info['baudRate']=int(items[1])
        else:
            info[items[0]]=items[1]

def getLineInfo(line):
    # Returns the LED indices and effect parameters
    cleanedLine = line.strip().split(' ')
    layers = []
    if '+' in cleanedLine[1]:
        layers=cleanedLine[1].split('+')
        for led in layers:
            led.strip()
    else:
        layers = cleanedLine[1]
        layers.strip()
        layers=[layers] # Convert to a list that can be iterated
    leds=[] # LED indices
    for layer in layers:
        leds+=player.getLayer(layer)

    # Parameters for effects function
    parameters=','.join(l[2:])

    lineInfo = dict()
    lineInfo['leds']=leds
    lineInfo['parameters']=parameters
    return lineInfo

    


def execCode(code):
    # Executes a string as python code
    # Function is needed for using a thread
    exec(code)


if __name__ == '__main__':
    # The text based interface prints out command options and
    # executes them accordingly
    # This interface was created primarily to test certain aspects
    # of the project and needs to be updated to provide an easier
    # means of control (like a web server or an app)
    player = None
    print(notes)
    try:
        loadInfo(loadFile)
        print('Loaded info from {}'.format(loadFile))
    except:
        print('Failed to load info from {}'.format(loadFile))
    try:
        # Create player class and initialize
        player = connect(info['port'],info['baudRate'])
        if 'layers' in info.keys():
            player.setLayers(info['layers'])
        print('Connected')
    except:
        print('Not connected')
    while True:
        # Console interface text
        print(setCommands)
        print(playerCommands)
        
        userInput = input('Specify Command: ')
        command = userInput.split()[0]
        if command == 'exec':
            # Used to execute a python statement
            # Just for testing
            code = ''.join(i + ' ' for i in userInput.split()[1:])
            # Start a new thread to keep interface active while LEDs update
            _thread.start_new_thread(execCode,(code,))
        elif command == 'play':
            # plays a preset pattern with a song
            player.reset()
            preset = userInput.split()[1] # Build string representing preset name
            player.loadEvents(info['play'][preset])
            try:
                player.loadEvents(info['play'][preset])
            except:
                print('Error loading events')
            # Start a new thread to keep interface active while LEDs update
            _thread.start_new_thread(player.play,())
        elif command == 'demo':
            # Plays a preset pattern
            player.reset()
            preset = userInput.split()[1] # Build string representing preset name
            player.loadEvents(info['demo'][preset])
            try:
                player.loadEvents(info['demo'][preset])
            except:
                print('Error loading events')
            _thread.start_new_thread(player.play,())
        elif command == 'set':
            # Set all the LEDs a specified color
            lineInfo = getLineInfo(userInput)
            exec('player.setPattern({},{})'.format(lineInfo['parameters'],lineInfo['leds']))

        elif command == 'glow':
            # Used for testing
            # Makes the LEDs continuously increase then decrease in intensity
            lineInfo = getLineInfo(userInput)
            for led in lineInfo['leds']:
                exec('player.setGlow({},{})'.format(led,lineInfo['parameters']))

        elif command == 'spiral':
            # Used for testing
            # New color grows along strand of LEDs
            lineInfo = getLineInfo(userInput)
            for led in lineInfo['leds']:
                exec('player.setSpiral({},{})'.format(led,lineInfo['parameters']))

        elif command == 'start':
            # Player starts playing loaded LED events
            # Start a new thread to keep interface active while LEDs update
            _thread.start_new_thread(player.play,())
        #elif command == 'p':
        #    player.pause()
        elif command == 'r':
            player.reset()
        elif command == 's':
            player.stop()
        elif command == 'q':
            break
