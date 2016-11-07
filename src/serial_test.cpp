#define DEVOLOPER

#ifdef DEVOLOPER
#include "serial_operation.h"
#include <Arduino.h>
#include <HardwareSerial.h>
HardwareSerial Serial;
#endif

#include <Servo/src/Servo.h>

Servo servo;

void setup()
{
  Serial.begin(9600);
  servo.attach(7);
  servo.write(90);
  Serial.println("Serial begin!");
}

int sequence = 0;
void loop()
{
  String cmd;
  while (Serial.available())
  {
    cmd += (char)Serial.read();
    delay(2);
  }
  if(cmd.length())
  {
    int angle;
    sscanf(cmd.c_str(), "%d", &angle);
    servo.write(angle);
    delay(200);
    Serial.print("angle:  ");
    Serial.println(angle);
  }
  delay(5);
}
