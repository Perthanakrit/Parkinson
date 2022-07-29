#include "Adafruit_ADXL343.h"


Adafruit_ADXL343  lox = Adafruit_ADXL343(12345);

void setup() {
  // Robojax.com I2C address update 20181206
  lox.begin(0x2B);// put any address between 0x29 to 0x7F 
}

void loop(){
  
}
