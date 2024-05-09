const int stepPin = 1; //
const int dirPin = 10; 
const int EN=8;
//const int trigPin = 12;
//const int echoPin = 13;
//const int irsenL=9;
//const int irsenR=1;
int enA = 6;
int in1 = 7;//
int in2 = 5;
// motor two
int enB = 3;
int in3 = 4;
int in4 = 2;
long duration;
int dist=5;
bool x,y,t,max_pos=false,low_pos=true;
 
void setup() {
  // Sets the two pins as Outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);

  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT); 

  pinMode(irsenL,OUTPUT);
  pinMode(irsenR,OUTPUT);
  
  Serial.begin(9600);
}
void loop() {
  int sensorL=digitalRead(irsenL);
  int sensorR=digitalRead(irsenR);
  Serial.println(sensorL);
  //Serial.println(irsenR);
  
 if(measure_dis()>10){
  while(!max_pos){
    stepper_run_UP();
  }
  delay(2000);
  if(irsenL==LOW && irsenR==LOW){
      motor_run_F();
      delay(2000);
      motor_run_stop();
  }
  if(irsenL==HIGH && irsenR==LOW){
      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);
      delay(2000);
      motor_run_stop();
  }
  if(irsenL==LOW && irsenR==HIGH){
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      digitalWrite(in3, LOW);
      digitalWrite(in4, LOW);
      delay(2000);
      motor_run_stop();
  }
  while(!low_pos){
    stepper_run_down();
  } 
  delay(2000);
 }
 else{
  motor_run_stop();
 }
}
  
void motor_run_F(){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enA,100);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enB,100);
  
}

void motor_run_B(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA,200);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB,200);
}

void stepper_run_UP(){
  digitalWrite(EN,LOW);
  digitalWrite (dirPin,HIGH);
  for(int x = 0; x < 1500; x++) {//23000
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(800); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(800); 
  }
  max_pos=true;
  low_pos=false;
  
}
void stepper_run_down(){
  digitalWrite(EN,LOW);
  digitalWrite (dirPin,LOW);
  for(int x = 0; x < 1500; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(600); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(600); 
  }
  low_pos=true;
  max_pos=false;
}
void stop_stepper(){
  digitalWrite(EN,HIGH);
  delay(2000);
}
void motor_run_stop(){
  digitalWrite(in1,LOW);
  digitalWrite(in2,LOW);
  digitalWrite(in3,LOW);
  digitalWrite(in4,LOW);
}


int measure_dis(){
  int dis;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
 // dis = (duration * 0.034 / 2);
  dis=20;
  //Serial.println(dis);

  return dis;
}
