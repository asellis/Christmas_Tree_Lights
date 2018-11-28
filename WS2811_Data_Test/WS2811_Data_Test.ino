// Testing manual data stream to led lights
#include "WS2811.hpp"


int wait = 1000;
int ledCount = 100;

void setup() {
  ledsetup();  
  for(int i=0; i<100; ++i)
  {
    sendPixel(255,255,255);
  }
  show();
}

void loop() {
  
  // Reset all pixels
  //setColor(200, 100, 50);
  /*
  resetLeds();
  show();
  
  delay(wait);
  sendPixel(100, 0, 0);
  show();
  delay(wait);
  sendPixel(0,100,0);
  show();
  delay(wait);
  sendPixel(0,0,100);
  show();
  delay(wait);
  sendPixel(100,0,0);
  sendPixel(0,100,0);
  sendPixel(0,0,100);
  show();
  delay(wait);
  */
}

void resetLeds()
{
  for(int i=0; i<ledCount; ++i)
  {
    sendPixel(0,0,0);
  }
  show();
}

void setColor(int r, int g, int b, int n = ledCount)
{
  // sets the color for the first n leds
  for(int i=0; i<n; ++i)
  {
    sendPixel(r, g, b);
  }
  show();
}
