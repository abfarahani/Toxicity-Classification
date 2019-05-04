from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import re
import os

"""
This function will calculate the sentiment values for each comment in the
training and testing files using vader and store the results into 
files referenced later
"""
def run(testCsvFile,trainCsvFile,testSentimentFile,trainSentimentFile,\
        singQuote, workDir):    
    words = {}

    lineCount = 0;
    
    analyzer = SentimentIntensityAnalyzer()
    
    allOutput = "";
    with open(testCsvFile, mode='r') as csv_file:
    	csv_reader = csv.DictReader(csv_file)
    	for row in csv_reader:
    		if lineCount == 0:
    			lineCount += 1
    		lineCount += 1
    		vs = analyzer.polarity_scores(row["comment_text"])
    		allOutput += str(row["id"])+','+str(vs["neg"])+','+\
            str(vs["neu"])+','+str(vs["pos"])+','+str(vs["compound"])+"\n"
    
    with open(testSentimentFile,"w") as output:
    	output.write(allOutput)
    
    allOutput = "";
    with open(trainCsvFile, mode='r') as csv_file:
    	csv_reader = csv.DictReader(csv_file)
    	for row in csv_reader:
    		if lineCount == 0:
    			lineCount += 1
    		lineCount += 1
    		vs = analyzer.polarity_scores(row["comment_text"])
    		allOutput += str(row["id"])+','+str(vs["neg"])+','\
                +str(vs["neu"])+','+str(vs["pos"])+','+str(vs["compound"])+"\n"
    		if singQuote:
    			row["comment_text"] = re.sub('[^a-zA-Z0-9\']+',' ', \
                     row["comment_text"])
    		else:
    			row["comment_text"] = re.sub('[^a-zA-Z0-9]+',' ', \
                     row["comment_text"])
    		row["comment_text"] = re.sub('\s+',' ',row["comment_text"])
    		row["comment_text"] = re.sub('^\s+','',row["comment_text"])
    		row["comment_text"] = re.sub('\s+$','',row["comment_text"]).lower()
    		arr = row["comment_text"].split(' ')
    		for j in range(0,len(arr)):
    			if not re.search("^\w+'\w+$",arr[j]):
    				continue
    			if re.search("^\w+'\w+$",arr[j]) and arr[j] not in words:
    				print(arr[j])
    			if arr[j] not in words:
    				words[arr[j]] = ""
    			words[arr[j]] += str(row["id"])+','+str(row["target"])+','\
                    +str(vs["neg"])+','\
                    +str(vs["neu"])+','+str(vs["pos"])+','\
                    +str(vs["compound"])+"\n"
            
    
    with open(trainSentimentFile,"w") as output:
    	output.write(allOutput)

    if not os.exists(workDir+"/words"):
        os.system("mkdir " + workDir+"/words")
    with open(workDir+"/wordsList.txt",mode="w") as wordListFile:
        for word in words:
            wordListFile.write(word+"\n")
            with open(workDir+"/words/"+word+".csv") as output:
                output.write(words[word])
