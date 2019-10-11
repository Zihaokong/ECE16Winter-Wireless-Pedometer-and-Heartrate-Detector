import time
import serial

ser = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Specify the Serial port of your Arduino

command = input("Which Objective do you want to test? Type 1 for Objective 1 or 2 for Objective 2: ")

try:
  while True:
    if command == '1':  # OLED
      message = input("Type the message you want to send: ")
      ser.write(message.encode("utf-8"))
    if command == '2':  # IMU
      if (ser.in_waiting > 0):
        print(ser.readline().decode('utf-8'))  # print the message from the Arduino
    else:
      command = input("Please enter a valid command (1 or 2): ")

except:  # catch all exceptions
  ser.close()
