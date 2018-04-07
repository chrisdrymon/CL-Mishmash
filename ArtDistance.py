import xml.etree.ElementTree as ET
from collections import Counter
import os
import pandas as pd

artPos = Counter()

def proieltbs(treebank, artpos, filename):
    """Returns a Counter artpos{articleposition:frequency}."""
    froot = treebank.getroot()

    for source in froot:
        for division in source:
            for sentence in division:
                for token in sentence:
                    if token.get('lemma') == 'ὁ' and token.get('part-of-speech') == 'S-':
                        if token.get('relation') == 'aux':
                            artdistance = int(token.get('head-id')) - int(token.get('id'))
                            if artdistance < 100:
                                artpos[artdistance] += 1
                                if artdistance < -100:
                                    print(filename, token.get('id'))
    # Subtracts Head-ID from Article-ID to gather distance between the two words. Adds it to counter.

    return artpos


def perseustbs(treebank, artpos, filename):
    """Returns a Counter artpost{articleposition:frequency}."""
    froot = treebank.getroot()

    for body in froot:
        for sentence in body:
            for word in sentence:
                if word.get('lemma') == 'ὁ' and word.get('relation') == 'ATR':
                    artdistance = int(word.get('head')) - int(word.get('id'))
                    artpos[artdistance] += 1
                    if artdistance > 1000:
                        print(word.get('id'))

    # Subtracts Head-ID from Article-ID to gather distance between the two words. Adds it to counter.

    return artpos


os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')

for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = ET.parse(file_name)
        tbroot = tb.getroot()
        print(file_name)
        if tbroot.tag == 'proiel':
            artPos = proieltbs(tb, artPos, file_name)
        if tbroot.tag == 'treebank':
            artPos = perseustbs(tb, artPos, file_name)

df = pd.DataFrame.from_dict(artPos, orient='index')

outname = 'NewArtDistance.csv'
outdir = '/home/chris/Desktop'
outpath = os.path.join(outdir, outname)
df.to_csv(outpath)

print(artPos)
