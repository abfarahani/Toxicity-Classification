import os
import re
from spellchecker import SpellChecker

"""
This function looks through all words in the target training file, applies
spell check to each word, and stores the results in a targetOutputFile -- by
default the target file is data/spellCorrections.txt

install package using:
    $ sudo pip3 install pyspellchecker

"""
def run(targTrainFile, targetOutputFile=""):

    if targetOutputFile == "":
        targetOutputFile = os.path.dirname(os.path.abspath(__file__)) +  \
            "/../data/spellCorrections.txt"
    
    spell = SpellChecker()

    allText = ""

    with open(targTrainFile,mode='r') as input:
        allText = input.read()

    allData = {}

    lines = allText.split("\n")
    for line in lines:
        print(line)
        exit(0)
        if re.search('^,.*$',line):
            continue
        arr = line.split(",")
        word = arr[0]
        if len(word)==0:
            continue
        allData[word] = line

    
    finalOutput = ""
    wordsSeen = 0

    for key in allData:
        wordsSeen += 1
        if re.search('^[\d\.]+$',key):
            continue
        misspelled = spell.unknown([key])
        for word in misspelled:
            trans = spell.correction(word)
            if word == trans:
                # Drop from allData, it's incorrect without replacement
                finalOutput += "del "+word+"\n"
                #print(word)
            elif trans in allData:
                #print(word+" => "+trans)
                finalOutput += key+":"+trans+"\n"
            else:
                #print("Many")
                for option in spell.candidates(word):
                    if option in allData:
                        finalOutput += key+":"+option+"\n"
                        break
        if wordsSeen % 10000 == 0:
            print(wordsSeen)


    with open(targetOutputFile,mode="w") as output:
        output.write(finalOutput)
        output.close()
