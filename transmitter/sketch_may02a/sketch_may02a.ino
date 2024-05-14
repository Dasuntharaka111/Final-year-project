#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#define CE_PIN 9
#define CSN_PIN 10
#define x A0
#define y A1

const uint64_t pipe = 0xE8E8F0F0E1LL;

RF24 radio(CE_PIN, CSN_PIN);
byte data[2];

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(pipe);
  pinMode(x, INPUT);
  pinMode(y, INPUT);
}

void loop() {
  data[0] = map(analogRead(x), 0, 1023, 0, 255); 
  data[1] = map(analogRead(y), 0, 1023, 0, 255);
  Serial.println(data[0]);
  }
  //delay(1000); // Delay between transmissions
