"""
Authors: Ramsin Khoshabeh
Contact: ramsin@ucsd.edu
Date: 29 October 2019
Description: A class to handle the PPG for the wearable
"""

# Imports
import serial
from time import sleep
from time import time as t
from scipy import signal as sig
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal as sig
from sklearn.mixture import GaussianMixture
from scipy.stats import norm
from scipy import signal as sig
from Lab8.my_wearable.BLE import BLE
class PPG:
    #basic attribute
    _maxlen = 0
    __time_buffer = []
    __data_buffer = []
    __fs = 0

    #buffer for live_plotting
    __total_time = [] #total time since turn on
    __total_filter_result = []  # the buffer to store the filtered data
    __total_ML_result = []  # all labels since it's started

    #number of heart beats and it's respective time location
    __heartbeats = [] # the buffer to store heart beat index
    __heartbeats_time = []

    #GMM
    _model = 0

    # Short buffers for window filtering
    __heuristics_filtered_data = []  # the 3 second buffer to use storing filtered data, used for heuristic
    __heuristic__ML_labels = []  # the 3 second buffer to store GMM label

    #live filtering, initials
    __live_buffer_index =0
    __num_of_windows = 0  # how many time live process is executed
    __low_initial = 0
    __high_initial = 0


    def __init__(self, maxlen, fs):
        self._maxlen = maxlen
        fig = plt.figure(1)
        fig.canvas.mpl_connect('key_press_event', self.__handle_keypress)
        self.__fs = fs
        return

    #function that saves file locally when graphing and enter is pressed
    def __handle_keypress(self, event):
        if event.key == 'enter':
            self.save_file("live_filtering.csv")



    def reset(self):
        self.__time_buffer = []
        self.__data_buffer = []
        return

    #put message string into basic time and data buffer, which is circular
    def append(self, msg_str):
        try:
            if msg_str[0] == "#":
                t, imu, ir = msg_str[1:].strip().split(",")
            else:
                t, imu, ir = msg_str.strip().split(",")
            if self._maxlen>len(self.__time_buffer):
                self.__time_buffer.append(int(t))
                self.__data_buffer.append(int(ir))
            else:
                self.__time_buffer[:-1] = self.__time_buffer[1:]
                self.__time_buffer[-1] = int(t)
                self.__data_buffer[:-1] = self.__data_buffer[1:]
                self.__data_buffer[-1] = int(ir)

        except ValueError:
            print("Invalid Data: " + msg_str)


    #read what's in time and data buffer, save locally.
    #used with append, when appending, call this function when "enter" is pressed
    def save_file(self, filename):
        with open("./Lab8/"+filename,"w+") as file:
            for i in range(0,self._maxlen):
                string = str(self.__time_buffer[i])+ "," + str(self.__data_buffer[i])+"\n"
                file.write(string)


    #load local file, save to basic time and data buffers
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
                #load first and third entry, which is time and IR
                self.__time_buffer.append(int(parsedList[0]))
                self.__data_buffer.append(int(parsedList[2]))
                self._maxlen = n
        return

    #plot time and data buffer with heart beat index.
    def plot(self):
        plt.figure("plot of IR data vs Time")
        plt.plot(self.__time_buffer, self.__data_buffer)
        plt.show()
        return

    #live plotting
    def plot_live(self):
        plt.cla()  # clear the axes

        #since the total time and filter result update every three seconds, plot happens during data are updated
        if len(self.__total_time) == len(self.__total_filter_result):

            #when the x axis spans too big, we slice it.

            plt.plot(self.__total_time, self.__total_filter_result)
            plt.plot(self.__total_time, self.__total_ML_result)
            #print("total beat: ",len(self.__heartbeats))
            #plt.plot(self.__heartbeats_time,self.__heartbeats,"x")
            # else:
            #     plt.plot(self.__total_time[-750:], self.__total_filter_result[-750:])
            #     plt.plot(self.__total_time[-750:], self.__total_ML_result[-750:])
            #     print(len(self.__heartbeats))

        plt.show(block=False)  # similar to interactive mode
        plt.pause(0.00001)

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
        self.__lowpass_filter(10)
        self.__highpass_filter(0.3)
        self.__data_buffer = np.gradient(self.__data_buffer)

    def check_fs(self,time_data, sampling_rate):
        time_data = self.__time_buffer
        diffs = np.diff(time_data)
        avg_diff = np.mean(diffs)
        estimated_fs = 1e3 / avg_diff
        print(estimated_fs,sampling_rate)
        if estimated_fs < sampling_rate:
            print('Warning: Low FS detected! Recollect data with an FS less than %3.2f Hz.' % estimated_fs)
        return estimated_fs

    #(normalized) train data, save to buffers, filter, reshape(-1,1), generate model
    def train(self, train_data):
        gmm = GaussianMixture(n_components=2)
        self.__data_buffer = train_data
        self.__filter_ppg()
        self.__data_buffer = np.array(self.__data_buffer).reshape(-1, 1)
        gmm.fit(self.__data_buffer)  # data has to be (-1,1)
        self._model = gmm
        self.reset()

    #plot new data's histogram
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

    #plot new data's labels
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

    #process the predicted data labels, and determine among those labels how many true heart beat are there
    #return an array of indexes where heart beat is detected.
    def hr_heuristics(self):
        label = {}#label dictionary
        hb_index = []#the indexes of heart beat being detected.

        # determine which is "heartbeat", which is "not heartbeat"
        tags, frequency = np.unique(self.__heuristic__ML_labels, return_counts=True)

        # assume number of not heartbeat is more than heartbeat
        # the larger number is "not heartbeat"
        # the dictionary correspond heartbeat to the label that gmm predicts
        # prevent only one classes got distinguished
        if len(tags) == 1:
            tags = np.append(tags,[1-tags[0]])
            frequency = np.append(frequency,[75-frequency[0]])
        if frequency[0] > frequency[1]:
            label["not heart beat"] = tags[0]
            label["heartbeat"] = tags[1]
        else:
            label["not heart beat"] = tags[1]
            label["heartbeat"] = tags[0]
        if(label["not heart beat"]==1):
            for x in range(len(self.__heuristic__ML_labels)):
                self.__heuristic__ML_labels[x] = 1-self.__heuristic__ML_labels[x]
        # get rid of small peak that is incorrectly labeled by machine learning, then count how many is left.
        # if the peak is higher than a threshold, and also the peak labeled as "heartbeat", we count it

        b, a = sig.butter(2, 2 / (0.5 * 50), btype='lowpass', analog=False,
                          output='ba')  # 1. order of filter, 2.Wn cut off freq
        self.__heuristics_filtered_data = sig.lfilter(b, a, self.__heuristics_filtered_data)


        local_maxes, _ = sig.find_peaks(self.__heuristics_filtered_data, height=[0, 100])
        for x in local_maxes:
            if self.__heuristic__ML_labels[x] == label["heartbeat"] and self.__heuristics_filtered_data[x] > 0 and self.__heuristics_filtered_data[x] < 20:

                hb_index.append(x)

        #offsetting the heartbeat index into global scale, that is, add how many sample it passed, so that
        #for live plotting heart beat, it can correspond to where it's actually at the peak of filter_data
        for i in range(0,len(hb_index)):
            hb_index[i] = hb_index[i] + (self.__num_of_windows-1)*self.__fs*3
        print("num of heartbeat",len(hb_index))
        return len(hb_index)

    #live appending mes_str for live processing
    #seconds： time interval of the window for live processing
    def live_appending(self, msg_str, seconds):
        #number of sample
        length = seconds * self.__fs


        # append to basic time and data buffer, if 75 samples come in, we do a processing
        # live_buffer_index counts how many samples it processed since turning on.
        self.append(msg_str)
        self.__live_buffer_index += 1
        if self.__live_buffer_index % length == 0:
            string = self.live_process(seconds)

            return string
        return ""


    def live_process(self,seconds):
        #keep track of how many time the filtering window is called, because first time the inital
        #condition is different. We need to initialize.
        self.__num_of_windows +=1

        #grab some seconds of data for processing
        ir_portion,time_portion = self.__get_data(seconds)
        self.__total_time.extend(time_portion)

        #generate filter coefficients.
        b_low, a_low = sig.butter(2, 10 / (0.5 * 50), btype="lowpass", analog=False, output='ba')
        b_high, a_high = sig.butter(4, 0.3 / (0.5 * 50), btype="highpass")

        #filter out the raw ir_portion, save it in heuristics data for calculating heartbeats
        # and push the filtered portion for live plotting

        signal_out = self.__filter_initial_condition(ir_portion,self.__low_initial,b_low,a_low,self.__high_initial,b_high,a_high)

        self.__heuristics_filtered_data = signal_out
        self.__push_data(signal_out)

        #use GMM to predict labels, and save it in heuristic ML labels also for calculating heartbeats
        # also save the portion of label to total labels for live plotting
        result = np.array(signal_out).reshape(-1, 1)
        self.__heuristic__ML_labels = self._model.predict(result)
        self.__total_ML_result.extend(self._model.predict(result))

        #get an array of indices of heartbeat.
        # using the indices to locate the time it happens and the peak value of it, for live plotting.
        heartbeat_index = self.hr_heuristics()
        time_value_buffer = []
        #heartbeat_value_buffer = []

        self.__heartbeats.append(heartbeat_index)
        self.__heartbeats_time.extend(time_value_buffer)

        #calculate time, rate.
        beat_num = 0

        if len(self.__total_time)>225:
            time_diff = (self.__total_time[-1]-self.__total_time[-225])/1000
            beat_num = self.__heartbeats[-1]+self.__heartbeats[-2]+self.__heartbeats[-3]
        else:
            time_diff = (self.__total_time[-1] - self.__total_time[0]) / 1000

        print("time diff",time_diff,"beat num",beat_num)
        rate = (beat_num / time_diff) * 60

        string = "HR:" + str(rate)
        return string
    def __get_data(self, seconds):
        time = self.__time_buffer[-1 * (seconds * self.__fs):]
        buffer = self.__data_buffer[-1 * (seconds * self.__fs):]
        return buffer, time

    def __push_data(self, buffer):
        self.__total_filter_result.extend(buffer)


    def __filter_initial_condition(self,buffer,z1_in_low,b_low,a_low,z1_in_high,b_high,a_high):

        signal_in = sig.detrend(buffer)
        #signal_in = self.normalize(signal_in)
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

        signal_out = np.gradient(signal_out)
        return signal_out

    def normalize(self,array):
        max = np.amax(array)
        min = np.amin(array)
        for i in range(0, len(array)):
            array[i] = (array[i] - min) / (max - min)
        return array