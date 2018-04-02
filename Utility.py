import string

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
    numers = str.maketrans('', '', '01234567890')

    return dalemma.translate(numers)