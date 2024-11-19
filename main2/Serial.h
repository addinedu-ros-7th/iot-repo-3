class Serial {
    int dataFlow;
    String inString;
    String categoryID;
    String productID;

public:
    Serial(): dataFlow(-1), inString(""), categoryID(""), productID("") {}

    void serialRead() {
      if (dataFlow == 1) {
        while(Serial.available() > 0) {
          dataFlow *= -1;
          inString = Serial.readString(); // 2600000000|12345
          // 데이터를 받는 부분
        }

      } else if (dataFlow == -1) {
            dataFlow *= -1;
            if(inString != "") {
            // 데이터 보내는 부분
                if (inString != "") {
                    String categoryID = inString.substring(0, inString.indexOf("|")); // 2600000000

                    String productID = (inString.substring(inString.indexOf("|"), inString.length() - 1)); // 12345

                    Serial.println(categoryID);
                    
                }
            } else {
                Serial.println("None");   // None
            }
      }
    }

    String getCategoryID() { return categoryID; }
    // void setCategoryID(String categoryid) { categoryID = categoryid; }

    String getProductID() { return productID; }
    // void setProductID(String productid) { productID = productid; }
};
