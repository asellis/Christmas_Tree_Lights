# Christmas_Tree_Lights
This project is to synchronize control of WS2811 LED lights on a Christmas Tree with music.

Please visit the [Christmas Tree Lights Wiki](https://github.com/asellis/Christmas_Tree_Lights/wiki) for more details on the setup.

# Video

[![Video](https://i.ytimg.com/vi/DiNhDXpTWDw/hqdefault.jpg?sqp=-oaymwEjCPYBEIoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLDUJtWhysvL5qJiwSRvviOEOSzPIQ)](https://www.youtube.com/watch?v=DiNhDXpTWDw)

# Overview
The system consists of a computer (or Raspberry Pi) that plays a music file and sends lighting synchronization and effects data through USB to an Arduino microcontroller which configures connected LED lighting strands accordingly.

Connected to the Arduino are 3 strands of WS2811 lights, each with 100 individually addressable LEDs (2 strands of 50 are connected together to make one long strand).  A 5V 30A power supply is being used to power the LEDs.  The lights are able to update at a rate around 20-25 times per second.

The Python code to control the LEDs are split into several files:
- LEDInterface.py is the main executable python file
- LEDPlayer.py is a class that plays the mp3 file, calculates LED color values based on different effects and decides when to update them based on a configuration text file
- LEDController.py is a class made for holding the current state of the LED color values and sending data to the Arduino
- SerialCom.py is a wrapper that handles all serial communications between the Python code and the Arduino

Arduino File
- LEDReader.ino receives commands and data from USB and updates and displays LED color values on the light strands

# Current Features
- Define which LEDs occur at certain vertical layer of the tree
- Play a set of LED events
- Play LED events synchronized with a song
- Update individual LEDs or all at once
- Apply a repeating color pattern
- Apply lighting effects: glow, spiral, fade, twinkle

# Credits/Libraries Used
FastLED (https://github.com/FastLED/FastLED)
pyserial
Vlc media player (python-vlc)
Audionautix for song (free to use music on YouTube)
We Wish You A Merry Xmas by Audionautix is licensed under a Creative Commons Attribution license (https://creativecommons.org/licenses/by/4.0/)
Artist: http://audionautix.com/