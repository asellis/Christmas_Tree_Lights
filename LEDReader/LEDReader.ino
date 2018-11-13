/* Reads serial input and executes the specified command
 * COMMANDS:
 * S  - sets the leds, folowed by bytes to update all leds
 * s  - show leds
 */

#include "FastLED.h"
#define SERIAL_BUFFER_SIZE 256   // increases serial buffer to ensure all data comes in

#define NUM_LEDS 300
CRGB leds[NUM_LEDS];

const int numBytes = NUM_LEDS * 3;    // The number of bytes needed for all the leds, 3 per led (R/G/B)
char receivedBytes[numBytes];    // a buffer to store all the led lights, will convert later to an int
                                // data received as char since we only need 8 bits per LED color
bool receiveDone = false;  // used to tell if there is more data still

void setup() {
  Serial.begin(500000);   // Starts serial to allow transfer of data

  // Setup LEDs, subject to change with added stands
  FastLED.addLeds<WS2811, 13, RGB>(leds, 100);
  FastLED.addLeds<WS2811, 12, RGB>(leds, 100);
  FastLED.addLeds<WS2811, 11, RGB>(leds, 100);
  //Serial.println("Start");

}

void loop() {
  recvCommand();
}

void recvCommand()
{
  // Checks serial input for a command
  // if there is input it will try to execute
  char command;
  if(Serial.available() > 0)
  {
    command = Serial.read();
    //Serial.println("Received");
    //Serial.println(command);
    readCommand(command);
  }
}

void recvData()
{
  // Receives data fo all LEDs
  int index = 0;
  char data;
  if(Serial.available() > 0)  // When the data has started to arrive
  {
    while(index < numBytes) // Read till receivedBytes array filled
    {
      if(Serial.available() > 0)  // To make sure data has arrived with every iteration
      {
        data = Serial.read();
        receivedBytes[index] = data;
        ++index;
      }
    }
    receiveDone = true; // Confirmation that the data has been received
  }
}

void readCommand(char serialCommand)
{
  // Attempts to execute the received command
  // Serial.println(serialCommand);
  switch(serialCommand)
  {
    case 'S': // Set LEDs
    {
      Serial.println("Ready");
      while(!receiveDone)
      {
        recvData();
      }
      setLED();
      receiveDone = false;
      break;
    }
    case 's': // Show all LEDs
    {
      FastLED.show();
      break;
    }
  }
  Serial.println("Done");
}

void setLED()
{
  int ledNum, r, g, b;
  for(int i=0; i<numBytes; i+=3)
  {
    // Get R/G/B data every third byte and convert to unsigned 8 bit int
    // Will result in values between 0 and 255
    r = (uint8_t)receivedBytes[i];
    g = (uint8_t)receivedBytes[i+1];
    b = (uint8_t)receivedBytes[i+2];

    // Set each LED
    ledNum = i/3;
    leds[ledNum].r = (int)r;
    leds[ledNum].g = (int)g;
    leds[ledNum].b = (int)b;
  }
}

