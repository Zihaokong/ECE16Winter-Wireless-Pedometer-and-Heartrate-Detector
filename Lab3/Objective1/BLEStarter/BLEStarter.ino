#include <AltSoftSerial.h>
AltSoftSerial hm10; // create the AltSoftSerial connection for the HM10

// Global Variables
char c = ' ';

// --------------------------------------------------------------------------------
// readBLE: read a single char from the HM-10 module and print to Serial
// --------------------------------------------------------------------------------
void readBLE() {
  c = hm10.read();
  Serial.print(c);
}

// --------------------------------------------------------------------------------
// writeBLE: write a single char from Serial to the HM-10 module
// --------------------------------------------------------------------------------
void writeBLE() {
  static bool newline = false;

  c = Serial.read();
  
  // We cannot send newline to the HM-10 so we have to catch it
  if (c!='\n' & c!='\r')
    hm10.print(c);
  
  // Also print to Serial Monitor so we can see what we typed
  // If there is a new line character, print the ">" character
  if (newline) {
    Serial.print("\n>");
    newline = false;
  }
  Serial.print(c);
  if (c=='\n')
    newline = true;
}

// --------------------------------------------------------------------------------
// setup: executed once at startup or reset
// --------------------------------------------------------------------------------
void setup() {
  hm10.begin(9600);
  Serial.begin(9600);
  
  Serial.println("==============================");
  Serial.println("HM-10 AltSoftSerial started");
  Serial.println("==============================");
}

// --------------------------------------------------------------------------------
// loop: main code; executed in an infinite loop
// --------------------------------------------------------------------------------
void loop()
{
  // Read a char from the BLE module and send to the Serial Monitor
  if(hm10.available())
    readBLE();

  // Read from the Serial Monitor and send to the BLE module
  if(Serial.available())
    writeBLE();
}
