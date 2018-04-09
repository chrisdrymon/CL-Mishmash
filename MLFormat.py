import xml.etree.ElementTree as ET
from collections import Counter
import os
import pandas as pd
from Utility import deaccent


def proieltbs(treebank, artpos):
    """Seach for an article then put every word from that sentence as well as their morphology into
     one dictionary value."""
    froot = treebank.getroot()

    for source in froot:
        for division in source:
            for sentence in division:
                for token in sentence:

    return artpos


def perseustbs(treebank, artpos, filename):
    """Seach for an article then put every word from that sentence as well as their morphology into
     one dictionary value."""
    froot = treebank.getroot()

    for body in froot:
        for sentence in body:
            for word in sentence:


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