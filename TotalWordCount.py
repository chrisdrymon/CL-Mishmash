import xml.etree.ElementTree as ET
import os


def perseuscount(treebank, totalwordcount):
    """Prints a wordcount for a Perseus treebank."""
    froot = treebank
    i = 0
    for body in froot:
        for sentence in body:
            for word in sentence:
                if word.tag == 'word':
                    i += 1
    totalwordcount = totalwordcount + i
    print(i)
    return(totalwordcount)


def proielcount(treebank, totalwordcount):
    """Prints a wordcount for a PROIEL treebank."""
    froot = treebank
    i = 0
    for source in froot:
        for division in source:
            for sentence in division:
                for token in sentence:
                    if token.tag == 'token':
                        i += 1
    totalwordcount = totalwordcount + i
    print(i)
    return(totalwordcount)


os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')

totalWordCount = 0
for file_name in indir:
    tb = ET.parse(file_name)
    tbroot = tb.getroot()
    print(file_name)
    if tbroot.tag == 'proiel':
        totalWordCount = proielcount(tbroot, totalWordCount)
    if tbroot.tag == 'treebank':
        totalWordCount = perseuscount(tbroot, totalWordCount)

print('Total:', totalWordCount)