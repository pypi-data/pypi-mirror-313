''''
to be added
'''

import copy
import re
from typing import Any, Callable, Dict, List, Optional, Tuple

from sastadev.alpino import getdehetwordinfo
from sastadev.basicreplacements import (basicexpansions, basicreplacements,
                                        getdisambiguationdict)
from sastadev.cleanCHILDEStokens import cleantokens
from sastadev.conf import settings
from sastadev.dedup import (cleanwordofnort, find_duplicates2,
                            find_janeenouduplicates, find_simpleduplicates,
                            find_substringduplicates2, getfilledpauses,
                            getprefixwords, getrepeatedtokens,
                            getunwantedtokens, nodesfindjaneenou)
from sastadev.deregularise import correctinflection
from sastadev.find_ngram import (Ngram, findmatches, ngram1, ngram2, ngram7,
                                 ngram10, ngram11, ngram16, ngram17)
from sastadev.iedims import getjeforms
from sastadev.lexicon import (WordInfo, de, dets, getwordinfo, het,
                              informlexicon, isa_namepart, known_word,
                              tswnouns, wordsunknowntoalpinolexicondict)
from sastadev.macros import expandmacros
from sastadev.metadata import (Meta, bpl_indeze, bpl_node, bpl_none, bpl_word,
                               bpl_wordlemma, defaultbackplacement,
                               defaultpenalty, filled_pause, fstoken, intj,
                               janeenou, longrep, mkSASTAMeta, repeated,
                               repeatedjaneenou, repeatedseqtoken, shortrep,
                               substringrep, unknownsymbol)
from sastadev.sasta_explanation import explanationasreplacement
from sastadev.sastatoken import Token, tokenlist2stringlist
from sastadev.sastatypes import (BackPlacement, MethodName, Nort, Penalty,
                                 Position, SynTree, UttId)
from sastadev.smallclauses import smallclauses
from sastadev.stringfunctions import (chatxxxcodes, consonants, deduplicate,
                                      endsinschwa, fullworddehyphenate,
                                      monosyllabic, vowels)
from sastadev.sva import getsvacorrections
from sastadev.tokenmd import TokenListMD, TokenMD, mdlist2listmd
from sastadev.treebankfunctions import (fatparse, getattval, getnodeyield,
                                        showtree)

Correction = Tuple[List[Token], List[Meta]]
MetaCondition = Callable[[Meta], bool]

SASTA = 'SASTA'

hyphen = '-'
repetition = 'Repetition'

replacepattern = '{} [: {} ]'
metatemplate = '##META {} {} = {}'
slash = '/'
space = ' '

#: The constant *disambiguationdict* contains words that should be replaced by a
#: different word to avoid unwanted readings of the original word. It is filled by a
#: call to the function *getdisambiguationdict* from the module *basicreplacements*.
#:
#: .. autofunction:: basicreplacements::getdisambiguationdict
#:
disambiguationdict = getdisambiguationdict()

#: The constant *wrongdet_excluded_words* contains words that lead to incorrect
#: replacement of uter determiners (e.g. *die zijn* would be replaced by *dat zijn*) and
#: therefore have to be excluded from determiner replacement.
wrongdet_excluded_words = ['zijn', 'dicht', 'met', 'ik']


class Ngramcorrection:
    def __init__(self, ngram, fpositions, cpositions, metafunction):
        self.ngram: Ngram = ngram
        self.fpositions: Tuple[Position, Position] = fpositions
        self.cpositions: Tuple[Position, Position] = cpositions
        self.metafunction = metafunction


def mkmeta(att: str, val: str, type: str = 'text') -> str:
    result = metatemplate.format(type, att, val)
    return result


def anychars(chars: str) -> str:
    result = '[' + chars + ']'
    return result


def opt(pattern: str) -> str:
    result = '(' + pattern + ')?'
    return result


def replacement(inword: str, outword: str) -> str:
    result = replacepattern.format(inword, outword)
    return result


# duppattern = r'(.)\1{2,}'
# dupre = re.compile(duppattern)
#: The pattern *gaatiepattern* identifies words ending in *tie* preceded by at least a
#: vowel and optionally a consonant.
gaatiepattern = r'^.*' + anychars(vowels) + opt(anychars(consonants)) + 'tie$'
gaatiere = re.compile(gaatiepattern)
gaattiepattern = r'^.*' + anychars(vowels) + 'ttie$'
gaattiere = re.compile(gaattiepattern)
neutersgnoun = 'boekje'  # select here an unambiguous neuter noun


def skiptokens(tokenlist: List[Token], skiptokenlist: List[Token]) -> List[Token]:
    '''

    :param tokenlist:
    :param skiptokenlist:
    :return: a tokenlist identical to the input tokenlist but with the tokens that also occur with the same pos
    in skiptokenlist marked with skip=True
    '''
    skippositions = {token.pos for token in skiptokenlist}
    resultlist = []
    for token in tokenlist:
        if token.pos in skippositions:
            newtoken = Token(token.word, token.pos, skip=True)
        else:
            newtoken = token
        resultlist.append(newtoken)
    return resultlist


def ngramreduction(reducedtokens: List[Token], token2nodemap: Dict[Token, SynTree], allremovetokens: List[Token],
                   allremovepositions: List[Position], allmetadata: List[Meta], ngramcor: Ngramcorrection) \
        -> Tuple[List[Token], List[Token], List[Meta]]:
    # metadat function should still be added / abstracted
    (fb, fe) = ngramcor.fpositions
    (cb, ce) = ngramcor.cpositions
    reducedleaves = [token2nodemap[tok.pos] for tok in reducedtokens]

    vnwpvvnwpvmatches = findmatches(ngramcor.ngram, reducedleaves)
    allfalsestarttokens = []
    metadata = []
    for match in vnwpvvnwpvmatches:
        positions = [pos for pos in range(match[0], match[1])]
        falsestartpositions = [tok.pos for i, tok in enumerate(
            reducedtokens) if i in positions[fb:fe]]
        falsestarttokens = [
            tok for tok in reducedtokens if tok.pos in falsestartpositions]
        allfalsestarttokens += falsestarttokens
        correcttokenpositions = [tok.pos for i, tok in enumerate(
            reducedtokens) if i in positions[cb:ce]]
        correcttokens = [
            tok for tok in reducedtokens if tok.pos in correcttokenpositions]
        allremovetokens += falsestarttokens
        allremovepositions += falsestartpositions
        metadata += ngramcor.metafunction(falsestarttokens,
                                          falsestartpositions, correcttokens)
    reducedtokens = [
        tok for tok in reducedtokens if tok not in allfalsestarttokens]
    allmetadata += metadata
    return reducedtokens, allremovetokens, allmetadata


def reduce(tokens: List[Token], tree: Optional[SynTree]) -> Tuple[List[Token], List[Meta]]:
    if tree is None:
        settings.LOGGER.error(
            'No tree for :{}\nNo reduction applied'.format(tokens))
        return ((tokens, []))

    tokennodes = tree.xpath('.//node[@pt or @pos]')
    tokennodesdict = {int(getattval(n, 'begin')): n for n in tokennodes}
    token2nodemap = {token.pos: tokennodesdict[token.pos]
                     for token in tokens if keycheck(token.pos, tokennodesdict)}

    reducedtokens = tokens
    allmetadata = []

    allremovetokens = []
    allremovepositions = []

    # throw out unwanted symbols - -- # etc
    unwantedtokens = getunwantedtokens(reducedtokens)
    unwantedpositions = [tok.pos for tok in unwantedtokens]
    allremovetokens += unwantedtokens
    allremovepositions += unwantedpositions
    reducedtokens = [n for n in reducedtokens if n not in unwantedtokens]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical',
                            unknownsymbol, 'Syntax') for token in unwantedtokens]
    allmetadata += metadata

    # remove  filled pauses

    filledpausetokens = getfilledpauses(reducedtokens)
    filledpausepositions = [token.pos for token in filledpausetokens]
    allremovetokens += filledpausetokens
    allremovepositions += filledpausepositions
    reducedtokens = [
        tok for tok in reducedtokens if tok not in filledpausetokens]
    reducednodes = [token2nodemap[tok.pos]
                    for tok in reducedtokens if keycheck(tok.pos, token2nodemap)]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical',
                            filled_pause, 'Syntax') for token in filledpausetokens]
    allmetadata += metadata

    # remove tsw incl goh och hé oke but not ja, nee, nou
    tswtokens = [n for n in reducedtokens if n.pos in token2nodemap
                 and getattval(token2nodemap[n.pos], 'pt') == 'tsw'
                 and getattval(token2nodemap[n.pos], 'lemma') not in {'ja', 'nee', 'nou'}
                 and getattval(token2nodemap[n.pos], 'lemma') not in tswnouns]
    tswpositions = [n.pos for n in tswtokens]
    allremovetokens += tswtokens
    allremovepositions == tswpositions
    reducedtokens = [n for n in reducedtokens if n not in tswtokens]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical',
                            intj, 'Syntax') for token in tswtokens]
    allmetadata += metadata

    # find duplicatenode repetitions of ja, nee, nou
    janeenouduplicatenodes = find_janeenouduplicates(reducedtokens)
    allremovetokens += janeenouduplicatenodes
    reducedtokens = [
        n for n in reducedtokens if n not in janeenouduplicatenodes]
    reducednodes = [token2nodemap[tok.pos]
                    for tok in reducedtokens if keycheck(tok.pos, token2nodemap)]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical', repeatedjaneenou, 'Syntax', subcat=repetition)
                for token in janeenouduplicatenodes]
    allmetadata += metadata

    # ASTA sec 6.3 p. 11
    # remove ja nee nou

    janeenounodes = nodesfindjaneenou(reducednodes)
    janeenoutokens = [tok for tok in reducedtokens if
                      keycheck(tok.pos, token2nodemap) and token2nodemap[tok.pos] in janeenounodes]
    janeenoupositions = [token.pos for token in janeenoutokens]
    allremovetokens += janeenoutokens
    allremovepositions += janeenoupositions
    reducedtokens = [tok for tok in reducedtokens if tok not in janeenoutokens]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical',
                            janeenou, 'Syntax') for token in janeenoutokens]
    allmetadata += metadata

    # short repetitions
    def oldcond(x: Nort, y: Nort) -> bool:
        return len(cleanwordofnort(x)) / len(cleanwordofnort(y)) < .5 and not informlexicon(cleanwordofnort(x))

    def cond(x: Nort, y: Nort) -> bool:
        return len(cleanwordofnort(x)) / len(cleanwordofnort(
            y)) < .5  # check on lexicon put off actually two variants should be tried if the word is an existin gword

    shortprefixtokens = getprefixwords(reducedtokens, cond)
    shortprefixpositions = [token.pos for token in shortprefixtokens]
    repeatedtokens = getrepeatedtokens(reducedtokens, shortprefixtokens)
    allremovetokens += shortprefixtokens
    allremovepositions += shortprefixpositions
    metadata = [
        mkSASTAMeta(token, repeatedtokens[token], 'ExtraGrammatical', shortrep, 'Tokenisation', subcat=repetition) for
        token in reducedtokens if token in repeatedtokens]
    allmetadata += metadata
    reducedtokens = [
        tok for tok in reducedtokens if tok not in shortprefixtokens]

    # long repetitions
    def longcond(x: Nort, y: Nort) -> bool:
        return len(cleanwordofnort(x)) / len(cleanwordofnort(y)) >= .5 and not informlexicon(cleanwordofnort(x))

    longprefixtokens = getprefixwords(reducedtokens, longcond)
    longprefixpositions = [token.pos for token in longprefixtokens]
    repeatedtokens = getrepeatedtokens(reducedtokens, longprefixtokens)
    allremovetokens += longprefixtokens
    allremovepositions += longprefixpositions
    metadata = [
        mkSASTAMeta(token, repeatedtokens[token], 'ExtraGrammatical', longrep, 'Tokenisation', subcat=repetition) for
        token in reducedtokens if token in repeatedtokens]
    allmetadata += metadata
    reducedtokens = [
        tok for tok in reducedtokens if tok not in longprefixtokens]

    # find unknown words that are a substring of their successor
    substringtokens, _ = find_substringduplicates2(reducedtokens)
    substringpositions = [token.pos for token in substringtokens]
    repeatedtokens = getrepeatedtokens(reducedtokens, substringtokens)
    allremovetokens += substringtokens
    allremovepositions += substringpositions
    metadata = [mkSASTAMeta(token, repeatedtokens[token], 'ExtraGrammatical', substringrep, 'Tokenisation',
                            subcat=repetition) for token in reducedtokens if token in repeatedtokens]
    allmetadata += metadata
    reducedtokens = [
        tok for tok in reducedtokens if tok not in substringtokens]

    # simple duplicates
    dupnodetokens = find_simpleduplicates(reducedtokens)
    dupnodepositions = [token.pos for token in dupnodetokens]
    repeatedtokens = getrepeatedtokens(reducedtokens, dupnodetokens)
    allremovetokens += dupnodetokens
    allremovepositions += dupnodepositions
    metadata = [mkSASTAMeta(token, repeatedtokens[token], 'ExtraGrammatical',
                            repeated, 'Tokenisation', subcat=repetition) for token in reducedtokens if
                token in repeatedtokens]
    allmetadata += metadata
    reducedtokens = [tok for tok in reducedtokens if tok not in dupnodetokens]

    # duplicate sequences
    dupnodetokens, dupinfo = find_duplicates2(reducedtokens)
    dupnodepositions = [token.pos for token in dupnodetokens]
    duppairs = []
    for token in dupnodetokens:
        for othertok in reducedtokens:
            if token.pos in dupinfo.longdups and othertok.pos == dupinfo.longdups[token.pos]:
                nwt = othertok
                duppairs.append((token, nwt))
                break
    allremovetokens += dupnodetokens
    allremovepositions += dupnodepositions
    metadata = [mkSASTAMeta(token, nwt, 'ExtraGrammatical',
                            repeatedseqtoken, 'Tokenisation', subcat=repetition)
                for token, nwt in duppairs]
    allmetadata += metadata
    reducedtokens = [tok for tok in reducedtokens if tok not in dupnodetokens]

    # remove unknown words if open class DO NOT DO this
    # unknown_word_tokens = [tok for tok in reducedtokens if getattval(token2nodemap[tok.pos], 'pt') in openclasspts
    #                        and not (asta_recognised_wordnode(token2nodemap[tok.pos]))]
    # unknown_word_positions = [token.pos for token in unknown_word_tokens]
    # allremovetokens += unknown_word_tokens
    # allremovepositions += unknown_word_positions
    # metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical',
    #                         unknownword, 'Tokenisation')
    #             for token in reducedtokens if token in unknown_word_tokens]
    # allmetadata += metadata
    # reducedtokens = [n for n in reducedtokens if n not in unknown_word_tokens]

    # ngram based cases

    # vnw pv vnw pv

    def metaf(falsestarttokens: List[Token], falsestartpositions: List[Position], correcttokens: List[Token]) \
            -> List[Meta]:
        return \
            [Meta('Retracing', 'Retracing with Correction', annotatedposlist=falsestartpositions,
                  annotatedwordlist=[c.word for c in falsestarttokens],
                  annotationposlist=[c.pos for c in correcttokens],
                  annotationwordlist=[c.word for c in correcttokens], cat='Retracing', subcat=None, source=SASTA,
                  penalty=defaultpenalty, backplacement=bpl_none)] + \
            [mkSASTAMeta(ftoken, ctoken, 'Retracing with Correction', fstoken, 'Retracing')
             for ftoken, ctoken in zip(falsestarttokens, correcttokens)]

    vnwpvvnwpvcor = Ngramcorrection(ngram1, (0, 2), (2, 4), metaf)
    reducedtokens, allremovetokens, allmetadata = ngramreduction(reducedtokens, token2nodemap, allremovetokens,
                                                                 allremovepositions, allmetadata, vnwpvvnwpvcor)

    vzdetvzdetcor = Ngramcorrection(ngram2, (0, 2), (2, 4), metaf)
    reducedtokens, allremovetokens, allmetadata = ngramreduction(reducedtokens, token2nodemap, allremovetokens,
                                                                 allremovepositions, allmetadata, vzdetvzdetcor)

    vgdetvgdetcor = Ngramcorrection(ngram7, (0, 2), (2, 4), metaf)
    reducedtokens, allremovetokens, allmetadata = ngramreduction(reducedtokens, token2nodemap, allremovetokens,
                                                                 allremovepositions, allmetadata, vgdetvgdetcor)
    vnwipvjxpvjvnwi = Ngramcorrection(ngram10, (0, 2), (3, 5), metaf)
    reducedtokens, allremovetokens, allmetadata = ngramreduction(reducedtokens, token2nodemap, allremovetokens,
                                                                 allremovepositions, allmetadata, vnwipvjxpvjvnwi)
    lemilemjlemilemj = Ngramcorrection(ngram11, (0, 2), (3, 5), metaf)
    reducedtokens, allremovetokens, allmetadata = ngramreduction(reducedtokens, token2nodemap, allremovetokens,
                                                                 allremovepositions, allmetadata, lemilemjlemilemj)

    dinjdknj = Ngramcorrection(ngram16, (0, 2), (3, 5), metaf)
    reducedtokens, allremovetokens, allmetadata = ngramreduction(reducedtokens, token2nodemap, allremovetokens,
                                                                 allremovepositions, allmetadata, dinjdknj)

    tevtev = Ngramcorrection(ngram17, (0, 2), (2, 4), metaf)
    reducedtokens, allremovetokens, allmetadata = ngramreduction(reducedtokens, token2nodemap, allremovetokens,
                                                                 allremovepositions, allmetadata, tevtev)

    # reducedleaves = [token2nodemap[tok.pos] for tok in reducedtokens]
    #
    # vnwpvvnwpvmatches = findmatches(ngram1, reducedleaves)
    # allfalsestarttokens = []
    # metadata = []
    # for match in vnwpvvnwpvmatches:
    #     positions = [pos for pos in range(match[0], match[1])]
    #     falsestartpositions = [tok.pos for i, tok in enumerate(reducedtokens) if i in positions[0:2]]
    #     falsestarttokens = [tok for tok in reducedtokens if tok.pos in falsestartpositions]
    #     allfalsestarttokens += falsestarttokens
    #     correcttokenpositions = [tok.pos for i, tok in enumerate(reducedtokens) if i in positions[2:5]]
    #     correcttokens = [tok for tok in reducedtokens if tok.pos in correcttokenpositions]
    #     allremovetokens += falsestarttokens
    #     allremovepositions += falsestartpositions
    #     metadata += [Meta('Retracing', 'Retracing with Correction',  annotatedposlist=falsestartpositions,
    #                  annotatedwordlist=[c.word for c in falsestarttokens], annotationposlist=[c.pos for c in correcttokens],
    #                  annotationwordlist=[c.word for c in correcttokens], cat='Retracing', subcat=None, source=SASTA,
    #                     penalty=defaultpenalty, backplacement=bpl_none)]
    #     metadata += [mkSASTAMeta(ftoken, ctoken, 'Retracing with Correction', fstoken,  'Retracing', )
    #                 for ftoken, ctoken  in zip(falsestarttokens, correcttokens)]
    #
    # reducedtokens = [tok for tok in reducedtokens if tok not in allfalsestarttokens]
    # allmetadata += metadata

    skipmarkedtokens = skiptokens(tokens, allremovetokens)

    # return (reducedtokens, allremovetokens, allmetadata)
    return (skipmarkedtokens, allmetadata)


def keycheck(key: Any, dict: Dict[Any, Any]) -> bool:
    if key not in dict:
        settings.LOGGER.error(
            'key {}  not in dictionary. Contents of dictionary:'.format(key))
        for akey, val in dict.items():
            valbgn = getattval(val, 'begin')
            valpt = getattval(val, 'pt')
            valword = getattval(val, 'word')
            valstr = '{}:{}:{}'.format(valbgn, valpt, valword)
            settings.LOGGER.error('{}={}'.format(akey, valstr))
    return key in dict


def combinesorted(toklist1: List[Token], toklist2: List[Token]) -> List[Token]:
    result = toklist1 + toklist2
    sortedresult = sorted(result, key=lambda tok: tok.pos)
    return sortedresult


# def getcorrection(utt, tree=None, interactive=False):
#     # NOT used anymore!!!!
#
#     allmetadata = []
#     rawtokens = sasta_tokenize(utt)
#     wordlist = tokenlist2stringlist(rawtokens)
#
#     tokens, metadata = cleantokens(rawtokens, repkeep=False)
#     allmetadata += metadata
#     tokensmd = TokenListMD(tokens, [])
#
#     # reducedtokens, allremovedtokens, metadata = reduce(tokens)
#     # allremovedtokens, metadata = reduce(tokens)
#     skipmarkedtokens, metadata = reduce(tokens, tree)
#     # reducedtokensmd = TokenListMD(reducedtokens, [])
#     reducedtokensmd = TokenListMD(skipmarkedtokens, [])
#
#     alternativemds = getalternatives(reducedtokensmd, tree, 0)
#     # alternativemds = getalternatives(tokensmd, allremovedtokens, tree, 0)
#     # unreducedalternativesmd = [TokenListMD(combinesorted(alternativemd.tokens, allremovedtokens), alternativemd.metadata) for alternativemd in alternativemds]
#
#     # correctiontokensmd = unreducedalternativesmd[-1] if unreducedalternativesmd != [] else tokensmd
#     correctiontokensmd = alternativemds[-1] if alternativemds != [] else tokensmd
#
#     correction = tokenlist2stringlist(correctiontokensmd.tokens)
#     allmetadata += correctiontokensmd.metadata
#
#     result = (correction, allmetadata)
#     return result


def getcorrections(rawtokens: List[Token], method: MethodName, tree: Optional[SynTree] = None,
                   interactive: bool = False) -> List[Correction]:
    allmetadata = []
    # rawtokens = sasta_tokenize(utt)
    wordlist = tokenlist2stringlist(rawtokens)
    utt = space.join(wordlist)
    origutt = utt
    # print(utt)

    # check whether the tree has the same yield
    origtree = tree
    treeyield = getnodeyield(tree)
    treewordlist = [getattval(n, 'word') for n in treeyield]

    if treewordlist != wordlist:
        revisedutt = space.join(wordlist)
        tree = fatparse(revisedutt, rawtokens)

    tokens, metadata = cleantokens(rawtokens, repkeep=False)
    allmetadata += metadata
    tokensmd = TokenListMD(tokens, [])

    # check whether there is a utterance final multiword explanation, and if so, align it with the utterance
    # use this aligned utterance as the correction, clean it, parse it

    # reducedtokens, allremovedtokens, metadata = reduce(tokens)
    reducedtokens, metadata = reduce(tokens, tree)
    reducedtokensmd = TokenListMD(reducedtokens, [])
    allmetadata += metadata

    # alternativemds = getalternatives(reducedtokensmd, tree, 0)
    alternativemds = getalternatives(reducedtokensmd, method, tree, '0')
    # unreducedalternativesmd = [TokenListMD(combinesorted(alternativemd.tokens, allremovedtokens), alternativemd.metadata) for alternativemd in alternativemds]

    intermediateresults = alternativemds if alternativemds != [] else [tokensmd]

    results = []
    for ctmd in intermediateresults:
        # correction = tokenlist2stringlist(ctmd.tokens)
        correction = ctmd.tokens
        themetadata = allmetadata + ctmd.metadata
        results.append((correction, themetadata))
    return results


# def getalternatives(origtokensmd, method, llremovedtokens, tree, uttid):
def getalternatives(origtokensmd: TokenListMD, method: MethodName, tree: SynTree, uttid: UttId):
    newtokensmd = explanationasreplacement(origtokensmd, tree)
    if newtokensmd is not None:
        tokensmd = newtokensmd
    else:
        tokensmd = origtokensmd

    tokens = tokensmd.tokens
    allmetadata = tokensmd.metadata
    # newtokens = []
    # alternatives = []
    alternativetokenmds = {}
    validalternativetokenmds = {}
    tokenctr = 0
    for token in tokens:
        tokenmd = TokenMD(token, allmetadata)
        alternativetokenmds[tokenctr] = getalternativetokenmds(
            tokenmd, method, tokens, tokenctr, tree, uttid)
        validalternativetokenmds[tokenctr] = getvalidalternativetokenmds(
            tokenmd, alternativetokenmds[tokenctr])
        tokenctr += 1

    # get all the new token sequences
    tokenctr = 0
    lvalidalternativetokenmds = len(validalternativetokenmds)
    altutts: List[List[TokenMD]] = [[]]
    newutts = []
    while tokenctr < lvalidalternativetokenmds:
        for tokenmd in validalternativetokenmds[tokenctr]:
            for utt in altutts:
                newutt = copy.copy(utt)
                newutt.append(tokenmd)
                newutts.append(newutt)
        altutts = newutts
        newutts = []
        tokenctr += 1

    # now turn each sequence of (token, md) pairs into a pair (tokenlist, mergedmetadata)
    newaltuttmds = []
    for altuttmd in altutts:
        if altuttmd != []:
            newaltuttmd = mdlist2listmd(altuttmd)
            newaltuttmds.append(newaltuttmd)

    # basic expansions
    # put off, taken care of in getvalidalternatives:  + [tokensmd]
    allalternativemds = newaltuttmds

    newresults = []
    for uttmd in allalternativemds:
        expansionmds = getexpansions(uttmd)
        newresults += expansionmds
    allalternativemds += newresults

    # combinations of tokens or their alternatives: de kopje, de stukkie, heeft gevalt

    newresults = []
    for uttmd in allalternativemds:
        # utterance = space.join([token.word for token in uttmd.tokens])
        utterance, _ = mkuttwithskips(uttmd.tokens)
        fatntree = fatparse(utterance, uttmd.tokens)
        newresults += getwrongdetalternatives(uttmd, fatntree, uttid)
    allalternativemds += newresults

    newresults = []
    for uttmd in allalternativemds:
        # utterance = space.join([token.word for token in uttmd.tokens])
        utterance, _ = mkuttwithskips(uttmd.tokens)
        # reducedtokens = [t for t in uttmd.tokens if not t.skip]
        # reduceduttmd = TokenListMD(reducedtokens, uttmd.metadata)
        fatntree = fatparse(utterance, uttmd.tokens)
        debug = False
        if debug:
            showtree(fatntree)
        uttalternativemds = getsvacorrections(uttmd, fatntree, uttid)
        newresults += uttalternativemds
    allalternativemds += newresults

    newresults = []
    for uttmd in allalternativemds:
        # utterance = space.join([token.word for token in uttmd.tokens])
        utterance, _ = mkuttwithskips(uttmd.tokens)
        fatntree = fatparse(utterance, uttmd.tokens)
        newresults += correctPdit(uttmd, fatntree, uttid)
    allalternativemds += newresults

    newresults = []
    for uttmd in allalternativemds:
        utterance, _ = mkuttwithskips(uttmd.tokens)
        fatntree = fatparse(utterance, uttmd.tokens)
        newresults += smallclauses(uttmd, fatntree)
        # showtree(fatntree, text='fatntree')
    allalternativemds += newresults

    # final check whether the alternatives are improvements. It is not assumed that the original tokens is included in the alternatives
    finalalternativemds = lexcheck(tokensmd, allalternativemds)

    return finalalternativemds


skiptemplate = "[ @skip {} ]"


def oldmkuttwithskips(tokens: List[Token], toskip: List[Token]) -> str:
    sortedtokens = sorted(tokens, key=lambda x: x.pos)
    resultlist = []
    for token in sortedtokens:
        if token in toskip:
            resultlist.append(skiptemplate.format(token.word))
        else:
            resultlist.append(token.word)
    result = space.join(resultlist)
    return result


def mkuttwithskips(tokens: List[Token], delete: bool = True) -> Tuple[str, List[Position]]:
    sortedtokens = sorted(tokens, key=lambda x: x.pos)
    resultlist = []
    tokenposlist = []
    for token in sortedtokens:
        if token.skip:
            if not delete:
                resultlist.append(skiptemplate.format(token.word))
                tokenposlist.append(token.pos)
        else:
            resultlist.append(token.word)
            tokenposlist.append(token.pos)
    result = space.join(resultlist)

    return result, tokenposlist


def OLDgetexpansions(uttmd: TokenListMD) -> List[TokenListMD]:
    '''

    :param uttmd: the list of tokens in the utterance with its metadata
    :return: zero or more alternative lists of tokens with metadata

    The function *getexpansions* generates alternative tokenlists plus metadata for
    words that are contractions and must be expanded into a sequence of multiple tokens.
    It checks whether a word is a contraction by checking whether it occurs in the
    dictionary *basicexpansions* from the module *basicreplacements*

        .. autodata:: basicreplacements::basicexpansions
            :no-value:

    '''

    expansionfound = False
    newtokens = []
    tokenctr = 0
    # newtokenctr = 0
    tokenposlist = []
    newmd = uttmd.metadata
    for tokenctr, token in enumerate(uttmd.tokens):
        if token.word.lower() in basicexpansions:
            expansionfound = True
            for (rlist, c, n, v) in basicexpansions[token.word.lower()]:
                rlisttokenctr = 0
                for rlisttokenctr, rw in enumerate(rlist):
                    if rlisttokenctr == 0:
                        newtoken = Token(rw, token.pos)
                    else:
                        newtoken = Token(rw, token.pos, subpos=rlisttokenctr)
                    newtokens.append(newtoken)
                    tokenposlist.append(token.pos)
                    nwt = Token(space.join(rlist), token.pos)
                meta1 = mkSASTAMeta(token, nwt, n, v, c, subcat=None, penalty=defaultpenalty,
                                    backplacement=bpl_none)
                newmd.append(meta1)

        else:
            newtoken = Token(token.word, token.pos)
            newtokens.append(newtoken)
            tokenposlist.append(token.pos)

    # adapt the metadata
    if expansionfound:
        meta2 = Meta('OrigCleanTokenPosList', tokenposlist, annotatedposlist=[],
                     annotatedwordlist=[], annotationposlist=tokenposlist,
                     annotationwordlist=[], cat='Tokenisation', subcat=None, source=SASTA, penalty=defaultpenalty,
                     backplacement=bpl_none)
        newmd.append(meta2)
        result = [TokenListMD(newtokens, newmd)]
    else:
        result = []

    return result


def getsingleitemexpansions(token: Token, intokenposlist) -> List[Tuple[TokenListMD, List[int]]]:
    lcword = token.word.lower()
    outtokenposlist = copy.copy(intokenposlist)
    if lcword in basicexpansions:
        results = []
        for (rlist, c, n, v, p) in basicexpansions[lcword]:
            outtokenposlist = copy.copy(intokenposlist)
            newtokens = []
            newmd = []
            for rlisttokenctr, rw in enumerate(rlist):

                if rlisttokenctr == 0:
                    newtoken = Token(rw, token.pos)
                else:
                    newtoken = Token(rw, token.pos, subpos=rlisttokenctr)
                newtokens.append(newtoken)
                outtokenposlist.append(token.pos)
                nwt = Token(space.join(rlist), token.pos)
            meta1 = mkSASTAMeta(token, nwt, n, v, c, subcat=None, penalty=p,
                                backplacement=bpl_none)
            newmd.append(meta1)
            result = (TokenListMD(newtokens, newmd), outtokenposlist)
            results.append(result)
    else:
        outtokenposlist.append(token.pos)
        results = [(TokenListMD([token], []), outtokenposlist)]

    return results


def combine(headresult: Tuple[TokenListMD, List[int]], tailresult: Tuple[TokenListMD, List[int]]) \
        -> Tuple[TokenListMD, List[int]]:
    '''

    :param headresult: an  expansion result for the head
    :param tailresult: an expansion result for the tail
    :return: the combination of the head result and the tailresult

    The function *combine* combines a result for the head of an input token list with a result of the tail of
    the input token list.
    It simply concatenates the token lists of the results, and the metadata of the results,
    and generates the tokenposlist for their combination.

    '''
    newtokens = headresult[0].tokens + tailresult[0].tokens
    newmd = headresult[0].metadata + tailresult[0].metadata
    newtokenposlist = tailresult[1]
    result = (TokenListMD(newtokens, newmd), newtokenposlist)
    return result


def getexpansions2(tokenlist: List[Token], intokenposlist: List[int]) -> List[Tuple[TokenListMD, List[int]]]:
    '''

    :param tokenlist: the list of tokens in the utterance
    :param intokenposlist: the list of token positions so far, initially the empty list
    :return: zero or more alternative lists of tuples of
       * tokens with metadata
       * accumulated list of token positions

    The function *getexpansions2* generates alternative tokenlists plus metadata for
    words that are contractions and must be expanded into a sequence of multiple tokens.
    It applies the function *getsingleitemexpansions* to the head (first) element of the *tokenlist* and
    recursively applies itself to the tail of *intokenlist*, after which it combines the results by the *combine* function.

        .. autofunction::  corrector::getsingleitemexpansions

        .. autofunction:: corrector::combine

    It checks whether a word is a contraction by checking whether it occurs in the
    dictionary *basicexpansions* from the module *basicreplacements*

        .. autodata:: basicreplacements::basicexpansions
            :no-value:

    '''
    finalresults = []
    if tokenlist == []:
        outtokenposlist = copy.copy(intokenposlist)
        finalresults = [(TokenListMD([], []), outtokenposlist)]
    else:
        headresults = getsingleitemexpansions(tokenlist[0], intokenposlist)
        for headresult in headresults:
            tailresults = getexpansions2(tokenlist[1:], headresult[1])
            results = [combine(headresult, tailresult)
                       for tailresult in tailresults]
            finalresults += [(TokenListMD(result[0].tokens,
                                          result[0].metadata), result[1]) for result in results]
    return finalresults


def gettokenyield(tokens: List[Token]) -> str:
    words = [token.word for token in tokens]
    result = space.join(words)
    return result


def getexpansions(uttmd: TokenListMD) -> List[TokenListMD]:
    '''

    :param uttmd: the list of tokens in the utterance with its metadata
    :return: a possibly empty list of alternative lists of tokens with metadata

    The function *getexpansions* generates alternative tokenlists plus metadata for
    words that are contractions and must be expanded into a sequence of multiple tokens.

    It does so by a call to the function *getexpansions2*, which recursively generates all alternatives with expansions:

    .. autofunction:: corrector::getexpansions2

    '''
    newtokenmds = []

    results = getexpansions2(uttmd.tokens, [])
    for result in results:
        result0yield = gettokenyield(result[0].tokens)
        uttmdyield = gettokenyield(uttmd.tokens)
        if result0yield != uttmdyield:  # otherwise we get unnecessary and undesired duplicates
            tokenposlist = result[1]
            meta2 = Meta('OrigCleanTokenPosList', tokenposlist, annotatedposlist=[],
                         annotatedwordlist=[], annotationposlist=tokenposlist,
                         annotationwordlist=[], cat='Tokenisation', subcat=None, source=SASTA, penalty=0,
                         backplacement=bpl_none)
            newmd = result[0].metadata
            newmd.append(meta2)
            newtokenmd = TokenListMD(result[0].tokens, newmd)
            newtokenmds.append(newtokenmd)

    return newtokenmds

    # adapt the metadata
    # finalresults = []
    # for result in results:
    #     meta2 = Meta('OrigCleanTokenPosList', tokenposlist, annotatedposlist=[],
    #                  annotatedwordlist=[], annotationposlist=tokenposlist,
    #                  annotationwordlist=[], cat='Tokenisation', subcat=None, source=SASTA, penalty=defaultpenalty,
    #                  backplacement=bpl_none)
    #     newmd = result.metadata
    #     newmd.append(meta2)
    #     finalresult = [TokenListMD(result.tokens, newmd)]
    #     finalresults.append(finalresult)


def lexcheck(intokensmd: TokenListMD, allalternativemds: List[TokenListMD]) -> List[TokenListMD]:
    finalalternativemds = [intokensmd]
    for alternativemd in allalternativemds:
        diff_found = False
        include = True
        intokens = intokensmd.tokens
        outtokens = alternativemd.tokens
        if len(intokens) != len(outtokens):
            diff_found = True
        else:
            for (intoken, outtoken) in zip(intokens, outtokens):
                if intoken != outtoken:
                    diff_found = True
                    if not known_word(outtoken.word):
                        include = False
                        break
        if diff_found and include:
            finalalternativemds.append(alternativemd)
    return finalalternativemds


# moved to metadata
# def mkSASTAMeta(token, nwt, name, value, cat, subcat=None, penalty=defaultpenalty, backplacement=defaultbackplacement):
#    result = Meta(name, value, annotatedposlist=[token.pos],
#                     annotatedwordlist=[token.word], annotationposlist=[nwt.pos],
#                     annotationwordlist=[nwt.word], cat=cat, subcat=subcat, source=SASTA, penalty=penalty,
#                     backplacement=backplacement)
#    return result


def updatenewtokenmds(newtokenmds: List[TokenMD], token: Token, newwords: List[str], beginmetadata: List[Meta],
                      name: str, value: str, cat: str, subcat: Optional[str] = None,
                      penalty: Penalty = defaultpenalty, backplacement: BackPlacement = defaultbackplacement) \
        -> List[TokenMD]:
    for nw in newwords:
        nwt = Token(nw, token.pos)
        meta = mkSASTAMeta(token, nwt, name=name, value=value, cat=cat, subcat=subcat, penalty=penalty,
                           backplacement=backplacement)
        metadata = [meta] + beginmetadata
        newwordtokenmd = TokenMD(nwt, metadata)
        newtokenmds.append(newwordtokenmd)
    return newtokenmds


# def gettokensplusxmeta(tree: SynTree) -> Tuple[List[Token], List[Meta]]: moved to sastatok.py


def findxmetaatt(xmetalist: List[Meta], name: str, cond: MetaCondition = lambda x: True) -> Optional[Meta]:
    cands = [xm for xm in xmetalist if xm.name == name and cond(xm)]
    if cands == []:
        result = None
    else:
        result = cands[0]
    return result


# def explanationasreplacement(tokensmd: TokenListMD, tree: SynTree) -> Optional[TokenListMD]: moved to sasta_explanation
# some words are known but very unlikely as such
#: The constant *specialdevoicingwords* contains known words that start with a
#: voiceless consonant for which the word starting with the corresponding voiced
#: consonant is much more likely in young children's speech.
specialdevoicingwords = {'fan'}


def initdevoicing(token: Token, voiceless: str, voiced: str, newtokenmds: List[TokenMD], beginmetadata: List[Meta]) \
        -> List[TokenMD]:
    '''
    The function *initdevoicing* takes as input *token*, checks whether it is an
    unknown word or a special known word. If the token's word starts with *voiceless*
    it creates a newword with the tokens's word initial character replaced by *voiced*.
    If the result is a known word, *newtokenmds* is updated with the new replacement
    and *beginmetadata*, and it returns *newtokenmds*.

    A known word is *special* if it is contained in the variable *specialdevoicingwords*.

    .. autodata:: corrector::specialdevoicingwords

    '''
    # initial s -> z, f -> v
    if not known_word(token.word.lower()) or token.word.lower() in specialdevoicingwords:
        if token.word[0] == voiceless:
            newword = voiced + token.word[1:]
            if known_word(newword):
                newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                                name='Pronunciation Variant',
                                                value='Initial {} devoicing'.format(
                                                    voiced),
                                                cat='Pronunciation', backplacement=bpl_word)

    return newtokenmds


def getalternativetokenmds(tokenmd: TokenMD, method: MethodName, tokens: List[Token], tokenctr: int,
                           tree: SynTree, uttid: UttId) -> List[TokenMD]:
    token = tokenmd.token
    beginmetadata = tokenmd.metadata
    newtokenmds: List[TokenMD] = []

    if token.skip:
        return newtokenmds

    # decapitalize initial token  except when it is a known name
    if tokenctr == 0 and token.word.istitle() and not isa_namepart(token.word):
        newword = token.word.lower()

        newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                        name='Character Case', value='Lower case', cat='Orthography')

    # dehyphenate
    if not known_word(token.word) and hyphen in token.word:
        newwords = fullworddehyphenate(token.word, known_word)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Dehyphenation', value='Dehyphenation', cat='Pronunciation',
                                        backplacement=bpl_word)

    # deduplicate jaaaaa -> ja; heeeeeel -> heel
    if not known_word(token.word):
        newwords = deduplicate(token.word, known_word, exceptions=chatxxxcodes)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Emphasis', value='Phoneme lengthening', cat='Pronunciation',
                                        backplacement=bpl_word)

    # basic replacements replace as by als, isse by is
    # here come the replacements
    if token.word.lower() in basicreplacements:
        for (r, c, n, v, p) in basicreplacements[token.word.lower()]:
            newwords = [r]
            newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                            name=n, value=v, cat=c, backplacement=bpl_word, penalty=p)
    # next replaced by conditions in basicreplacements.py
    # if token.word.lower() in {'wel', 'niet'}:
    #     beginval = str(token.pos)
    #     wordnode = find1(tree, f'.//node[@pt="ww" and @begin="{beginval}"]')
    #     if wordnode is not None:
    #         newwords = ['ietsjes']
    #         newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
    #                                         name='Disambiguation', value='Avoid unknown reading',
    #                                         cat='Lexicon', backplacement=bpl_wordlemma)

    moemoetxpath = './/node[@lemma="moe" and @pt!="n" and not(%onlywordinutt%)]'
    expanded_moemoetxpath = expandmacros(moemoetxpath)
    if token.word.lower() == 'moe' and tree.xpath(expanded_moemoetxpath) != [] and (
            tokenctr == 0 or tokens[tokenctr - 1].word.lower() != 'beetje'):
        newwords = ['moet']
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Informal pronunciation', value='Final t-deletion', cat='Pronunciation',
                                        backplacement=bpl_word)

    # dee -> deze of deed
    if token.word.lower() == 'dee':
        newwords = ['deze']
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Wrong pronunciation', value='Coda reduction', cat='Pronunciation',
                                        backplacement=bpl_word, penalty=5)
        newwords = ['deed']
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Informal pronunciation', value='Final t-deletion', cat='Pronunciation',
                                        backplacement=bpl_word)

    # beurt -> gebeurt
    if token.word.lower() == 'beurt':
        newwords = ['gebeurt']
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Wrong pronunciation', value='Unstressed syllable drop', cat='Pronunciation',
                                        backplacement=bpl_word, penalty=5)
        newwords = ['deed']
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Informal pronunciation', value='Final t-deletion', cat='Pronunciation',
                                        backplacement=bpl_word)

    # words unknown to Alpino e.g *gymmen* is replaced by *trainen*
    if token.word.lower() in wordsunknowntoalpinolexicondict:
        newwords = [wordsunknowntoalpinolexicondict[token.word.lower()]]
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                    name='Word unknown to Alpino', value='Unknown word', cat='lexicon',
                                    backplacement=bpl_wordlemma)


    # find document specific replacements

    # find organisation specific replacements

    # find childes replacements, preferably with vocabulary from the same age

    # gaatie
    if not known_word(token.word):
        newwords = gaatie(token.word)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Word combination', value='Cliticisation', cat='Pronunciation',
                                        backplacement=bpl_none)

    # extend to gaat-ie

    # dediacritisize

    # iedims
    if token.word.endswith('ie') or token.word.endswith('ies'):
        newwords = getjeforms(token.word)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='RegionalForm', value='ieDim', cat='Morphology', backplacement=bpl_word)

    # overregularised verb forms: gevalt -> gevallen including  incl  wrong verb forms: gekeekt -> gekeken
    if not known_word(token.word):
        nwms = correctinflection(token.word)
        for nw, metavalue in nwms:
            newtokenmds += updatenewtokenmds(newtokenmds, token, [nw], beginmetadata,
                                             name='InflectionError', value=metavalue, cat='Morphology',
                                             backplacement=bpl_word)

    # wrong verb forms: gekeekt -> gekeken: done!

    # me ze (grote/oudere/ kleine) moeder /vader/zusje/ broer -> mijn me s done by Alpino, here we do ze
    # next xpath does not work because it must be preceded by a . !!
    # zexpathmodel = """//node[@word="ze" and @begin={begin} and (@rel="--"  or (@rel="obj1" and parent::node[@cat="pp"])) and @end = ancestor::node[@cat="top"]/descendant::node[@pt="n"]/@begin]"""
    if token.word.lower() == 'ze' or token.word.lower() == 'su':
        # find the node that corresponds to this token in the tree
        # zexpath = zexpathmodel.format(begin=str(tokenctr))
        # zenode = find1(tree, zexpath)
        tokennodes = getnodeyield(tree)
        zenode = tokennodes[tokenctr]
        if tokenctr < len(tokens) - 1:
            nexttoken = tokens[
                tokenctr + 1]  # do not take it from the tree because it may have been replaced by something else, e.g. avoid: ze dee -> ze deed -/-> z'n deed!
            zerel = getattval(zenode, 'rel')
            zeparent = zenode.getparent()
            zeparentcat = getattval(zeparent, 'cat')
            # nextpt = getattval(nextnode, 'pt')
            nexttokeninfo = getwordinfo(nexttoken.word.lower())
            nexttokenpts = {pt for (pt, _, _, _) in nexttokeninfo}
            if (zerel == '--' or zerel == 'mwp' or (zerel == 'obj1' and zeparentcat == 'pp')) and 'n' in nexttokenpts:
                newword = "z'n"
                newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                                name='Pronunciation Variant', value='N-less informal possessive pronoun',
                                                cat='Pronunciation', backplacement=bpl_word)

    # e-> e(n)
    enexceptions = {'inne', 'mette', 'omme', 'oppe', 'vanne'}
    if not known_word(
            token.word) and token.word.lower() not in basicreplacements and token.word.lower() not in enexceptions:
        if endsinschwa(token.word) and not monosyllabic(token.word):
            newword = token.word + 'n'
            if known_word(newword):
                newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                                name='Pronunciation Variant', value='N-drop after schwa',
                                                cat='Pronunciation', backplacement=bpl_word)

    # initial s -> z
    newtokenmds = initdevoicing(token, 's', 'z', newtokenmds, beginmetadata)
    # initial f -> v
    newtokenmds = initdevoicing(token, 'f', 'v', newtokenmds, beginmetadata)

    # replaceambiguous words with one reading not known by the child by a nonambiguous word with the same properties
    if method in {'tarsp', 'stap'}:
        if token.word.lower() in disambiguationdict:
            cond, newword = disambiguationdict[token.word.lower()]
            if cond(token, tree):
                newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                                name='Disambiguation', value='Avoid unknown reading',
                                                cat='Lexicon', backplacement=bpl_wordlemma)

    # ...en -> e: groten  -> grote (if adjective); goten -> grote

    # drop e at the end incl duplicated consonants (ooke -> ook; isse -> is ? DOne, basicreplacements

    # losse e -> een / het / de

    for newtokenmd in newtokenmds:
        morenewtokenmds = getalternativetokenmds(
            newtokenmd, method, tokens, tokenctr, tree, uttid)
        newtokenmds += morenewtokenmds

    return newtokenmds


def getvalidalternativetokenmds(tokenmd: TokenMD, newtokenmds: List[TokenMD]) -> List[TokenMD]:
    validnewtokenmds = [
        tokenmd for tokenmd in newtokenmds if known_word(tokenmd.token.word)]
    # and now we add the original tokenmd
    validnewtokenmds += [tokenmd]
    return validnewtokenmds



def gaatie(word: str) -> List[str]:
    '''
    The function *gaatie*
    * replaces a word of the form *X-ie* by the string f'{X} ie' if X is a verb form
    * replaces a word of the form *XVttie* by the string f'{X}{V}t ie where V is vowel and XVt is a verb form
    * replaces  a word that matches with  *gaatiepattern*  (e.g.
    *gaatie*) by a sequence of two words where the first word equals word[:-2] (
    *gaat*) and is a known word and the second word equals word[-2:] (*ie*).

    .. autodata:: corrector::gaatiepattern
    '''
    results = []
    # kan-ie, moet-ie, gaat-ie, wil-ie
    if word.endswith('-ie') and informlexicon(word[:-3]):
        result = space.join([word[:-3], 'ie'])
        results.append(result)
    # moettie, gaattie,
    if gaattiere.match(word) and informlexicon(word[:-3]):
        result = space.join([word[:-3], 'ie'])
        results.append(result)
    if gaatiere.match(word):
        # and if it is a verb this is essential because now tie is also split into t ie
        if informlexicon(word[:-2]):
            result = space.join([word[:-2], word[-2:]])
            results.append(result)
    return results


def oldgaatie(word: str) -> List[str]:
    '''
    The function *gaatie* replaces  a word that matches with  *gaatiepattern*  (e.g.
    *gaatie*) by a sequence of two words where the first word equals word[:-2] (
    *gaat*) and is a known word and the second word equals word[-2:] (*ie*).

    .. autodata:: corrector::gaatiepattern
    '''
    results = []
    if gaatiere.match(word):
        # and if it is a verb this is essential because now tie is also split into t ie
        if informlexicon(word[:-2]):
            result = space.join([word[:-2], word[-2:]])
            results.append(result)
    return results


def getwrongdetalternatives(tokensmd: TokenListMD, tree: SynTree, uttid: UttId) -> List[TokenListMD]:
    '''
    The function *getwrongdetalternatives* takes as input a TokenListMD *tokensmd*,  the
    original parse of the utterance (*tree*) and the *uttid* of the utterance.

    It inspects each token in the token list of *tokensmd* that should not be skipped
    and that is a utrum determiner. If the token that immediately follows this
    determiner is not a token to be ignored we obtain the gender properties of the
    token's word (there can be multiple if it is ambiguous). If one of the properties
    is neuter gender and none is uter, then the uter determiner is replaced by its neuter
    variant as a new alternative.

    The token following must be ignored if it has the property *skip=True* or if it
    belongs to words that would lead to wrong corrections, as specified in the constant
    *wrongdet_excluded_words*:

    .. autodata:: corrector::wrongdet_excluded_words

    The properties of the token following are determined by the function
    *getdehetwordinfo* from the module *alpino*:

    .. autofunction:: alpino::getdehetwordinfo
    '''
    correctiondone = False
    tokens = tokensmd.tokens
    metadata = tokensmd.metadata
    ltokens = len(tokens)
    tokenctr = 0
    newtokens = []
    while tokenctr < ltokens:
        token = tokens[tokenctr]
        if not token.skip and token.word in dets[de] and tokenctr < ltokens - 1:
            nexttoken = tokens[tokenctr + 1]
            # we want to exclude some words
            if nexttoken.skip:
                wordinfos: List[WordInfo] = []
            elif nexttoken.word in wrongdet_excluded_words:
                wordinfos = []
            else:
                wordinfos, _ = getdehetwordinfo(nexttoken.word)
            if wordinfos != []:
                for wordinfo in wordinfos:  # if there are multiple alternatives we overwrite and therefore get the last alternative
                    (pos, dehet, infl, lemma) = wordinfo
                    if dehet == het and infl in ['e', 'de']:
                        # newcurtoken = replacement(token, swapdehet(token))
                        newcurtokenword = swapdehet(token.word)
                        newcurtoken = Token(newcurtokenword, token.pos)
                        meta = mkSASTAMeta(token, newcurtoken, name='GrammarError', value='deheterror', cat='Error',
                                           backplacement=bpl_node)
                        metadata.append(meta)
                        correctiondone = True
                    else:
                        newcurtokenword = token.word
                newtokens.append(Token(newcurtokenword, token.pos))
            else:
                newcurtokenword = token.word
                newtokens.append(token)
        else:
            newtokens.append(token)
        tokenctr += 1
    result = TokenListMD(newtokens, metadata)
    if correctiondone:
        results = [result]
    else:
        results = []
    return results


def getindezemwp(prevtokennode: SynTree, tokennode: SynTree) -> bool:
    ok = True
    ok = ok and getattval(prevtokennode, 'lemma') in {'in'}
    ok = ok and getattval(prevtokennode, 'rel') in {'mwp'}
    ok = ok and getattval(tokennode, 'lemma') in {'deze'}
    ok = ok and getattval(tokennode, 'rel') in {'mwp'}
    return ok


def correctPdit(tokensmd: TokenListMD, tree: SynTree, uttid: UttId) -> List[TokenListMD]:
    '''
    The function *correctPdit* replaces demonstrative pronouns immediately preceded by
    an adposition by the pronoun *hem*. It sets the value of the *backplacement*
    attribute of the metadata to *bpl_node* so that it will be replaced again by the
    original node after the parse has been done, unless the original parse contained the multiword
    unit *in deze*. Then the *backplacement* attribute gets the value *bpl_indeze* so
    that in a later stage some special replacements will be performed.

    The function takes as input:

    * *tokensmd* of type *TpkenListMD* : the list of tokens wit hassociated metadata

    *tree* of type *SynTree*: the parse of the original utterance

    *uttid* of type *UttId*: the utterance identifier of the utterance (currently not
    used)

    It yields a list  containing the alternatives generated (of type List[TokenListMD].
    '''
    correctiondone = False
    tokennodes = getnodeyield(tree)
    tokens = tokensmd.tokens
    metadata = tokensmd.metadata
    newtokens = []
    tokenctr = 0
    nonskiptokenctr = 0
    prevtoken = None
    for token in tokens:
        tokennode = next(filter(lambda x: getattval(x, 'begin') == str(
            token.pos + token.subpos), tokennodes), None)
        tokenlemma = getattval(tokennode, 'lemma')
        if not token.skip and prevtoken is not None and not prevtoken.skip and tokenlemma in {'dit', 'dat', 'deze',
                                                                                              'die'}:
            tokenrel = getattval(tokennode, 'rel')
            tokenpt = getattval(tokennode, 'pt')
            prevtokennode = tokennodes[nonskiptokenctr - 1] if tokenctr > 0 else None
            if prevtokennode is not None:
                prevpt = getattval(prevtokennode, 'pt')
                prevparent = prevtokennode.getparent()
                prevparentrel, prevparentcat = getattval(
                    prevparent, 'rel'), getattval(prevparent, 'cat')
                indezemwp = getindezemwp(prevtokennode, tokennode)
                if (prevpt == 'vz' and prevparentcat != 'pp' and tokenrel not in {'det'} and tokenpt == 'vnw') or \
                        indezemwp:
                    newtoken = Token('hem', token.pos, subpos=token.subpos)
                    bpl = bpl_indeze if indezemwp else bpl_node
                    meta = mkSASTAMeta(token, newtoken, name='parsed as', value='hem', cat='AlpinoImprovement',
                                       backplacement=bpl, penalty=15)
                    metadata.append(meta)
                    newtokens.append(newtoken)
                    correctiondone = True
                else:
                    newtokens.append(token)
            else:
                newtokens.append(token)
        else:
            newtokens.append(token)
        tokenctr += 1
        if not token.skip:
            nonskiptokenctr += 1
        prevtoken = token
    result = TokenListMD(newtokens, metadata)
    if correctiondone:
        results = [result]
    else:
        results = []
    return results


def parseas(w: str, code: str) -> str:
    result = '[ @add_lex {} {} ]'.format(code, w)
    return result


def swapdehet(dedet: str) -> Optional[str]:
    if dedet in dets[de]:
        deindex = dets[de].index(dedet)
    else:
        deindex = -1
    if dedet in dets[het]:
        hetindex = dets[het].index(dedet)
    else:
        hetindex = -1
    if deindex >= 0:
        result = dets[het][deindex]
    elif hetindex >= 0:
        result = dets[de][hetindex]
    else:
        result = None
    return result


def outputalternatives(tokens, alternatives, outfile):
    for el in alternatives:
        print(tokens[el], slash.join(alternatives[el]), file=outfile)


def mkchatutt(intokens: List[str], outtokens: List[str]) -> List[str]:
    result = []
    for (intoken, outtoken) in zip(intokens, outtokens):
        newtoken = intoken if intoken == outtoken else replacement(
            intoken, outtoken)
        result.append(newtoken)
    return result


def altmkchatutt(intokens: List[str], outtoken: str) -> List[str]:
    result = []
    for intoken in intokens:
        newtoken = intoken if intoken == outtoken else replacement(
            intoken, outtoken)
        result.append(newtoken)
    return result
