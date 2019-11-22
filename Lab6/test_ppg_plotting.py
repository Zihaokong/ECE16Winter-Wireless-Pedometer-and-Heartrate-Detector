"""
Author: Ramsin Khoshabeh
Contact: ramsin@ucsd.edu
Date: 07 April 2019
Description: An entry point for testing the PPG class
"""

import traceback
import time

from Lab6.MyWearable.BLE import BLE
from Lab6.MyWearable.ppg import PPG

""" -------------------- Settings -------------------- """
run_config = False                # whether to config PC HM-10 or not
baudrate = 9600                   # PySerial baud rate of the PC HM-10
serial_port = "COM6"   # Serial port of the PC HM-10
peripheral_mac = "78DB2F16821E" # Mac Address of the Arduino HM-10

signal_len = 30 # length of signal in seconds (start with 10)
sample_rate = 25                  # samples / second
buff_len = signal_len*sample_rate # length of the data buffers
plot_refresh = 1                 # draw the plot every X samples (adjust as needed)

""" -------------------- Test #1 -------------------- """
# ppg = PPG(buff_len, sample_rate)
# hm10 = BLE(serial_port, baudrate, run_config)
# hm10.connect(peripheral_mac)
#
#
#
# try:
#     counter = 0
#     while(True):
#         msg = hm10.read_line(';')
#         if len(msg) > 0:
#             ppg.append(msg)
#             if counter % plot_refresh == 0:
#                 ppg.plot_live()
#             counter += 1
# except KeyboardInterrupt:
#     print("\nExiting due to user input (<ctrl>+c).")
#     hm10.close()
# except Exception as e:
#     print("\nExiting due to an error.")
#     traceback.print_exc()
#     hm10.close()

# """ -------------------- Test #2 -------------------- """
ppg = PPG(buff_len, sample_rate)
ppg.load_file('PPGRaw1.csv')
ppg.process()
