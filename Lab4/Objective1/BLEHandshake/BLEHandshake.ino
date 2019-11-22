/********************************************************************************
** Bidirectional BLE Communication using a 2-step handshake protocol
*********************************************************************************/


// BT Library
#include <AltSoftSerial.h>
AltSoftSerial hm10; // create the AltSoftSerial connection for the HM10

// Global Variables
char in_text[64];                           // Character buffer
bool bleConnected = false;                  // false == not connected, true == connected
unsigned long sendTimer = 0;                // timer for sending data once connected

// --------------------------------------------------------------------------------
// This function handles the BLE handshake
// It detects if central is sending "AT+...", indicating the handshake is not complete
// If a "T" is received right after an "A", we send back the handshake confirmation
// The function returns true if a connection is established and false otherwise
// --------------------------------------------------------------------------------
bool bleHandshake(char input) {
  static char lastChar;

  if (lastChar == 'A' & input == 'T') {
    hm10.print("#");
    delay(50);
    lastChar = "";
    hm10.flushInput();
    bleConnected = true;
    return true;
  }
  else {
    lastChar = input;
    return false;
  }
}

// --------------------------------------------------------------------------------
// This function reads characters from the HM-10
// It calls the bleHandshake() function to see if we are connecting
// Otherwise, it fills a buffer "in_text" until we see a ";" (our newline stand-in)
// --------------------------------------------------------------------------------
bool readBLE() {
  static int i = 0;
  char c = hm10.read(); 
  delay(50);
  if (bleHandshake(c)) {
    i = 0;
  }
  else {
    // If the buffer overflows, go back to its beginning
    if (i >= sizeof(in_text) - 1)
      i = 0;
    // All of our messages will terminate with ';' instead of a newline
    if (String(c) == ";") {

      in_text[i] = '\0'; // terminate the string
      i = 0;
      return true;
    }
    else {
      in_text[i++] = c;
    }
  }
  return false; // nothing to print
}

// --------------------------------------------------------------------------------
// Forward data from Serial to the BLE module
// This is useful to set the modes of the BLE module
// --------------------------------------------------------------------------------
void writeBLE() {
  static boolean newline = true;
  while (Serial.available()) {
    char c = Serial.read();
    
    // We cannot send newline to the HM-10 so we have to catch it
    if (c != '\n' & c != '\r')
      hm10.print(c);

    // Also print to Serial Monitor so we can see what we typed
    // If there is a new line character, print the ">" character
    if (newline) {
      Serial.print("\n>");
      newline = false;
    }

    Serial.print(c);
    if (c == '\n')
      newline = true;
  }
}

// --------------------------------------------------------------------------------
// Setup: executed once at startup or reset
// --------------------------------------------------------------------------------
void setup() {
  Serial.begin(9600);
  hm10.begin(9600);

  Serial.println("==============================");
  Serial.println("BLE Handshake Code Started");
  Serial.println("==============================");
}

// --------------------------------------------------------------------------------
// Loop: main code; executed in an infinite loop
// --------------------------------------------------------------------------------


void loop() {

  // Check if Python is sending a message to the Arduino. Also checks for handshake.
  if (hm10.available()) {
    // Read a message from the BLE module and send to the Serial Monitor
    //readBLE1();
    
    if (readBLE()) {
      Serial.println(in_text);
    }
  }

  // Read from the Serial Monitor and send to the BLE module
  if (Serial.available())
    writeBLE();
  delay(20);

  // If we know we are connected, start sending data back
  if (bleConnected) {
    if (millis() - sendTimer > 1000) {
      sendTimer = millis();
      hm10.print("*;");
    }
  }

}
