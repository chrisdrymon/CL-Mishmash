import xml.etree.ElementTree as Et
import os
from utility import deaccent


def proieltbs(treebank, artcount, auxcount, procount):
    froot = treebank.getroot()
    fartcount = 0
    fauxcount = 0
    fprocount = 0
    for source in froot:
        for division in source:
            for sentence in division:
                alltokesinsent = sentence.findall(".*[@form]")
                for token in alltokesinsent:
                    if deaccent(token.get('lemma')) == 'ο':
                        artcount += 1
                        fartcount += 1
                        if token.get('relation') == 'aux':
                            auxcount += 1
                            fauxcount += 1
                        else:
                            procount += 1
                            fprocount +=1

    print('Percent Pronoun', fprocount / fartcount)
    return artcount, auxcount, procount


def perseustbs(treebank, artcount, auxcount, procount):
    froot = treebank.getroot()
    fartcount = 0
    fauxcount = 0
    fprocount = 0
    for body in froot:
        for sentence in body:
            alltokesinsent = sentence.findall(".*[@form]")
            for word in alltokesinsent:
                if deaccent(word.get('lemma')) == 'ο':
                    artcount += 1
                    fartcount += 1
                    if word.get('relation') == 'ATR':
                        auxcount += 1
                        fauxcount += 1
                    else:
                        procount += 1
                        fprocount += 1
    print('Percent Pronoun', fprocount / fartcount)

    return artcount, auxcount, procount


os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')
artCount = 0
auxCount = 0
proCount = 0
for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = Et.parse(file_name)
        tbroot = tb.getroot()
        print(file_name)
        if tbroot.tag == 'proiel':
            artCount, auxCount, proCount = proieltbs(tb, artCount, auxCount, proCount)
        else:
            artCount, auxCount, proCount = perseustbs(tb, artCount, auxCount, proCount)
print('Total articles:', artCount)
print('Article articles:', auxCount)
print('Pronouns:', proCount)
print('Percent Pronoun', proCount/artCount)