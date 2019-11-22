"""
Author: Ramsin Khoshabeh
Contact: ramsin@ucsd.edu
Date: 07 April 2019
Description: An entry point for the using the BLE communication class
"""

import traceback
import time
from mywearable.BLE import BLE

""" -------------------- Settings -------------------- """
run_config = True                 # whether to config PC HM-10 or not
baudrate = 9600                   # PySerial baud rate of the PC HM-10
serial_port = "COM6" #TODO: SERIAL_PORT   # Serial port of the PC HM-10
peripheral_mac = "78DB2F16821E" #TODO: MAC_ADDR   # Mac Address of the Arduino HM-10

""" -------------------- Main Wearable Code -------------------- """
hm10 = BLE(serial_port, baudrate, run_config)
hm10.connect(peripheral_mac)

print("Starting main loop:")
counter = 0



while True:
    try:
        while 1:
            string = hm10.read_lines()
            time.sleep(1)
            print(string)
            if "*" in string:
                counter+=1
                output = "Number: "+str(counter)+";"
                hm10.write(output)

    # 1. Read a line of text from hm10 that is terminated by ';'
        # 2. If the message is '*':
        #   2.1. write 'Number: x;' to hm10 (where 'x' is counter)
        #   2.2. increment counter by 1
        #TODO: COMPLETE_THIS_SECTION
    except KeyboardInterrupt:
        print("\nExiting due to user input (<ctrl>+c).")
        hm10.close()
        break
    except Exception as e:
        print("\nExiting due to an error.")
        traceback.print_exc()
        hm10.close()
        break