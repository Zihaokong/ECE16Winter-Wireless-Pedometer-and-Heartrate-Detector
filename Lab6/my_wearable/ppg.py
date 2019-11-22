"""
Authors: Ramsin Khoshabeh
Contact: ramsin@ucsd.edu
Date: 29 October 2019
Description: A class to handle the PPG for the wearable
"""

# Imports
import serial
from time import sleep
from time import time
from scipy import signal as sig
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal as sig

class PPG:
    # Attributes of the class PPG
    _maxlen = 0
    __time_buffer = []  # private variable (encapsulation)
    __data_buffer = []  # private variable (encapsulation)
    __heartbeats = []
    __fs = 0  # sampling rate

    """ ================================================================================
    Constructor that sets up the PPG class. It will only run once.
    :param maxlen: (int) max length of the buffer
    :param fs: (int) sampling rate from the Arduino
    :return: None
    ================================================================================ """

    def __init__(self, maxlen, fs):
        self._maxlen = maxlen  # Set the max length of the buffer
        print("max buffer length is ",self._maxlen)
        sleep(1)
        fig = plt.figure(1)
        fig.canvas.mpl_connect('key_press_event', self.__handle_keypress)
        self.__fs = fs
        return

    """ ================================================================================
    A callback function that triggers when a key is pressed with the plot open
    :param event: the input event that triggered the callback
    :return: None
    ================================================================================ """

    def __handle_keypress(self, event):
        if event.key == 'enter':
            self.save_file("PPGRaw5.csv")

    """ ================================================================================
    Resets the PPG to default state
    :return: None
    ================================================================================ """

    def reset(self):
        self.__time_buffer = []
        self.__data_buffer = []
        return

    """ ================================================================================
    Appends new elements to the data and time buffers by parsing 'msg_str' and splitting
    it, assuming comma separation. It also keeps track of buffer occupancy. Once the 
    buffer is full, it will become a circular buffer and drop samples from the beginning
    as a FIFO buffer.
    :param msg_str: (str) the string containing data that will be appended to the buffer
    :return: None
    ================================================================================ """

    def append(self, msg_str):
        try:
            bufferCurrentPos = 0#how many stuff in buffer
            listTOWrite = []#the list to save to two lists
            dataList = msg_str.split(";")
            #parse the incoming data by ;, so we have datalist
            # that is [(time,value),(time,value),(time,value)]



            for i in range(len(dataList)):
                listTOWrite = dataList[i].strip().split(",")#first strip any split \n and ,

                #case 1, there is # in data, delete "#"
                for x in listTOWrite:
                    if x.startswith("#"):
                        k = x[1:].strip()
                        listTOWrite[0] = k

                if len(listTOWrite) == 3: #prevent lost data during transmission
                    print("time: ", listTOWrite[0],"heart rate: ", listTOWrite[2])
                    self.__time_buffer.append(int(listTOWrite[0]))
                    self.__data_buffer.append(int(listTOWrite[2]))
                    print(len(self.__time_buffer))
                    bufferCurrentPos = len(self.__time_buffer)
                if bufferCurrentPos >= self._maxlen:
                    print("buffer is full, the number is ", listTOWrite[2])
                    self.__time_buffer = self.__time_buffer[1:]
                    self.__time_buffer.append(int(listTOWrite[0]))
                    self.__data_buffer = self.__data_buffer[1:]
                    self.__data_buffer.append(int(listTOWrite[2]))


        except ValueError:
            print("invalid Data")

    ### TO DO ###
    # 1. Inside of a try-except block
    # 2.1. Split the incoming message by looking for ','
    # 2.2. Store the time to a temporary variable (make sure to cast as an int)
    # 2.3. Store the PPG data to temporary variable (make sure to cast as an int)
    #      - This will be on index 2 since IMU data is index 1!!!
    # 2. If there is a ValueError or IndexError exception
    # print that there was invalid data
    # 3. Check if our buffers are full by checking that the length of one of the
    #    buffers (both should be have the same length) is equal to maxlen
    # 1.1. If the buffers are full, shift both buffers left by one value
    # 1.2. Assign the last value of the time buffer with the new time value
    # 1.3. Assign the last value of the data buffer with the new PPG data value
    # 4. If the buffers are not full, simply append the new time & data to the buffers
    # 5. Return nothing

    """ ================================================================================
    Saves the contents of the buffer into the specified file one line at a time.
    :param filename: (str) the name of the file that will store the buffer data
    :return: None
    ================================================================================ """

    def save_file(self, filename):
        with open(filename,"w+") as file:
            for i in range(0,self._maxlen):
                string = str(self.__time_buffer[i]) +"," + str(self.__data_buffer[i])+"\n"
                file.write(string)
    ### TO DO ###
    # 1. Open the file with mode set to write (this will overwrite any data)
    # 2. In a for-loop, iterate over the buffers
    # 2.1. Assemble a "row" string from the buffers formatted as "<t>,<d>\n"
    # 2.2. Write the row to the file
    # 3. Close the file or use the "with" keyword
    # 4. Return nothing

    # NOTE: This method is the same as in the Pedometer class

    """ ================================================================================
    Loads the contents of the file 'filename' into the time and data buffers
    :param filename: (str) the name (full path) of the file that we read from
    :return: None
    ================================================================================ """

    def load_file(self, filename):
        self.reset()

        with open(filename, "r+") as file:
            n = 0
            while 1:
                n += 1
                string = file.readline()
                parsedList = string.strip().split(",")

                if len(parsedList) == 1:
                    break

                self.__time_buffer.append(int(parsedList[0]))
                self.__data_buffer.append(int(parsedList[1]))
                self._maxlen = n
            return

        ### TO DO ###
        # 1. Open the file with mode set to read
        # 2. Loop forever until _maxlen is reached
        # 2.1. Read a line from the file
        # 2.2. Check to see if the line is None
        # 2.2.1. If it is, break out of the loop (the end of file was reached)
        # 2.3. Strip any newline characters from the line and split it with ','
        # 2.4. Append time value to the time buffer
        # 2.5. Append data value to the data buffer
        # 2.6. Keep track of the number of times the while loop runs in a variable
        # 3. Return nothing

        # NOTE: This method is the same as in the Pedometer class

    """ ================================================================================
    Plots the data in the time and data buffers onto a figure
    :param: None
    :return: None
    ================================================================================ """

    def plot(self):

        max = np.amax(self.__data_buffer)

        min = np.amin(self.__data_buffer)

        plt.xlim(self.__time_buffer[0], self.__time_buffer[-1])
        plt.ylim(min,max)
        plt.plot(self.__time_buffer[0:self._maxlen], self.__data_buffer[0:self._maxlen])
        array1 = []
        array2 = []
        for x in self.__heartbeats:
            array1.append(self.__time_buffer[x])
            array2.append(self.__data_buffer[x])
        plt.plot(array1,array2,"x")
        plt.show()
        return
    ## TO DO ##
    # 1. Open a new figure (if needed)
    # 2. Plot the time buffer versus the data buffer (stylize however you like)
    # 3. Show the plot
    # 4. Return nothing

    # NOTE: This method is the same as in the Pedometer class

    """ ================================================================================
    Live plot the data in the data buffer onto a figure and update continuously
    :param: None
    :return: None
    ================================================================================ """

    def plot_live(self):
        plt.cla()  # clear the axes
        plt.plot(self.__time_buffer,self.__data_buffer)
        print("length: ",len(self.__time_buffer),len(self.__data_buffer))
        plt.show(block=False)  # similar to interactive mode
        plt.pause(0.001)
## TO DO ##
# 1. Clear the plot axes (https://matplotlib.org/3.1.1/api/pyplot_summary.html)
# 2. Plot the the data buffer (Note: the time buffer is not being plotted!)
# 3. Show the plot with the argument: block=False
# 4. Pause the plot for 0.001 seconds
# 5. Return nothing

    def __lowpass_filter(self, cutoff):  # __ makes this a private method
        b, a = sig.butter(2, cutoff/(0.5*50), btype='lowpass', analog=False,output='ba')  # 1. order of filter, 2.Wn cut off freq

        self.__data_buffer = sig.lfilter(b,a,self.__data_buffer)
        return
    def __highpass_filter(self, cutoff):  # __ makes this a private method
        b, a = sig.butter(4, cutoff/(0.5*50), 'highpass', analog=False)
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

    def __filter_ppg(self):
        self.__demean_filter()
        self.__lowpass_filter(16)
        self.__highpass_filter(0.9)
        self.__data_buffer = np.gradient(self.__data_buffer)
    def __find_heartbeats(self):
        # self.__filter_ppg()
        # self.__peaks, dictionary = sig.find_peaks(self.__data_buffer)
        # self.__lower_threshold = 1.3
        # self.__upper_threshold = 100
        # for i in self.__peaks:
        #     if self.__data_buffer[i] > self.__lower_threshold and self.__data_buffer[i] < self.__upper_threshold:
        #         self.__heartbeats.append(i)

        # Objective 5
        temp_data = self.__data_buffer
        filtered_output = []
        lower_bound = 0
        upper_bound = 3*self.__fs
        while upper_bound<=self._maxlen:
            print("lower bound: ", lower_bound, "upper bound: ", upper_bound)
            self.__data_buffer = temp_data[lower_bound:upper_bound]
            self.__filter_ppg()
            filtered_output.extend(self.__data_buffer)
            lower_bound = upper_bound
            upper_bound = upper_bound+3*self.__fs

        self.__data_buffer = filtered_output
        if len(self.__data_buffer)< self._maxlen:
            self.__time_buffer[0:len(self.__data_buffer)]
        self.__peaks, dictionary = sig.find_peaks(self.__data_buffer)
        self.__lower_threshold = 1.3
        self.__upper_threshold = 100
        for i in self.__peaks:
            if self.__data_buffer[i] > self.__lower_threshold and self.__data_buffer[i] < self.__upper_threshold:
                self.__heartbeats.append(i)






    def process(self):
        self.__find_heartbeats()
        self.plot()



