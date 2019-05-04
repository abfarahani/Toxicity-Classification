import os
import re
import csv

import argparse

"""
This function looks at stats in all the word files, the sentiment calculations
generated in the previous process step, and uses those values to predict
toxic scores using statistics and limits provided by the user
"""
def main(args):
    
    wordStats = {}
    
    # Read in statistical informatio for every word targeted
    dirlist = os.listdir(args.wordDir+"/wordStats")
    for file in dirlist:
    	word = re.sub(r"^([^\.]+)\.stats.csv",r"\1",file)
    	wordStats[word] = {}
    	allLines = ""
    	with open("wordStats/"+file,mode="r") as input:
    		allLines = input.read()
    	lines = allLines.split("\n")
    	for line in lines:
    		arr = line.split(",")
    		if len(arr) == 0:
    			continue
    		wordStats[word][arr[0]] = {}
    		wordStats[word][arr[0]]["count"] = arr[1]
    		wordStats[word][arr[0]]["mean"] = arr[2]
    		wordStats[word][arr[0]]["median"] = arr[3]
    		wordStats[word][arr[0]]["std"] = arr[4]
    		wordStats[word][arr[0]]["skew"] = arr[5]
    		wordStats[word][arr[0]]["mode"] = arr[6]
    
    trainSent = {}
    testSent = {}
    allLines = ""
    
    # Define the train sentament
    with open(args.wordDir+"/trainSentament.csv",mode="r") as input:
    	allLines = input.read()
    lines = allLines.split("\n")
    for line in lines:
    	arr = line.split(",")
    	if len(arr) < 5:
    		continue
    	trainSent[arr[0]] = arr[4]
    
    # Define the test sentament
    allLines = ""
    with open(args.wordDir+"/testSentament.csv",mode="r") as input:
    	allLines = input.read()
    lines = allLines.split("\n")
    for line in lines:
    	arr = line.split(",")
    	if len(arr) < 5:
    		continue
    	testSent[arr[0]] = arr[4]
    
    
    lineCount = 0
    #
    # Now iterate through each of the comments in test, look at the statistics
    # and limits to determine predictions and write those to the output
    #
    with open(args.o, mode='w') as output:
        output.write('id,prediction\n')
        with open(args.test, mode='r') as csv_file:
            	csv_reader = csv.DictReader(csv_file)
            	for row in csv_reader:
            		if lineCount == 0:
            			lineCount += 1
            		lineCount += 1
            		row["comment_text"] = re.sub('[^a-zA-Z0-9]+',' ',\
                         row["comment_text"])
            		row["comment_text"] = re.sub('\s+',' ',row["comment_text"])
            		row["comment_text"] = re.sub('^\s+','',row["comment_text"])
            		row["comment_text"] = re.sub('\s+$','',row["comment_text"])\
                    .lower()
            		arr = row["comment_text"].split(' ')
            		score = 0
            		words = []
            		counts = []
            		means = []
            		medians = []
            		stds = []
            		modes = []
            		skews = []
            		sent = str(round(float(testSent[row["id"]]),1))
            		if sent == "0.0":
            			sent = "-0.0"
            		for j in range(0,len(arr)):
            			word = arr[j]
            			words.append(word)
            			if word in wordStats \
            				and sent in wordStats[word] \
            				and int(wordStats[word][sent]["count"]) > 1 \
            				and float(wordStats[word][sent]["skew"]) < args.s0:
            				counts.append(float(wordStats[word][sent]["count"]))
            				means.append(float(wordStats[word][sent]["mean"]))
            				medians.append(float(wordStats[word][sent]["median"]))
            				stds.append(float(wordStats[word][sent]["std"]))
            				modes.append(float(wordStats[word][sent]["mode"]))
            				skews.append(float(wordStats[word][sent]["skew"]))
            		if len(stds) > 0:
            			maxStd = max(stds)
            			if maxStd == 0:
            				output.write(row["id"] + "," + str(score)+"\n")
            				continue
            			stdSum = 0
            			modStds = []
            			for j in range(0,len(stds)):
            				modStds.append(maxStd-stds[j])
            				stdSum += maxStd-stds[j]
            			if stdSum == 0:
            				output.write(row["id"] + "," + str(score)+"\n")
            				continue
            			for j in range(0,len(stds)):
            				if skews[j] <= args.s2:
            					score += ((maxStd-stds[j])/stdSum)*means[j]
            				elif skews[j] <= args.s1:
            					score += ((maxStd-stds[j])/stdSum)*medians[j]
            				else:
            					score += ((maxStd-stds[j])/stdSum)*modes[j]
            			output.write(row["id"] + "," + str(score)+"\n")
            		else:
            			output.write(row["id"] + "," + str(score)+"\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='These are the arguments '\
        + 'for formating Kaggle competition Jigsaw Unintended Bias in '\
        + 'Toxicity Classification data before applying sentament anylysis '\
        + 'to data')

    parser.add_argument('-test','--test',required=True,\
        help="Define the path to the test file provided by the Kaggle "\
        +'competition')

    parser.add_argument('-wd','--wordDir',required=False,\
        default=os.path.dirname(os.path.realpath(__file__))+"../data",\
        help="DPath to work directory used during the execution of previous "\
        + "steps in sentiment process")

    parser.add_argument('-s0','--s0',required=False,type=float,default=.6,\
        help="Any results with skew value greater than this will be ignored "\
        +"- default = 0.6")

    parser.add_argument('-s1','--s1',required=False,type=float,default=.3,\
        help="Any results with skew value in range [s1,s0) use mode for "\
        +"part of contribution for prediction - default = 0.3")

    parser.add_argument('-s2','--s2',required=False,type=float,default=.15,\
        help="Any results with skew value in range [s2,s1) use median for "\
        +"part of contribution for prediction and results with skew in range "\
        +" [0,s2) use mean - default = 0.15")

    parser.add_arguments('-o','--o',required=True,help='Define the output '\
        +"file to store all predictions"
        )

    parser.add_argument('-singQuote','--singQuite',required=False,\
                        action='store_true',default=False, help="Use results "\
                        + "that included single quotes in words.")

    args = parser.parse_args()
    
    main(args)