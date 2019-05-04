[![Deon badge](https://img.shields.io/badge/ethics%20checklist-deon-brightgreen.svg?style=popout-square)](http://deon.drivendata.org/)

# team-jigsaw-final
CSCI 8360 Final - Kaggle - Jigsaw Unintended Bias in Toxicity Classification

## Team Jigsaw Final

## Member (Ordered by last name alphabetically)
* Abolfazl Farahani (a.farahani@uga.edu)
* Jonathan Myers (submyers@uga.edu)
* Saed Rezayi (saedr@uga.edu)

## Synopsis

This package provides you with tools designed for the Kaggle competition problem Jigsaw Unintended Bias in Toxicity Classification (https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification). While we provide a range of options, the most succesfull results came from Long Sort-Term Memory (LSTM) applied simultaniously to multiple word2vec data sources.

## Outline

This package comes with the following directories, scripts, and files:

* src/ : Directory hold scripts referenced by the main scripts
* doc/ : Directory holds the document we wrote for this project
* data/ : An area used by the Sentiment python processes
* formatData.py : Reformats the data supplied by Kaggle for later compulations
* calcSentiment.py : Takes the formated data and generates files for each word storing sentement values and statistics
* applySentiment.py : Takes the data stored in the "data/" directory and predicts toxicity scores for the test.csv data from Kaggle

## Programs

### Deep Model

We implemented two models namely LSTM and CNN to address the classification task. 

#### Requiremnets

This project requires Python 3.x with `keras`, `sklearn`, `nltk`, `re`, and `bs4` libraries installed.

#### Installation

You can install the jigsaw package using the following command:

`$ pip install --user -i https://test.pypi.org/simple/ jigsaw`

#### Usage

To run the model navigate to the `src/` directory and run the following command:

`$ python train.py -i /path/to/training-set/ -t /path/to/test-set -o /path/to/output -e /path/to/embedding`

List of command line arguments to pass to the program are as follows:

	--input: Path to training set.
	--test: Path to test set.
	--output: Path to submission file.
	--embedding: path to embedding file.
	--text_column: name of the column that contains the text.
	--label_column: name of the column that contains the labels.
	--preprocess: if set the text will be processed.
	--chunk_size: width and height of chunk, two values.
	--overlap: value determining whether to merge.
	--model: the deep neural network model (CNN or LSTM).

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
$ sudo pip3 install spellchecker
```

##### 2 - Format Data

Format data by executing the formatData.py script. By default, the script makes files over several steps and stores them in the "data" direcotry of this package, but you may specify another location. Here are the arguments

```
usage: formatData.py [-h] -train TRAIN -test TEST [-singQuote] [-wd WORKDIR]
```

TRAIN is a path to the Kaggle file train.csv, TEST is a path to the Kaggle file test.csv, singQuote is an option to include single quotes that occur in words (like "we're"), and the WORKDIR is a directory noted in the previous paragraph (default: package directory "data/")

##### 3 - Calculate Sentiment

The script calcSentiment.py applies the Vader package to all comments stored in the train.csv and test.csv files and then generates files under the work directory (see earlier sections on the work directory) for each word in the subdirectories words/ and wordStats/.

```
usage: calcSentiment.py [-h] -train TRAIN -test TEST [-wd WORKDIR]
                        [-singQuote]
```
Train and test data from Kaggle is required, the work directory is optional and has a default value (see previous section), and the single quote is optional (and is False by default).

##### 4 - Predict Toxicity

The script applySentiment.py takes the values calculated and stored in the "data/" directory (or a different directory if one was specified earlier), and applies those values to the test.csv file from Kaggle to generate a submission.csv file for the Kaggle compitition. The script takes the following arguments:

```
usage: applySentiment.py [-h] -test TEST [-wd WORDDIR] [-s0 S0] [-s1 S1]
                         [-s2 S2] -o O [-singQuote]
```

TEST is a path to the Kaggle file test.csv, WORKDIR is a directory noted in the previous sections (default: package directory "data/"), and the values s0, s1, and s2, are constants applied to the application of statistical data to generate predictions (default: .6, .3, and .15 respectively)
