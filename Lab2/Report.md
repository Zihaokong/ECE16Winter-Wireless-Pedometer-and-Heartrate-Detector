Zihao Kong

A15502295
# **Lab2**
## **Introduction**
This lab is about how to connect a OLED monitor and a IMU sensor to Arduino board, and being able to use Python as a way to do Serial Communication.


## **Objective 1** 
1. _The objective is to connect OLED to board and be able to type commands in Serial Monitor, letting it print on the board_
2. _Steps_

* Include respective library: U8x8lib.h
* Downloading the start code
* Serial.read to acquire every byte in Serial Monitor, saving it in a char array
* Print it on screen 


## **Objective 2**
1. _The objective is to use an IMU and plot data_
2. _Steps_

* Download the starter code.
* Print gx gy gz ax ay az on screen with correct formatting
* Connect OLED in series with the IMU, SDA and SCL pin goes to A5 and A4 
* Display the gx gy gz ax ay az on screen by using a long enough array to store these numbers, and use function called dtostrf to write multiple strings into a char array buffer.
* Send the big char array buffer on screen by using showMessage.


## **Objective 3**
1. _This objevtive is to use a viberating motor and be able to control its state._
2. _the code is very similar to the CommandToggle code, which turns the state on and off by setting boolean variables_
	

## **Objective 4**
1. _This objective is to use python as a Serial message sender and receiver._
2. _Steps_

* Download starter code
* Because of the pyserial module, we can use functions inside to write and request messages.