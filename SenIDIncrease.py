import xml.etree.ElementTree as ET
import os

os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')

for file_name in indir:
    tb = ET.parse(file_name)
    tbroot = tb.getroot()
    print(file_name)
    for body in tbroot:
        for sentence in body:
            if sentence.tag == "sentence":
                oldid = sentence.get('id')
                newid = int(oldid) + 101
                sentence.set('id', str(newid))
                print(newid)
    tb.write("newAlci.xml", encoding = "unicode")