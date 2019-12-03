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
from sklearn.mixture import GaussianMixture
from scipy.stats import norm
from scipy import signal as sig
from Lab7.my_wearable.BLE import BLE
class PPG:
    # Attributes of the class PPG
    _maxlen = 0
    __time_buffer = []  # private variable (encapsulation)
    __data_buffer = []  # private variable (encapsulation)
    __heartbeats = []
    __fs = 0  # sampling rate
    _model = 0
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
        #fig = plt.figure(1)
        #fig.canvas.mpl_connect('key_press_event', self.__handle_keypress)
        self.__fs = fs
        return

    """ ================================================================================
    A callback function that triggers when a key is pressed with the plot open
    :param event: the input event that triggered the callback
    :return: None
    ================================================================================ """

    def __handle_keypress(self, event):
        if event.key == 'enter':
            self.save_file("test.csv")

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
            #how many stuff in buffer
            t, imu, ir = msg_str.strip().split(",")
            #print("time:", int(t), "heart rate:", int(ir))
            if self._maxlen>len(self.__time_buffer):
                self.__time_buffer.append(int(t))
                self.__data_buffer.append(int(ir))

                #print("button pos:", len(self.__time_buffer))
            else:
                #print("excede length ")
                self.__time_buffer[:-1] = self.__time_buffer[1:]
                self.__time_buffer[-1] = int(t)
                self.__data_buffer[:-1] = self.__data_buffer[1:]
                self.__data_buffer[-1] = int(ir)

        except ValueError:
            print("Invalid Data: " + msg_str)

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
        self.normalize()
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
        #print("length: ",len(self.__time_buffer),len(self.__data_buffer))
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

        self.__lowpass_filter(7)
        self.__highpass_filter(0.9)
        #self.__data_buffer = np.gradient(self.__data_buffer)


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




    def hr_heuristics(self):
        #determine which is "heartbeat", which is "not heartbeat"
        data = self.__result
        tags, frequency = np.unique(data,return_counts=True)
        label = {}

        #assume number of not heartbeat is more than heartbeat
        #the bigger number is "not heartbeat"
        #the dictionary corespond heartbeat to the label that gmm predicts
        if frequency[0] > frequency[1]:
            label["not heart beat"] = tags[0]
            label["heartbeat"] = tags[1]
        else:
            label["not heart beat"] = tags[1]
            label["heartbeat"] = tags[0]


        # filter out the noise in result, prevent small peaks, then find local max
        self.__lowpass_filter(7)
        local_maxes,_ = sig.find_peaks(self.__data_buffer,height =[0,0.5])


        new_time = []
        # get rid of small peak that is incorrectly labeled by machine learning, then count how many is left.
        heartbeat = 0
        for x in local_maxes:
            #if the peak is higher than a threshold, and also the peak labeled as "heartbeat", we count
            if self.__result[x] == label["heartbeat"] and self.__data_buffer[x] >0.18:
                new_time.append(self.__time_buffer[x])
                self.__heartbeats.append(self.__data_buffer[x])
                heartbeat+=1

        #plot result
        # plt.plot(self.__time_buffer, self.__data_buffer)
        # plt.plot(new_time, self.__heartbeats, "x")
        # plt.plot(self.__time_buffer,self.__result)
        # plt.show()

        #calculate
        time_diff = (self.__time_buffer[-1] - self.__time_buffer[0])/1000
        rate = (heartbeat/time_diff)*60

        string = "heart beat per min is:" +str(rate)
        print(string)
        return string



    # At a bare minimum, you can do the following steps. BUT you should definitely consider the edge cases we discussed in class!!!
    # 1. Find the indices of the maximum of the peaks from the labels
    # 2. Next compute the time difference between all of the peaks
    # 3. Prune the outlier peaks
    # 3.1 For example, you coul loop through the time differences and check if the length is above a threshold
    # 3.2 If it is below the threshold, then discard it as a false reading
    ## Remember: You could try a low-pass filter instead of doing time thresholding. It's your choice which one you prefer. Get creative!
    # 4. Get the total count of valid heartbeat times from the labels
    # 5. Calculate the estimated heart rate given the valid beats
    # 6. Store the HR in your HR buffer
    # 7. Return the current HR

    def check_fs(self,time_data, sampling_rate):
        time_data = self.__time_buffer
        diffs = np.diff(time_data)
        avg_diff = np.mean(diffs)
        estimated_fs = 1e3 / avg_diff
        print(estimated_fs,sampling_rate)
        if estimated_fs < sampling_rate:
            print('Warning: Low FS detected! Recollect data with an FS less than %3.2f Hz.' % estimated_fs)
        return estimated_fs

    def train(self, train_data):
        gmm = GaussianMixture(n_components=2)
        self.__data_buffer = train_data
        self.__filter_ppg()
        self.__data_buffer = np.array(self.__data_buffer).reshape(-1, 1)
        gmm.fit(self.__data_buffer)  # data has to be (-1,1)
        self._model = gmm
    # 1. Create a GMM object and specify the number of components (classes) in the object
    # 2. Fit the model to our training data. NOTE: You may need to reshape with np.reshape(-1,1)
    # 3. Return None

    def plt_hist(self, data, bin_count):
        mu1 = self._model.means_[0,0]
        mu2 = self._model.means_[1,0]
        var1, var2 = self._model.covariances_
        wgt1, wgt2 = self._model.weights_

        self.__data_buffer = data
        self.__filter_ppg()

        x = np.linspace(np.min(self.__data_buffer), np.max(self.__data_buffer), num=1000).reshape([1000, 1])
        plt.figure("histogram of data")
        plt.hist(self.__data_buffer, bins=bin_count, density=True)
        plt.plot(x,wgt1*norm.pdf(x, mu1, np.sqrt(var1))+wgt2*norm.pdf(x, mu2, np.sqrt(var2)))
        plt.xlabel("PPG reading")
        plt.ylabel("Count number")
        plt.title("IR Signal Histogram (Sum)")
        plt.tight_layout()
        plt.show(block = True)

        # plt.figure()
        # plt.hist(self.__data_buffer, bins=bin_count, density=True)
        # plt.plot(x,wgt1*norm.pdf(x, mu1, np.sqrt(var1)))
        # plt.plot(x,wgt2*norm.pdf(x, mu2, np.sqrt(var2)))
        # plt.xlabel("PPG reading individual")
        # plt.ylabel("Count number")
        # plt.title("IR Signal Histogram (Individual)")
        # plt.tight_layout()
        #plt.show()

    # 1. Retrieve Gaussian parameters (these are all attributes of the self.__model)
    # 1.1 Retrieve means for class 0 and class 1
    # 1.1 Retrieve the covariances for class 0 and 1 and take the square root of each
    # 1.2 Retrieve the weights for class 0 and 1
    # 2. Create a vector 'x' that will be a vector with a 1000 elements from the min(ir) value to the max(ir) value. HINT: Use np.linspace(). You may need to use np.reshape(x,[1000,1])
    # 3. Compute normal curves for class 0 and 1 HINT: This is done by multiplying the weight by the normalized pdf. Use a function called norm.pdf
    # 4. Create a new figure
    # 5. Plot the histogram
    # 6. Plot the sum of the normal curves NOTE: Distinguish the two curves by making them different colors.
    # 7. Label the plots HINT: X axis is the PPG reading and y axis the count number.
    # 8. Title the plot "IR Signal Histogram"
    # 9. Call plt.tight_layout()
    # 10. Show the plot and set block to false
    # 11. Create a new figure
    # 12. Plot the histogram
    # 13. Plot each individual curves
    # 14. Label and title the plots
    # 15. Return None

    def plt_labels(self, data, time):#data being filtered.
        self.__data_buffer = data
        self.__filter_ppg()
        self.__data_buffer = np.array(self.__data_buffer).reshape(-1, 1)
        result = self._model.predict(self.__data_buffer)
        plt.figure()
        plt.plot(time,result)
        plt.plot(time,self.__data_buffer)
        plt.xlabel("PPG reading, (predicting Label)")
        plt.ylabel("Count number, label")
        plt.title("IR Signal Histogram (Predicting Label)")
        plt.show(block = True)
# 1. Calculate the labels by running the IR data through the model
# 2. Create a new figure
# 3. Plot the time and IR data
# 4. Plot the time and label data
# 5. Label the x and y axes
# 6. Title the plot "GMM Labels"
# 7. Show the plot and set block to false
# 8. Return None

    def process(self):
        #plt.figure("plot of test.csv")
        self.__filter_ppg()
        result = np.array(self.__data_buffer).reshape(-1,1)
        #plt.plot(self.__time_buffer,self.__data_buffer)
        self.__result = self._model.predict(result)#new Data
        #plt.plot(self.__time_buffer,self.__result)

        #plt.show()         # YOU ALREADY HAVE THIS METHOD! Just at these lines of code to the method
        string = self.hr_heuristics()

        hm10 = BLE("COM4",9600,False)
        hm10.connect("78DB2F16821E")
        hm10.write(string+";")
        print("process finish")



        # 1. Using the GMM model from the previous objective, call the GMM's predict() method to classify the new data
        # 2. Next call hr_heuristics() to calculate the heart rate
        # 3. Return the HR

    def normalize(self):
        max = np.amax(self.__data_buffer)
        min = np.amin(self.__data_buffer)
        for i in range(0, len(self.__data_buffer)):
            self.__data_buffer[i] = (self.__data_buffer[i] - min) / (max - min)

