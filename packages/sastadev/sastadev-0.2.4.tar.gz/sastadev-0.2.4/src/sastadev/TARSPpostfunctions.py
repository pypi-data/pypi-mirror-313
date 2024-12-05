'''
The module TARSPpostfunctions defines functions for the TARSP post part of the methods

'''
from collections import Counter
from typing import Dict, List

from sastadev.allresults import AllResults
from sastadev.conf import settings
from sastadev.query import core_process
from sastadev.sastatypes import QId, QueryDict, Stage, SynTree
from sastadev.treebankfunctions import getmeta

OndVC = 'T071'
OndWVC = 'T076'
OndWBVC = 'T075'

#: The variable (constant) *vuqueryids* contains a list of Query identifiers for
#: queries for fixed expressions (V.U.).
vuqueryids = ['T094', 'T095', 'T096', 'T150']
#: The variable (constant) *tarsp_clausetypes* contains the (lower case) values for the
#: subcategory of a query that represent clause types.
tarsp_clausetypes = ['mededelende zin', 'vragen', 'gebiedende wijs']
#: The variable (constant) *excludedqids* contains a list of QIds for queries that
#: should be excluded in computing G.O. Fase.
excludedqids = ['T039', 'T048', 'T049', 'T052']   # TARSP p. 21: hè, Into, Inversie, Kop
#: The variable (constant) *gofase_minthreshold* contains the value of the minimum
#: percentage of analysis units that must have been scored to be included in G.O. Fase.
gofase_minthreshold = 0.05  # 5% p21 Tarsp 2005


def getqueriesbystage(queries: QueryDict) -> Dict[Stage, List[QId]]:
    '''
    The function *getqueriesbystage* creates a dictionary with a stage as key and a
    list of QIds as value.

    It selects those QIds for which the query's (lower cased) subcategory is contained
    in the constant *tarsp_clausetypes*:

    .. autodata:: TARSPpostfunctions::tarsp_clausetypes

    and which is not included in the list of *excludedqids*:

    .. autodata:: TARSPpostfunctions::excludedqids

    if these conditions are met, the QId is appended to the dictionary item with key
    equal to the stage of the query associated with QId.
    '''
    results = {}
    for qid in queries:
        if queries[qid].subcat.lower() in tarsp_clausetypes and qid not in excludedqids:
            stage = queries[qid].fase
            if stage in results:
                results[stage].append(qid)
            else:
                results[stage] = [qid]
    return results


def vutotaal(allresults: AllResults, _: SynTree) -> int:
    '''
    The function *vutotaal* computes the total number of  "Vaste Uitdrukkingen" (VU) in
    the variable *allresults*. It uses the set *vuqueryids* to determine which
    queries to take into account and which not:

     .. autodata:: vuqueryids
    '''
    scores = []
    for qid in vuqueryids:
        if qid in allresults.coreresults:
            scores.append(allresults.coreresults[qid])
        else:
            scores.append(Counter())
#    scores = [allresults.coreresults[qid] for qid in vuqueryids]
    counts = [len(s) for s in scores]
    result = sum(counts)
    return result


def gtotaal(allresults: AllResults, _: SynTree) -> int:
    '''
    The function *gtotaal* computes the number of utterances to be analysed. It does
    so by subtracting the number of V.U. utterances and the results for *Atotaal* from
    the total number of utterances.
    '''
    Atotaal = 0
    vutotaal = allresults.postresults['T151']
    Gtotaal = allresults.uttcount - Atotaal - vutotaal
    return Gtotaal


def countutts(acounter: Counter):
    '''
    The function *countutts* returns the sum of the values for each key in
    *acounter*.
    '''
    result = 0
    for k in acounter:
        result += acounter[k]
    return result


def getuttcountsbystage(queriesbystage: Dict[Stage, List[QId]], allresults: AllResults)\
        -> Dict[Stage, int]:
    '''
    The function *getuttcountsbystage* computes a dictionary *uttcounts* of Stage,
    int items based on the input parameters *queriesbystage* and *allresults*.

    For each qid in *queriesbystage* that is a qid for a core query, it counts the
    number of utterances marked in  *allresults.coreresults*. For this it uses the
    function *countutts*:

    .. autofunction:: TARSPpostfunctions::countutts

    '''
    uttcounts = {}
    for stage in queriesbystage:
        uttcounts[stage] = 0
        for qid in queriesbystage[stage]:
            if qid in allresults.coreresults:
                uttcounts[stage] += countutts(allresults.coreresults[qid])
    return uttcounts


def getstage(uttcounts: Dict[Stage, int], allresults: AllResults) -> Stage:
    '''
    The function *getstage* computes the stage on the basis of the *uttcounts*
    dictionary with Stage, int items and *allresults*

    The stage is taken into consideration if its number of scores divided by *gtotaal* is
    greater or equal to the value of *gofase_minthreshold*:

    .. autodata:: TARSPpostfunctions::gofase_minthreshold

    From the remaining candidates the highest stage value is selected.
    '''
    cands = []
    gtotaal = allresults.postresults['T152']
    for el in uttcounts:
        if gtotaal != 0:
            if uttcounts[el] / gtotaal >= gofase_minthreshold:
                cands.append(el)
        else:
            settings.LOGGER.error('gtotaal has value 0')
    if cands == []:
        result = 1
    else:
        result = max(cands)
    return result


def gofase(allresults: AllResults, thequeries: QueryDict) -> Stage:
    '''
    The function *gofase* computes the stage given the results in the parameter
    *allresults* and the queries in the parameter *thequeries*.

    It first obtains *queriesbystage*, a dictionary of Stage, List[QId] items, via the
    function  *getqueriesbystage* applied to *thequeries*:

    .. autofunction:: TARSPpostfunctions::getqueriesbystage

    Next, it obtains *uttcounts*,  a dictionary of Stage, int items by applying the
    function  *getuttcountsbystage* to *queriesbystage* and *allresults*:

    .. autofunction:: TARSPpostfunctions::getuttcountsbystage

    Finally, it obtains the stage by applying the function *getstage* to *uttcounts*
    and *allresults*:

    .. autofunction:: TARSPpostfunctions::getstage

    and then it returns the obtained *stage*.
    '''
    result = 0
    queriesbystage: Dict[Stage, List[QId]] = getqueriesbystage(thequeries)
    uttcounts: Dict[Stage, int] = getuttcountsbystage(queriesbystage, allresults)
    result: Stage = getstage(uttcounts, allresults)

    return result


def genpfi(stage: Stage, allresults: AllResults, allqueries: QueryDict) -> int:
    '''
    The function *genpfi* computes the *Profielscore* (PF) for the stage given by the
    parameter *stage* on the basis of *allresults* and the query dictionary *allqueries*.
    It selects the queries of the given stage that are core queries and that are not
    *star2* queries.

    From these, it only selects the ones for which the number of results is larger than 0.
    It adds *OndVC* if *OndWVC* or *OndWBVC* has been scored.
    Special measures for *Xneg*, *OndB*, *VCW* and *BX* still have to be implemented.
    The description in Schlichting (p. 23) is not specific enough.
    '''
    theqids = [qid for qid in allqueries if allqueries[qid].fase == stage and allqueries[qid].process == core_process
               and allqueries[qid].stars != 'star2']
    coreresults = allresults.coreresults
    scoredqids = [qid for qid in theqids if qid in coreresults and len(coreresults[qid]) > 0]
    # OndVC
    if OndWVC in theqids or OndWBVC in scoredqids:
        scoredqids.append(OndVC)
    # XNeg
    # OndB
    # VCW
    # BX
    result = len(scoredqids)
    return result


def pf2(allresults: AllResults, allqueries: QueryDict) -> int:
    '''
    The function *pf2* uses the function *genpfi* to compute the 'Profielscore' for Stage II
    '''
    return genpfi(2, allresults, allqueries)


def pf3(allresults: AllResults, allqueries: QueryDict) -> int:
    '''
    The function *pf3* uses the function *genpfi* to compute the 'Profielscore' for Stage III
    '''
    return genpfi(3, allresults, allqueries)


def pf4(allresults: AllResults, allqueries: QueryDict) -> int:
    '''
    The function *pf4* uses the function *genpfi* to compute the 'Profielscore' for Stage IV
    '''
    return genpfi(4, allresults, allqueries)


def pf5(allresults: AllResults, allqueries: QueryDict):
    '''
    The function *pf5* uses the function *genpfi* to compute the 'Profielscore' for Stage V
    '''
    return genpfi(5, allresults, allqueries)


def pf6(allresults: AllResults, allqueries: QueryDict) -> int:
    '''
    The function *pf6* uses the function *genpfi* to compute the 'Profielscore' for Stage VI
    '''
    return genpfi(6, allresults, allqueries)


def pf7(allresults: AllResults, allqueries: QueryDict) -> int:
    '''
    The function *pf7* uses the function *genpfi* to compute the 'Profielscore' for Stage VII
    '''
    return genpfi(7, allresults, allqueries)


def pf(allresults: AllResults, allqueries: QueryDict) -> int:
    '''
    The function *pf* computes the *'Profielscore'* for the whole sample (*PF*) by
    summing the  'Profielscore's per stage as computed by *pf2* through *pf7*.

    The *'Profielscore's* per stage are computed by *pf2* through *pf7*, each of which
    uses the function *genpfi*:

    .. autofunction:: TARSPpostfunctions::genpfi

    '''
    postresults = allresults.postresults
    result = sum([postresults['T154'], postresults['T155'], postresults['T158'],
                  postresults['T159'], postresults['T160'], postresults['T161']])
    return result


def getname(allresults: AllResults, allqueries: QueryDict) -> str:
    '''
    The function *getname* obtains the name of the patient/child being investigated
    from the metadata. It uses the function *getmeta* to achieve this.

    '''
    result = getmeta('name')
    return result


def getchildage(allresults: AllResults, allqueries: QueryDict) -> str:
    '''
    The function *getchildage* is intended to obtain the age of the child being
    investigated from the metadata. It still has to be implemented. Currently it simply returns the empty string..

    '''
    result = ''
    return result
