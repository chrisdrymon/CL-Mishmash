import xml.etree.ElementTree as ET
import os
from collections import Counter

os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')
punctuationCounter = Counter()
periodWords = []
wordDict = {}

# This will create a dictionary matching old ID's to their new ones. Then it will assign the new ID.
for file_name in indir:
    i = 1
    if not file_name == 'README.md' and not file_name == '.git':
        print(file_name)
        tb = ET.parse(file_name)
        tbroot = tb.getroot()
        if tbroot.tag == 'treebank':
            for body in tbroot:
                for sentence in body:
                    for word in sentence:
                        if word.tag == 'word':
                            sentenceID = str(sentence.get('id'))
                            wordID = str(word.get('id'))
                            sentWordID = str(sentenceID + '-' + wordID)
                            wordDict[sentWordID] = i
                            word.set('id', str(i))
                            i += 1

# This will assign new head ID's that are in accordance with the new numbering system.
            for body in tbroot:
                for sentence in body:
                    for word in sentence:
                        if word.tag == 'word':
                            sentenceID = str(sentence.get('id'))
                            headID = str(word.get('head'))
                            sentHeadID = str(sentenceID + '-' + headID)
                            if sentHeadID in wordDict:
                                newHeadID = wordDict[sentHeadID]
                                word.set('head', str(newHeadID))

            tb.write(file_name, encoding = "unicode")
            print("Rewrote:", file_name)

print(punctuationCounter)
