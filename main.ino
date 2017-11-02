#include <dht.h>
#include <Wire.h>

dht DHT;

#define TEMPERATURE_PIN 7
#define VIBRATION_PIN 2
#define GAS_PIN A0
#define BUZZER 6

//sensitivity variables
int minimum = 200;
int maximum= 1023;
int maxdelay = 400;

float temp = 0;
float vibr = 0;
float gas = 0;
int tempcount = 0;
int elapsed = 0;
int flag = 0;

//void buzzer(int sig){
// 
//}

void setup(){
  Serial.begin(9600);
  pinMode(BUZZER, OUTPUT);
}

void loop()
{ 
  elapsed = 0;
  temp = 0;
  vibr = 0;
  gas = 0;
  tempcount = 0;
  while(elapsed < 55){
    int temperature = DHT.read11(TEMPERATURE_PIN);
    temperature = DHT.temperature;
    if(temperature >= -274.0){
      temp = temp + temperature;
      tempcount = tempcount + 1;
    }
    delay(5);
    int vreading = analogRead(VIBRATION_PIN);
    vreading = constrain(vreading, minimum, maximum);
    vreading = map(vreading, minimum, maximum, 0, 15);
    vibr = vibr + vreading;
    delay(5);
    float sensor_volt;
    float RS_gas; // Get value of RS in a GAS
    float ratio; // Get ratio RS_GAS/RS_air
    int greading = analogRead(GAS_PIN);
    gas = gas + greading;
    delay(5);
    elapsed = elapsed+15;   
  }
  
  temp = temp/tempcount;
  vibr = vibr/4;
  gas = gas/4; 
  if(Serial.available()){  
    Serial.print(DHT.temperature);
    Serial.print(" ");
    Serial.print(vibr);
    Serial.print(" ");
    Serial.println(gas);  
    int sig = Serial.read();
    sig = sig-48;
//    Serial.print("Sig :    ");
//    Serial.println(sig);
     if(sig == 1){
        tone(BUZZER, 1000, 500);        
      }    
      else if(sig == 2){
        tone(BUZZER, 1500, 500);      
      }    
      else if(sig == 3){
        tone(BUZZER, 2000, 500); 
      }     
  }

}

