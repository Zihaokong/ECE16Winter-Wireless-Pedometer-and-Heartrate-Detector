
import os
import glob
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from scipy.stats import norm
from scipy import signal as sig
def check_fs(time_data, sampling_rate):
    diffs = np.diff(time_data)
    avg_diff = np.mean(diffs)
    estimated_fs = 1e3 / avg_diff
    print(estimated_fs,sampling_rate)
    if estimated_fs < sampling_rate:
        print('Warning: Low FS detected! Recollect data with an FS less than %3.2f Hz.' % estimated_fs)
    return estimated_fs

def load_file(sample_rate, path, validation_name):
    names = glob.glob(path+"*")
    gmm_validate_t = []
    gmm_validate_ir = []

    gmm_training_t = []
    gmm_training_ir = []
    i = 0
    for x in names:
        a,x = x.split("\\")
        names[i] = x
        i+=1
    v_loc = names.index(validation_name)

    #delete validation name in the name sets, process data in validation name folder into validation set
    names.pop(v_loc)
    location = path + validation_name
    validation_sets = os.listdir(path+validation_name)
    offset_value = 0
    for x in validation_sets:
        dest = location +"/"+ x
        validate_t, validate_ir= read_file(dest)
        check_fs(validate_t,sample_rate)
        for i in range(0,len(validate_t)):
            validate_t[i] = validate_t[i] + offset_value

        gmm_validate_t.extend(validate_t)
        offset_value = gmm_validate_t[-1]
        gmm_validate_ir.extend(validate_ir)

    #for the rest, load data
    offset_value = 0
    for i in range(len(names)):
        names[i] = path+names[i]

        training_sets = os.listdir(names[i])

        for j in range(len(training_sets)):
            dest = names[i] + "/" + training_sets[j]
            training_t, training_ir = read_file(dest)
            check_fs(training_t,sample_rate)

            for k in range(0, len(training_t)):
                training_t[k] = training_t[k] + offset_value

            gmm_training_t.extend(training_t)
            offset_value = gmm_training_t[-1]
            gmm_training_ir.extend(training_ir)
    return gmm_validate_t,gmm_validate_ir,gmm_training_t,gmm_training_ir

def read_file(path):
    t_array = []
    ir_array = []
    with open(path) as file:
        t_array = []
        ir_array = []
        while 1:
            text = file.readline()
            if text == "":
                break
            else:
                t,ir = text.strip().split(",")
                t_array.append(int(t))
                ir_array.append(int(ir))
    ir_array = normalize(ir_array)
    t_array = offset_time(t_array)
    return t_array, ir_array

def normalize(array):
    max = np.amax(array)
    min = np.amin(array)
    for i in range(0,len(array)):
        array[i] = (array[i] - min)/(max - min)
    return array

def offset_time(array):
    offset = array[0]
    for i in range(0,len(array)):
        array[i] = array[i] - offset
    return array


def plot(x,y):

    max = np.amax(y)

    min = np.amin(y)

    plt.xlim(x[0], x[-1])
    plt.ylim(min,max)
    plt.plot(x,y)
    plt.show()
    return


def lowpass_filter(signal,cutoff):  # __ makes this a private method
    b, a = sig.butter(2, cutoff/(0.5*50), btype='lowpass', analog=False,output='ba')  # 1. order of filter, 2.Wn cut off freq

    signal = sig.lfilter(b,a,signal)
    return signal

def highpass_filter(signal, cutoff):  # __ makes this a private method
    b, a = sig.butter(4, cutoff/(0.5*50), 'highpass', analog=False)
    signal = sig.lfilter(b, a, signal)
    return signal

def smoothing_filter(signal, N):
    M = N+1
    filter = sig.boxcar(M)
    signal = sig.lfilter(filter/M,1,signal)
    return signal

def demean_filter(signal):
    # Compute the mean using a sliding window
    filtered = sig.detrend(signal)
    signal = filtered
    return signal

def filter_ppg(signal):
    signal = demean_filter(signal)
    signal = lowpass_filter(signal,15)
    signal = highpass_filter(signal,0.9)
    #signal = np.gradient(signal)
    return signal

# gmm_validate_t, gmm_validate_ir, gmm_training_t, gmm_training_ir = load_file(25,"../HR Data/",validation_name="LF")
# gmm_training_ir = filter_ppg(gmm_training_ir)
# gmm_validate_ir = filter_ppg(gmm_validate_ir)
#
# #plt.hist(gmm_training_ir,bins = "auto",density=True)
# plt.show()
#
# gmm = GaussianMixture(n_components=2)
# gmm_training_ir = np.array(gmm_training_ir).reshape(-1,1)
# gmm_validate_ir = np.array(gmm_validate_ir).reshape(-1,1)
# gmm.fit(gmm_training_ir)#data has to be (-1,1)
# mu1 = gmm.means_[0, 0]
# mu2 = gmm.means_[1, 0]
# var1, var2 = gmm.covariances_
# wgt1, wgt2 = gmm.weights_
#
#
# x = np.linspace(np.min(gmm_training_ir),np.max(gmm_training_ir),num = 1000).reshape([1000,1])
# plt.hist(gmm_training_ir,bins = "auto",density=True)
# plt.plot(x,wgt1*norm.pdf(x, mu1, np.sqrt(var1)))
# plt.plot(x,wgt2*norm.pdf(x, mu2, np.sqrt(var2)))
#
# #plot sum
# #plt.plot(x,wgt1*norm.pdf(x, mu1, np.sqrt(var1))+wgt2*norm.pdf(x, mu2, np.sqrt(var2)))
#
#
# plt.tight_layout()
# plt.xlabel("PPG reading")
# plt.ylabel("Count number")
# plt.title("IR Signal Histogram")
# plt.show()
#
#
# #plot validate data
# # results = gmm.predict(gmm_validate_ir)
# # plt.plot(gmm_validate_t,results)
# # plt.plot(gmm_validate_t,gmm_validate_ir)
# # plt.show()
#
#
# #plot training data
# # results = gmm.predict(gmm_training_ir)
# # plt.plot(gmm_training_t,results)
# # plt.plot(gmm_training_t,gmm_training_ir)
# # plt.show()