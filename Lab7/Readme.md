Zihao Kong

A15502295
# **Lab7**
## **Introduction**
The goal of this lab is to use machine learning instead of thresholding to find peaks.

## **Objective 1** 
1. _In order to implement machine learning, we need to have massive data collection process._
2. _And in order to make the data consistent, we need to collect 25HZ sampling rate data._
3. _Every one has five data, we have around 45 pieces we could use._
4. _Because the data is still not much, we use cross validation process._

## **Objective 2**
1. _For this objective, we use GMM model to classify two types of signal, one is peak and one is not peak._
2. _It's unsupervised learning, so label 1 could be peak sometimes, and some times 0 is the peak._
3. _We count how many time a data that is between 0 to 1 appear in all data points, generatiing a gaussian pdf. We can classify data based on those PDFs._
4. _This is a picture of two Gaussian curves histgram._
![Image of Heartbeat python live](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab7/images/hist_individual_JM.png)
6. _After around 10 second, we save our data into a CSV, then we use Plot function from pedometer, to plot the graph, it should look like the same as last picture._

## **Objective 3**
1. _In this task, we are inplementing GMM into our ppg class, create API for people to use._
2. _We create a new attribute called __Model, in order to save our pretrained model._
3. _We divide 9 folder into 3 sets, one is training sets, one is validating sets and one is testing sets._
4. _Training sets is for training models, we use validating and testing sets to test results_
![Picture of testing sets precision](https://github.com/UCSD-Product-Engineering/ece16-fa19-Zihaokong/blob/master/Lab7/images/test_label.png)


## **Objective 4** 
1. _For this objective, we are minimize the error caused by machine learning. We use algorithms to determine which "heartbeat" is fake based on it's length._
2. _After that, we use 30 seconds of new data to test our result._
3. _to process the new data, we need to normalize it, filter it to use. It turns out very good._
