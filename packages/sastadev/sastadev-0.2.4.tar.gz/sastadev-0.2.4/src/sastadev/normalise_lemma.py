'''
This module normalises Alpino lemmata for noun compounds. The lemma for a noun compound in Alpino is a sequence of
lemma for the compound parts separated by underscores.

Example: word = verkeerslichtjes. Alpino lemma = verkeer_licht.
But for many applications we need the 'normal' lemma for such as compound, i.e.
for *verkeerslichtje* that is *verkeersicht*. This is achieved by the function *normalizelemma*

The function has been tested against all noun compounds in Lassy-Klein

'''
# @TODO@
# () in woorden
# 1 hyphen te veel/te weinig
# splitsen in test, eigenlijke module, stringfuncties verplaatsen
# documentatie


import re
from typing import List

from sastadev import readcsv, xlsx

hyphen = '-'
tab = '\t'
cmpsep = '_'
c = r'[bcdfghjklmnpqrstvwxz]'
vr = 'aeiou'
v = fr'[{vr}]'
notv = fr'[^{vr}]'
bv = f'({v})'
bc = f'({c})'
df = r'ai|au|ei|eu|oe|oi|ou|ui'

bdf = f'({df})'

vowels = 'AEIOUYaeiouy'
aigu = 'ÁÉÍÓÚÝáéíóúý'
grave = 'ÀÈÌÒÙ\u1ef2àèìòù\u1ef3'
trema = 'ÄËÏÖÜ\u0178äëïöüÿ'
tilde = 'Ã\u1EBC\u0128Õ\u0168\u1EF8ã\u1EBD\u0129õ\u0169\u1EF9'
circumflex = 'ÂÊÎÔÛ\u0176âêîôû\u0177'


diacritics = aigu + grave + trema + tilde + circumflex
undiacritics = 5 * vowels


testset = [('water_pok', 'waterpokken'),
           ('zee_hond', 'zeehondje'),
           ('rijk_museum', 'rijksmusea'),
           ('klap_roos', 'klaprozen'),
           ('maan_bol', 'maanbolletje'),
           ('linde_laan', 'lindelanen'),
           ('ijs_verkoper', 'ijsjesverkopers'),
           ('verkeer_licht', 'verkeerslichtje'),
           ('hoofd_stad', 'hoofdsteden'),
           ('bewind_man', 'bewindslui'),
           ('bewind_man', 'bewindslieden'),
           ('bewind_man', 'bewindsmannen'),
           ('klein_kind', 'kleinkinderen'),
           ('offer_lam', 'offerlammeren'),
           ('beleid_politicus', 'beleidspolitici'),
           ('wereld_zee', 'wereldzeeën')
           ]


def iscompound(lemma: str) -> bool:
    result = cmpsep in lemma
    return result


def apply(regex, sub, rawform, lemma, lemmatest=False, keeplastsep=False):

    if not lemmatest and not iscompound(lemma):
        return lemma
    else:
        # form = rawform.lower() if all([c.isupper() for c in rawform]) else rawform
        form = rawform
        candlemma = regex.sub(sub, form)
        lemmaparts = lemma.split(cmpsep)
        lastpart = lemmaparts[-1]
        if candlemma.endswith(lastpart):
            if keeplastsep:
                llastpart = len(lastpart)
                result = candlemma[: -llastpart] + \
                    cmpsep + candlemma[-llastpart:]
                return result
            else:
                return candlemma
        elif candlemma.endswith(lastpart.lower()):  # poepchinees v. poep_Chinees
            sep = cmpsep if keeplastsep else ''
            return candlemma[:-len(lastpart)] + sep + lastpart.lower()
        else:
            lemmacorrs = lemma_alt(lastpart)
            for lemmacorr in lemmacorrs:
                if candlemma.endswith(lemmacorr):
                    sep = cmpsep if keeplastsep else ''
                    resultlemma = candlemma[:-len(lemmacorr)] + sep + lastpart
                    return resultlemma

            return None

# het gelid	de gelederen
# het lid	de leden
# het schip	de schepen
# de smid	de smeden
# de gelegenheid	de gelegenheden
# de overheid	de overheden
# de moeilijkheid	de moeilijkheden
# de aanwezigheid	de aanwezigheden
# scheepjes

# koe - koeien
# vlo - vlooien
# uitgang -nen (naast andere mogelijkheden)
# lende - lendenen (ook: lenden). Dit woord komt oorspronkelijk van het archaïsche woord lenden, waarvan de -n uit de officiële spelling gehaald is vanwege het verdwijnen van die -n in de spreektaal.
# uitgang -iën met accentwisseling (in archaïsch taalgebruik)
# kleinood - kleinodiën (ook: kleinoden)
# sieraad - sieradiën (ook: sieraden)
# uitgang -en
# epos - epen (ook: epossen)
# genius - geniën (NB. genie - genieën)
#
# politicus - politici
#
# been - beenderen (botten) (ook: benen (ledematen))
# blad - bladeren (van planten) (ook: bladen (papier))
# ei - eieren
# gelid - gelederen
# gemoed - gemoederen
# goed - goederen
# hoen - hoenderen
# kalf - kalveren
# kind - kinderen
# kleed - kle(de)ren (kledingstukken) (ook: kleden (vloerbedekking))
# lam - lammeren
# lied - liederen
# rad - raderen
# rund - runderen
# volk - volkeren (naties) (ook: volken (populaties))
#
# politica - politica's
# politicus - politici (zowel mannen als vrouwen; zie medicus & musicus)
# medicus - medici
# musicus - musici
# genus - genera
# index - indices (indexen)
# tempus - tempora
# plurale tantum - pluralia tantum
# singulare tantum - singularia tantum
# opus - opera (opussen)
# casus - casus (casussen)
# collega - (vroeger: collegae) collega's
# medium - media (medium (persoon) - mediums)
# museum - musea (museums)
# jubileum - jubilea (jubileums)
# datum - data (datums)
# decennium - decennia (decenniën)
# preses - presides (presessen)
# quaestor - quaestores (quaestors, quaestoren)
# quaestrix - qaestrices
# matrix - matrices (matrixen)
#
# bewindsman - bewindslieden, bewindslui, bewindsmannen
# politieman - politielui, politielieden, politiemannen
# timmerman - timmerlui, timmerlieden, timmermannen
# tuinman - tuinlui, tuinlieden, tuinmannen
# vakman - vaklui, vaklieden, vakmannen
# visserman - visserlui, visserlieden, vissermannen
# voddenman - voddenlui, voddenlieden, voddenmannen
# voerman - voerlui, voerlieden, voermannen
# vogelman - vogellui, vogellieden, vogelmannen
# zeeman - zeelui, zeelieden, zeemannen


patterns = [
    # listed exceptions
    (r'kleertjes?$', 'kleed'),
    (r'kleren$', 'kleed'),
    (r'klederen$', 'kleed'),
    (r'steden$', 'stad'),
    (r'jongetjes?$', 'jongen'),
    (r'excuses$', 'excuus'),
    # e/i alternatiom
    (fr'{bc}e{bc}en$', r'\1i\2'),  # schepen - schip, leden -lid
    (fr'{bc}e{bc}eren$', r'\1i\2'),  # gelederen - gelid
    (fr'ee{bc}jes?$', r'i\1'),  # scheepje - schip;  scheepjes - schip
    # dimunitives
    (r'tjes?$', r''),  # keutje, keutjes
    (r'pjes?$', r''),  # boompje, boompjes
    (r'kjes?$', r'g'),  # koninkje, koningkjes
    (r'jes?$', r''),  # kapje, kapjes
    (r'etjes?$', r''),  # tekeningetje, tekeningetjes
    (r"'tjes?$", ""),  # auto'tje, auto'tjes
    (fr'{bv}\1tjes?', r'\1'),  # autootje(s) - auto
    (fr'{bc}\1etjes?$', r'\1'),  # bolletje, bolletjes
    (fr'{bc}\1ekes?$', r'\1'),  # bolleke, bollekes
    # vaatje -> vat, gaatje -> gat, paadje -> pad
    (fr'{bv}\1([dt])jes?$', r'\1\2'),
    (r'ientjes?$', 'ine'),  # machientje(s) -> machine
    (r'ietjes?$', 'y'),  # babietje(s) -> baby
    # plural
    (fr'{bc}\1en?$', r'\1'),  # bakken (ter) wille
    (r'en?$', ''),  # leeuwen, banden, woorden, dienste
    (r'en$', 'e'),  # ribben - ribbe,
    (r'en$', 'os'),  # epen - epos
    (r'a$', r'um'),  # musea
    (r'a$', 'on'),  # lexica - lexicon
    (r'zen?$', r's'),  # vaarzen, muizen, huize
    (r'ven?$', r'f'),  # larven, duiven, halve
    (fr'{bv}zen?$', r'\1\1s'),  # vazen, loze, Genuezen
    (fr'{bv}ven?$', r'\1\1f'),  # raven,
    (fr'{bc}ven?$', r'\1f'),  # kalven, halve
    (fr'{bc}zen?$', r'\1f'),  # vaarzen,
    (fr'{bc}veren$', r'\1f'),  # kalveren
    (fr'{bc}zeren$', r'\1f'),  # ??
    (fr'{bv}{bc}en?$', r'\1\1\2'),  # manen, Antillianen, rare,
    (r'den', ''),  # getijden, weiden
    (r'iën$', 'ium'),  # mitochondriën / mitochondrium
    (r's$', ''),   # appels, oudooms  plural and genitive
    (r"s'$", "s"),  # genitive plural generaals', Hans'
    (r"z'$", 'z'),  # Chavez'
    (r"sh'$", "sh"),  # Bush'
    (r"ce'$", 'ce'),  # Prince'
    (r"'s$", ""),  # azalea's
    (fr'{bdf}ien$', r'\1'),   # koeien
    (fr'{bv}\1ien$', r'\1'),  # vlooien
    (r'iën$', 'ie'),  # provinciën
    (r'ën$', ''),   # zeeën genieën
    (fr'{bc}{bv}{bc}iën$', r'\1\2\2\3'),  # kleinodiën, sieradiën
    (r'i$', 'us'),  # politici
    (r'era$', 'us'),  # genera
    (r'lui$', 'man'),  # timmerman
    (r'lieden$', 'man'),  # timmerman
    (r'mensen$', 'man'),  # brandweermensen
    (r'en$', 'man'),  # Engelsen/Engelsman, Fransen, Fransman
    (r'ices$', 'ex'),  # indices
    (r'ices$', 'ix'),  # matrices
    (r'heden$', 'heid'),  # gelegenheden
    (r'eren$', ''),   # kinderen
    (r'es$', 'is'),  # bases  -> basis
    (r'ies$', 'y'),  # babies -> baby
    (fr'{bc}\1eren$', r'\1'),  # lammeren
    (r'deren$', ''),  # hoenderen
    (r'nen$', ''),  # lendenen
    (r'iën', 'ius'),  # geniën - genius
    ('ia$', 'e'),  # singularia
    ('ora$', 'us'),  # tempora
    ('ae$', 'a'),  # collegae
    ('es$', ''),  # praetores
    (r'ides$', 'es'),  # presides
    (r'i$', 'o'),  # saldi
    (r'sters?$', 'er'),  # werkster(s) -> werker
    (fr'{bv}\1{bc}sters?$', r'\1\2er'),  # maakster(s) -> maker
    (r'stertjes?$', 'er'),  # werkstertje(s) -> werker
    (fr'{bv}\1{bc}stertjes?$', r'\1\2er')  # maakstertje(s) -> maker

]

spellingcorrections = [
    (fr'{bv}\1\1+{bc}({notv}|$)', r'\1\1\2\3'),   # heeeeel -> heel
    # heeeele -> hele
    (fr'{bv}\1\1+{bc}{bv}', r'\1\2\3'),

]

subs = [(re.compile(pat), sub) for pat, sub in patterns]
spellsubs = [(re.compile(pat), sub) for pat, sub in spellingcorrections]

lemma_alternatives = [('c', 'k'),    # productie -> produktie
                      ('k', 'c'),  # helikopter -< helicopter
                      ('eau', 'o'),  # bureau -> buro]
                      ('pannenkoek', 'pannekoek')]
lemmasubs = [(re.compile(pat), sub) for pat, sub in lemma_alternatives]


def istitlecase(wrd: str) -> bool:
    if wrd == '':
        return False
    elif wrd[0].isupper() and all([c.islower() for c in wrd[1:]]):
        return True
    else:
        return False


def spellcorr(word: str) -> List[str]:
    return spellcorr2(word, spellsubs)


def lemma_alt(lemma: str) -> List[str]:
    return spellcorr2(lemma, lemmasubs)


def spellcorr2(word: str, spellsubs: list) -> List[str]:
    results = []
    finalresults = []
    newword = word
    for regex, repl in spellsubs:
        if regex.search(newword):
            newword2 = regex.sub(repl, newword, count=1)
            results.append(newword2)
    for wrd in results:
        finalresults = spellcorr(wrd)
    return finalresults + results


def longestcommonprefix(word1: str, word2: str) -> str:
    result = ''
    max = min(len(word1), len(word2))
    for c1, c2 in zip(word1[:max], word2[:max]):
        if c1 == c2:
            result += c1
        else:
            return result
    return result


def adaptcase(rawword: str, lemma: str) -> str:
    result = ''
    lcrawword = rawword.lower()
    lclemma = lemma.lower()
    cmnprefix = longestcommonprefix(lcrawword, lclemma)
    prefixlen = len(cmnprefix)
    conversion = []
    for lc, wc in zip(lemma[:prefixlen], rawword[:prefixlen]):
        if lc.islower():
            newwc = wc.lower()
        elif lc.isupper():
            newwc = wc.upper()
        else:
            newwc = wc
        result += newwc
    result += rawword[prefixlen:].lower()
    return result


def adapt_diacritics(rawword: str, lemma: str) -> str:
    result = ''
    ddrawword = undiacritic(rawword.lower())
    ddlemma = undiacritic(lemma.lower())
    cmnprefix = longestcommonprefix(ddrawword, ddlemma)
    prefixlen = len(cmnprefix)
    conversion = []
    result = lemma[:prefixlen]
    result += rawword[prefixlen:]
    return result


def undiacritic(wrd: str) -> str:
    result = ''
    for ch in wrd:
        try:
            pos = diacritics.index(ch)
            result += undiacritics[pos]
        except ValueError:
            result += ch
    return result


def normaliselemma(rawword: str, lemma: str, lemmatest=False, keeplastsep=False) -> str:
    rawwordparts = rawword.split(hyphen)
    lemmaparts = lemma.split(hyphen)
    if len(lemmaparts) != len(rawwordparts):
        # print(f'Hyphen mismatch: {rawword} v. {lemma}')
        result = normaliselemma_simple(
            rawword, lemma, lemmatest=lemmatest, keeplastsep=keeplastsep)
    else:
        results = []
        for lm, wrd in zip(lemmaparts, rawwordparts):
            newresultpart = normaliselemma_simple(
                wrd, lm, lemmatest=lemmatest, keeplastsep=keeplastsep)
            if newresultpart is not None:
                results.append(newresultpart)
            else:
                # print(f'No lemma found for {wrd}')
                results.append('<None>')
        result = hyphen.join(results)
    return result


def normaliselemma_simple(rawword: str, lemma: str, lemmatest=False, keeplastsep=False) -> str:
    result = None

    word = adaptcase(rawword, lemma)
    word = adapt_diacritics(word, lemma)

    for regex, sub in subs:
        if result is None:
            result = apply(regex, sub, word, lemma,
                           lemmatest=lemmatest, keeplastsep=keeplastsep)

    if result is None:
        altwords = spellcorr(word)
        for regex, sub in subs:
            for altword in altwords:
                if result is None:
                    result = apply(regex, sub, altword,
                                   lemma, lemmatest=lemmatest)

    return result


def treatitem(lemma, word, file=None, store=False):
    cleanlemma = lemma.strip()
    cleanword = word.strip()
    newlemma = normaliselemma(cleanword, cleanlemma)
    if file is None:
        print(cleanword, cleanlemma, newlemma)
    else:
        print(cleanword, cleanlemma, newlemma, file=file)


if __name__ == '__main__':

    localtest = True
    test1 = False
    test2 = False
    test3 = False
    test4 = False  # True
    reftest = False  # True
    lemmatest = False  # True

    if localtest:
        alemma = 'staat_bos_beheer'  # 'bewind_man' # 'kleuter_bureau'
        word = 'staatsbossenbeheer'  # 'bewindslieden' # 'kleuterburo'
        reflemma = 'staatsbossenbeheer'  # 'kleuterbureau'
        newlemma = normaliselemma(word, alemma, keeplastsep=True)
        print(newlemma)

    if reftest:
        outgoldfilename = './lemmatests/newcompoundlemmas-gold.txt'
        goldfilename = './lemmatests/compoundlemmas-gold.txt'
        golddata = readcsv.readcsv(goldfilename, sep=tab)
        mismatchctr = 0
        newrecs = []
        for _, rec in golddata:
            rawalemma = rec[1]
            rawword = rec[0]
            rawreflemma = rec[2]
            alemma = rawalemma.strip()
            word = rawword.strip()
            reflemma = rawreflemma.strip()
            newlemma = normaliselemma(word, alemma)
            if newlemma != reflemma:
                mismatchctr += 1
                print(
                    f'Mismatch: {newlemma} =/= {reflemma} for {alemma}/{word}')
            if newlemma is not None:
                newrec = [word, alemma, newlemma]
            else:
                newrec = [word, alemma, reflemma]
            newrecs.append(newrec)
        print(f'{mismatchctr} mismatches found')
        with open(outgoldfilename, 'w', encoding='utf8') as outgoldfile:
            for newrec in newrecs:
                print(tab.join(newrec), file=outgoldfile)
    if test1:
        outfilename = './lemmatests/compoundlemmasout.txt'
        outfile = open(outfilename, 'w', encoding='utf8')

        testfilename = './lemmatests/lemmanormtestset.txt'
        externaltestset = readcsv.readcsv(testfilename, sep=';')

        realtestset = externaltestset

        for _, rec in realtestset:
            lemma = rec[0]
            word = rec[1]
            treatitem(lemma, word, file=outfile)

    if test2:
        childestestfilename = './lemmatests/childes_compound_telling.txt'
        childestestset = readcsv.readcsv(childestestfilename, sep='\t')

        for _, rec in childestestset:
            lemma = rec[2]
            word = rec[3]
            treatitem(lemma, word, file=outfile)

    if test3:
        hyphenfilename = './lemmatests/hyphenwordsLassy.xlsx'
        header, data = xlsx.getxlsxdata(hyphenfilename)

        for rec in data:
            alemma = rec[0].strip()
            word = rec[1].strip()

            newlemma = normaliselemma(word, alemma)
            mismatchctr = 0
            if newlemma != alemma:
                mismatchctr += 1
                print(f'Mismatch: {newlemma} =/= {alemma} for {word}')
        print(f'{mismatchctr} mismatches found')

    if test4:
        spelltestlist = ['buro', 'produktie', 'kado', 'appelstrooop']
        spelltestlist = ['strooop', 'heeeeele', 'deeeelde', 'strooompje']
        for wrd in spelltestlist:
            corrections = spellcorr(wrd)
            print(corrections)
        lemmalist = ['bureau', 'productie', 'pannenkoek']
        for lemma in lemmalist:
            alternatives = lemma_alt(lemma)
            print(alternatives)

    if lemmatest:
        # newlemma = normaliselemma('A-elementen', 'A-element', lemmatest=True)
        # newlemma = normaliselemma('Antillianen', 'Antilliaan', lemmatest=True)
        newlemma = normaliselemma(
            'Parlementslid', 'parlementslid', lemmatest=True)
        print(newlemma)
        lassytyposfn = './lemmatests/lassytypos.xlsx'
        lassytypoheader, lassytypos = xlsx.getxlsxdata(lassytyposfn)
        lassytyposdict = {}
        for rec in lassytypos:
            lassytyposdict[rec[0]] = rec[3]
        infilename = './lemmatests/LassyKlein_nword+lemma.xlsx'
        header, data = xlsx.getxlsxdata(infilename)
        for rec in data:
            word = rec[0]
            reflemma = rec[1]
            newlemma = normaliselemma(word, reflemma, lemmatest=True)
            if newlemma is None or newlemma != reflemma:
                if word in lassytyposdict and lassytyposdict[word] != "bingo":
                    pass
                else:
                    print(f'{word}\t{newlemma}\t{reflemma}')
