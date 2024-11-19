#ifndef PRODUCT_H
#define PRODUCT_H

class Product {
private:
    String productID;
    String categoryID;
public:
    Product(): productID(""), categoryID("") {}
    Product(String pID, String cID)
        : productID(pID),categoryID(cID) {}
    String getProductID() { return productID; }
    String getCategoryID() { return categoryID; }
    void displayProductInfo() {
        Serial.println("Product ID: " + productID);
        Serial.println("Category ID: " + categoryID);
    }
};

#endif