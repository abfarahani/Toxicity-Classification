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
* applySentiment.py : Takes the data stored in the "data/" directory and predicts toxicity scores for the test.csv data from Kaggle
