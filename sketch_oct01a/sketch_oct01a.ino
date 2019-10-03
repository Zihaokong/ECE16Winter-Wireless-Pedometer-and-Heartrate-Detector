boolean state = false;  // stopwatch state ? 0 off : 1 on
int counter = 0;        // stopwatch counter
int cache = 0;          // stopwatch memory
unsigned long throttle; // throttle
unsigned long initTime; // initial time

/**
 * Setup
 */
void setup() {
  Serial.begin(9600);
  pinMode(4, INPUT_PULLUP); // initialize pin
  initTime = millis();
  throttle = millis();  // initialize throttle
}

/**
 * Loop
 */
void loop() {
  int value = digitalRead(4); // acuqire pin value
  if (checkButton(value)) {
  
    if (!state) {       // from off to on
      initTime = millis();
      Serial.println("Start");
    } else {            // from on to off
      cache += counter;
      Serial.println("Stop");
    }
    state = !state;     // toggle state
    delay(1000);
  } else {
    if (state) {
      unsigned long currTime = millis();
      unsigned long tdiff = currTime - initTime;
      if (millis() - throttle > 1000) {
        counter = floor(tdiff / 1000);
        Serial.println(cache + counter);
        throttle = millis();
      }
    }
  }
}

/**
 * Check Button Status
 * @param int value
 * @return boolean result
 */
boolean checkButton(int value) {
  return (value == 0) ? true : false;
}
