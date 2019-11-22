Zihao Kong

A15502295
# **Lab4**
## **Introduction**
The goal of this lab is to keep build connection between computer and Arduino, and do more 
advanced communication.

## **Objective 1** 
1. _We built a crude BLE “handshaking” protocol to connect our two HM-10’s. So everytime 
we run the python, the laptop BLE module will be set and ready to connect._
2. _The BLEs start to "handshake" is when laptop send "AT+NAME?" and Arduino will send "#"
once it detects the "A" and "T"_
3. _We download the program outline from the website and completed several functions based on instructions_
4. _The functions are:_
* connect
* check_connection
* read
* read_line
* read_lines

## **Objective 2**
1. _After we build BLE handshake, we need to connect IMU to the board as well, because we need to send the gyro data to Computer's side to plot.
we are also implementing a button for switch the BLE to sleep mode when we are not using it_
2. _To do so, we use the function called toggleSleep() and attachInterrupt() _

## **Objective 3**
1. _Basically, this objective is for laptop to gather 10 seconds of data and use Python's IO
to save them into a txt file_
2. _We first use hm10.readline to get a single of line of gx,gy,gz_
3. _We then use Open(name, "w") to write specific things to the file._

## **Objective 4**
1. _After we have a txt file contain 500 set of gyro values, we want to use them to plot on 
matplotlib._
2. _We firstly have a function that has two mode, one is read runtime data from the BLE, and plot 500 of them on the graph,
the other one is read from an existed file, plot them on matplotlib._
3. _We use subplot in order to plot three graphs into one single tab._