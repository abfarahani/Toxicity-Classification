import os
import re

removeList = []
allLines = ""

with open("spellCorrections.txt",mode="r") as input:
	allLines = input.read()

lines = allLines.split("\n")
for line in lines:
	if re.search("^del\s+.*$",line):
		line = re.sub("^del\s+","",line)
		removeList.append(line)

# Now remove those words from the train and test files
outputLines = ""
with open("trainWordStatsFilter.csv",mode="r") as input:
        allLines = input.read()
lines = allLines.split("\n")
for line in lines:
        word = line
        word = re.sub("^(\w+),.*$",r"\1",line)
        if word not in removeList:
                outputLines += line + "\n"
with open("trainWordStatsFilterDel.csv",mode="w") as output:
        output.write(outputLines)

outputLines = ""
with open("testWordCountsFilter.csv",mode="r") as input:
        allLines = input.read()
lines = allLines.split("\n")
for line in lines:
        word = line
        word = re.sub("^(\w+),.*$",r"\1",line)
        if word not in removeList:
                outputLines += line + "\n"
with open("testWordCountsFilterDel.csv",mode="w") as output:
        output.write(outputLines)
