#include <Adafruit_NeoPixel.h>
#define PIN 13

void setup() {
  // put your setup code here, to run once:
  Adafruit_NeoPixel strip = Adafruit_NeoPixel(100, PIN, NEO_RGB + NEO_KHZ400);
  strip.begin();
  for(int i=0; i<100; ++i)
  {
    strip.setPixelColor(i, 255, 255, 255);
  }
  strip.show();
}

void loop() {
  // put your main code here, to run repeatedly:

}
