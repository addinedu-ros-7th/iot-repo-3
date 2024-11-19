#include "Queue.h"
#include "Product.h"
#include <Stepper.h>
#include "Ser.h"

const int STEP_N1 = 8;
const int STEP_N2 = 9;
const int STEP_N3 = 10;
const int STEP_N4 = 11;
const int DETECT_PIN = 13;
const int FRONT_DETECT_PIN = 12;
// const int ENB = 6;
// const int IN3 = 4;
// const int IN4 = 5;
Queue<Product> productQueue;

// ---- Serial ---- 
Ser ser;

// ---- sorter ----
int sorterStatus = 0;
Stepper stepper(2048, STEP_N4, STEP_N2, STEP_N3, STEP_N1);
int currStepperPos = 0;
int absStepperPos = 0;
unsigned long lastDetectTime = 0;
unsigned long sorterWaitTime = 0;

void moveToPosition(int absStepperPos) {
    stepper.step(absStepperPos - currStepperPos);
    currStepperPos = absStepperPos;
}
// ---- sorter ----

void setup() {
    delay(2000);
    Serial.begin(115200);
    Serial.println("Setup started.");
    stepper.setSpeed(10);
    pinMode(DETECT_PIN, INPUT);
    pinMode(FRONT_DETECT_PIN, INPUT);
    Serial.println("Setup finished.");
}
/* 0: waiting
   1: get signal
   2: moving
   3: arrivied
*/
void loop() {
// -----------------
    ser.serialRead();
    if (ser.getCategoryID()) {
        Serial.println(ser.getCategoryID());

        Product temp(ser.getProductID(), ser.getCategoryID());
        productQueue.enqueue(temp);

        Product ptemp;
        productQueue.peek(ptemp);
        ptemp.displayProductInfo();
    }
    
// ------------------
    // 컨베이어 하부 Sorting
    if (sorterStatus == 0) {
        if (!productQueue.isEmpty()) {
            sorterStatus = 1;
        }
    } else if (sorterStatus == 1) {
        Product temp;
        productQueue.peek(temp);
        if (temp.getCategoryID() == "1100000000") {
            moveToPosition(256);
        } else if (temp.getCategoryID() == "2600000000") {
            moveToPosition(0);
        } else if (temp.getCategoryID() == "4100000000") {
            moveToPosition(-256);
        }
        sorterStatus = 2;
    } else if (sorterStatus == 2) {
        if (millis() - lastDetectTime > 1500) {
          if (digitalRead(DETECT_PIN)) {
            delay(50);
            if (digitalRead(DETECT_PIN)) {
              lastDetectTime = millis();
              Product temp;
              productQueue.dequeue(temp);
              temp.displayProductInfo();
              sorterWaitTime = millis();
              sorterStatus = 3;
            }
          }
        }
    } else if (sorterStatus == 3) {
        if (millis() - sorterWaitTime > 1500) {
            sorterStatus = 0;
        }
    }
} 