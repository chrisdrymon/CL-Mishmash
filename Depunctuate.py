import xml.etree.ElementTree as ET
import os
from collections import Counter

os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')
punctuationCounter = Counter()

# This creates a list of every word-id that will have the "presentation-after='.'" added to it.
for file_name in indir:
    periodWords = []
    if not file_name == 'README.md' and not file_name == '.git':
        print(file_name)
        tb = ET.parse(file_name)
        tbroot = tb.getroot()
        if tbroot.tag == 'treebank':
            for body in tbroot:
                for sentence in body:
                    for word in sentence:
                        if word.tag == 'word' and word.get('form') == '.':
                            periodWords.append(int(word.get('id'))-1)

# This will assign "presentation-after='.'" to all the words in periodWords.
            for body in tbroot:
                for sentence in body:
                    for word in sentence:
                        if word.tag == 'word' and int(word.get('id')) in periodWords:
                            word.set('presentation-after', '.')

# This deletes all word elements which have the form '.'.
            for body in tbroot:
                for sentence in body:
                    for word in sentence.findall('word'):
                        if word.get('form') == '.':
                            sentence.remove(word)

            tb.write(file_name, encoding = "unicode")
            print("Rewrote:", file_name)

print(punctuationCounter)
