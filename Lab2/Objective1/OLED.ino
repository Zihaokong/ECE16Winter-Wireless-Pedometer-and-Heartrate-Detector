#include "U8x8lib.h"

#include "Wire.h"

// OLED setup
#define OLED_RESET 4 // this value resets the OLED
U8X8_SSD1306_128X32_UNIVISION_HW_I2C u8x8(OLED_RESET);

// --------------------------------------------------------------------------------
// Initialize the OLED with base font for fast refresh
// --------------------------------------------------------------------------------


int i = 0;
char out_str[16];
int characterCounter = 0;

void initDisplay() {
  u8x8.begin();
  u8x8.setPowerSave(0);
  u8x8.setFont(u8x8_font_amstrad_cpc_extended_r);
  u8x8.setCursor(0, 0);
}

// --------------------------------------------------------------------------------
// A function to write a message on the display
// "row" specifies which row to print on... 1, 2, 3, etc.
// "clearDisplay" specifies if everything should be wiped or not
// --------------------------------------------------------------------------------
void showMessage(const char * message, int row, bool cleardisplay) {
  if (cleardisplay) {
    u8x8.clearDisplay();
  }
  u8x8.setCursor(0, row);
  u8x8.print(message);
}

void setup() {
  initDisplay();
  showMessage("Initializing...", 1, true);
  showMessage("Success!", 2, true);

  Serial.begin(9600);

}
//
//
//if (i >= 16) {
//        Serial.println("too long");
//        showMessage("too long", 1, true);
//        memset(out_str, 0, sizeof(out_str));
//        i = 0;
//      }



//设置限制
void loop() {

  if (Serial.available()) {
    char tmp = Serial.read();
    if (tmp == '\n') {
      i = 0;
      Serial.println(out_str);
      showMessage(out_str, 1, true);
      memset(out_str, 0, sizeof(out_str));
    }
    else {
      out_str[i] = tmp;
      i++;
      if(i>=16){
        Serial.println("toolong");
        showMessage("too long", 1, true);
        memset(out_str, 0, sizeof(out_str));
      }
    }
  }
}
