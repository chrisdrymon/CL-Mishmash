import xml.etree.ElementTree as ET
import os
from Utility import deaccent


def perseuscount(froot, i, j):
    """Prints every instance of this articular infinitive construction for Perseus treebank."""
    idtoheadid = {}
    inflist = []
    verbslistbyid = []
    idtoform = {}
    for body in froot:
        for sentence in body:
            for word in sentence:
                if word.tag == 'word':
                    # Create artheadid{ID:HeadID}
                    idtoheadid[word.get('id')] = word.get('head')
                    # Create a list of every id of an infinitive.
                    if word.get('postag')[4] == 'n':
                        inflist.append(word.get('id'))
                    # Create a dictionary idtoform{ID:form}
                    idtoform[word.get('id')] = word.get('form')
                    if word.get('postag')[0] == 'v':
                        verbslistbyid.append(word.get('id'))

    for body in froot:
        for sentence in body:
            for word in sentence:
                if word.tag == 'word':
                    if deaccent(word.get('form')) == 'του' and word.get('head') in inflist:
                        infinitiveid = word.get('head')
                        mainverbid = idtoheadid[infinitiveid]
                        if mainverbid in verbslistbyid:
                            for infsubj in sentence:
                                if infsubj.tag == 'word':
                                    if infsubj.get('head') == infinitiveid and infsubj.get('relation') == 'SBJ':
                                        for infobj in sentence:
                                            if infobj.get('postag')[7] == 'a' and infobj.get('head') == infinitiveid \
                                                    and infobj.get('relation') == 'OBJ':
                                                print(sentence.get('subdoc'), idtoform[mainverbid], infsubj.get('form'),
                                                      "(SUBJ)", word.get('form'), idtoform[infinitiveid],
                                                      infobj.get('form'))
                                                i += 1
                                    if infsubj.get('head') == mainverbid and infsubj.get('relation') == 'OBJ':
                                        for infobj in sentence:
                                            if infobj.get('postag')[7] == 'a' and infobj.get('head') == infinitiveid \
                                                    and infobj.get('relation') == 'OBJ':
                                                print(sentence.get('subdoc'), idtoform[mainverbid], infsubj.get('form'),
                                                      "(OBJ)", word.get('form'), idtoform[infinitiveid],
                                                      infobj.get('form'), idtoform[infinitiveid])
                                                i += 1

#                                        for infobj in sentence:
     #                                       if infobj.tag == 'word':
      #                                          if infobj.get('postag')[7] == 'a'\
       #                                                 and infobj.get('head') == infinitiveid\
        #                                                and infobj.get('relation') == 'OBJ':
         #                                           print(sentence.get('subdoc'), idtoform[mainverbid],
          #                                                infsubj.get('form'), word.get('form'),
           #                                               idtoform[word.get('head')], infobj.get('form'))
            #                                        if int(infobj.get('id')) < int(infsubj.get('id')):
             #                                           print('^^Backwards!')
              #                                          j += 1
               #                                     i += 1
    return i, j


def proielcount(froot, i, j):
    """Prints every instance of this articular infinitive construction for PROIEL treebanks."""
    idtoheadid = {}
    inflist = []
    verbslistbyid = []
    idtoform = {}

    for source in froot:
        for division in source:
            for sentence in division:
                for token in sentence:
                    if token.tag == 'token' and token.get('empty-token-sort') is None:
                        # Create artheadid{ID:HeadID}
                        idtoheadid[token.get('id')] = token.get('head-id')
                        # Create a list of every id of an infinitive.
                        if token.get('morphology')[3] == 'n':
                            inflist.append(token.get('id'))
                        # Create a dictionary idtoform{ID:form}
                        idtoform[token.get('id')] = token.get('form')
                        if token.get('part-of-speech') == 'V-':
                            verbslistbyid.append(token.get('id'))

    for source in froot:
        for division in source:
            for sentence in division:
                if sentence.tag == 'sentence':
                    for token in sentence:
                        if token.tag == 'token' and token.get('empty-token-sort') is None:
                            if deaccent(token.get('form')) == 'του' and token.get('head-id') in inflist:
                                infinitiveid = token.get('head-id')
                                mainverbid = idtoheadid[infinitiveid]
                                if mainverbid in verbslistbyid:
                                    for infsubj in sentence:
                                        if infsubj.tag == 'token' and infsubj.get('empty-token-sort') is None:
                                            if infsubj.get('morphology')[6] == 'a' and \
                                                    infsubj.get('head-id') == mainverbid:
                                                for infobj in sentence:
                                                    if infobj.tag == 'token' and infobj.get('empty-token-sort') is None:
                                                        if infobj.get('morphology')[6] == 'a' and \
                                                                infobj.get('head-id') == infinitiveid:
                                                            print(token.get('citation-part'), idtoform[mainverbid],
                                                                  infsubj.get('form'), token.get('form'),
                                                                  idtoform[token.get('head-id')], infobj.get('form'))
                                                            if int(infobj.get('id')) < int(infsubj.get('id')):
                                                                print('^^Backwards!')
                                                                j += 1
                                                            i += 1

    return i, j


os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')

infCount = 0
backwardCount = 0
for file_name in indir:
    tb = ET.parse(file_name)
    tbroot = tb.getroot()
#    print(file_name)
#    if tbroot.tag == 'proiel':
#        infCount, backwardCount = proielcount(tbroot, infCount, backwardCount)
    if tbroot.tag == 'treebank':
        print(file_name)
        infCount, backwardCount = perseuscount(tbroot, infCount, backwardCount)

print('Total:', infCount)
