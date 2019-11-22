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
    __time_buffer = []  # private variable (encapsulation)
    __data_buffer = []  # private variable (encapsulation)
    __steps = 0

    _digitChecker = 0

    """ ================================================================================
    Constructor that sets up the Pedomter class. It will only run once.
    :param max len: (int) max length of the buffer
    :param file_flag: (bool) set whether we will be working with a file or not
    :return: None
    ================================================================================ """

    def __init__(self, maxlen, file_flag):
        self._maxlen = maxlen  # Set the max length of the buffer
        self._file_flag = file_flag  # Set whether we are writing to a file or not
        self.__steps = 0
        return

    """ ================================================================================
    Resets the pedometer to default state
    :return: None
    ================================================================================ """

    def reset(self):
        self._maxlen = 0
        self.__time_buffer = []
        self.__data_buffer = []
        __steps = 0
        return

    """ ================================================================================
    Appends new elements to the data and time buffers by parsing 'msg_str' and splitting
    it, assuming comma separation. It also keeps track of buffer occupancy and notifies
    the user when the buffers are full.
    :param msg_str: (str) the string containing data that will be appended to the buffer
    :return: None
    ================================================================================ """


    def append(self, msg_str):
        if self._maxlen <= len(self.__time_buffer) or self._maxlen <= len(self.__data_buffer) :
            print("buffer is full")
            return None
        try:
            bufferCurrentPos = 0#how many stuff in buffer
            listTOWrite = []#the list to save to two lists
            dataList = msg_str.split(";")
            #parse the incoming data by ;, so we have datalist
            # that is [(time,value),(time,value),(time,value)]


            error_list = []
            abnormal = False
            for i in range(len(dataList)):
                listTOWrite = dataList[i].strip().split(",")#first strip any split \n and ,

                #case 1, there is # in data, delete "#"
                for x in listTOWrite:
                    if x.startswith("#"):
                        k = x[1:].strip()
                        listTOWrite[0] = k
                #case 2, the incoming byte somehow didn't read fully, so time or sum value becomes very small
                # a simple algorithm to check if the incoming byte is full or loss some data, if lost, then discard this sample
                if  len(str(listTOWrite[0])) > self._digitChecker:
                    self._digitChecker = len(str(listTOWrite[0]))
                    print("good data")
                    abnormal = False

                elif len(str(listTOWrite[0])) < self._digitChecker and len(str(listTOWrite[0])) != 0:
                    print(listTOWrite[0],"digit check is at ",self._digitChecker)
                    print("bad data")
                    abnormal = True



                if len(listTOWrite) == 2 and abnormal != True and len(listTOWrite[1])>3:

                    print("list to write 0 ", listTOWrite[0]," list to write 1 ", listTOWrite[1])
                    self.__time_buffer.append(listTOWrite[0])
                    self.__data_buffer.append(listTOWrite[1])
                    print(len(self.__time_buffer))
                    bufferCurrentPos = len(self.__time_buffer)
                if bufferCurrentPos >= 500:
                    break
            if bufferCurrentPos >= 500:
                return False
            else:
                return True
        except ValueError:
            print("invalid Data")


    ### TO DO ###
    # 1. Check if the length of one of buffers (both should be the same) is equal to maxlen
    # 1.1. If they are equal, print a message that the buffer is full
    # 1.2. do nothing and return
    # 2. Inside of a try-except block
    # 2.1. Split the incoming message by looking for ','
    # 2.2. Append the time to the time buffer (make sure to cast as an int)
    # 2.3. Append the data to the data buffer (make sure to cast as an int)
    # 3. If there is a ValueError exception
    # print that there was invalid data
    # 4. Return True if the buffer is not full yet, False otherwise

    """ ================================================================================
    Saves the contents of the buffer into the specified file one line at a time.
    :param filename: (str) the name of the file that will store the buffer data
    :return: None
    ================================================================================ """

    def printPrivate(self):
        z = 0
        for i in range(0,500):
            print(self.__time_buffer[i], self.__data_buffer[i])


    def save_file(self, filename):
        with open(filename,"w+") as file:
            for i in range(0,500):
                string = self.__time_buffer[i] +"," + self.__data_buffer[i]+"\n"
                file.write(string)
    ### TO DO ###
    # 1. Open the file with mode set to write (this will overwrite any data)
    # 2. In a for-loop, iterate over the buffers
    # 2.1. Assemble a "row" string from the buffers formatted as "<t>,<d>\n"
    # 2.2. Write the row to the file
    # 3. Close the file or use the "with" keyword
    # 4. Return nothing

    """ ================================================================================
    Loads the contents of the file 'filename' into the time and data buffers
    :param filename: (str) the name (full path) of the file that we read from
    :return: None
    ================================================================================ """

    def load_file(self, filename):
        self.__time_buffer = []
        self.__data_buffer = []

        with open(filename, "r+") as file:
            n = 0
            while 1:
                n+=1
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
        # 2. Loop forever
        # 2.1. Read a line from the file
        # 2.2. Check to see if the line is None
        # 2.2.1. If it is, break out of the loop (the end of file was reached)
        # 2.3. Strip any newline characters from the line and split it with ','
        # 2.4. Append time value to the time buffer
        # 2.5. Append data value to the data buffer
        # 2.6. Keep track of the number of times the while loop runs in a variable
        # 3. Set the object's _maxlen (self._maxlen) to the loop count variable
        # 4. Return nothing

    """ ================================================================================
    Plots the data in the time and data buffers onto a figure
    :param: None
    :return: None
    ================================================================================ """

    def plot(self):
        plt.figure()
        plt.xlim(self.__time_buffer[0], self.__time_buffer[-1])
        plt.ylim(-20000, 20000)
        plt.plot(self.__time_buffer[0:499],self.__data_buffer[0:499])
        plt.show()
        return
    ## TO DO ##
    # 1. Open a new figure (if needed)
    # 2. Plot the time buffer versus the data buffer (stylize however you like)
    # 3. Show the plot
    # 4. Return nothing

    """ ================================================================================
    This function runs the contents of the __data_buffer through a low-pass filter. It
    first generates filter coefficients and  runs the data through the low-pass filter.
    Note: In the future, we will only generate the coefficients once and reuse them.
    :param cutoff: (int) the cutoff frequency of the filter
    :return: None
    ================================================================================ """
    # 3 good
    def __lowpass_filter(self, cutoff):  # __ makes this a private method
        b, a = sig.butter(3, cutoff/(0.5*50), btype='lowpass', analog=False,output='ba')  # 1. order of filter, 2.Wn cut off freq

        self.__data_buffer = sig.lfilter(b,a,self.__data_buffer)
        return
    ### TO DO ###)
    # 1. Use the butter() command from Scipy to produce the filter coefficients
    #    for a 3rd order (N=3) filter and set analog to False. Remember that
    #    'cutoff' must be normalized between 0-1!
    # 2. Filter the data using the lfilter() command
    # 3. Assign the filtered data to the data buffer
    # 4. Return nothing

    """ ================================================================================
    This function runs the contents of the __data_buffer through a high-pass filter. It
    first generates filter coefficients and runs the data through the high-pass filter.
    Note: In the future, we will only generate the coefficients once and reuse them.
    :param cutoff: (int) the cutoff frequency of the filter
    :return: None
    ================================================================================ """

    def __highpass_filter(self, cutoff):  # __ makes this a private method
        b, a = sig.butter(3, cutoff/(0.5*50), 'highpass', analog=False)
        self.__data_buffer = sig.lfilter(b, a, self.__data_buffer)

    ### TO DO ###
    # 1. Use the butter() command from Scipy to produce the filter coefficients
    #    for a 3rd order (N=3) filter and set analog to False. Remember that
    #    'cutoff' must be normalized between 0-1!
    # 2. Filter the data using the lfilter() command
    # 3. Assign the filtered data to the data buffer
    # 4. Return nothing

    """ ================================================================================
    Runs the contents of the __data_buffer through a moving average filter
    :param N: order of the smoothing filter (the filter length = N+1)
    :return: None
    ================================================================================ """

    def __smoothing_filter(self, N):
        M = N+1
        filter = sig.boxcar(M)
        self.__data_buffer = sig.lfilter(filter/M,1,self.__data_buffer)
        return
    ### TO DO ###
    # 1. Create a boxcar window of length M (M = N+1) and normalize it by M
    # 2. Filter the data using the lfilter() command where b is the window and a=1
    # 3. Assign the filtered data to the data buffer
    # 4. Return nothing

    """ ================================================================================
    Runs the contents of the __data_buffer through a de-meaning filter.
    :param: None
    :return: None
    ================================================================================ """

    def __demean_filter(self):
        # Compute the mean using a sliding window
        filtered = sig.detrend(self.__data_buffer)
        self.__data_buffer = filtered
        return

    """ ================================================================================
    The main process block of the pedometer. When completed, this will run through the
    filtering operations and heuristic methods to compute and return the step count.
    For now, we will use it as our "playground" to filter and visualize the data.
    :param None:
    :return: Current step count
    ================================================================================ """

    def filter_pedometer(self):
        self.__demean_filter()
        self.__smoothing_filter(5)
        self.__data_buffer = np.gradient(self.__data_buffer)
        self.__lowpass_filter(5)

        return

    ## TO DO ##
    # 1. Run the raw data through the demean filter
    # 2. After, run the smoothing_filter with a window of 5
    # 3. Take the gradient of the data using np.gradient
    # 4. Use a lowpass fiter with a cutoff frequency of around 5Hz, REMEMBER to calculate the normalized cutoff frequency and use that in your function call
    # 5. Return




    def find_peaks(self):
        self.__peaks = []
        self.filter_pedometer()
        self.__peaks, dictionary= sig.find_peaks(self.__data_buffer,15)
        #print(self.__peaks)
        return
    ## TO DO ##
    # 1. Initialize self.__peaks to an empty list
    # 2. Filter all of the data in the self.__data_buffer (HINT: you wrote a method that does this!)
    # 3. Find the indices of all the peaks above the 0 threshold and store them in self.__peaks. (HINT: try scipy.signal.find_peaks)
    # 4. Return



    """ ================================================================================
    Saves the contents of the buffer into the file line by line 
    :param filename: (str) the name of the file that will store the buffer data
    :return: None
    ================================================================================ """


    def __count_steps(self):
        inds = []
        for i in self.__peaks:

            if self.__data_buffer[i] > 100 and self.__data_buffer[i] < 4000:
                self.__steps +=1
                inds.append(i)

                #my plot data_buffer[inds] is in process, the graph has both data and their associated peaks in it
        return inds
        ## TO DO ##
        # 1. initialize variable inds to be an empty list
        # 2. Parse through all the indices in self.__peaks
        # 2.1. check to see if the value of self.__data_buffer at the index of the peak is greater than the lower threshold and smaller than the upper threshold
        # 2.1.1. increment the step counter self.__steps
        # 2.1.2. appeand that peak into inds
        # 3. plot the contents of self.__data_buffer[inds] (DON'T USE self.plot() THIS IS FOR YOUR REFERRENCE ONLY! Write it in __count_steps and then comment it out!!!!)

        #return


    def process(self):
        # self.reset()
        # self.load_file("Lab5/walking_50hz.txt")
        # self.__demean_filter()
        # self.plot()

        self.load_file("Lab5/walking_100hz.txt")
        raw_data = self.__data_buffer
        self.find_peaks()
        filter_data = self.__data_buffer
        points = self.__count_steps()
        print("numbre of step: ",len(points))
        plt.plot(self.__time_buffer,raw_data,self.__time_buffer,filter_data)
        plt.axhline(y=4000)
        plt.axhline(y=100)
        x = []
        y = []
        for elements in points:
            x.append(self.__time_buffer[elements])
            y.append(self.__data_buffer[elements])
        plt.scatter(x,y)
        plt.show()


