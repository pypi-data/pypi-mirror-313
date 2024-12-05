from typing import Callable, List

from sastadev.macros import expandmacros
from sastadev.sastatypes import SynTree
from sastadev.treebankfunctions import (adjacent, find1, get_left_siblings,
                                        getattval, parent)

nietxpath = './/node[@lemma="niet"]'
wordxpath = './/node[@pt]'

vzn1basexpath = './/node[ @cat="pp" and (node[@pt="vz"] and node[(@pt="n" or @pt="vnw") and not (%Rpronoun%) and @rel="obj1"] and not(node[@pt="vz" and @vztype="fin"]))]'
vzn1xpath = expandmacros(vzn1basexpath)
vzn2xpath = './/node[node[@lemma="in" and @rel="mwp"] and node[@lemma="deze" and @rel="mwp"]]'
vzn3xpath = './/node[@pt="vz" and ../node[(@lemma="dit" or @lemma="dat")  and @begin>=../node[@pt="vz"]/@end and count(node)<=3] ]'
#vzn4basexpath = './/node[node[@pt="vz" and @rel="hd" and ../node[%Rpronoun% and @rel="obj1" and @end <= ../node[@rel="hd"]/@begin]]]'
#vzn4xpath = expandmacros(vzn4basexpath)

#: The constant *voslahbijxpath* selects nodes (PPs) that contain an adposition and an R-pronoun or a index node
#: coindexed with an R-pronoun.
#:
#: **Remark** It is not actually checked whether the indexed node has an R-pronoun as its antecedent
#:
#: **Remark** We may have to do something special for *pobj1*
#:
voslashbijxpath = expandmacros(""".//node[node[@pt="vz" and @rel="hd"] and
            node[@rel="obj1" and
                 ((@index and not(@word or @cat)) or
                  (%Rpronoun%)
                 )]]""")

#: The constant *vobijxpath* uses the macro *Vobij* to identify adverbial pronouns.
#: The macro **Vobij** is defined as follows::
#:
#:   Vobij = """(@pt="bw" and (contains(@frame,"er_adverb" ) or contains(@frame, "tmp_adverb") or @lemma="daarom") and
#:               @lemma!="er" and @lemma!="daar" and @lemma!="hier" and @lemma!="waar" and
#:               (starts-with(@lemma, 'er') or starts-with(@lemma, 'daar') or
#                 starts-with(@lemma, 'hier') or starts-with(@lemma, 'waar'))
#:              )"""
#:
vobijxpath = expandmacros('.//node[%Vobij%]')


def notadjacent(n1, n2, t): return not adjacent(n1, n2, t)


def xneg(stree):
    nodepairs = []
    nietnodes = stree.xpath(nietxpath)
    for nietnode in nietnodes:
        pnietnode = parent(nietnode)
        leftnietsiblings = get_left_siblings(nietnode)
        leftsiblings = get_left_siblings(pnietnode)
        ppnietnode = parent(pnietnode)
        if getattval(pnietnode, 'cat') == "advp" and len(leftsiblings) == 1 and getattval(ppnietnode, 'rel') == '--':
            result = True
            theleftsibling = leftsiblings[0]
        elif getattval(pnietnode, 'cat') != "advp" and getattval(pnietnode, 'rel') == '--' and len(leftnietsiblings) == 1:
            result = True
            theleftsibling = leftnietsiblings[0]
        else:
            result = False
        if result:
            nodepairs.append((theleftsibling, nietnode))
    if nodepairs == []:
        return None
    else:
        return nodepairs[0]


def xneg_neg(stree):
    (x, neg) = xneg(stree)
    return neg


def xneg_x(stree):
    (x, neg) = xneg(stree)
    return x


def VzN(stree):
    results = []
    results += stree.xpath(vzn1xpath)
    results += stree.xpath(vzn2xpath)
    results += stree.xpath(vzn3xpath)
    #results += stree.xpath(vzn4xpath) # does not belong here after all, these will be scored under Vo/Bij
    return results


def auxvobij(stree: SynTree, pred: Callable[[SynTree, SynTree, SynTree], bool]) -> List[SynTree]:
    '''

    :param stree: the syntactic structure to be analysed
    :param pred: a predicate that the results found must satisfy
    :return: a list of matching nodes

    The function *auxvobij* finds nodes that are found by the *voslashbijxpath* and selects from these those
    that satisfy the predicate *pred*. It is used to distinguish cases of R-pronoun + adposition that are *adjacent*
    (which should be analysed as TARSP *Vobij*) from those that are not adjacent (which should be analysed as TARSP
    Vo/Bij).

    .. autodata:: queryfunctions::voslashbijxpath

    '''
    RPnodes = stree.xpath(voslashbijxpath)
    results = []
    for RPnode in RPnodes:
        # find the head node
        headnode = find1(RPnode, 'node[@rel="hd"]')

        # find the obj1node
        obj1node = find1(RPnode, 'node[@rel="obj1"]')

        if headnode is not None and obj1node is not None:
            if pred(obj1node, headnode, stree):
                results.append(RPnode)
    return results


def vobij(stree: SynTree) -> List[SynTree]:
    '''

    :param stree: syntactic structure to be analysed
    :return: List of matching nodes

    The function *vobij* uses the Xpath expression *vobijxpath* and the function *auxvobij* to obtain its resulting nodes:

    * The *vobijxpath* expression matches with so-called adverbial pronouns:

      .. autodata:: queryfunctions::vobijxpath

    * The function *auxvobij*  finds adjacent R-pronoun + adposition cases:

      .. autofunction:: queryfunctions::auxvobij

    '''
    results1 = stree.xpath(vobijxpath)
    results2 = auxvobij(stree, vobijpred)
    results = results1 + results2
    return results


def voslashbij(stree: SynTree) -> List[SynTree]:
    '''

    :param stree: syntactic structuire to be analysed
    :return: List of matching nodes

    The function *voslashbij* uses the function *auxvobij* to find non-adjacent R-pronoun + adposition cases:

    .. autofunction:: queryfunctions::auxvobij
          :noindex:


    '''
    results = auxvobij(stree, notadjacent)
    return results

def vobijpred(obj1node, headnode, stree) -> bool:
    #check for adjacency  (er naar is ok, er gisteren naar not)
    cond1 = adjacent(headnode, obj1node, stree)

    # check whether the obj1node precedes the headnode: daar naar is ok, naar daar is not ok
    headposition = int(getattval(headnode, 'end'))
    obj1position = int(getattval(obj1node, 'end'))
    cond2 = obj1position < headposition
    result = cond1 and cond2
    return result

