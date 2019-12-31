Zihao Kong

A15502295
# **Lab8**
## **Introduction**
Last time we integrate live filtering by filtering window by window on the entire data buffer,
this Lab, we are using the same technique to plot data live.

## **Objective 0** 
1. _In order to fit finger precisely between IR emitter and receiver, we use thermo plastic material to make
 ourselves a finger holder. With receiver and emitter on top and bottom side._

## **Objective 1** 
1. _The goal is to filter every three seconds, but one problem is that the initial condition will be different every time a filter is applied,
so that when they are plotted together, it won't be consistent._
2. _And in order to make the data consistent, we need to keep track of the initial condition. We use it by 
using the function called lfilter_zi(). This function will generate a Z1 that can be used as another input of filters.
3. _We filter every three seconds and then record the initial conditon, used in next filter._
4. _This is the result of live filter_
![Image of live filter](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab8/images/live_filter.png)

## **Objective 2**
1. _For this objective, we take what we have in Objective 1, which is in live_filter.py, we integrate the function into PPG and Pedometer class._
2. _First we add a function called live_appending, with message and how many seconds of buffer as parameter. 
This function takes a new data and appending to our self.data_buffer, but checking for every 75 samples._
3. _If 75 samples are reached, it calls a function called live_process, which takes how many seconds we are processing once as well. In 
this case, it's three. This function process 75 samples with initial conditions taken care._
4. _After processing, the new data is appended to another buffer which records every data since program started. This is for live plotting._
5. _The program then calculates how many steps/heartbeats and execute hueristic function to get rid of wrong peaks._

## **Objective 3**
1. _In this objective, we write a main, getting data from Arduino and process._
2. _We get data that looks like <time>,<IMU>,<IR>; then we call pedometer live append and ppg live append function, the former will ignore ir value and the latter will ignore
IMU value, both start to calculate until 75 data comes in._
3. _After calculating, pedometer.live_append() and ppg.live_append() will return respective result, one is S: <steps> the other is HR: <value>,
then we combine these two strings together, and send to OLED screen via hm10._

## **Objective 4**
1. _For the viberating motor, I make it viberate whenever the machine is turned on or off, so that user will have a response instead of just pressing botton and don't know what's going on._