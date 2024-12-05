from collections import Counter
from typing import Any, Dict, List

from sastadev.allresults import (AllResults, ExactResultsDict, MatchesDict,
                                 ResultsKey)
from sastadev.methods import lastuttqidcondition, maxsamplesize
from sastadev.sastatypes import (AnalysedTrees, FileName, Matches, MethodName,
                                 Position, QId, ResultsCounter, ResultsDict,
                                 SampleSizeTuple, UttId, UttWordDict)
from sastadev.treebankfunctions import getnodeyield


def exact2results(exactresults: ExactResultsDict) -> ResultsDict:
    """
    :param exactresults: dictionary key= queryid, value is a list of (uttid, position) pairs
    :return: dictionary (key=queryid, value is a Counter uttid: count)
    """
    results: ResultsDict = {}
    for reskey in exactresults:
        uttidlist = [uttid for (uttid, _) in exactresults[reskey]]
        resultvalue = Counter(uttidlist)
        results[reskey] = resultvalue
    return results


def reduceallresults(allresults: AllResults, samplesizetuple: SampleSizeTuple, methodname: MethodName) -> AllResults:
    '''
    reduces *allresults* by taking into account the samplesizetuple
    :param allresults:
    :param samplesizetuple:
    :return:
    '''
    (uttidlist, wordcount, cutoffpoint) = samplesizetuple
    uttcount = len(uttidlist)
    maxuttcount, maxwordcount = maxsamplesize[methodname].maxuttcount, maxsamplesize[methodname].maxwordcount
    if wordcount is not None and maxwordcount is not None and wordcount < maxwordcount:
        return allresults
    elif maxuttcount is not None and uttcount < maxuttcount:
        return allresults
    elif allresults.annotationinput:
        newexactresults: ExactResultsDict = reduceexactresults(allresults.exactresults,
                                                               uttidlist, cutoffpoint, methodname)  # done
        newcoreresults: Dict[QId, ResultsCounter] = exact2results(
            newexactresults)  # done
        newallutts: UttWordDict = reduceallutts(
            allresults.allutts, uttidlist)  # done
        newallresults = AllResults(allresults.uttcount, newcoreresults, newexactresults, allresults.postresults,
                                   allresults.allmatches, allresults.filename, allresults.analysedtrees,
                                   newallutts, allresults.annotationinput)
    else:

        newuttcount: int = len(uttidlist)  # done
        newexactresults: ExactResultsDict = reduceexactresults(allresults.exactresults,
                                                               uttidlist, cutoffpoint, methodname)  # done
        newcoreresults: Dict[ResultsKey, ResultsCounter] = exact2results(
            newexactresults)  # done
        # @@ I assume these need no change
        newpostresults: Dict[ResultsKey, Any] = allresults.postresults
        newallmatches: MatchesDict = reducematches(
            allresults.allmatches, uttidlist, cutoffpoint, methodname)  # done
        newfilename: FileName = allresults.filename  # done
        newanalysedtrees: AnalysedTrees = reduceanalysedtrees(
            allresults.analysedtrees, uttidlist)  # done
        newallutts: UttWordDict = reduceallutts(
            allresults.allutts, uttidlist)  # done
        newannotationinput: bool = allresults.annotationinput  # done

        newallresults = AllResults(newuttcount, newcoreresults, newexactresults, newpostresults, newallmatches,
                                   newfilename, newanalysedtrees, newallutts, newannotationinput)
    return newallresults


def reduceexactresults(exactresultsdict: Dict[QId, ExactResultsDict], uttidlist: List[UttId],
                       cutoffpoint: Position, methodname: MethodName) -> Dict[QId, ResultsCounter]:
    newexactresultsdict = {}
    lastuttid = uttidlist[-1]

    for reskey in exactresultsdict:
        newexactresults = []
        for uttid, position in exactresultsdict[reskey]:
            if (uttid in uttidlist and uttid != lastuttid) or \
                    (uttid == lastuttid and cutoffpoint is not None and
                     not (position > cutoffpoint) and lastuttqidcondition[methodname](reskey)):
                newexactresults.append((uttid, position))
        newexactresultsdict[reskey] = newexactresults
    return newexactresultsdict


def reduceresults(resultsdict: Dict[QId, Counter], samplesizetuple: SampleSizeTuple, methodname: MethodName):
    (uttidlist, wordcount, cutoffpoint) = samplesizetuple
    uttcount = len(uttidlist)
    maxuttcount, maxwordcount = maxsamplesize[methodname].maxuttcount, maxsamplesize[methodname].maxwordcount
    if wordcount is not None and maxwordcount is not None and wordcount < maxwordcount:
        newresultsdict = resultsdict
    elif maxuttcount is not None and uttcount <= maxuttcount:
        newresultsdict = resultsdict
    else:
        newresultsdict = {}
        lastuttid = uttidlist[-1]
        for reskey in resultsdict:
            newresults = []
            for uttid in resultsdict[reskey]:
                if (uttid in uttidlist and uttid != lastuttid) or \
                        (uttid == lastuttid and lastuttqidcondition[methodname](
                            reskey)):  # no condition on the position, we have no info on it
                    newresults.append(uttid)
            newresultsdict[reskey] = Counter(newresults)
    return newresultsdict


def reducematches(matchesdict: MatchesDict, uttidlist: List[UttId], cutoffpoint: Position,
                  methodname: MethodName) -> MatchesDict:
    newmatchesdict = {}
    lastuttid = uttidlist[-1]
    for reskey, uttid in matchesdict:
        if uttid in uttidlist and uttid != lastuttid:
            newmatchesdict[(reskey, uttid)] = matchesdict[(reskey, uttid)]
        else:
            if uttid == lastuttid and lastuttqidcondition[methodname](reskey):
                newmatches: Matches = []
                for match in matchesdict[(reskey, uttid)]:
                    (m, tree) = match
                    treeyield = getnodeyield(tree)
                    lefttreeyield = treeyield[: cutoffpoint]
                    if m in lefttreeyield:
                        newmatches.append((m, tree))
                newmatchesdict[(reskey, uttid)] = newmatches

    return newmatchesdict


def reduceanalysedtrees(analysedtrees: AnalysedTrees, uttidlist: List[UttId]) -> AnalysedTrees:
    newtrees = []
    for uttid, tree in analysedtrees:
        if uttid in uttidlist:
            newtrees.append((uttid, tree))
    return newtrees


def reduceallutts(uttworddict: UttWordDict, uttidlist: List[UttId]) -> UttWordDict:
    newdict = {}
    for uttid in uttidlist:
        if uttid in uttworddict:
            newdict[uttid] = uttworddict[uttid]
    return newdict


def reduceexactgoldscores(exactgoldscores: ExactResultsDict, samplesizetuple: SampleSizeTuple, methodname: MethodName):
    (uttidlist, wordcount, cutoffpoint) = samplesizetuple
    uttcount = len(uttidlist)
    maxuttcount, maxwordcount = maxsamplesize[methodname].maxuttcount, maxsamplesize[methodname].maxwordcount
    if wordcount is not None and maxwordcount is not None and wordcount < maxwordcount:
        newexactgoldscores = exactgoldscores
    elif maxuttcount is not None and uttcount <= maxuttcount:
        newexactgoldscores = exactgoldscores
    else:
        newexactgoldscores: ExactResultsDict = reduceexactresults(exactgoldscores,
                                                                  uttidlist, cutoffpoint, methodname)  # ongoing
        # newcoreresults: Dict[QId, ResultsCounter] = exact2results(newexactresults)   # keep out do ouside
    return newexactgoldscores
