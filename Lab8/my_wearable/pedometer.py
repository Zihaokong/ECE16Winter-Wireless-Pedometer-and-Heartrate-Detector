"""
Authors: Avak Archanian / Ramsin Khoshabeh / Edward Wang
Contact: aarchani@ucsd.edu / ramsin@ucsd.edu / ejaywang@eng.ucsd.edu
Date: 25 October 2019
Description: A class to handle the pedometer for the wearable
"""

# Imports
import serial
from time import sleep
from time import time
from scipy import signal as sig
import numpy as np
from matplotlib import pyplot as plt


class Pedometer:
    # Attributes of the class Pedometer
    _maxlen = 0
    _file_flag = False
    __time_buffer = []
    __data_buffer = []
    __result_buffer = []
    __total_time = []

    __peaks_index = []
    __peaks = []
    __steps = 0

    _sampling_rate = 0

    __live_buffer_index = 0 #how many elements are appended to data buffer from the beginning of time
    __num_of_windows = 0 # how many time live process is executed
    __low_initial = 0
    __high_initial = 0


    def __init__(self, maxlen, file_flag, sampling_rate):
        self._maxlen = maxlen  # Set the max length of the buffer
        self._file_flag = file_flag  # Set whether we are writing to a file or not
        self.__steps = 0
        self._sampling_rate = sampling_rate
        return


    def reset(self):
        self._maxlen = 0
        self.__time_buffer = []
        self.__data_buffer = []
        __steps = 0
        return

    #append the time and imu part of msg_str to time and data buffer. buffer is circular, meaning that any
    #data over will be added, discarding older data
    def append(self, msg_str):
        try:
            if msg_str[0] == "#":
                t, imu, ir = msg_str[1:].strip().split(",")
            else:
                t, imu, ir = msg_str.strip().split(",")

            if self._maxlen > len(self.__time_buffer):
                self.__time_buffer.append(int(t))
                self.__data_buffer.append(int(imu))

            else:
                self.__time_buffer[:-1] = self.__time_buffer[1:]
                self.__time_buffer[-1] = int(t)
                self.__data_buffer[:-1] = self.__data_buffer[1:]
                self.__data_buffer[-1] = int(imu)

        except ValueError:
            print("Invalid Data: " + msg_str)

    # grab data from self.data_buffer, starting from the trail.
    # seconds: how many seconds it should grab.
    # return the data it grabs.
    def __get_data(self, seconds):
        buffer = self.__data_buffer[-1 * (seconds * self._sampling_rate):]
        time = self.__time_buffer[-1 * (seconds * self._sampling_rate):]
        return buffer, time

    def __push_data(self,buffer):
        self.__result_buffer.extend(buffer)

        # plt.figure("data")
        # plt.plot(self.__data_buffer)
        # plt.show()


    #live appending message string to self.data buffer, execute a live_process every 75 data.
    #msg_str: the message hm10 reads
    #seconds: number of seconds for a small window of data
    def live_appending(self,msg_str,seconds):
        length = seconds*self._sampling_rate
        self.append(msg_str)
        self.__live_buffer_index += 1
        if self.__live_buffer_index % length ==0:
            string = self.live_process(seconds)

            return string
        else:
            return ""



    #grab some seconds of data from self.data_buffer and process it.
    #seconds: number of seconds data is sliced.
    def live_process(self,seconds):
        self.__num_of_windows +=1
        buffer, portion_time = self.__get_data(seconds)
        self.__total_time.extend(portion_time)
        b_low, a_low = sig.butter(3, 4 / (0.5 * 50), btype="lowpass", analog=False, output='ba')
        b_high, a_high = sig.butter(3, 0.2 / (0.5 * 50), btype="highpass")

        signal_out = self.__filter_initial_condition(buffer,self.__low_initial,b_low,a_low,self.__high_initial,b_high,a_high)
        self.__push_data(signal_out)
        self.__find_peaks(signal_out)
        string = self.__count_steps()
        return "S:" + string

    #filter the buffer with initial condition considered.
    #buffer: the signal in
    def __filter_initial_condition(self,buffer,z1_in_low,b_low,a_low,z1_in_high,b_high,a_high):
        signal_in = sig.detrend(buffer)

        signal_in = np.gradient(signal_in)

        if self.__num_of_windows ==1:
            z1_in_low = sig.lfilter_zi(b_low, a_low)
            z1_in_low = z1_in_low * signal_in[0]


        signal_out, z1_out_low = sig.lfilter(b_low, a_low, signal_in, zi=z1_in_low)
        self.__low_initial = z1_out_low

        if self.__num_of_windows == 1:
            z1_in_high = sig.lfilter_zi(b_high, a_high)
            z1_in_high = z1_in_high * signal_in[0]
        signal_out, z1_out_high = sig.lfilter(b_high, a_high, signal_out, zi=z1_in_high)
        self.__high_initial = z1_out_high



        return signal_out


    def save_file(self, filename):
        with open("./Lab8/" + filename, "w+") as file:
            for i in range(0, self._maxlen):
                string = str(self.__time_buffer[i]) + "," + str(self.__data_buffer[i]) + "\n"
                file.write(string)

    def load_file(self, filename):
        self.reset()
        with open(filename, "r+") as file:
            n = 0
            while 1:
                n += 1
                string = file.readline()
                parsedList = string.strip().split(",")
                if len(parsedList) == 1:
                    print("Pedometer finish loading, len of time buffer:", len(self.__time_buffer), "len of data buffer:",
                          len(self.__data_buffer))
                    break
                self.__time_buffer.append(int(parsedList[0]))
                self.__data_buffer.append(int(parsedList[1]))
                self._maxlen = n
            return


    def plot(self):
        plt.figure("IMU values verses Time")
        plt.plot(self.__time_buffer,self.__data_buffer)
        plt.show()
        return

    def plot_live(self):
        plt.cla()  # clear the axes
        plt.plot(self.__result_buffer)

        peak_time = []
        peak_value = []
        for x in self.__peaks:
            peak_time.append(self.__total_time[x])



        plt.show(block=False)  # similar to interactive mode
        plt.pause(0.000001)

    def __lowpass_filter(self, cutoff):  # __ makes this a private method
        b, a = sig.butter(3, cutoff/(0.5*50), btype='lowpass', analog=False,output='ba')  # 1. order of filter, 2.Wn cut off freq
        self.__data_buffer = sig.lfilter(b,a,self.__data_buffer)
        return


    def __highpass_filter(self, cutoff):  # __ makes this a private method
        b, a = sig.butter(3, cutoff/(0.5*50), 'highpass', analog=False)
        self.__data_buffer = sig.lfilter(b, a, self.__data_buffer)


    def __smoothing_filter(self, N):
        M = N+1
        filter = sig.boxcar(M)
        self.__data_buffer = sig.lfilter(filter/M,1,self.__data_buffer)
        return

    def __demean_filter(self):
        # Compute the mean using a sliding window
        filtered = sig.detrend(self.__data_buffer)
        self.__data_buffer = filtered
        return

    def filter_pedometer(self):
        self.__demean_filter()
        self.__smoothing_filter(5)
        self.__data_buffer = np.gradient(self.__data_buffer)
        self.__lowpass_filter(5)

        return



    def __find_peaks(self,signal_out):

        self.__peaks_index, dictionary= sig.find_peaks(signal_out,height=[2500,10000])
        for i in range(0,len(self.__peaks_index)):
            self.__peaks_index[i] = self.__peaks_index[i] + (self.__num_of_windows-1)*self._sampling_rate*3

        self.__peaks.extend(self.__peaks_index)
        return

    def __count_steps(self):
        self.__steps = len(self.__peaks)
                #my plot data_buffer[inds] is in process, the graph has both data and their associated peaks in it
        return str(self.__steps)


