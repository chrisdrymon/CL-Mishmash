import xml.etree.ElementTree as ET
from collections import Counter
import string
import os
import pandas as pd

artPos = Counter()


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


def proieltbs(treebank, artpos, filename):
    """Returns a Counter artpos{articleposition:frequency}."""
    froot = treebank.getroot()

    for source in froot:
        for division in source:
            for sentence in division:
                for token in sentence:
                    if token.get('lemma') == 'ὁ' and token.get('part-of-speech') == 'S-':
                        artdistance = int(token.get('head-id')) - int(token.get('id'))
                        if artdistance < 65:
                            artpos[artdistance] += 1
#                            if artdistance > 12 and artdistance < 100:
#                                print(filename, token.get('id'))
    # Subtracts Head-ID from Article-ID to gather distance between the two words. Adds it to counter.

    return artpos


def perseustbs(treebank, artpos, filename):
    """Returns a Counter artpost{articleposition:frequency}."""
    froot = treebank.getroot()

    insertedlist = []

    for body in froot:
        for sentence in body:
            for word in sentence:
                if word.get('insertion_id'):
                    senid = str(sentence.get('id'))
                    wordid = str(word.get('id'))
                    insertedlist.append(str(senid + '-' + wordid))

    for body in froot:
        for sentence in body:
            for word in sentence:
                if word.get('lemma') == 'ὁ' and word.get('relation') == 'ATR':
                    senid = str(sentence.get('id'))
                    wordid = str(word.get('head'))
                    uniqueid = str(senid + '-' + wordid)
                    if uniqueid not in insertedlist:
                        artdistance = int(word.get('head')) - int(word.get('id'))
                        artpos[artdistance] += 1
                        if artdistance == 22:
                            print(uniqueid)

    # Subtracts Head-ID from Article-ID to gather distance between the two words. Adds it to counter.

    return artpos


os.chdir('/home/chris/Desktop/KoineTB')
indir = os.listdir('/home/chris/Desktop/KoineTB')

for file_name in indir:
    tb = ET.parse(file_name)
    tbroot = tb.getroot()
    print(file_name)
    if tbroot.tag == 'proiel':
        artPos = proieltbs(tb, artPos, file_name)
    if tbroot.tag == 'treebank':
        artPos = perseustbs(tb, artPos, file_name)

df = pd.DataFrame.from_dict(artPos, orient='index')

outname = 'ArtDistance.csv'
outdir = '/home/chris/Desktop'
outpath = os.path.join(outdir, outname)
df.to_csv(outpath)

print(artPos)
