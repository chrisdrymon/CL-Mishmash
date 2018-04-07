import xml.etree.ElementTree as ET
import os
from Utility import resequence

# Run resequence so we don't have to deal with making unique sentence-word ids throughout script.
resequence()

os.chdir('/home/chris/Desktop/Treebanks')
indir = os.listdir('/home/chris/Desktop/Treebanks')
puncInQuestion = ';'

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
                        if word.tag == 'word' and word.get('form') == puncInQuestion:
                            periodWords.append(int(word.get('id'))-1)

# This will assign "presentation-after=" to the puncInQuestion variable to all the words in periodWords.
            for body in tbroot:
                for sentence in body:
                    for word in sentence:
                        if word.tag == 'word' and int(word.get('id')) in periodWords:
                            word.set('presentation-after', puncInQuestion)

# This deletes all word elements which have the form matching puncInQuestion.
            for body in tbroot:
                for sentence in body:
                    for word in sentence.findall('word'):
                        if word.get('form') == puncInQuestion:
                            sentence.remove(word)

            tb.write(file_name, encoding = "unicode")
            print("Rewrote:", file_name)

# Resequence to account for the deleted word elements.
resequence()
