import statistics
import os
from scipy.stats import skew, mode

"""
This script reads in a list of all words and generates a file for each word in
subdirectories of a target directory:
    words
and then calculates all the statistics for each word and generates a file
storing the statistics calculated in the direcotry:
    wordStats
This script will make the directory if needed.
"""
def run(workDir):
    allLines = ""
    with open(workDir+"/wordsList.txt",mode="r") as input:
    	allLines = input.read()
    
    allWords = allLines.split("\n")
    
    if not os.path.exists(workDir+"/wordStats"):
        os.system('mkdir '+workDir+"/wordStats")
    
    for word in allWords:
    	if len(word) == 0 or len(word) > 250:
    		continue
    	if not os.path.exists(workDir+"/words/"+word+".csv"):
    		continue
    	with open(workDir+"/words/"+word+".csv",mode="r") as input:
    		allLines = input.read()
    
    	lines = allLines.split("\n")
    	scoreHash = {}
    	scoreArr = []
    	for line in lines:
    		arr = line.split(",")
    		if len(arr) != 6:
    			continue
    		if float(arr[1]) == 0:
    			continue
    		if arr[5] not in scoreHash:
    			scoreHash[float(arr[5])] = []
    			scoreArr.append(float(arr[5]))
    		scoreHash[float(arr[5])].append(float(arr[1]))
    
    	scoreArr.sort()
    	targets = []
    	set = []
    	i = -1.0
    	allOutput = []
    	while i < 1:
    		targets = []
    		set = []
    		for j in range(0,len(scoreArr)):
    			if scoreArr[j] >= i-0.05 and scoreArr[j] < i+0.05:
    				targets.append(scoreArr[j])
    		for j in range(0,len(targets)):
    			for k in range(0,len(scoreHash[targets[j]])):
    				set.append(scoreHash[targets[j]][k])
    		if len(set) == 0:
    			allOutput.append(str(round(i,1))+",0,0,0,0,0,0")
    		elif len(set) == 1:
    			allOutput.append(str(round(i,1))+","+str(len(set))
    				+","+str(statistics.mean(set))
    				+","+str(statistics.median(set))
    				+",0,0,"+str(statistics.mode(set)))
    		else:
    			modeVals = mode(set)
    			modeVal = max(modeVals.mode)
    			allOutput.append(str(round(i,1))+","+str(len(set))
    				+","+str(statistics.mean(set))
    				+","+str(statistics.median(set))
    				+","+str(statistics.stdev(set))
    				+","+str(skew(set))
    				+","+str(modeVal) )
    		i += 0.1
    	with open(workDir+"/wordStats/"+word+".stats.csv",mode="w") as output:
    		output.write("\n".join(allOutput))
