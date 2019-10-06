unsigned long startTime = millis();
int count = 0;
bool isStart = false;
boolean isPress = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(4, INPUT);

}

void loop() {
  int state = digitalRead(4);
  if (state == LOW) {
    if (isStart == false && isPress == false) { //if the button is pressed, watch hasn't started, then activate watch, the button is pressed, so isPress then becomes true
      isStart = true;
      Serial.println("start"); 
    }
    else if (isStart == true && isPress == true) {//if the button is pressed, watch started, that means it has to stop, isPress then come back to original state.
      isStart = false;
      isPress = false;
      Serial.println("stop");
      delay(500);
    }

  }
  else if (state == HIGH) {
    
    if (isStart == true) {//if button is not pressed, and game started, then it starts count, or nothing happens
      isPress = true;
      if (millis() - startTime > 1000) {
        isPress = false;
        count = count + 1;
        startTime = millis();
        Serial.println(count);
        //Serial.println(state);

      }
    }
  }
}
