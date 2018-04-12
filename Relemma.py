import xml.etree.ElementTree as ET
import os

os.chdir('/home/chris/Desktop/NTTB')
indir = os.listdir('/home/chris/Desktop/NTTB')

#Deletes the '#' followed by a number from any lemma it occurs in.
for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        print(file_name)
        tb = ET.parse(file_name)
        tbroot = tb.getroot()
        for source in tbroot:
            for division in source:
                for sentence in division:
                    for token in sentence:
                        if token.tag == 'token':
                            if '#' in str(token.get('lemma')):
                                token.set('lemma', (token.get('lemma')[0:-2]))
        tb.write(file_name, encoding="unicode")
        print("Relemmaed:", file_name)