#ifndef WS2811_HPP
#define WS2811_HPP

void sendBit( bool bitVal );
void sendByte( unsigned char byte );
void show();

void ledsetup();

void sendPixel( unsigned char r, unsigned char g, unsigned char b);

#endif
