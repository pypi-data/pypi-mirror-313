'''
defines functions for the STAP post part of the methods

'''
from collections import Counter

from sastadev.allresults import mkresultskey

BB_ids = ['S010', 'S011', 'S012']
S013qid = 'S013'
S013reskey = mkresultskey(S013qid)


def BB_totaal(allresults, _):
    scores = []
    for qid in BB_ids:
        if qid in allresults.coreresults:
            scores.append(allresults.coreresults[qid])
        else:
            scores.append(Counter())
    counts = [len(s) for s in scores]
    result = sum(counts)
    return result


def GLVU(allresults, _):
    total_length_VU = 0
    if S013reskey in allresults.coreresults:
        for key in allresults.coreresults[S013reskey]:
            total_length_VU += allresults.coreresults[S013reskey][key]
    result = total_length_VU / allresults.uttcount
    return result


def GL5LVU(allresults, _):
    counts = []
    if S013reskey in allresults.coreresults:
        for key in allresults.coreresults[S013reskey]:
            counts.append(allresults.coreresults[S013reskey][key])
    sorted_counts = counts.sort()
    result = sum(counts[45:50]) / 5
    return result
