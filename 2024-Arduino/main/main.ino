#include "KedexController.h"
#include <Servo.h>
// #include <Stepper.h>

Servo servo;
int value = 80;

const int STEP_N1 = 8;
const int STEP_N2 = 9;
const int STEP_N3 = 10;
const int STEP_N4 = 11;

// Stepper stepper(512, STEP_N4, STEP_N2, STEP_N3, STEP_N1);

const int DETECT_PIN = 13;

const int ENB = 6;
const int IN3 = 4;
const int IN4 = 5;

KedexController kedex(STEP_N1, STEP_N2, STEP_N3, STEP_N4, DETECT_PIN, ENB, IN3, IN4);

void setup() {
    Serial.begin(115200);
    pinMode(DETECT_PIN, INPUT);
    pinMode(ENB, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);

    analogWrite(ENB, 0);

    while (!Serial) {
      ;
    }
    kedex.stepInit();

    servo.attach(3);
    servo.write(value);
    kedex.moveToPosition(0);
}

/*
  0: waiting
  1: get signal
  2: moving
  3: arrivied
*/

int temp = 0;

void loop() {
  bool dStatus = kedex.detect();
  
  if (dStatus == true) {
    kedex.serialRead();
    if (kedex.getBarcodeAvail()) {
      kedex.conveyorMove();
      kedex.setStepperToPos();
      delay(1500);
      kedex.resetFlags();
      value = 0;
      servo.write(value);
      delay(1000);
      kedex.setBarcodeAvail(LOW);
      dStatus = false;
    } else {
      value = 80;
      servo.write(value);
      delay(1000);
      kedex.moveToPosition(0);
      delay(1500);
      kedex.setCategoryID("");
    }
  } else {
    value = 80;
    servo.write(value);
    delay(1000);
    kedex.setStepperToPos();
    delay(1500);
  }
}
