import xml.etree.ElementTree as Et
import os
from utility import deaccent


def proieltbs(treebank):
    froot = treebank.getroot()
    for source in froot:
        for division in source:
            if division.tag == 'title':
                title = division.text
            if division.tag == 'author':
                author = division.text
            for sentence in division:
                alltokesinsent = sentence.findall(".*[@form]")
                for token in alltokesinsent:
                    subject = 'ellipsed'
                    vobject = 'ellipsed'
                    if deaccent(token.get('lemma')) == 'περισσευω' and not token.get('morphology')[4] == 'a':
                        verbid = token.get('id')
                        for word in alltokesinsent:
                            if word.get('head-id') == verbid and word.get('relation') == 'sub':
                                subject = word.get('form')
                            if word.get('head-id') == verbid and word.get('relation') == 'obj':
                                vobject = word.get('form')
                        print(author, title, subject, token.get('form'), vobject)
    return


def perseustbs(treebank):
    froot = treebank.getroot()
    author = froot.find(".//author")
    author = author.text
    title = froot.find(".//title")
    title = title.text
    for body in froot:
        for sentence in body:
            mainverb = 'ellipsed'
            alltokesinsent = sentence.findall(".*[@form]")
            for verb in alltokesinsent:
                subject = 'ellipsed'
                vobject = 'ellipsed'
                if deaccent(verb.get('lemma')) == 'περισσευω' and not verb.get('postag')[5] == 'a':
                    verbid = verb.get('id')
                    for word in alltokesinsent:
                        if word.get('head') == verbid and word.get('relation') == 'sub':
                            subject = word.get('form')
                        if word.get('head') == verbid and word.get('relation') == 'obj':
                            vobject = word.get('form')
                    print(author, title, subject, verb.get('form'), vobject)
    return


os.chdir('/home/chris/Desktop/Treebanks')
indir = os.listdir('/home/chris/Desktop/Treebanks')
for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = Et.parse(file_name)
        tbroot = tb.getroot()
#        print(file_name)
        if tbroot.tag == 'proiel':
            proieltbs(tb)
        else:
            perseustbs(tb)
