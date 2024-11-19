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
    // Serial.println(result);
    // Serial.println("---------------------------------");
    // 보내야 할 데이터 븐류코드|상품코크|각도
    return result;
}

class KedexController {
  public:
    int kedexStatus;
    int stepperPos;
    int dataFlow;
    String inString = "";
    unsigned long waitingStartTime;
    int step_n1_pin;
    int step_n2_pin;
    int step_n3_pin;
    int step_n4_pin;
    int detect_pin;
    int conv_enb_pin;
    int conv_in3_pin;
    int conv_in4_pin;
    String categoryID = "";
    String productID = "";

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
    { kedexStepper.setSpeed(10); }

    // KedexController(int stepperSpeed): 
    // kedexStatus(0), stepperPos(0), front(0), end(0), kedexStepper(512,11,9,10,8)
    // { kedexStepper.setSpeed(stepperSpeed); }

    int getKedexStatus() { return kedexStatus; }
    void setKedexStatus(int status) { kedexStatus = status; }

    String getCategoryID() { return categoryID; }
    void setCategoryID(String categoryid) { categoryID = categoryid; }

    String getProductID() { return productID; }
    void setProductID(String productid) { productID = productid; }


    void serialRead() {
    // 시리얼에서 값 읽어와서 int productID, String sku, String productName, destinationID 값 저장한 Product 객체 만들기
      if (dataFlow == 1) {
        while(Serial.available() > 0) {
          dataFlow *= -1;
          // String tempString = Serial.readString();
          // tempString.trim();
          // int firstSpace = tempString.indexOf(' ');
          // inString = tempString.substring(0, firstSpace);
          inString = Serial.readString();
          // 데이터를 받는 부분
        }
      } else if (dataFlow == -1) {
        dataFlow *= -1;
        if(inString != "") {
          // 데이터 보내는 부분
          if (inString != "") {
              String str1 = inString.substring(0, inString.indexOf("|"));
              // setCategoryID(str1.toInt());
              categoryID = str1;
              String str2 = (inString.substring(inString.indexOf("|"), inString.length() - 1));
              // setProductID(str2.toInt());
              productID = str2;

              // Product temp(productID, categoryID);
              // product_queue.enqueue(temp);

              String str = String(getCategoryID());
              // char* str = String(categoryID);
              Serial.println(categoryID);
              
          }
        }
        else {
          Serial.println("None");
        }
      }
    }

    void factoryFlow() {
      if ((categoryID != 0) && (productID != 0)) {
        setStepperToPos();
      }
    }

    void setStepperToPos() {
      Product temp;
      product_queue.peek(temp);
      if (temp.getCategoryID() == 1100000000) {
        stepperPos = 512;
        kedexStepper.step(stepperPos);
      } else if (temp.getCategoryID() == 2600000000) {
        stepperPos = 0;
        kedexStepper.step(stepperPos);
      }
      else if (temp.getCategoryID() == 4100000000) {
        stepperPos = -512;
        kedexStepper.step(stepperPos);
      }
    }

    bool detect() {
      if (digitalRead(detect_pin) == HIGH) {
        Product temp;
        product_queue.dequeue(temp);
        //stepperPos = 0;
        return true;
      }
      return false;
    }

    void conveyorMove() {
      // if (kedexStatus != 0) {
      //   digitalWrite(conv_in3_pin, HIGH); 
      //   digitalWrite(conv_in4_pin, LOW); 4
      //   analogWrite(conv_enb_pin, 64); 
      // }
      // else {
      //     analogWrite(conv_enb_pin, 0);
      // }

      // Product temp;
      // product_queue.peek(temp);
      // product_queue.dequeue(temp);
      String str = String(getCategoryID());
      if (str == "1100000000") {
        digitalWrite(conv_in3_pin, HIGH); 
        digitalWrite(conv_in4_pin, LOW); 
        analogWrite(conv_enb_pin, 64);
      } else if (str == "2600000000") {
        digitalWrite(conv_in3_pin, LOW); 
        digitalWrite(conv_in4_pin, HIGH); 
        analogWrite(conv_enb_pin, 64);
      }
      else if (str == "4100000000") {
        digitalWrite(conv_in3_pin, LOW); 
        digitalWrite(conv_in4_pin, LOW); 
        analogWrite(conv_enb_pin, 0);
      }
    }
};
#endif