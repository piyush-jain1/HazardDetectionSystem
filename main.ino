#include <dht.h>
#include <Wire.h>

dht DHT;

#define TEMPERATURE_PIN 7
#define VIBRATION_PIN 2
#define GAS_PIN A0
#define BUZZER 6
#define MOTORA 10
#define MOTORB 5

//sensitivity variables
int minimum = 200;
int maximum= 1023;
int maxdelay = 400;
int buzzer_count = 0;
int buzzer_on = 0;

float temp = 0;
float vibr = 0;
float gas = 0;
int tempcount = 0;
int elapsed = 0;
int flag = 0;
int fan_on = 0;
int vibr_on = 0;
int fire_on = 0;

void setup(){
  Serial.begin(9600);
  pinMode(BUZZER, OUTPUT);
  pinMode(MOTORA, OUTPUT);
  pinMode(MOTORB, OUTPUT);
}

void loop()
{ 
  elapsed = 0;
  temp = 0;
  vibr = 0;
  gas = 0;
  tempcount = 0;
  
    int temperature = DHT.read11(TEMPERATURE_PIN);
    temperature = DHT.temperature;
    if(temperature >= -274.0){
      temp = temp + temperature;
      tempcount = tempcount + 1;
    }
//    delay(5);
    int vreading = analogRead(VIBRATION_PIN);
    vreading = constrain(vreading, minimum, maximum);
    vreading = map(vreading, minimum, maximum, 0, 15);
    vibr = vibr + vreading;
//    delay(5);
    float sensor_volt;
    float R0 = 13.5;
    float RS_gas; // Get value of RS in a GAS
    float ratio; // Get ratio RS_GAS/RS_air
    int greading = analogRead(GAS_PIN);
    sensor_volt=(float)greading/1024*5.0;
    RS_gas = (5.0-sensor_volt)/sensor_volt;
    ratio = RS_gas/R0;  // ratio = RS/R0
    gas = gas+ratio;
//    delay(5);
  if (tempcount == 0){
    tempcount = 1;
  }
  temp = temp/tempcount;
  vibr = vibr/1;
  gas = gas/1; 
  if(Serial.available()){
      
    Serial.print(temp);
    Serial.print(" ");
    Serial.print(vibr);
    Serial.print(" ");
    Serial.println(gas);  
    int sig = Serial.read();
    sig = sig-48;
   if(buzzer_on == 1)
   {
      if(buzzer_count < 200){
        int freq = 1000;
        if(fire_on == 1){
          freq = 800;
        }
        else if(vibr_on == 1){
          freq = 1200;
        }
        else if(fan_on == 1){
          freq = 1400;
        }
        tone(BUZZER, freq, 5);
        if(fan_on == 1){
          digitalWrite(MOTORA,HIGH);
          digitalWrite(MOTORB,LOW);
        }
        buzzer_count = buzzer_count + 1;  
      }
      else{
          digitalWrite(MOTORA,LOW);
          digitalWrite(MOTORB,LOW);
          buzzer_on = 0; 
          fan_on = 0;
      }
   }
   if(buzzer_on == 0){ 
    fan_on = 0;
    fire_on = 0;
    vibr_on = 0;
   if(sig == 1){
      buzzer_on = 1;
      fire_on = 1;
      buzzer_count = 0;       
    }    
    else if(sig == 2){
      buzzer_on = 1;
      buzzer_count = 0;  
      vibr_on = 1;
    }    
    else if(sig == 3){
      buzzer_on = 1;
      buzzer_count = 0; 
      fan_on = 1; 
    }
   }     
  }
}
