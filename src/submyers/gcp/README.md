### Sentiment 

#### Outline

We looked to sentiment as an initial sentence measurement to expand on the data supplied by Kaggle. Generating the data and evaluating the resulting values entails the following steps, which later sections will cover in greater detail:

1. Retrieve Data, Install Packages
2. Format Data
3. Calculate Sentiment
4. Predict Toxicity

##### 1 - Retrive Data, Install Packages

If you have not already, get the train.csv and test.csv files for the Kaggle competition "Jigsaw Unintended Bias in Toxicity Classification" (https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/data). Once you have the files, install the 
following python packages

```
$ sudo pip3 install vaderSentiment
$ sudo pip3 install keras
$ sudo pip3 install statistics
```

##### 2 - Format Data

Format data by executing the formatData.py script. By default, the script makes files over several steps and stores them in the "data" direcotry of this package, but you may specify another location. Here are the arguments



##### 3 - Calculate Sentiment

##### 4 - Predict Toxicity

