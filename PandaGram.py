import pandas as pd
from collections import Counter
import math
import os
import glob
from utility import deaccent

theText = ''
path = '/home/chris/PycharmProjects/learn/Texts/'
for filename in glob.glob(os.path.join(path, '*.txt')):
    newText = open(filename).read()
    theText = theText + newText
# Combines every text file in the Text folder into a single
# string "theText".

plainText = deaccent(theText)
wordList = plainText.lower().split()
wordCounter = Counter()
bigramList = []
bigramCounter = Counter()
bigramDic = {}

for word in wordList:
    wordCounter[word] += 1
# Adds every unique word in wordList to a counter
# object with corresponding frequency.

i = 0
minGram = 12
listLength = len(wordList)
while i < listLength - 1:
    thegram = wordList[i] + '-' + wordList[i+1]
    bigramList.append(thegram)
    bigramCounter[thegram] +=1
    if bigramCounter[thegram] > minGram:
        freq1 = wordCounter[wordList[i]]
        freq2 = wordCounter[wordList[i+1]]
        biFreq = bigramCounter[thegram]
        perc1 = bigramCounter[thegram]/wordCounter[wordList[i]]
        perc2 = bigramCounter[thegram]/wordCounter[wordList[i+1]]
        pmiCalc = math.log(biFreq*(listLength-1)/
                           (freq1*freq2),2)
        bigramDic[thegram] = [freq1, freq2, biFreq, perc1, perc2, pmiCalc]

    i += 1
# Simultaneously creates bigramList of every bigram occurrence
# in the form "wordone-wordtwo" while also making the Counter
# object bigramCounter. Then it creates the dictionary object
# bigramDic with values (frequency of each gram and PMI score)
# for each key (the bigram).

df = pd.DataFrame.from_items(bigramDic.items(), orient='index',
                             columns=['Freq1','Freq2','BiFreq','Perc1','Perc2','PMI'])
# Formats the data the way we want.

print("There are", len(bigramList), "bigrams.")
print("There are", len(bigramCounter), "unique bigrams.")
print(len(bigramDic), "of them occurred", minGram, "times or more.")

outname = 'NTGram.csv'
outdir = '/home/chris/Desktop'
outpath = os.path.join(outdir, outname)
df.to_csv(outpath)
