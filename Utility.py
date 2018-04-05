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
    wordDict = {}

    # This will create a dictionary matching old ID's to their new ones. Then it will assign the new ID.
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
                                sentenceID = str(sentence.get('id'))
                                wordID = str(word.get('id'))
                                sentWordID = str(sentenceID + '-' + wordID)
                                wordDict[sentWordID] = i
                                word.set('id', str(i))
                                i += 1

                # This will assign new head ID's that are in accordance with the new numbering system.
                for body in tbroot:
                    for sentence in body:
                        for word in sentence:
                            if word.tag == 'word':
                                sentenceID = str(sentence.get('id'))
                                headID = str(word.get('head'))
                                sentHeadID = str(sentenceID + '-' + headID)
                                if sentHeadID in wordDict:
                                    newHeadID = wordDict[sentHeadID]
                                    word.set('head', str(newHeadID))

                tb.write(file_name, encoding="unicode")
                print("Resequenced:", file_name)
