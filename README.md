# Christmas_Tree_Lights
This project is to control WS2811 LED lights on a Christmas Tree.  This is a work in progress, but is in a state where tree events can be paired up with music.

Please visit the [Christmas Tree Lights Wiki](https://github.com/asellis/Christmas_Tree_Lights/wiki) for more details on the setup.

# Video

[![Video](https://i.ytimg.com/vi/DiNhDXpTWDw/hqdefault.jpg?sqp=-oaymwEjCPYBEIoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLDUJtWhysvL5qJiwSRvviOEOSzPIQ)](https://www.youtube.com/watch?v=DiNhDXpTWDw)

# Setup
There are 3 strands of WS2811 lights, each with 100 lights (2 strands of 50 are connected together to make one long strand), which are connected to an Arduino (Mega 2560) off of 3 seperate PWM pins.  A 5V 30A power supply is being used to power the LEDs.  Eventually, a Rasperry Pi will be used to send serial commands to the Arduino as to which lights to update.  Right now a computer is being used to send serial commands while developing the code.  The lights are able to update at around 20-25 fps.

On the software side of things, the FastLED library is used to store all the LED color info on the Arduino and is used to update the lights.  pyserial is used to send serial commands from a computer using running python code.

The Python code to control the LEDs are plit into several files:
- SerialCom.py handles all serial communications between the Python code and the Arduino
- LEDController.py is a class made for updating the LEDs in various ways
- LEDInterface.py is still a work in process, but its purpose is to issue commands of what LEDs or effect you want to apply
- LEDPlayer.py contains the means of playing events and setting patterns
- LEDInterface.py is an interface for controlling and playing events
- LEDReader is the Arduino application for controlling LEDs and receiving serial commands

# Current Features
- Update individual LEDs
- Update all LEDs at once
- Apply a pattern
- Layer the tree
- Glow
- Spiral
- Fade
- Twinkle
- Play a set of events
- Play events paired with a song
- Interface for playing events

# Currently working on
- Interface (making it easier to use)
- Documentation
- Wiki with instructions for use

# Credits/Libraries Used
FastLED (https://github.com/FastLED/FastLED)

pyserial

vlc (python-vlc)

Audionautix for song (free to use music on YouTube)

We Wish You A Merry Xmas by Audionautix is licensed under a Creative Commons Attribution license (https://creativecommons.org/licenses/by/4.0/)
Artist: http://audionautix.com/ 