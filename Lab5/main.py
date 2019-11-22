"""
Author: Ramsin Khoshabeh
Contact: ramsin@ucsd.edu
Date: 07 April 2019
Description: An entry point for the using the BLE communication class
"""
print("main")
import traceback
import time
from Lab4.mywearable.BLE import BLE
import matplotlib.pyplot as plt
from Lab5.mywearable.pedometer import Pedometer
""" -------------------- Settings -------------------- """
run_config = True                 # whether to config PC HM-10 or not
baudrate = 9600                   # PySerial baud rate of the PC HM-10
serial_port = "COM6" #TODO: SERIAL_PORT   # Serial port of the PC HM-10
peripheral_mac = "78DB2F16821E" #TODO: MAC_ADDR   # Mac Address of the Arduino HM-10

""" -------------------- Main Wearable Code -------------------- """
hm10 = BLE(serial_port, baudrate, run_config)
hm10.connect(peripheral_mac)
pedoInstanc = Pedometer(500,True)

#connect BLE


print("Starting main loop:")

#read a line everytime and the line is gx,gy,gz, then write them in a file



bufferAvailable = True
while True:
    try:
        string = hm10.read_lines()
        if bufferAvailable == True:
            bufferAvailable = pedoInstanc.append(string)

        else:
            pedoInstanc.save_file("Lab5/walking_100hz.txt")
            break
    except KeyboardInterrupt:
        print("\nExiting due to user input (<ctrl>+c).")
        hm10.close()
        break
    except Exception as e:
        print("\nExiting due to an error.")
        traceback.print_exc()
        hm10.close()
        break

pedoInstanc = Pedometer(500,True)
pedoInstanc.load_file("Lab5/walking_100hz.txt")
pedoInstanc.process()



#generate xAxis for three plot





