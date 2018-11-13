#include "WS2811.hpp"
#include "Arduino.h"

#define PIXEL_DDR DDRB
#define PIXEL_PORT PORTB
#define PIXEL_BIT 7   // Using pin 13 which will be the last bit

// Bit width times, H=high, L=low
// 1 bit in ns
#define T1H 700
#define T1L 600

// 0 bit in ns
#define T0H 350
#define T0L 800

// Time for bit latch
#define RES 300000

#define NS_PER_SEC (1000000000L)
#define CYCLES_PER_SEC (F_CPU)
#define NS_PER_CYCLE (NS_PER_SEC/CYCLES_PER_SEC)
#define NS_TO_CYCLES(n) ((n)/NS_PER_CYCLE)
#define DELAY_CYCLES(n) __builtin_avr_delay_cycles(n)

void sendBit( bool bitVal )
{
  // Send 1
	if(bitVal)
	{
		bitSet(PIXEL_PORT, PIXEL_BIT);
		DELAY_CYCLES(NS_TO_CYCLES(T1H));
		bitClear(PIXEL_PORT, PIXEL_BIT);
		DELAY_CYCLES(NS_TO_CYCLES(T1L));
	}
  // Send 0
	else
	{
		cli();
		bitSet(PIXEL_PORT, PIXEL_BIT);
		DELAY_CYCLES(NS_TO_CYCLES(T0H));
		bitClear(PIXEL_PORT, PIXEL_BIT);
		sei();
		DELAY_CYCLES(NS_TO_CYCLES(T0L));
	}
}

void sendByte( unsigned char byte )
{
  for(unsigned char bit=0; bit<8; bit++)
  {
    sendBit(bitRead(byte, 7)); // send highest bit first
    byte <<= 1; // Shift byte
  }
}

void sendPixel( unsigned char r, unsigned char g, unsigned char b)
{
  sendByte(r);
  sendByte(g);
  sendByte(b);
}

void show()
{
  DELAY_CYCLES(NS_TO_CYCLES(RES));
}

void ledsetup()
{
  bitSet(PIXEL_DDR, PIXEL_BIT);
}
