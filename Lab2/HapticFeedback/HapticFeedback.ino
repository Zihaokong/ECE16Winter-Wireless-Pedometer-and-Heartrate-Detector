String command;
unsigned long startTime = millis();
bool isOpen = false;
void setup() {
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);
  // put your setup code here, to run once:

}

void loop() {
  String command = Serial.readString();
  if (command == "start\n") {
    Serial.println("start");
    isOpen = true;
  }
  else if (command == "stop\n") {
    Serial.println("stop");
    isOpen = false;
  }
  Serial.println(isOpen);
  if (isOpen == true) {
    digitalWrite(4, LOW);
    delay(2000);
    digitalWrite(4, HIGH);
    delay(1000);
    
    
  }



  // put your main code here, to run repeatedly:

}
