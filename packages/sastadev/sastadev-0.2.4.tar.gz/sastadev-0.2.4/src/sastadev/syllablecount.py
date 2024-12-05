import os
import re
from typing import List

from sastadev.readcsv import readcsv
from sastadev.stringfunctions import (dutch_base_diphthongs,
                                      dutch_base_triphthongs,
                                      dutch_trema_diphthongs, tremavowels,
                                      vowels)
from sastadev.xlsx import mkworkbook

qupattern = fr'([Qq])([Uu])([^{tremavowels}])'
qure = re.compile(qupattern)

yogapattern = '^y'
yogare = re.compile(yogapattern)

ouillpattern = r'(ou)(i)(ll)'
ouillre = re.compile(ouillpattern)

ieuwpattern = r'([EeIi]e)(u)(w)'
ieuwre = re.compile(ieuwpattern)

syllable_exception_dictionary = {
    'cacao': 2, 'cue': 1, 'camargue': 3, 'bye': 1, 'Paraguay': 3}
syll1vseqs = ['aau', 'ai', 'ay', 'eoi', 'eui', 'ey', 'eau',
              'oeu', 'oey', 'oi', 'ooy', 'oy', 'uay', 'uei', 'uy']
syll2vseqs = ['aaa', 'aaia', 'aaie', 'aaiee', 'aaii', 'aaio', 'aaioe', 'ae', 'aea', 'aee', 'aeo', 'aeu',
              'aia', 'aie', 'aii', 'aio', 'ao', 'aoe', 'aoo', 'aou', 'aue', 'ayee', 'ayeu', 'ea', 'eaa',
              'eaai', 'eae', 'eai', 'eea', 'eeaa', 'eeau', 'eee', 'eeee', 'eeei', 'eei', 'eeie', 'eeo',
              'eeoe', 'eeoo', 'eia', 'eiaa', 'eie', 'eii', 'eio', 'eo', 'eoe', 'eoo', 'eou', 'eue', 'euu',
              'ia', 'iaa', 'iae', 'iai', 'iau', 'iea', 'ieaa', 'ieau', 'iee', 'ieee', 'iei', 'ieo', 'ieoe',
              'ieoo', 'ieou', 'ieu', 'ieui', 'ieuo', 'ieuu', 'ii', 'iie', 'io', 'ioe', 'ioo', 'iou',
              'iu', 'oa', 'oai', 'oau', 'oea', 'oeaa', 'oee', 'oeee', 'oeei', 'oeia', 'oeiaa', 'oeie',
              'oeiee', 'oeii', 'oeio', 'oeo', 'oeoo', 'oia', 'oie', 'ooe', 'ooia', 'ooiau', 'ooie', 'ooiee',
              'ooii', 'ooio', 'ooioo', 'oua', 'ouai', 'oue', 'ouee', 'oui', 'oyaa', 'oyau', 'oyee', 'oyeu',
              'ua', 'uaa', 'uai', 'ue', 'uee', 'ueu', 'uia', 'uiaa', 'uie', 'uii', 'uo', 'uoo', 'ya', 'yaa',
              'ye', 'yi', 'yo', 'yoo']
syll3vseqs = ['aaieo', 'aaieoo', 'aoi', 'eao', 'eeeie',
              'eeeii', 'eoa', 'ioa', 'ioui', 'oeieo', 'oeieoo']

voweltierpattern = f'[{vowels}]+'
voweltierre = re.compile(voweltierpattern)

vowelyvowels = [f'{v1}y{v2}' for v1 in vowels for v2 in vowels]

vowelsyllpairs = [(1, dutch_base_diphthongs + dutch_trema_diphthongs + dutch_base_triphthongs + syll1vseqs),
                  (2, vowelyvowels + syll2vseqs),
                  (3, syll3vseqs)]
vowelsylldict = {vs: cnt for (cnt, vslist) in vowelsyllpairs for vs in vslist}


def countsyllables(word: str) -> int:
    # if in exceptiondictionary return value
    lcword = word.lower()
    if lcword in syllable_exception_dictionary:
        return syllable_exception_dictionary[lcword]
    # deal with hyphens
    wordparts = lcword.split('-')
    if len(wordparts) > 1:
        syllcounts = [countsyllables(part) for part in wordparts]
        adjustedsyllcounts = [cnt if cnt != 0 else 1 for cnt in syllcounts]
        result = sum(adjustedsyllcounts)
        return result

    # do necessary replacements
    reducedword = lcword
    # remove u after q unless followed by tremavowel
    reducedword = qure.sub(r'\1\3', reducedword)
    # remove y at the beginning of a word (yoga v. halcyon) will not work in compounds hulpyogi
    reducedword = yogare.sub(r'', reducedword)
    # oui -> ou before ll
    reducedword = ouillre.sub(r'\1\3', reducedword)
    # ieuw, eeuw -> iew, eew
    reducedword = ieuwre.sub(r'\1\3', reducedword)

    # compute the vowel tier: List[str]
    vt = getvoweltier(reducedword)

    countlist = [vowelsyllcount(el) for el in vt]

    result = sum(countlist)
    return result


def getvoweltier(word: str) -> List[str]:
    matches = voweltierre.finditer(word)
    result = [match.group() for match in matches]
    return result


def vowelsyllcount(word: str) -> int:
    if len(word) == 1:
        result = 1
    else:
        cutoff = getfirsttremavowelpos(word)
        if cutoff >= 0:
            result = vowelsyllcount(
                word[:cutoff]) + vowelsyllcount(word[cutoff:])
        elif word in vowelsylldict:
            result = vowelsylldict[word]
        else:
            print(f'unknown vowel sequence:{word}')
            result = len(word)
    return result


def getfirsttremavowelpos(word: str) -> int:
    for i, char in enumerate(word):
        if char in tremavowels:
            return i
    return -1


def test1():
    wordlist = ['B-kant', 'ABC-biljet', 'A-B-C-actie', 'cue', 'aan', 'na', 'baan', 'cadeau', 'chaos', 'naäpen',
                'be-edigen', 'haaibaai', 'iaen', 'iaën',
                'eeuw', 'kieuw', ]
    for word in wordlist:
        vt = getvoweltier(word)
        print(word, vt)
        for vs in vt:
            cnt = vowelsyllcount(vs)
            print(f'---{vs}: {cnt}')


def test2():
    reflist = [('B-kant', 2), ('ABC-biljet', 3), ('A-B-C-actie', 5), ('cue', 1), ('aan', 1), ('na', 1), ('baan', 1),
               ('cadeau', 2), ('chaos', 2), ('naäpen', 3),
               ('be-edigen', 4), ('haaibaai', 2), ('iaen',
                                                   2), ('iaën', 3), ('eeuw', 1), ('kieuw', 1),
               ('koeieoog', 3), ('expressfout', 2), ('desavoueer', 4)]
    fail = False
    cntr = 0
    for word, refcnt in reflist:
        cntr += 1
        sc = countsyllables(word)
        try:
            assert sc == refcnt
        except Exception:
            mark = 'OK' if sc == refcnt else 'NO'
            print(f'{mark}: word={word}, result={sc}, ref={refcnt}')
            fail = True
    print(f'{cntr} tests performed')
    if fail:
        raise AssertionError


def celextest():
    celexreffilename = './celexsyllables/celexsyllablequeryresults.txt'
    data = readcsv(celexreffilename, header=True, sep='\\', quotechar="[")
    diffdata = []
    diffcounter = 0
    for i, row in data:
        word = row[0]
        refcnt = int(row[2])
        sc = countsyllables(word)
        if sc != refcnt:
            diffcounter += 1
            diffrow = [word, sc, refcnt]
            diffdata.append(diffrow)
            # print(f'NO: word={word}, result={sc}, ref={refcnt}')
    print(f'{diffcounter} differences found')
    outfilename = 'syllcount_celex_mismatches.xlsx'
    outpath = r'D:\Dropbox\jodijk\Utrecht\Projects\SASTA emer\syllablecount'
    outfullname = os.path.join(outpath, outfilename)
    diffheader = ['word', 'syllcount', 'refcount']
    wb = mkworkbook(outfullname, [diffheader], diffdata, freeze_panes=(1, 0))
    wb.close()


if __name__ == '__main__':
    # test1()
    # test2()
    celextest()
