from Lab8.my_wearable.BLE import BLE
from Lab8.my_wearable.ppg import PPG
import traceback
from scipy import signal as sig
import matplotlib.pyplot as plt
import numpy as np
#BLE config
run_config = False
baudrate = 9600
serial_port = "COM4"
peripheral_mac = "78DB2F16821E"


#ppg config
signal_len = 30#second
sample_rate = 25# samples / second
buff_len = signal_len*sample_rate # length of the data buffers
plot_refresh = sample_rate/2


ppg = PPG(buff_len, sample_rate)
#ppg.load_file("GMM_YL_3.csv")
#hm10 = BLE(serial_port, baudrate, run_config)
#hm10.connect(peripheral_mac)

buffer = [0]*3*sample_rate

#get a buffer filled with data
def get_data(buffer,file):
    x=0
    isEnd = False
    while 1:
        if x == len(buffer):
            break
        else:
            string = file.readline()
            if len(string) == 0:
                isEnd = True
                break
            t, imu, ir = string.strip().split(",")
            buffer[x] = int(ir)
            x+=1
    if isEnd != True:
        return buffer
    else:
        print("it reaches end")

num = 0
def filter_initial_condition(buffer,z1_in_low,b_low,a_low,z1_in_high,b_high,a_high):
    # plt.figure("before")
    # plt.plot(buffer)

    signal_in = sig.detrend(buffer)
    if num ==1:
        z1_in_low = sig.lfilter_zi(b_low, a_low)
        z1_in_low = z1_in_low * signal_in[0]
    signal_out, z1_out_low = sig.lfilter(b_low, a_low, signal_in, zi=z1_in_low)
    z1_in_low = z1_out_low

    # plt.figure("after")
    # plt.plot(signal_out)
    # plt.show()


    if num == 1:
        z1_in_high = sig.lfilter_zi(b_high, a_high)
        z1_in_high = z1_in_high * signal_in[0]
    signal_out, z1_out_high = sig.lfilter(b_high, a_high, signal_out, zi=z1_in_high)
    z1_in_high = z1_out_high



    return signal_out,z1_in_low,z1_out_high




def filter3second(buffer, file,z1_in_low,z1_in_high):
    #grab data from file to buffer ,run four filters, return the filtered signal.

    signal_in = get_data(buffer, file)
    b_low, a_low = sig.butter(2, 4 / (0.5 * 50), btype="lowpass", analog=False, output='ba')
    b_high, a_high = sig.butter(4, 0.3 / (0.5 * 50), btype="highpass")
    signal_out,z1_in_low,z1_in_high = filter_initial_condition(signal_in,z1_in_low,b_low,a_low,z1_in_high,b_high,a_high)
    return signal_out,z1_in_low,z1_in_high

circular_data = []
z1_in_low = 0
z1_in_high = 0
with open("./Lab8/live_filtering.csv","r") as file:
    while 1:
        try:
            num+=1
            result,z1_in_low,z1_in_high = filter3second(buffer,file,z1_in_low,z1_in_high)
            print("low:",z1_in_low,"high:",z1_in_high)
            circular_data.extend(result)
        except IndexError:
            print("error")
            break



origin = []
with open("./Lab8/live_filtering.csv", "r") as file:
    while 1:

        string = file.readline()
        if len(string) == 0:
            break
        t, imu, ir = string.strip().split(",")
        origin.append(int(ir))




    plt.plot(origin)
    plt.figure("circular")
    plt.plot(circular_data)
    plt.show()



















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
# hm10.close()
# ppg.plot()
