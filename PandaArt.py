import xml.etree.ElementTree as ET
from collections import Counter
import string
import os
import pandas as pd

formOrLemma = 'lemma'
wordCounter = Counter()
artCounter = Counter()
finalDict = {}
firstWordList = []


def deaccent(dastring):
    """Returns an unaccented version of dastring."""
    aeinput = "άἀἁἂἃἄἅἆἇὰάᾀᾁᾂᾃᾄᾅᾆᾇᾰᾱᾲᾳᾴᾶᾷἈἉΆἊἋἌἍἎἏᾈᾉᾊᾋᾌᾍᾎᾏᾸᾹᾺΆᾼέἐἑἒἓἔἕὲέἘἙἚἛἜἝΈῈΈ"
    aeoutput = "ααααααααααααααααααααααααααΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑεεεεεεεεεΕΕΕΕΕΕΕΕΕ"
    hoinput = "ΉῊΉῌἨἩἪἫἬἭἮἯᾘᾙᾚᾛᾜᾝᾞᾟήἠἡἢἣἤἥἦἧὴήᾐᾑᾒᾓᾔᾕᾖᾗῂῃῄῆῇὀὁὂὃὄὅόὸόΌὈὉὊὋὌὍῸΌ"
    hooutput = "ΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗηηηηηηηηηηηηηηηηηηηηηηηηοοοοοοοοοΟΟΟΟΟΟΟΟΟ"
    iuinput = "ΊῘῙῚΊἸἹἺἻἼἽἾἿΪϊίἰἱἲἳἴἵἶἷΐὶίῐῑῒΐῖῗΫΎὙὛὝὟϓϔῨῩῪΎὐὑὒὓὔὕὖὗΰϋύὺύῠῡῢΰῦῧ"
    iuoutput = "ΙΙΙΙΙΙΙΙΙΙΙΙΙΙιιιιιιιιιιιιιιιιιιιΥΥΥΥΥΥΥΥΥΥΥΥυυυυυυυυυυυυυυυυυυυ"
    wrinput = "ώὠὡὢὣὤὥὦὧὼώᾠᾡᾢᾣᾤᾥᾦᾧῲῳῴῶῷΏὨὩὪὫὬὭὮὯᾨᾩᾪᾫᾬᾭᾮᾯῺΏῼῤῥῬ"
    wroutput = "ωωωωωωωωωωωωωωωωωωωωωωωωΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩρρΡ"
    # Strings to feed into translator tables to remove diacritics.

    aelphas = str.maketrans(aeinput, aeoutput, "⸀⸁⸂⸃·,.—")
    # This table also removes text critical markers and punctuation.

    hoes = str.maketrans(hoinput, hooutput, string.punctuation)
    # Removes other punctuation in case I forgot any.

    ius = str.maketrans(iuinput, iuoutput, '0123456789')
    # Also removes numbers (from verses).

    wros = str.maketrans(wrinput, wroutput, string.ascii_letters)
    # Also removes books names.

    return dastring.translate(aelphas).translate(hoes).translate(ius).translate(wros).lower()


def proiellist(treebank, wordtype, firstwordlist):
    """Find every word of the chosen part of speech which appears
    and add it to a firstwordlist if it's not already part of that list."""
    froot = treebank.getroot()
    for source in froot:
        for division in source:
            for sentence in division:
                for token in sentence:
                    if token.get('part-of-speech') == 'Ne' or token.get('part-of-speech') == 'Nb':
                        accented = str(token.get(wordtype))
                        unaccented = deaccent(accented)
                        if unaccented not in firstwordlist:
                            firstwordlist.append(unaccented)
    return firstwordlist


def perseuslist(treebank, wordtype, firstwordlist):
    """Find every word of the chosen morphology which appears
    and add it to a firstwordlist if it's not already part of that list."""
    froot = treebank.getroot()
    for body in froot:
        for sentence in body:
            for word in sentence:
                morph = str(word.get('postag'))
                if morph[0] == 'n':
                    accented = str(word.get(wordtype))
                    unaccented = deaccent(accented)
                    if unaccented not in firstwordlist:
                        firstwordlist.append(unaccented)
    return firstwordlist


def proieltbs(treebank, wordtype):
    """Returns a list of two Counters filled with article stats for the given treebank and wordform."""
    wordcounter = Counter()
    idtoworddict = {}
    artheadid = {}
    artwordcounter = Counter()
    froot = treebank.getroot()

    for source in froot:
        for division in source:
            for sentence in division:
                for token in sentence:
                    if token.get('part-of-speech') == 'Ne' or token.get('part-of-speech') == 'Nb':
                        idtoworddict[token.get('id')] = token.get(wordtype)
                        notaccented = deaccent(token.get(wordtype))
                        wordcounter[notaccented] += 1
    # Creates wordcounter(EveryWordofThatPOS:OccurrenceCount)
    # Creates idtoworddict{WordIDThatCorrespondsTo:EveryWordofThatPOS}

    for source in froot:
        for division in source:
            for sentence in division:
                for token in sentence:
                    if token.get('lemma') == 'ὁ':
                        artheadid[token.get('id')] = token.get('head-id')
    # Creates artheadid{ArticleIDs:HeadNounIDs}

    for key in artheadid:
        headnounid = artheadid[key]
        if headnounid in idtoworddict:
            accents = idtoworddict[headnounid]
            noaccents = deaccent(accents)
            artwordcounter[noaccents] += 1
    # Creates artnouncounter(EveryWordofThatPOS:ArticularOccurrences)

    counters = [wordcounter, artwordcounter]
    return counters


def perseustbs(treebank, wordtype):
    """Returns a list of two Counters filled with article stats for the given treebank and wordform."""
    wordcounter = Counter()
    idtoworddict = {}
    artheadid = {}
    artwordcounter = Counter()
    froot = treebank.getroot()

    for body in froot:
        for sentence in body:
            for word in sentence:
                morph = str(word.get('postag'))
                if morph[0] == 'n':
                    senwordid = str(sentence.get('id')) + '-' + str(word.get('id'))
                    idtoworddict[senwordid] = word.get(wordtype)
                    notaccented = deaccent(word.get(wordtype))
                    wordcounter[notaccented] += 1
    # Creates wordcounter(EveryWordofThatPOS:OccurrenceCount)
    # Creates idtoworddict{Sentence-WordIDThatCorrespondsTo:EveryWordofThatPOS}

    for body in froot:
        for sentence in body:
            for word in sentence:
                if word.get('lemma') == 'ὁ':
                    artid = str(sentence.get('id')) + '-' + str(word.get('id'))
                    headid = str(sentence.get('id')) + '-' + str(word.get('head'))
                    artheadid[artid] = headid
    # Creates artheadid{ArticleIDs:HeadNounIDs}

    for key in artheadid:
        headnounid = artheadid[key]
        if headnounid in idtoworddict:
            accents = idtoworddict[headnounid]
            noaccents = deaccent(accents)
            artwordcounter[noaccents] += 1
    # Creates artwordcounter(EveryWordofThatPOS:ArticularOccurrences)

    counters = [wordcounter, artwordcounter]
    return counters


def dictexpand(listofcounters, firstwordlist, finaldict):
    """For each treebank, expand finalDict with its new article stats."""
    wordcounter = listofcounters[0]
    artcounter = listofcounters[1]
    for word in firstwordlist:
        if word in wordcounter:
            totesoccur = wordcounter[word]
            artoccur = artcounter[word]
            percart = artoccur / totesoccur
            if word in finaldict:
                finaldict[word] += [totesoccur, artoccur, percart]
            else:
                finaldict[word] = [totesoccur, artoccur, percart]
        else:
            if word in finaldict:
                finaldict[word] += [0, 0, 0]
            else:
                finaldict[word] = [0, 0, 0]
    return finaldict


os.chdir('/home/chris/Desktop/Treebanks')
indir = os.listdir('/home/chris/Desktop/Treebanks')

for file_name in indir:
    tb = ET.parse(file_name)
    tbroot = tb.getroot()
    if tbroot.tag == 'proiel':
        firstWordList = proiellist(tb, formOrLemma, firstWordList)
    if tbroot.tag == 'treebank':
        firstWordList = perseuslist(tb, formOrLemma, firstWordList)
# Updates firstWordList from each treebank.

filenameList = []
firstWordListLen = len(firstWordList)

for file_name in indir:
    tb = ET.parse(file_name)
    tbroot = tb.getroot()
    filenameList.append(file_name)
    if tbroot.tag == 'proiel':
        listOfCounters = proieltbs(tb, formOrLemma)
        finalDict = dictexpand(listOfCounters, firstWordList, finalDict)
    if tbroot.tag == 'treebank':
        listOfCounters = perseustbs(tb, formOrLemma)
        finalDict = dictexpand(listOfCounters, firstWordList, finalDict)
# Takes Counters from proieltbs or perseustbs and adds them to the finalDict

fnNum = len(filenameList)
finalDict2 = {}

for key in finalDict:
    i = 0
    j = 1
    realTotOcc = 0
    realTotArt = 0
    while i < (fnNum*3-1):
        realTotOcc += finalDict[key][i]
        i += 3
    if realTotOcc > 6:
        while j < (fnNum*3-1):
            realTotArt += finalDict[key][j]
            j += 3
        realPerc = realTotArt/realTotOcc
        finalDict2[key] = finalDict[key] + [realTotOcc, realTotArt, realPerc]
# This adds three more values on to the end of every key-value to give the total article stats across all
# treebanks, but removes keys that occur fewer times than the required count.

df = pd.DataFrame.from_items(finalDict2.items(), orient='index', columns=['Total', 'Articular', 'PercArt']*(fnNum + 1))

outname = 'ArtDistance.csv'
outdir = '/home/chris/Desktop'
outpath = os.path.join(outdir, outname)
df.to_csv(outpath)

print(finalDict2)
print(filenameList)
print(len(firstWordList))
print(len(finalDict2))