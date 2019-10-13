#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"


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

int i = 0;
char out_str[16];
int characterCounter = 0;

void initDisplay() {
  u8x8.begin();
  u8x8.setPowerSave(0);
  u8x8.setFont(u8x8_font_amstrad_cpc_extended_r);
  u8x8.setCursor(0, 0);
}

void showMessage(const char * message, int row, bool cleardisplay) {
  if (cleardisplay) {
    u8x8.clearDisplay();
  }
  u8x8.setCursor(0, row);
  u8x8.print(message);
}










// --------------------------------------------------------------------------------
// Function to check the interrupt pin if there is data available in the buffer
// --------------------------------------------------------------------------------
void interruptPinISR() {
  imuDataReady = true;
}

// --------------------------------------------------------------------------------
// Initialize the IMU (only on startup)
// --------------------------------------------------------------------------------
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

// --------------------------------------------------------------------------------
// Function to read a single sample of IMU data
// Currently, this reads 3 acceleration axis, temperature, and 3 gyro axis.
// You should edit this to read only the sensors you end up using.
// For this, you need to edit the number of registers/addresses requested
// --------------------------------------------------------------------------------
void readIMU() {
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);                   // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);

  Wire.requestFrom(MPU_addr, 14, true); // request a total of 14 registers

  //Accelerometer (3 Axis)
  ax = Wire.read() << 8 | Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  ay = Wire.read() << 8 | Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  az = Wire.read() << 8 | Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)

  //Temperature
  tp = Wire.read() << 8 | Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)

  //Gyroscope (3 Axis)
  gx = Wire.read() << 8 | Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  gy = Wire.read() << 8 | Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  gz = Wire.read() << 8 | Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
}

// --------------------------------------------------------------------------------
// Function to grab new samples
// --------------------------------------------------------------------------------
bool getData()
{
  bool newData = false;
  if (imuDataReady)
  {
    readIMU();
    newData = true;
  }
  return newData;
}

// --------------------------------------------------------------------------------
// Function to write data to Serial (for plotting on Serial Plotter)
// --------------------------------------------------------------------------------
void writeToSerial() {
  Serial.print(gx);
  Serial.print(" ");
  Serial.print(gy);
  Serial.print(" ");
  Serial.println(gz);


}

// --------------------------------------------------------------------------------
// Function to write data to the OLED (for printing text values of the IMU data)
// --------------------------------------------------------------------------------
void writeToOLED() {

  // TODO: convert floating point IMU values (both accelerometer and gyroscope)
  // to char arrays using the function dtostrf() and then combining them with
  // the function sprintf(). Then write that result to the OLED just like you did
  // with OLEDStarter.ino.
  char a_x[10];
  char a_y[10];
  char a_z[10];
  char g_x[10];
  char g_y[10];
  char g_z[10];
  char out1[70];
  dtostrf(ax, 6, 0, a_x);
  dtostrf(ay, 6, 0, a_y);
  dtostrf(az, 6, 0, a_z);
  dtostrf(gx, 6, 0, g_x);
  dtostrf(gy, 6, 0, g_y);
  dtostrf(gz, 6, 0, g_z);
  sprintf(out1, "Ax%sGx%s\nAy%sGy%s\nAz%sGz%s", a_x, g_x, a_y, g_y, a_z, g_z);
  showMessage(out1, 1, true);
}

// --------------------------------------------------------------------------------
// Function to do the usual Arduino setup
// --------------------------------------------------------------------------------
void setup() {
  pinMode(13,OUTPUT);
  // Initialize the IMU
  initIMU();
  initDisplay();
  showMessage("Initializing...", 1, true);
  showMessage("Success!", 2, true);

  // Initialize Serial port
  Serial.begin(9600);
  digitalWrite(13,LOW);
}

// --------------------------------------------------------------------------------
// Main loop
// --------------------------------------------------------------------------------



void loop() {
  

  if (getData()) {
    writeToSerial();
    if(gy >4000||gx>4000||gz>4000){
      digitalWrite(13,HIGH);
    }
    writeToOLED();
    digitalWrite(13,LOW);
  }

  // TODO: call the appropriate function from above for writing data here
}
