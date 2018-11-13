# Christmas_Tree_Lights
This project is to control WS2811 LED lights on a Christmas Tree.

This is a work in progress, but it is currently in a state where commands can be passed to update the LEDs on a tree.

# Setup
There are 3 strands of WS2811 lights, each with 100 lights (2 strands of 50 are connected together to make one long strand), which are connected to an Arduino (Mega 2560) off of 3 seperate PWM pins.  A 5V 30A power supply is being used to power the LEDs.  Eventually, a Rasperry Pi will be used to send serial commands to the Arduino as to which lights to update.  Right now a computer is being used to send serial commands while developing the code.  The lights are able to update at around 20-25 fps.

On the software side of things, the FastLED library is used to store all the LED color info on the Arduino and is used to update the lights.  pyserial is used to send serial commands from a computer using running python code.

The Python code to control the LEDs are plit into several files:
- SerialCom.py handles all serial communications between the Python code and the Arduino
- xLEDController.py is a class made for updating the LEDs in various ways
- xLEDInterface.py is still a work in process, but its purpose is to issue commands of what LEDs or effect you want to apply
- LEDReader is the Arduino application for controlling LEDs and receiving serial commands

# Current Features
- Update individual LEDs
- Update all LEDs at once
- Apply a pattern

# Features Currently working on
- Layers, select a portion of the strand to update a certain way
- Glow and while loops (multi-threading)
- Interface (will probably stay as a text based interface and commands will be less for testing)

# Other Features to look into
- Reading commands from a file (will be after figuring out layers and commands in a while loop)
- Pairing with music
- Controlling from Android

# Images
To be added

# Credits
FastLED (https://github.com/FastLED/FastLED)