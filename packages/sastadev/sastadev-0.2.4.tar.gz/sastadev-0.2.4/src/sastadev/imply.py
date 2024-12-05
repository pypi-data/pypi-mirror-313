'''
The *imply* module implements the function *removeimplies* to remove matches that are implied by a given match
'''

from sastadev.sastatypes import Match, MatchesDict, QueryDict
from sastadev.treebankfunctions import getattval as gav
from sastadev.treebankfunctions import getnodeyield


def removeimplies(matches: MatchesDict, queries: QueryDict) -> MatchesDict:
    toremovekeys = []
    for qid, uttid in matches:
        thematch = matches[(qid, uttid)]
        thequery = queries[qid]
        for impliedqid in thequery.implies:
            if (impliedqid, uttid) in matches:
                theimpliedmatch = matches[impliedqid]
                valid = contains(thematch, theimpliedmatch)
                if valid:
                    toremovekeys.append((impliedqid, uttid))

    newmatches = {key: val for key,
                  val in matches.items() if key not in toremovekeys}
    return newmatches


def contains(match: Match, impliedmatch: Match) -> bool:
    matchnodeyield = getnodeyield(match)
    impliedmatchnodeyield = getnodeyield(impliedmatch)
    matchpositions = {gav(node, 'end') for node in matchnodeyield}
    impliedmatchpositions = {gav(node, 'end')
                             for node in impliedmatchnodeyield}
    # of moeten de laagste identiek zijn?
    result = impliedmatchpositions.issubset(matchpositions)
    return result
