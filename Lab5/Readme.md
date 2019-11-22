Zihao Kong

A15502295
# **Lab5**
## **Introduction**
The goal of this lab is sampling and signal processing using python, the best tool for 
analyzing data. We learned how data filtering works in class and applied it using Scipy API.
Drawing graphs and based on graph, use algorithms to find how many steps we walked.

## **Objective 1** 
1. _To effectively analyzing data, We take the L1-Norm of 3 accelerometer data, converting
it to one, so we can draw the data in a single line._
2. _We first complete the Append(), save_file() and plot() functions._
* Append(): read data from hm10 in Arduino, parse it by ";" and by "," then we save the time stamp into array __time_buffer, save data into __data_buffer.
* save_file(): save the content of __time_buffer and __data_buffer into file, divided by","
* load_file(): load the content of given filename, using file.readline, and then parse the data by ",", save it to respective array.
3. _After we have all methods, we collect data from different frequencies, such as 0.1Hz, 2Hz, 5Hz, 100Hz._
* The ovservation is that when frequency is very low, it's hard to represent data because the interval between data points is long, and during these 
time, several steps might be passed already. And it doesn't work for very high frequency as well because Arduino might lose data during communication,
for example, time stamp should be 11124512, but only 11245 is sent, so it will cause data points to behave weird.
4. _Here is a picture._
![2Hz data points](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab5/Objective1/IMU_sampling_2Hz.png?raw=true)

## **Objective 2**
1. _We learn filtering and apply it using Scipy._
2. _We first finish lowpass_filter(), highpass_filter(), smoothing_filter() and demeaning_filter(), these four filters are helpful
for us to process data and get what we wanted._
3. _Then we test each filter, taking pictures of data after filtering._
4. _This is a sample picture of lowpass filter with cutoff frequency of 0.1Hz._
![Image of cutoff frequency 0.1Hz](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab5/images/IMU_filtered_LPF0.1.PNG?raw=true)

## **Objective 3**
1. _We integrated filters we made in objective 2 and use method to process data and find number of steps._
* The order of these filters are: 1. Demean, 2. Moving Average, 3. take gradient, 4. Lowpass filter.
2. _We plot raw data before and processed data after. Then count the peaks of processed data, as it's going to be the actual steps we take._

## **Objective 4**
1. _We use low threshold 100 and upper threshold 4000 to detect the peak, if a peak point is between these two values, we count this as a step._
2. _For later part of the lab, I can't figure Why my OLED is not working, So I still need to work on it in class, asking teachers._

