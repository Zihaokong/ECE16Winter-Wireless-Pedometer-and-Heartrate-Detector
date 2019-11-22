Zihao Kong

A15502295
# **Lab6**
## **Introduction**
The goal of this lab is to install IR receiver and emitter so we can integrate heart rate detecting function to our wearable. After we integrate IR receiver and emitter,
we need to implement similar band pass filter and gradient technique to filter our data and count heartbeats similar to count steps.

## **Objective 1** 
1. _For the background, We use infrared light to measure how much blood flow through our fingertip in time, thus we can detect a heartbeat._
2. _Following the circuit diagram, we install out IR receiver and emitter on board._
3. _We use Analog pin1 to read analog signal and transfer to number between 1 to 1023._
4. _We put our finger on top of the receiver and emitter, receiving a signal that goes up and down consistently._
5. _Here is a picture._
![Image of plotting Heartbeat signal](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab6/images/HeartbeatsArduino.jpg)

## **Objective 2**
1. _For this objective, we are building a python class called PPG, it includes every function
needed for this Lab._
2. _First we change the Arduino code, letting it send <timestamp>,<L1>,<IR data>._
3. _Second, we copy the save, load, plot, and append function from pedometer to PPG, 
we edit the append function, parse the data into three categories, and save the last one into our
data buffer._
4. _We then complete the plot_live function, so that for every 10 frame, instead of waiting for buffer to complete, we can plot live data as buffer is updated._
5. _This is a picture of Live Plot._
![Image of Heartbeat python live](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab6/images/HeartbeatsPythonLive.jpg)
6. _After around 10 second, we save our data into a CSV, then we use Plot function from pedometer, to plot the graph, it should look like the same as last picture._

## **Objective 3**
1. _This task involves filtering data, similar to what was done in Lab 5._
2. _We first collect 5 pieces of total 150s of data from five different trials._
3. _And then we use low pass, high pass, demean, and gradient to process our data, untill we
clearly see data with consisten peaks. We need to play around with parameters of those functions._
4. _We record each result of using one filter, taking pictures to record progress._
![Picture of Using demean filter](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab6/images/PPG1dm.png)
![Picture of Using low pass filter](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab6/images/PPG1lp.png)
![Picture of Using high pass filter](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab6/images/PPG1hp.png)
![Picture of Using gradient](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab6/images/PPG1grad.png)

## **Objective 4** 
1. _For this objective, we use find peak function and take a low threshold of 0 and high threshold of 100 to find our peaks._
2. _After find them, we store the index of where the peaks are at, storing them into "Heartbeats" array, and use plot() to draw them on the graph._
![Picture of Final offline detection result](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab6/images/Heartbeats.png)

## **Objective 5**
1. _For this objective, we simulate online heartbeat detection by taking a small piece of buffer, processing it first, and save it to another array called "Filtered data"._
2. _After slicing the databuffer and finish, we plot them altogether._
3. _The result will vary a little bit because for small portion of data, those filters we use might produce different output because the wave is essentially different, so small variation is not strange._
