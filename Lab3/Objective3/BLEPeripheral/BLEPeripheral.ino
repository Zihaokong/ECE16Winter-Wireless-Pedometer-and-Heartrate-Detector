#include <AltSoftSerial.h>
AltSoftSerial hm10;

char c = ' ';
int numberOfCharacters = 0; //variable for counting the row position of cursor.
bool isStart = false; //state of the clock counter
long startTime = millis(); // non-blocking timing.


//module of OLED and its components.
#include "U8x8lib.h"
#define OLED_RESET 4
U8X8_SSD1306_128X32_UNIVISION_HW_I2C u8x8(OLED_RESET);
void initDisplay() {
  u8x8.begin();
  u8x8.setPowerSave(0);
  u8x8.setFont(u8x8_font_amstrad_cpc_extended_r);
  u8x8.setCursor(0, 0);
}

//in order to set the cursor position manually, I add another parameter "col"
void showMessage(const char * message, int col, int row, bool cleardisplay) {
  if (cleardisplay) {
    u8x8.clearDisplay();
  }
  u8x8.setCursor(col, row);
  u8x8.print(message);
}

char readBLE() {//execute multiple times, read from laptop
  c = hm10.read();
  Serial.print(c);
  return c;
}


void writeBLE() {
  static bool newline = false;
  c = Serial.read();

  // We cannot send newline to the HM-10 so we have to catch it
  if (c != '\n' & c != '\r')
    hm10.print(c);

  // Also print to Serial Monitor so we can see what we typed
  // If there is a new line character, print the ">" character
  if (newline) {
    Serial.print("\n>");
    newline = false;
    numberOfCharacters = 0;

    //if "Number :1\n" was sent to Arduino, then this executes and clear display of OLED
    u8x8.clearDisplay();
    u8x8.setCursor(0, 1);
  }
  Serial.print(c);

  if (c == '\n')
    newline = true;
}

void setup() {
  hm10.begin(9600);
  Serial.begin(9600);

  Serial.println("==============================");
  Serial.println("HM-10 AltSoftSerial started");
  Serial.println("==============================");

  initDisplay();
  u8x8.clearDisplay();


}


void loop()
{
  // Read a char from the BLE module and send to the Serial Monitor
  if (hm10.available()) {
    char c;
    c = readBLE();
    //if it sees a C from the word "Connected", the counter start working
    if (c == "C") isStart = true;

    //this part control the printing on OLED screen, since showMessage receive a pointer of char, and this readBLE execute every frame, reading a byte, I use
    //NumberofCharacters to count the current position of the cursor, thus being able to print word. 
    showMessage(&c, numberOfCharacters, 1, false);
    numberOfCharacters += 1;
  }
  //for every second, it set the cursor to zero position, and send * to python.
  if (isStart = true) {
    if (millis() - startTime > 1000) {
      startTime = millis();
      hm10.print("*");
      
      numberOfCharacters = 0;
      u8x8.setCursor(0, 1);

    }
  }
//  else{
//    
//  }

    // Read from the Serial Monitor and send to the BLE module
    if (Serial.available())
      writeBLE();
}
