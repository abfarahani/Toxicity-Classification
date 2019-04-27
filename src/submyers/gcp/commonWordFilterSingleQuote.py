import os
import re

testLines = {}
trainLines = {}
bothSets = {}

commonWords = []

fileContent = ""

# Initially mark the existance of each test word
with open("testWordCountsSingQuote.csv",mode='r') as input:
	fileContent = input.read()

lines = fileContent.split("\n")
for line in lines:
	if re.search("^,.*$",line):
		continue
	word = re.sub("^([\w\']+),.*$",r"\1",line)
	if len(word) == 0:
		continue
	if len(word) > 250:
		continue
	if word not in bothSets:
		bothSets[word] = 1
		testLines[word] = line

# Now increment the existance of each train word
fileContent = ""
with open("trainWordStatsSingQuote.csv",mode='r') as input:
	fileContent = input.read()

lines = fileContent.split("\n")
for line in lines:
	if re.search("^,.*$",line):
		continue
	word = re.sub("^([\w\']+),.*$",r"\1",line)
	if len(word) == 0:
		continue
	if len(word) > 250:
		continue
	if word in bothSets:
		bothSets[word] = 2
		trainLines[word] = line

# Determine all words common
for word in bothSets:
	if bothSets[word] == 2:
		commonWords.append(word)

commonWords.sort()

# Write out filtered files
with open("testWordCountsFilterSingQuote.csv",mode="w") as testOutput:
	with open("trainWordStatsFilterSingQuote.csv",mode="w") as trainOutput:
		testOut = ""
		trainOut = ""
		for word in commonWords:
			testOut += testLines[word] + "\n"
			trainOut += trainLines[word] + "\n"
		testOutput.write(testOut)
		trainOutput.write(trainOut)
		trainOutput.close()
	testOutput.close()





