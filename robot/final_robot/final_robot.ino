#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define CE_PIN 9
#define CSN_PIN 10

const int stepPin = 2;
const int dirPin = 4;
const int EN = 7;

int enA = 6;
int in1 = 15;
int in2 = 16;

int enB = 3;
int in3 = 17;
int in4 = 18;

const byte address[6] = "00001";
char receivedData[32] = "";
RF24 radio(CE_PIN, CSN_PIN);
int data[2];
byte incoming_data;
unsigned long lastReceiveTime = 0;


unsigned long stepperTimer = 0;
int stepperdelay = 900;  
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
  //Serial.println("Nrf24L01 Receiver Starting");
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();

  digitalWrite(dirPin, stepperDirection);
  digitalWrite(stepPin, stepInState);
  digitalWrite(EN, LOW);
}

void loop() {
  currentMicros = micros();
  lastReceiveTime= millis();
  radioFun();
  //stop_stepper();
 stepper_run();
  
}

void radioFun() {
  if (radio.available()) {
    radio.read(data, sizeof(data));
    radio.read(&receivedData, sizeof(receivedData));
    //Serial.println("Serial start");
    //Serial.print("data[1]");
    //Serial.println(data[1]);
    //Serial.print("data[0]");
    //Serial.println(data[0]);
   
    if (data[1] > 250) {
      motor_run_F();
      //Serial.println("forward");
    } else if ((data[1] < 100) & (data[1]>=0)) {
      motor_run_B();
    } else if ((data[1] > 100 && data[1] < 220)&& data[0]>100 && data[0]<220) {
      motor_run_stop();
    }
    else if (data[0] > 250){
      right();
    }
    else if ((data[0]<100) && (data[0]>=0)){
      left();
    }
    
  }
}

void motor_run_F() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, 100);
  digitalWrite(in4,HIGH);
  digitalWrite(in3, LOW);
  analogWrite(enB, 65);
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
  digitalWrite(in4, HIGH);
  digitalWrite(in3, LOW);
  analogWrite(enB, 100);
}

void motor_run_B() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
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
    
    if (stepsCounter >19000) {
      stepperDirection = !stepperDirection;
      digitalWrite(dirPin, stepperDirection);
      stepsCounter = 0;
    }
  }
}
void stop_stepper(){
  digitalWrite(EN,HIGH);
}
