import xml.etree.ElementTree as ET
import os

os.chdir('/home/chris/Desktop/Treebanks')
indir = os.listdir('/home/chris/Desktop/Treebanks')

for file_name in indir:
    tb = ET.parse(file_name)
    tbroot = tb.getroot()
    print(file_name)
    for body in tbroot:
        for sentence in body:
            if sentence.tag == "sentence":
                oldid = sentence.get('id')
                newid = int(oldid) + 1050
                sentence.set('id', str(newid))
                print(newid)
    tb.write("newdeip.xml", encoding = "unicode")