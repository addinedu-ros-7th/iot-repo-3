#ifndef KEDEXCONTROLLER_H
#define KEDEXCONTROLLER_H

#include "Queue.h"
#include "Product.h"
#include <Stepper.h>

// data: 123|productname|112 -> 123
String split(String &data, char seperator)
{
    int seperatorPosition = data.indexOf(seperator);
    String result;
    if(seperatorPosition != -1)
    {
        result = data.substring(0, seperatorPosition);
        data = data.substring(seperatorPosition + 1, data.length());
    }
    else
    {
        result = data;
        data= "";
    }
    // 보내야 할 데이터 븐류코드|상품코크|각도
    return result;
}

class KedexController {
  public:
    int kedexStatus;
    int stepperPos;
    int dataFlow = -1;
    unsigned long waitingStartTime;
    int step_n1_pin;
    int step_n2_pin;
    int step_n3_pin;
    int step_n4_pin;
    int detect_pin;
    int conv_enb_pin;
    int conv_in3_pin;
    int conv_in4_pin;
    unsigned long conv_start_time = 0;
    String categoryID = "";
    String productID = "";
    String inString = "";

    const int STEP_N1 = 8;
    const int STEP_N2 = 9;
    const int STEP_N3 = 10;
    const int STEP_N4 = 11;
    const int DETECT_PIN = 13;
    const int FRONT_DETECT_PIN = 12;

    Stepper kedexStepper;
    Queue<Product> product_queue;

    KedexController(int step_n1_pin, int step_n2_pin, int step_n3_pin, int step_n4_pin, 
                    int detect_pin, 
                    int conv_enb_pin, int conv_in3_pin, int conv_in4_pin):
    kedexStatus(0), stepperPos(0), dataFlow(-1), inString(""),
    step_n1_pin(step_n1_pin), step_n2_pin(step_n2_pin), step_n3_pin(step_n3_pin), step_n4_pin(step_n4_pin),
    detect_pin(detect_pin),
    conv_enb_pin(conv_enb_pin), conv_in3_pin(conv_in3_pin), conv_in4_pin(conv_in4_pin),
    kedexStepper(512,step_n4_pin,step_n2_pin,step_n3_pin,step_n1_pin),
    product_queue()
    { kedexStepper.setSpeed(50); }

    int getKedexStatus() { return kedexStatus; }
    void setKedexStatus(int status) { kedexStatus = status; }

    String getCategoryID() { return categoryID; }
    void setCategoryID(String categoryid) { categoryID = categoryid; }

    String getProductID() { return productID; }
    void setProductID(String productid) { productID = productid; }

    unsigned long getConv_start_time() { return conv_start_time; }
    void setConv_start_time(unsigned long temp) { conv_start_time = temp; }

    int sorterStatus = 0;
    int currStepperPos = 0;
    int absStepperPos = 0;
    unsigned long lastDetectTime = 0;
    unsigned long sorterWaitTime = 0;

    void moveToPosition(int absStepperPos) {
        kedexStepper.step(absStepperPos - currStepperPos);
        currStepperPos = absStepperPos;
    }

    void stepInit() {
      kedexStepper.step(0);
    }

    bool barcodeStatus = LOW;
    void setBarcodeAvail(bool status) {
      // if(status == true) {

      // } else {status == false) {
        
      // }
      
      barcodeStatus = status;
    }

    bool getBarcodeAvail() {
      return barcodeStatus;
    }

    void serialRead() {
    // 시리얼에서 값 읽어와서 int productID, String sku, String productName, destinationID 값 저장한 Product 객체 만들기
      if (dataFlow == 1) {
        if(Serial.available() > 0) {
          dataFlow *= -1;
          inString = Serial.readString();
          if(inString == "\n" || inString == "") {
            inString = "";
            // setBarcodeAvail(LOW);
          } else {
            String str1 = inString.substring(0, inString.indexOf("|"));
            String str2 = inString.substring(inString.indexOf("|"), inString.length() - 1);
            categoryID = str1;
            productID = str2;
            setBarcodeAvail(true);
          }
          // 데이터를 받는 부분
        }
      } else if (dataFlow == -1) {
        dataFlow *= -1;
        if(inString != "") {
          String str = String(getCategoryID());
          Serial.println(str);
          // }
        } else {
          Serial.println("");
        }
      }
    }

    void setStepperToPos() {
      String str = String(getCategoryID());
      if (str == "1100000000") {
        stepperPos = 400;
        moveToPosition(stepperPos);
      } else if (str == "2600000000") {
        stepperPos = 0;
        moveToPosition(stepperPos);
      } else if (str == "4100000000") {
        stepperPos = -400;
        moveToPosition(stepperPos);
      } else {
        stepperPos = 0;
        moveToPosition(stepperPos);
      }
      // str = "";
      // setBarcodeAvail(LOW);
    }

    bool detect() {
      if (digitalRead(detect_pin) == HIGH) {
        delay(125);
        return true;
      }
      return false;
    }

    int temp = 0;
    void resetFlags() {
      temp = 0;
    }

    void conveyorMove() {
      int status = kedexStatus;
      digitalWrite(conv_in3_pin, LOW); 
      digitalWrite(conv_in4_pin, HIGH);

      if (temp == 0) {
        analogWrite(conv_enb_pin, 150);
        delay(1300);
        analogWrite(conv_enb_pin, 80);
        delay(300);
        temp = 1;
      }
      // analogWrite(conv_enb_pin, 80);

      analogWrite(conv_enb_pin, 0);
    }
};
#endif