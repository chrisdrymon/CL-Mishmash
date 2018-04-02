import xml.etree.ElementTree as ET
import os


def perseuscount(treebank):
    """Find every word of the chosen morphology which appears
    and add it to a firstwordlist if it's not already part of that list."""
    froot = treebank
    i = 0
    for body in froot:
        for sentence in body:
            for word in sentence:
                if word.tag == 'word':
                    i += 1
    print(i)


def proielcount(treebank):
    """Returns a list of two Counters filled with article stats for the given treebank and wordform."""
    froot = treebank
    i = 0
    for source in froot:
        for division in source:
            for sentence in division:
                for token in sentence:
                    if token.tag == 'token':
                        i += 1
    print(i)


os.chdir('/home/chris/Desktop/Treebanks')
indir = os.listdir('/home/chris/Desktop/Treebanks')

for file_name in indir:
    tb = ET.parse(file_name)
    tbroot = tb.getroot()
    print(file_name)
    if tbroot.tag == 'proiel':
        proielcount(tbroot)
    if tbroot.tag == 'treebank':
        perseuscount(tbroot)
# Updates firstWordList from each treebank.