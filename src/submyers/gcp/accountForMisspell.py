import os
import re
from spellchecker import SpellChecker

spell = SpellChecker()

allText = ""

with open("trainWordStatsFilter.csv",mode='r') as input:
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

#print(str(len(allData)))
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


with open("spellCorrections.txt",mode="w") as output:
	output.write(finalOutput)
	output.close()
