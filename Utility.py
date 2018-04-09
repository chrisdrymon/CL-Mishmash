import string
import os
import xml.etree.ElementTree as ET


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


def denumber(dalemma):
    """Removes number from the string dalemma."""

    numers = str.maketrans('', '', '01234567890')

    return dalemma.translate(numers)


def resequence():
    """Numbers each word element in a treebank with a unique sequential id starting from 1. Then adjusts
    head-ids to match the new numbering."""
    os.chdir('/home/chris/Desktop/CustomTB')
    indir = os.listdir('/home/chris/Desktop/CustomTB')
    worddict = {}

    # This will create a dictionary matching old ID's to their new ones so heads can be reassigned
    # then it will assign the new sequential IDs.
    for file_name in indir:
        i = 1
        if not file_name == 'README.md' and not file_name == '.git':
            print(file_name)
            tb = ET.parse(file_name)
            tbroot = tb.getroot()
            if tbroot.tag == 'treebank':
                for body in tbroot:
                    for sentence in body:
                        for word in sentence:
                            if word.tag == 'word':
                                sentenceid = str(sentence.get('id'))
                                wordid = str(word.get('id'))
                                sentwordid = str(sentenceid + '-' + wordid)
                                worddict[sentwordid] = i
                                word.set('id', str(i))
                                i += 1

                # This will assign new head ID's that are in accordance with the new numbering system.
                for body in tbroot:
                    for sentence in body:
                        for word in sentence:
                            if word.tag == 'word':
                                sentenceid = str(sentence.get('id'))
                                headid = str(word.get('head'))
                                sentheadid = str(sentenceid + '-' + headid)
                                if sentheadid in worddict:
                                    newheadid = worddict[sentheadid]
                                    word.set('head', str(newheadid))

                tb.write(file_name, encoding="unicode")
                print("Resequenced:", file_name)

            if tbroot.tag == 'proiel':
                for source in tbroot:
                    for division in source:
                        for sentence in division:
                            for token in sentence:
                                if token.tag == 'token':
                                    sentenceid = str(sentence.get('id'))
                                    wordid = str(token.get('id'))
                                    sentwordid = str(sentenceid + '-' + wordid)
                                    worddict[sentwordid] = i
                                    token.set('id', str(i))
                                    i += 1

                for source in tbroot:
                    for division in source:
                        for sentence in division:
                            for token in sentence:
                                if token.tag == 'token':
                                    sentenceid = str(sentence.get('id'))
                                    headid = str(token.get('head-id'))
                                    sentheadid = str(sentenceid + '-' + headid)
                                    if sentheadid in worddict:
                                        newheadid = worddict[sentheadid]
                                        token.set('head-id', str(newheadid))

                tb.write(file_name, encoding="unicode")
                print("Resequenced:", file_name)
