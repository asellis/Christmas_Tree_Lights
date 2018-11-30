# An interface to execute commands for xmas LED controller

from LEDPlayer import LEDPlayer
from time import sleep
import _thread
import sys
import os
currentDir = os.getcwd()
demoDir = currentDir+'/PremadeEvents/'

loadFile='loadInfo.txt'

notes = """
This is a text base interface for controlling LEDs
Will automatically try to load presets from file {}
""".format(loadFile)


setCommands = """
--- Set Commands ---
PATTERN     set layer [(patern1),(patern2),...]
GLOW        glow layer parameter1=value1 parameter2=value2 ...
SPIRAL      spiral layer parameter1=value1 parameter2=value2 ...
"""
playerCommands = """
--- Player Commands ---
START       start
PLAY        play preset
PREMADE     demo preset
RESET       r
STOP        s
QUIT        q
"""

info=dict()
info['play']=dict()
info['demo']=dict()
info['port']=''
info['baudRate']=500000

def connect(port,baudRate):
    return LEDPlayer(port=port,baudRate=baudRate)

def loadInfo(file):
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
            l=[int(i) for i in items[1].split(',')]
            info['layers']=l
        elif items[0]=='baudRate':
            info['baudRate']=int(items[1])
        else:
            info[items[0]]=items[1]

def getLineInfo(line):
    l = line.strip().split(' ')
    layers = []
    if '+' in l[1]:
        layers=l[1].split('+')
        for led in layers:
            led.strip()
    else:
        layers = l[1]
        layers.strip()
        layers=[layers]
    leds=[]
    for layer in layers:
        leds+=player.getLayer(layer)

    # Parameters
    parameters=','.join(l[2:])

    lineInfo = dict()
    lineInfo['leds']=leds
    lineInfo['parameters']=parameters
    return lineInfo

    


def execCode(code):
    exec(code)


if __name__ == '__main__':
    player = None
    print(notes)
    try:
        loadInfo(loadFile)
        print('Loaded info from {}'.format(loadFile))
    except:
        print('Failed to load info from {}'.format(loadFile))
    try:
        player = connect(info['port'],info['baudRate'])
        if 'layers' in info.keys():
            player.setLayers(info['layers'])
        print('Connected')
    except:
        print('Not connected')
    while True:
        print(setCommands)
        print(playerCommands)
        userInput = input('Specify Command: ')
        command = userInput.split()[0]
        if command == 'exec':
            code = ''.join(i + ' ' for i in userInput.split()[1:])
            _thread.start_new_thread(execCode,(code,))
        elif command == 'play':
            player.reset()
            preset = ''
            for item in userInput.split()[1:]:
                preset += item
            player.loadEvents(info['play'][preset])
            try:
                player.loadEvents(info['play'][preset])
            except:
                print('Error loading events')
            _thread.start_new_thread(player.play,())
        elif command == 'demo':
            player.reset()
            preset = ''
            for item in userInput.split()[1:]:
                preset += item
            player.loadEvents(info['demo'][preset])
            try:
                player.loadEvents(info['demo'][preset])
            except:
                print('Error loading events')
            _thread.start_new_thread(player.play,())
        elif command == 'set':
            lineInfo = getLineInfo(userInput)
            exec('player.setPattern({},{})'.format(lineInfo['parameters'],lineInfo['leds']))

        elif command == 'glow':
            lineInfo = getLineInfo(userInput)
            for led in lineInfo['leds']:
                exec('player.setGlow({},{})'.format(led,lineInfo['parameters']))
        elif command == 'spiral':
            lineInfo = getLineInfo(userInput)
            for led in lineInfo['leds']:
                exec('player.setSpiral({},{})'.format(led,lineInfo['parameters']))

        elif command == 'start':
            _thread.start_new_thread(player.play,())
        #elif command == 'p':
        #    player.pause()
        elif command == 'r':
            player.reset()
        elif command == 's':
            player.stop()
        elif command == 'q':
            break
