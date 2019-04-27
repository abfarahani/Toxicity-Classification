import csv
import statistics
import re

words = {}
allWords = []
lineCount = 0

with open('../train.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:
		if lineCount == 0:
			lineCount += 1
		if lineCount % 10000 == 0:
			print(str(lineCount)+"\n")
		row["comment_text"] = re.sub('[^a-zA-Z0-9]+',' ',row["comment_text"])
		row["comment_text"] = re.sub('\s+',' ',row["comment_text"])
		row["comment_text"] = re.sub('^\s+','',row["comment_text"])
		row["comment_text"] = re.sub('\s+$','',row["comment_text"]).lower()
		arr = row["comment_text"].split(' ')
		for j in range(0,len(arr)):
			if arr[j] not in words:
				words[arr[j]] = []
				allWords.append(arr[j])
			words[arr[j]].append(float(row["target"]))
		lineCount += 1

allWords.sort()
with open("trainWordStats.csv",mode="w") as output:
	for i in range(0,len(allWords)):
		word = allWords[i]
		if len(word)==0:
			continue
		if len(words[word]) > 1:
			output.write(word+','+str(len(words[word]))+','+str(statistics.mean(words[word]))+","+str(statistics.median(words[word]))+","+str(statistics.stdev(words[word])))
			words[word].sort()
			counts = {}
			idxs = []
			for toxic in words[word]:
				if toxic not in counts:
					counts[toxic] = 0
					idxs.append(toxic)
				counts[toxic] += 1
			idxs.sort()
			line = ""
			for j in range(0,len(idxs)):
				line += ","+str(idxs[j])+":"+str(counts[idxs[j]])
			output.write(line+"\n")
		if( (i+1) % 10000 == 0 ):
			print(str(i))
output.close()
