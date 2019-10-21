Zihao Kong

A15502295
# **Lab3**
## **Introduction**
The goal of this lab is to get familiar with BLE chip and use it
to build connection between Arduino and Laptop.

## **Objective 1** 
1. _Before we use the starter code, there is a library to install called AltSoftSerial,
which contains convenient API for users to use in BLE module._
2. _After we install the API, we are able to include it it our C code_
3. _The objective is to test the AT commands on Serial monitor and see which one does what thing._
4. _Those commands are:_
* AT
* AT+NAME(YOURNAME)
* AT+NAME?
* AT+ROLE(0,1)
* AT+ROLE?
* AT+IMME(0,1)
* AT+IMME?
* AT+BAUD(0)
* AT+BAUD?
* AT+ADDR?
* AT+DISC?
* AT+CON(YOUR DEVICE ADDRESS)
* AT+RESET
* AT+RENEW


## **Objective 2**
1. _In order to build connection, we find a partner and connect with each other._
2. _To do so, we choose a central and a peripheral_
* Central has IMME1 and ROLE1
* Peripheral has IMME0 and ROLE0
3. _Then the central askes peripheral for its address._
4. _Once the connection is established, we exchange our name with role._


## **Objective 3**
1. _This is building connection between laptop and Arduino._
2. _Computer is the central, and Arduino is the Peripheral, Computer use python code and pyserial library to send 
informtaion to Arduino, And Arduino uses AltSoftSerial to send information to computer._
* Pyserial: Read_BL()E, Write_BLE()
* AltSoftSerial: ReadBLE(), WriteBLE()
3. _Before serial communication starts, on computer's side, we have to Serial Write AT, AT+
IMME1, AT+NOTL1, AT+ROLE1, AT+RESET as the configuration step._
4. _Then we use a while loop to keep writing AT+CON in order to build connection_
5. _When computer reads "OK+CONNAOK+CONN", then break while loop, use WriteBLE to send a Connected_
6. _On Arduino side, once a "C" char is read, the isStart boolean becomes true, then it sends a star every second to computer._
7. _When Computer readBLE function returns a *, it writes Number: (x), in which x is a counter of how many * has been sent._
8. _Number: (x) is printed on OLED screen, because we integrate the code in LAB2, import modules and use showMessage() to print what's been sent from Computer._