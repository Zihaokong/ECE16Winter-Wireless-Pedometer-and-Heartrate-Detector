bool mode = true;
char stuff[] = "abc";
char stuff1[] = "def";
int count = 0;
bool isPress = false;
void setup() {
  pinMode(4, INPUT);
  Serial.begin(9600);
  // put your setup code here, to run once:

}

void loop() {
  int state = digitalRead(4);
  if (state == LOW) {//if the button is pressed, then isPress becomes true
    count = 0;
    isPress = true;
  }
  else if (state == HIGH) {//if the button is unpressed, if the bool "isPress" is true, it will print stuff based on the current mode, otherwise nothing happens.
    if (count == 0 && isPress == true) {//count guarantee stuff is only been printed once, and everytime this execute, mode changes.
      if (mode == true) {
        Serial.println(stuff);
        mode = false;
      }
      else if (mode == false) {
        Serial.println(stuff1);
        mode = true;
      }
      count += 1;

      isPress = false;
    }
  }
  else {
  }
}
