/* This program is used to receive data through a serial connection with the Arduino
 *  to update the LED colors.
 * PROTOCOL:
 * 1. The Arduino receives a one byte command
 * 2. The Arduino replies "Ready" when receiving LED data
 * 3. The Arduino receives LED data packet
 * 4. The Arduino replies "Done" when finished with command
 * COMMANDS:
 *  S  - Set LED color information in Arduino memory
 *  W  - show all LEDs by writing the color data to the LEDs
 */

#include "FastLED.h"
#define SERIAL_BUFFER_SIZE 256   // increases serial buffer to ensure all data comes in

#define NUM_LEDS 300

// Each strand uses its own pin and has size equal to the number of LEDs on the strand
// CRGB is from FastLED library
CRGB Strand1[100];
CRGB Strand2[100];
CRGB Strand3[100];

#define NUM_BYTES NUM_LEDS*3    // The number of bytes needed for all the leds, 3 per led (R/G/B)
char receivedBytes[NUM_BYTES];  // a buffer to store all the led lights, will convert later to an int
                                // data received as char since we only need 8 bits per LED color

void setup() {
  // setup function called when Arduino starts
  Serial.begin(500000);   // Starts serial to allow transfer of data at a baud rate of 5000000

  // Setup LEDs
  // <LED type, pin, color type>(Strand, number of LEDs in strand)
  FastLED.addLeds<WS2811, 13, RGB>(Strand1, 100);
  FastLED.addLeds<WS2811, 12, RGB>(Strand2, 100);
  FastLED.addLeds<WS2811, 11, RGB>(Strand3, 100);
  //Serial.println("Start");
}

void loop() {
  // Called after setup is complete
  // Background loop
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
    execCommand(command); // Parses and executes command
  }
}

bool recvData()
{
  // Receives data packet of all LEDs
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
    return true; // Confirmation that the data has been received
  }
  return false;
}

void execCommand(char serialCommand)
{
  // Attempts to execute the received command
  // Serial.println(serialCommand);
  switch(serialCommand)
  {
    case 'S': // Set LED color information in Arduino memory
    {
      Serial.println("Ready");
      while(!recvData())
      {
        continue;
      }
      setLEDStrandArrays();
      break;
    }
    case 'W': // show all LEDs by writing the color data to the LEDs
    {
      FastLED.show();
      break;
    }
  }
  Serial.println("Done");
}

void setLEDStrandArrays()
{  
  // Transfers the recieved data into the strand arrays
  int ledNum, r, g, b;
  for(int i=0; i<NUM_BYTES; i+=3)
  {
    // Get R/G/B data and convert to unsigned 8 bit int
    r = (uint8_t)receivedBytes[i];
    g = (uint8_t)receivedBytes[i+1];
    b = (uint8_t)receivedBytes[i+2];

    // Set each LED in the Stand arrays
    // if statement to select LED strand
    if(i<(100*3))
    {
      ledNum = i/3;
      Strand1[ledNum].r = (int)r;
      Strand1[ledNum].g = (int)g;
      Strand1[ledNum].b = (int)b;
    }
    else if(i>=(100*3) && i<(200*3))
    {
      ledNum = (i-(100*3))/3;
      Strand2[ledNum].r = (int)r;
      Strand2[ledNum].g = (int)g;
      Strand2[ledNum].b = (int)b;
    }
    else if(i>=(200*3))
    {
      ledNum = (i-(200*3))/3;
      Strand3[ledNum].r = (int)r;
      Strand3[ledNum].g = (int)g;
      Strand3[ledNum].b = (int)b;
    }
  }
}
