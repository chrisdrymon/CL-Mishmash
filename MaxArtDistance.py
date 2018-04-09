import xml.etree.ElementTree as ET
import os


def maxproiel(froot, maxds):
    """Returns the maximum distance that any article is from the beginning of a sentence and from the end
    of a sentence."""
    leftmost = maxds[0]
    rightmost = maxds[1]
    for source in froot:
        for division in source:
            for sentence in division:
                for token in sentence:
                    if token.get('lemma') == 'ὁ':
                        i = -1
                        while sentence[i].get('empty-token-sort'):
                            i -= 1
                        testnumber = (int(sentence[i].get('id')) - int(token.get('id')))
                        if testnumber > rightmost:
                            rightmost = testnumber
                            print("New max:", leftmost, rightmost, "at", token.get('citation-part'))
                        testnumber = (int(sentence[0].get('id')) - int(token.get('id')))
                        if testnumber < leftmost:
                            leftmost = testnumber
                            print("New min:", leftmost, rightmost, "at", token.get('citation-part'))
    maxds = [leftmost, rightmost]
    return maxds


def maxperseus(froot, maxds):
    """Returns the maximum distance that any article is from the beginning of a sentence and from the end
    of a sentence."""
    leftmost = maxds[0]
    rightmost = maxds[1]
    for body in froot:
        for sentence in body:
            sentlist = sentence.findall('word')
            for word in sentlist:
                if word.get('lemma') == 'ὁ':
                        testnumber = (int(sentlist[-1].get('id')) - int(word.get('id')))
                        if testnumber > rightmost:
                            rightmost = testnumber
                            print("New max:", leftmost, rightmost, "at", sentence.get('subdoc'), "in", froot.get('cts'))
                        testnumber = (int(sentlist[0].get('id')) - int(word.get('id')))
                        if testnumber < leftmost:
                            leftmost = testnumber
                            print("New min:", leftmost, rightmost, "at", sentence.get('subdoc'), "in", froot.get('cts'))
    maxds = [leftmost, rightmost]
    return maxds


maxDs = [0,0]
os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')
for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = ET.parse(file_name)
        tbroot = tb.getroot()
        if tbroot.tag == 'proiel':
            maxDs = maxproiel(tbroot, maxDs)
        if tbroot.tag == 'treebank':
            maxDs = maxperseus(tbroot, maxDs)