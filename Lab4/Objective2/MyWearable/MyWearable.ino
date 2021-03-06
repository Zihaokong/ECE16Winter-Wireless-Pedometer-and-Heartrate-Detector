/********************************************************************************
** Bidirectional BLE Communication using a 2-step handshake protocol
*********************************************************************************/


// BT Library
#include <AltSoftSerial.h>
AltSoftSerial hm10; // create the AltSoftSerial connection for the HM10
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"

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

    if (c == '\n')
      newline = true;
  }
}

const int buttonPin = 3;
bool asleep = false;
volatile bool buttonPressed = false;






void buttonInterruptISR() {
  static unsigned long lastInterrupt = 0;
  unsigned long interruptTime = millis();
  if (interruptTime - lastInterrupt > 200)
    buttonPressed = true;
  lastInterrupt = interruptTime;
}

void toggleSleep() {
  //complete the if statement conditional for when the system should be going to sleep
  Serial.print("toggle sleep");
  if (buttonPressed) {
    asleep = !asleep;
    if (asleep) {
      Serial.print("Going to sleep");
      hm10.write("AT");
      delay(300);
      hm10.write("AT+ADTY3");
      delay(300);
      hm10.write("AT+SLEEP");
      asleep = true;
    }
    // Complete the if statement for when the system should be waking up
    else {
      Serial.println("Waking up!");
      hm10.write("AT+aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
      delay(300);
      hm10.write("AT+ADTY0");
      delay(1000);
      hm10.write("AT+RESET");
      asleep = false;
      Serial.print("Awake");
    }

    buttonPressed = false;
  }
}



// Define IMU pin variables
const int interruptPin = 2;
volatile bool imuDataReady = false;

// IMU data variables
int16_t ax, ay, az, tp, gx, gy, gz;

// IMU setup
const int MPU_addr = 0x68;  // I2C address of the MPU-6050
MPU6050 IMU(MPU_addr);      // Instantiate IMU object


#include "U8x8lib.h"
#define OLED_RESET 4
U8X8_SSD1306_128X32_UNIVISION_HW_I2C u8x8(OLED_RESET);

char IMUSend[18];

void interruptPinISR() {
  imuDataReady = true;
}

void initIMU() {

  // Initialize the IMU and the DMP (Digital Motion Processor) on the IMU
  IMU.initialize();
  IMU.dmpInitialize();
  IMU.setDMPEnabled(true);

  // Initialize I2C communications
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(MPU_addr);               // PWR_MGMT_1 register
  Wire.write(0);                      // Set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  // Create an interrupt for pin2, which is connected to the INT pin of the MPU6050
  pinMode(interruptPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), interruptPinISR, RISING);
}

void readIMU() {
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);                   // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);

  Wire.requestFrom(MPU_addr, 14, true); // request a total of 14 registers

  //Temperature
  tp = Wire.read() << 8 | Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)

  //Gyroscope (3 Axis)
  gx = Wire.read() << 8 | Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  gy = Wire.read() << 8 | Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  gz = Wire.read() << 8 | Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
}

bool getData()
{
  bool newData = false;
  if (imuDataReady)
  {
    readIMU();
    newData = true;
    imuDataReady = false;
  }
  return newData;
}

void sendDataIMU() {
  char g_x[10];
  char g_y[10];
  char g_z[10];
  dtostrf(gx, 5, 0, g_x);
  dtostrf(gy, 5, 0, g_y);
  dtostrf(gz, 5, 0, g_z);
  sprintf(IMUSend, "%s,%s,%s;", g_x, g_y, g_z);
  delay(20);
  hm10.write(IMUSend);
  Serial.println(IMUSend);
}



// --------------------------------------------------------------------------------
// Setup: executed once at startup or reset
// --------------------------------------------------------------------------------
void setup() {

  pinMode(3, INPUT_PULLUP);
  Serial.begin(9600);
  hm10.begin(9600);
  Serial.println("==============================");
  Serial.println("BLE Handshake Code Started");
  Serial.println("==============================");
  attachInterrupt(digitalPinToInterrupt(3), buttonInterruptISR, FALLING);
  initIMU();
}

// --------------------------------------------------------------------------------
// Loop: main code; executed in an infinite loop
// --------------------------------------------------------------------------------


void loop() {

  if (buttonPressed) {
    toggleSleep();
  }

  if (asleep == false) {
    if (hm10.available()) {
      // Read a message from the BLE module and send to the Serial Monitor
      if (readBLE()) {
        Serial.println(in_text);
      }
    }
    // Read from the Serial Monitor and send to the BLE module
    if (Serial.available())
      writeBLE();
    // If we know we are connected, start sending data back
    if (bleConnected) {
      if (millis() - sendTimer > 1000) {
        sendTimer = millis();
        hm10.print("*;");
      }

      
      if (getData() == true) {
        sendDataIMU();
      }
    }
  }

  // Check if Python is sending a message to the Arduino. Also checks for handshake.
}
