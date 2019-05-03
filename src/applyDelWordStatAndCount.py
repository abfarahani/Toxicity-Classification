import os
import re

"""
This function looks at the output file generated from running the spell
correction process and removes all words for which the spell checker could
not find a rational alternative spelling
"""
def run(spellCorrectFiles="",testWordInputFile ="",trainWordInputFile="", \
        testWordOutputFile="", trainWordOutputFile=""):
    removeList = []
    allLines = ""
    
    if spellCorrectFiles == "":
        spellCorrectFiles = os.path.dirname(os.path.abspath(__file__)) +  \
            "/../data/spellCorrections.txt"
    if trainWordInputFile == "":
        trainWordInputFile = os.path.dirname(os.path.abspath(__file__)) +  \
            "/../data/trainWordStatsFilter.csv"
    if testWordInputFile == "":
        testWordInputFile = os.path.dirname(os.path.abspath(__file__)) +  \
            "/../data/testWordCountsFilter.csv"
    if trainWordOutputFile == "":
        trainWordOutputFile = os.path.dirname(os.path.abspath(__file__)) +  \
            "/../data/trainWordStatsFilterDel.csv"
    if testWordOutputFile == "":
        testWordOutputFile = os.path.dirname(os.path.abspath(__file__)) +  \
            "/../data/testWordCountsFilterDel.csv"
    
    with open(spellCorrectFiles,mode="r") as input:
    	allLines = input.read()
    
    lines = allLines.split("\n")
    for line in lines:
    	if re.search("^del\s+.*$",line):
    		line = re.sub("^del\s+","",line)
    		removeList.append(line)
    
    # Now remove those words from the train and test files
    outputLines = ""
    with open(trainWordInputFile,mode="r") as input:
            allLines = input.read()
    lines = allLines.split("\n")
    for line in lines:
            word = line
            word = re.sub("^(\w+),.*$",r"\1",line)
            if word not in removeList:
                    outputLines += line + "\n"
    with open(trainWordOutputFile,mode="w") as output:
            output.write(outputLines)
    
    outputLines = ""
    with open(testWordInputFile,mode="r") as input:
            allLines = input.read()
    lines = allLines.split("\n")
    for line in lines:
            word = line
            word = re.sub("^(\w+),.*$",r"\1",line)
            if word not in removeList:
                    outputLines += line + "\n"
    with open(testWordOutputFile,mode="w") as output:
            output.write(outputLines)
