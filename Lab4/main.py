"""
Author: Ramsin Khoshabeh
Contact: ramsin@ucsd.edu
Date: 07 April 2019
Description: An entry point for the using the BLE communication class
"""

import traceback
import time
from Lab4.mywearable.BLE import BLE
import matplotlib.pyplot as plt
""" -------------------- Settings -------------------- """
run_config = True                 # whether to config PC HM-10 or not
baudrate = 9600                   # PySerial baud rate of the PC HM-10
serial_port = "COM6" #TODO: SERIAL_PORT   # Serial port of the PC HM-10
peripheral_mac = "78DB2F16821E" #TODO: MAC_ADDR   # Mac Address of the Arduino HM-10

""" -------------------- Main Wearable Code -------------------- """
hm10 = BLE(serial_port, baudrate, run_config)
hm10.connect(peripheral_mac)
#connect BLE


print("Starting main loop:")


file = open("IMU_raw.txt","w+")





#read a line everytime and the line is gx,gy,gz, then write them in a file
def saveData(BLE, file):
    message = BLE.read_line()
    a = message.split(";")
    newList = []
    for x in a:
        listTOWrite = x.strip().split(",")
        for x in listTOWrite:
            if x.startswith("#"):
                k = x[1:].strip()
                listTOWrite[0] = k

        if len(listTOWrite) == 3:
            stringToWrite = "" + listTOWrite[0] + " " + listTOWrite[1] + " " + listTOWrite[2]+"\n"
            file.write(stringToWrite)

    return 1;


mode = 1
#read data from BLE if mode is 0
def readData(BLE,file,mode):
    if mode == "0":
        listTOWrite = []
        message = BLE.read_line()
        a = message.split(";")
        newList = []
        for x in a:
            listTOWrite = x.strip().split(",")
            for x in listTOWrite:
                if x.startswith("#"):
                    k = x[1:].strip()
                    listTOWrite[0] = k
            if len(listTOWrite) == 2:
                stringToWrite = "" + listTOWrite[0] + " " + listTOWrite[1] +"\n"
                file.write(stringToWrite)
        return listTOWrite[0],listTOWrite[1]







    elif mode == "1":
        message = file.readline()
        a = message.split(" ")
        c = ["","",""]
        i=0
        for x in a:
            c[i] = x.rstrip()
            i=i+1
        print(c)
        return c[0],c[1],c[2]
    else:
        return

#500 list to put data in
gx = [None]*500
gy = [None]*500
gz = [None]*500


counter = 0
while True:
    x=0
    try:
        while counter<=500:
            counter += saveData(hm10, file)
            #SAVE 500 DATA

        #code for select mode and plot data
        mode = input("0 for READBLE 1 for READSaveFile")
        while x < 500:
            gx[x], gy[x], gz[x] = readData(hm10, file,mode)
            x += 1

        print(len(gx))
        print(len(gy))
        print(len(gz))
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

#close file and plot
file.close()

#generate xAxis for three plot
xAxis = []
for x in range(0,500):
    xAxis.append(x)
print(xAxis)
plt.subplot(131) # Cut figure into 2x3 matrix; axes in 1st
plt.plot(xAxis,gx)
plt.subplot(132) # Cut figure into 2x3 matrix; axes in 1st
plt.plot(xAxis,gy)
plt.subplot(133) # Cut figure into 2x3 matrix; axes in 1st
plt.plot(xAxis,gz)

plt.show()




