import os
import random
import re
import csv

random.seed(20190421) # The date generated was 2019-04-21

allLines = ""
allWordHash = {}
allWordList = []

# Read in all filtered words
with open("trainWordStatsFilter.csv",mode='r') as input:
	allLines = input.read()
	input.close()

# Store all words in local variables
lines = allLines.split("\n")
for line in lines:
	arr = line.split(",")
	word = arr[0]
	if len(word) == 0:
		continue
	if len(word) > 250:
		continue
	if word not in allWordHash:
		allWordHash[word] = 1
		allWordList.append(word)

allWordList.sort()
with open('wordIdxListFilter.txt',mode='w') as output:
	for i in range(0,len(allWordList)):
		allWordHash[allWordList[i]] = i+1
		output.write(allWordList[i]+","+str(i+1)+"\n")
	output.close()


# Now iterate through the train data to build output lines
outputLines = []
lineCount = 0
with open('train.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:
		if lineCount == 0:
			lineCount += 1
		lineCount += 1

		# Format the text
		row["comment_text"] = re.sub('[^a-zA-Z0-9]+',' ',row["comment_text"])
		row["comment_text"] = re.sub('\s+',' ',row["comment_text"])
		row["comment_text"] = re.sub('^\s+','',row["comment_text"])
		row["comment_text"] = re.sub('\s+$','',row["comment_text"]).lower()

		# Split text into a word array
		arr = row["comment_text"].split(' ')

		# Count each word
		wordCounts = {}
		for j in range(0,len(arr)):
			if arr[j] not in allWordHash:
				continue
			if arr[j] not in wordCounts:
				wordCounts[arr[j]] = 0
			wordCounts[arr[j]] += 1

		# Build a line for the libsvm file
		libsvmLine = ""
		if row["target"] == '0.0':
			libsvmLine = "0"
		else:
			libsvmLine = "1"
		for j in range(0,len(allWordList)):
			if allWordList[j] in wordCounts:
				libsvmLine += " "+str(allWordHash[allWordList[j]])+":"+str(wordCounts[allWordList[j]])
#			else:
#				libsvmLine += " "+str(allWordHash[allWordList[j]])+":0"
#			if allWordList[j] in wordCounts:
#				libsvmLine += " "+allWordList[j]+":"+str(wordCounts[allWordList[j]])
#			else:
#				libsvmLine += " "+allWordList[j]+":0"

		# Put the LibSVM line into an list
		outputLines.append(libsvmLine)

# Generate a list of indexes for the outputLines list
outputIdxs = []
for i in range(0,len(outputLines)):
	outputIdxs.append(i)

# Suffle the index list
random.shuffle(outputIdxs)

# Generate 10 different files for training and testing random forest
for i in range(0,10):
	testLines = ""
	trainLines = ""
	startIdx = int((i*len(outputIdxs))/10)
	endIdx = int(((i+1)*len(outputIdxs))/10)
	for j in range(0,len(outputIdxs)):
		if j >= startIdx and j < endIdx:
			testLines += outputLines[outputIdxs[j]] + "\n"
		else:
			trainLines += outputLines[outputIdxs[j]] + "\n"
	with open("testFilter"+str(i)+".libsvm",mode="w") as test:
		test.write(testLines)
		test.close()
	with open("trainFilter"+str(i)+".libsvm",mode="w") as train:
		train.write(trainLines)
		train.close()

# Write out the whole libsvm
with open("trainFilterAll.libsvm",mode="w") as train:
	train.write("\n".join(outputLines))
	train.close()


#
# Now generate a test libsvm file for evaluation
#
outputLines = []
lineCount = 0
with open('test.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:
		if lineCount == 0:
			lineCount += 1
		lineCount += 1

		# Format the text
		row["comment_text"] = re.sub('[^a-zA-Z0-9]+',' ',row["comment_text"])
		row["comment_text"] = re.sub('\s+',' ',row["comment_text"])
		row["comment_text"] = re.sub('^\s+','',row["comment_text"])
		row["comment_text"] = re.sub('\s+$','',row["comment_text"]).lower()

		# Split text into a word array
		arr = row["comment_text"].split(' ')

		# Count each word
		wordCounts = {}
		for j in range(0,len(arr)):
			if arr[j] not in allWordHash:
				continue
			if arr[j] not in wordCounts:
				wordCounts[arr[j]] = 0
			wordCounts[arr[j]] += 1

		# Build a line for the libsvm file
		libsvmLine = "0"
		for j in range(0,len(allWordList)):
			if allWordList[j] in wordCounts:
				libsvmLine += " "+str(allWordHash[allWordList[j]])+":"+str(wordCounts[allWordList[j]])
#			else:
#				libsvmLine += " "+str(allWordHash[allWordList[j]])+":0"
#			if allWordList[j] in wordCounts:
#				libsvmLine += " "+allWordList[j]+":"+str(wordCounts[allWordList[j]])
#			else:
#				libsvmLine += " "+allWordList[j]+":0"

		# Put the LibSVM line into an list
		outputLines.append(libsvmLine)


with open("testFilterAll.libsvm",mode="w") as train:
	train.write("\n".join(outputLines))
	train.close()
