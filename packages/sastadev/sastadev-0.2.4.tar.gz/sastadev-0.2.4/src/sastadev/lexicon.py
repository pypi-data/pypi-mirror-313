'''
The lexicon module is the interface to the lexicon.
It is intended to abstract from the concrete lexicon used.

Currently we especially use the CELEX lexicon.
This module also contains some special word lists. Perhaps we should set up a special Exception List module
for this purpose.


'''
import os
from typing import Any, Dict, List, Optional

from sastadev import celexlexicon, treebankfunctions
from sastadev.conf import settings
from sastadev.namepartlexicon import (namepart_isa_namepart,
                                      namepart_isa_namepart_uc)
from sastadev.readcsv import readcsv
from sastadev.sastatypes import CELEX_INFL, DCOITuple, Lemma, SynTree, WordInfo

space = ' '

celex = 'celex'
alpino = 'alpino'

# the CHAT codes xxx and yyy must be recognised as valid codes and as valid words in some cases
chatspecials = ['xxx', 'yyy']


lexicon = celex

#Alpino often analyses certain words as tsw though they should be analysed as nouns
tswnouns = ['baby', 'jongen', 'juf', 'juffrouw', 'mam', 'mama', 'mamma', 'meisje', 'mens', 'meneer', 'mevrouw',
            'pap', 'papa', 'pappa', 'stouterd', 'opa', 'oma']

de = '1'
het = '2'
# List of de-determiners, List of corresponding het-determiners, and implicitly by this a mapping between the two
dets = {}
dets[de] = ['de', 'die', 'deze', 'onze', 'welke', 'iedere', 'elke', 'zulke']
dets[het] = ['het', 'dat', 'dit', 'ons', 'welk', 'ieder', 'elk', 'zulk']

def initializelexicon(lexiconfilename) -> set:
    lexicon = set()
    fptuples = readcsv(lexiconfilename, header=False)
    for _, fp in fptuples:
        strippedword = fp[0].strip()
        lexicon.add(strippedword)
    return lexicon

def initializelexicondict(lexiconfilename) -> Dict[str,str]:
    lexicon = {}
    fptuples = readcsv(lexiconfilename, header=False)
    for _, fp in fptuples:
        strippedword = fp[0].strip()
        strippedreplacement = fp[1].strip()
        lexicon[strippedword] = strippedreplacement
    return lexicon


def isa_namepart(word: str) -> bool:
    '''
    is the word a name part
    :param word:
    :return:
    '''
    return namepart_isa_namepart(word)


def isa_namepart_uc(word: str) -> bool:
    '''
    is the word in upper case a name part
    :param word:
    :return:
    '''
    return namepart_isa_namepart_uc(word)


def lookup(dct: Dict[str, Any], key: str) -> str:
    '''
    looks up key in dct, if so it returns dct[key] else ''
    :param dct:
    :param key:
    :return:
    '''
    result = dct[key] if key in dct else ''
    return result


def pvinfl2dcoi(word: str, infl: CELEX_INFL, lemma: Lemma) -> Optional[DCOITuple]:
    '''
    encodes the CELEX code infl for word (which must be a pv) as a DCOI Tuple
    at least if the CELEX lexicon is used, else None
    :param word:
    :param infl:
    :param lemma:
    :return:
    '''
    if lexicon == celex:
        results = celexlexicon.celexpv2dcoi(word, infl, lemma)
        wvorm = lookup(results, 'wvorm')
        pvtijd = lookup(results, 'pvtijd')
        pvagr = lookup(results, 'pvagr')
        positie = lookup(results, 'positie')
        buiging = lookup(results, 'buiging')
        dcoi_infl = []
        atts = [wvorm, pvtijd, pvagr, positie, buiging]
        for att in atts:
            if att != '':
                dcoi_infl.append(att)
        result = tuple(dcoi_infl)
    else:
        result = None
    return result


def getwordposinfo(word: str, pos: str) -> List[WordInfo]:
    '''
    yields the list of WordInfo for word str with part of speech code pos by looking it up in the lexicon in use
    :param word:
    :param pos:
    :return:
    '''
    results = []
    if lexicon == celex:
        results = celexlexicon.getwordposinfo(word, pos)
    return results


def getwordinfo(word: str) -> List[WordInfo]:
    '''
    yields the list of WordInfo for word str  by looking it up in the lexicon in use
    :param word:
    :return:
    '''
    results = []
    if lexicon == celex:
        results = celexlexicon.getwordinfo(word)
    return results


def informlexicon(word: str) -> bool:
    '''
    checks whether word is in the  word form lexicon
    :param word:
    :return:
    '''
    allwords = word.split(space)
    result = True
    for aword in allwords:
        if lexicon == 'celex':
            result = result and celexlexicon.incelexdmw(aword)
        elif lexicon == 'alpino':
            result = False
        else:
            result = False
    return result


def informlexiconpos(word: str, pos: str) -> bool:
    '''
    checks whether word with part of speech code pos is in the word form lexicon
    :param word:
    :param pos:
    :return:
    '''

    allwords = word.split(space)
    result = True
    for aword in allwords:
        if lexicon == 'celex':
            result = result and celexlexicon.incelexdmwpos(aword, pos)
        elif lexicon == 'alpino':
            result = False
        else:
            result = False
    return result


def chatspecial(word: str) -> bool:
    result = word in chatspecials
    return result


def known_word(word: str) -> bool:
    '''
    a word is considered to be a known_word if it occurs in the word form lexicon,
    if it is a name part, or if it is a chatspecial item
    :param word:
    :return:
    '''
    result = informlexicon(word) or isa_namepart(word) or chatspecial(word)
    return result


def getinflforms(thesubj: SynTree, thepv: SynTree, inversion: bool) -> List[str]:
    '''
    yields the list of  finite verb word forms that
    -agrees with the subject node (thesubj),
    -has the same lemma as the word form in the pv node
    -is compatible with whether there is inversion or not
    :param thesubj:
    :param thepv:
    :param inversion:
    :return:
    '''
    if lexicon == 'celex':
        pt = treebankfunctions.getattval(thepv, 'pt')
        pos = celexlexicon.pos2posnum[pt]
        infl = celexlexicon.dcoiphi2celexpv(thesubj, thepv, inversion)
        lemma = treebankfunctions.getattval(thepv, 'lemma')
        results = celexlexicon.getinflforms(lemma, pos, infl)
    else:
        results = []
    return results

nochildwordsfilename = 'nochildwords.txt'
nochildwordsfolder = 'data/nochildwords'
nochildwordsfullname = os.path.join(settings.SD_DIR, nochildwordsfolder, nochildwordsfilename)
nochildwords = initializelexicon(nochildwordsfullname)

lexiconfoldername = 'data/wordsunknowntoalpino'
wordsunknowntoalpinofilename = 'wordsunknowntoalpino.txt'
wordsunknowntoalpinofullname = os.path.join(settings.SD_DIR, lexiconfoldername, wordsunknowntoalpinofilename)
wordsunknowntoalpinolexicondict = initializelexicondict(wordsunknowntoalpinofullname)
