#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define CE_PIN 9
#define CSN_PIN 10

const int stepPin = 18;
const int dirPin = 8;
const int EN = 19;

int enA = 6;
int in1 = 7;
int in2 = 5;
int Incoming_data;
int enB = 3;
int in3 = 4;
int in4 = 2;

struct RemoteControlData {
  byte x;
  byte y;
};
//RemoteControlData remoteData;
const uint64_t pipe = 0xE8E8F0F0E1LL;

RF24 radio(CE_PIN, CSN_PIN);
byte data[2];
unsigned long lastReceiveTime = 0;
int incoming_data;

unsigned long stepperTimer = 0;
int stepperdelay = 800;  
int stepsCounter = 0;
bool stepperDirection=1;  
byte stepInState=0;
unsigned long currentMicros;

void setup() {
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);

  Serial.begin(9600);
  Serial.println("Nrf24L01 Receiver Starting");
  radio.begin();
  radio.openReadingPipe(1, pipe);
  radio.startListening();

  // Start the stepper motor moving in the initial direction
  digitalWrite(dirPin, stepperDirection);
  digitalWrite(stepPin, stepInState);
  digitalWrite(EN, LOW);
}

void loop() {
  currentMicros = micros();
  radioFun();
 /* if (Serial.available()>0){
    Incoming_data=Serial.read();
    if(Incoming_data=='s'){
      stepper_run();
    }
    else{
      stop_stepper();
    }
  }
  
  */
  
}
 
  


void radioFun() {
  if (radio.available()) {
    radio.read(data, sizeof(data));
    Serial.println(data[0]);
 /*   
    if (data[1] > 250) {
      motor_run_F();
      //Serial.println("forward");
    } else if (data[1] < 60 && data[1]>0) {
      motor_run_B();
    } else if ((data[1] > 130 && data[1] < 160)&& data[0]>130 && data[0]<160) {
      motor_run_stop();
    }
    else if (data[0] > 250){
      right();
    }
    else if (data[0]<50 && data[0]>0){
      left();
    }
    
  */  
  }
  
}

void motor_run_F() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enA, 100);
  digitalWrite(in4, HIGH);
  digitalWrite(in3, LOW);
  analogWrite(enB, 100);
}
void right() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, 100);
  digitalWrite(in4, LOW);
  digitalWrite(in3, LOW);
  analogWrite(enB, 100);
}
void left() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  analogWrite(enA, 100);
  digitalWrite(in4, LOW);
  digitalWrite(in3, HIGH);
  analogWrite(enB, 100);
}

void motor_run_B() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, 200);
  digitalWrite(in4, LOW);
  digitalWrite(in3, HIGH);
  analogWrite(enB, 200);
}

void motor_run_stop() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void stepper_run() {
  //currentMicros = micros();
  if ((currentMicros - stepperTimer )>= stepperdelay) {
    stepperTimer=currentMicros;
    if(stepInState > 0){
      stepInState=0;
    }
    else{
      stepInState=1;
      }
    digitalWrite(stepPin, stepInState);
    stepsCounter++;
    
    if (stepsCounter >9000) {
      stepperDirection = !stepperDirection;
      digitalWrite(dirPin, stepperDirection);
      stepsCounter = 0;
    }
  }
}
void stop_stepper(){
  digitalWrite(EN,HIGH);
}
