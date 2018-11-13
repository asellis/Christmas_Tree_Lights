# An interface to execute commands for xmas LED controller

from xLEDController import xLEDController
from time import sleep
import _thread

commands = """
COMMANDS:
    exec (followed by python code, executes code)
    glow
    stop
    quit
"""

ctrl = xLEDController()

def execCode(code):
    exec(code)

while True:
    print(commands)
    userInput = input('Specify Command: ')
    command = userInput.split()[0]
    if command == 'exec':
        code = ''.join(i + ' ' for i in userInput.split()[1:])
        _thread.start_new_thread(execCode,(code,))
    elif command == 'glow':
        _thread.start_new_thread(execCode, ('ctrl.glow()',))
    elif command == 'stop':
        ctrl.stop()
    elif command == 'quit':
        break
