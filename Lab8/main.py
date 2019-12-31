from Lab8.my_wearable.BLE import BLE
from Lab8.my_wearable.ppg import PPG
from Lab8.my_wearable.pedometer import Pedometer
from Lab8.data_prepare import *
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
plot_refresh = sample_rate/25

#pedometer config
max_len = signal_len * sample_rate

hm10 = BLE(serial_port, baudrate, run_config)
hm10.connect(peripheral_mac)
ppg = PPG(buff_len,sample_rate)
pedometer = Pedometer(max_len,True,sample_rate)


a = np.random.permutation(9)
training_sets = a[0:9]
validation_sets = a[6:8]
testing_sets = a[8:]
tr_t, tr_ir,va_t, va_ir,te_t, te_ir = load_file(training_sets,validation_sets,testing_sets,"../HR Data/")
ppg.train(tr_t)

string = ''
counter = 0
while 1:
    #message is read in, and it's appending to ppg's buffer, ppg's buffer is updating,
    #and live plot
    msg = hm10.read_line(';')


    if len(msg) > 0:
        Step =pedometer.live_appending(msg,3)
        HR = ppg.live_appending(msg,3)
        HR = HR[0:8]
        string = Step+ " " + HR+";"
        if len(string)!= 2:
            print(string)
            hm10.write(string)
        if counter % plot_refresh == 0:
            pass
            ppg.plot_live()
            #pedometer.plot_live()
        counter += 1
