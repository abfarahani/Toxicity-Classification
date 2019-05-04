from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import math

## LOAD IN ALL SENTENCES ##

trainScores = {}
vaderScores = {}
line_count = 0
worst = 0
worstLine = ""
diffs = []
mean = 0
std = 0
analyzer = SentimentIntensityAnalyzer()

with open('../../../data/train.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        trainScores[row["comment_text"]] = float(row["target"])
        #print(f'{row["id"]}, {row["target"]} => {row["comment_text"]}')
        vs = analyzer.polarity_scores(row["comment_text"])
        vaderScores[row["comment_text"]] = float(vs["neg"])
        diffs.append((trainScores[row["comment_text"]]-vaderScores[row["comment_text"]])**2)
        mean += diffs[line_count-1]
        if( diffs[line_count-1] > worst ):
            worst = diffs[line_count-1] 
            worstLine = f'{row["comment_text"]}\n' + str(vaderScores[row["comment_text"]]) + ',' + str(trainScores[row["comment_text"]]) + ',' + str(worst)
        line_count += 1
        if(line_count > 30000):
            break
    print(f'Processed {line_count} lines.')


print(worstLine)

mean = mean/(line_count-1)

for i in range(0,line_count-1):
    std += (mean-diffs[i])**2

std = std/(line_count-1);
std = math.sqrt(std);

print(str(mean) + ", " + str(std) + ", " + str(line_count))
