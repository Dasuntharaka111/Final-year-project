#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#define CE_PIN 9
#define CSN_PIN 10
#define x A0
#define y A1
#include<printf.h>
char xyData[32] = "";

const byte address[6] = "00001";
RF24 radio(CE_PIN, CSN_PIN);
int data[2];

void setup()
{
 Serial.begin(9600);
 radio.begin();
 radio.openWritingPipe(address);
 radio.setPALevel(RF24_PA_MIN);
 radio.stopListening();
 pinMode(x,INPUT);
 pinMode(y,INPUT);

}

void loop()
{

  data[0] = map(analogRead(x), 0, 1023, 0, 255); 
  data[1]= map(analogRead(y), 0, 1023, 0, 255);
  Serial.println(data[1]);
  radio.write(data, sizeof(data));
}
