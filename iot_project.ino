int serial;
int led = 9;
int led_status = 0;
int dataFlow = -1;
int light = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(led, OUTPUT);

  while (!Serial) {
    ;  // 시리얼 포트가 열릴 때까지 대기
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if (dataFlow == 1) {
    if(Serial.available() > 0) {
      dataFlow *= -1;
      serial = Serial.parseInt();
      
      if (serial == 1) {
        digitalWrite(led, HIGH);
      }
      else {
        digitalWrite(led, LOW);
      }
    }
  } else if (dataFlow == -1) {
    dataFlow *= -1;
    light = analogRead(A0);
    Serial.println(light);
  }
  delay(100);
}
