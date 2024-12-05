'''
The module *Sziplus* implements two TARSP language measures:

* Vr5+: through the function *vr5plus*:

  .. autofunction:: Sziplus::vr5plus

  In the meantime a different implementation using macros has replaced this function,
  so it has become obsolete

* 6+: through the function *sziplus6*:

  .. autofunction:: Sziplus::sziplus6

'''


from typing import List

from sastadev.sastatypes import SynTree
from sastadev.treebankfunctions import getattval

#: the variable (constant) *clausequery*  is an XPath query that searches for nodes
#: that are clauses.
clausequery = './/node[@cat="smain" or @cat="ssub" or @cat="sv1" or ' \
              '@cat="whq" or @cat="whrel" or @cat="whsub" or @cat="cp" ]'

#: the variable (constant) *vrquery* is an XPath query that searchs for nodes that are
#: wh-questions.
vrquery = './/node[@cat="whq" or @cat="whsub" or (@cat="whrel" and ../node[@cat="top"])]'


def empty(alist: list) -> bool:
    return (alist == [])


def notempty(alist: list) -> bool:
    return (not empty(alist))


def noposcatin(node: SynTree) -> bool:
    '''
    The function *noposcatin* checks whether a node has none of the following
    attributes: *pt*, *pos*, *cat*
    '''
    result = 'pt' not in node.attrib and 'pos' not in node.attrib and 'cat' not in node.attrib
    return result


def isindexnode(node: SynTree) -> bool:
    '''
    The function *isinexnode* determines whether a node is an *index node*. It is if:

    * the node has an *index* attribute
    * the node has no part of speech or syntactic category attribute (as determined by the function *noposcatin*).

    The function *noposcatin* is defined as follows:

    .. autofunction:: Sziplus::noposcatin

    * **Remark** The function *noposcatin* is better replaced by a function that checks for the absence of the attributes *cat* and *word*.

    '''
    result = 'index' in node.attrib and noposcatin(node)
    return result


def isvcinforppart(node: SynTree) -> bool:
    '''
    The function *isvcinforppart* determines whether a node is a node for a nonfinite
    verbal complement. That is the case if

    *  its category is one of *inf*, *teinf*, or *ppart*
    * its relation has the value *vc*

    '''
    rel = getattval(node, 'rel')
    cat = getattval(node, 'cat')
    if rel == 'vc' and cat in ['inf', 'teinf', 'ppart']:
        result = True
    else:
        result = False
    return result


def isrealnode(node: SynTree) -> bool:
    '''
    The fucntion *isrealnode* determines whether a nide is a real node, which it is if:

    * it is not a node for an interpunction sign
    * it is not a nonfinite complement
    * if it is not a separable particle word of a verb
    * if it is not an index node 9as detemined by the function *isindexnode*)

    The function *isindexnode* is defined as follows:

    .. autofunction:: Sziplus::isindexnode
    '''
    pt = getattval(node, 'pt')
    rel = getattval(node, 'rel')
    if pt == 'let':
        result = False
    elif isvcinforppart(node):
        result = False
    elif rel == 'svp' and 'pt' in node.attrib:
        result = False
    elif isindexnode(node):
        result = False
    else:
        result = True
    return result


def isbodysv1(node: SynTree) -> bool:
    if node is None:
        result = False
    else:
        result = 'cat' in node.attrib and node.attrib['cat'] in ['sv1', 'ssub'] \
                 and 'rel' in node.attrib and node.attrib['rel'] == 'body'
    return result


def getnodecount(clause: SynTree) -> int:
    '''
    The function *getnodecount* counts the number of real nodes in *clause*. It
    considers each child of *clause*:

    * if the child is a real node (as determined by the function *isrealnode*, the counter goes up by 1

     * if it is an *sv1* or *ssub* clause body, the function *getnodecount* is recursively applied to the child, and the result added to the counter. This is for structures such whq[ *wie* body/sv1[ *heeft dat gedaan* ]] and cp[ *omdat* body/ssub[ *hij ziek is* ]]

    * if it is a nonfinite complement (as determined by the function *isvcinforppart*), the function *getnodecount* is recursively applied to child, the result added to the counter, minus 1 (we do not count the verb inside a nonfinite complement because it is part of the "gezegde".


    The function *isrealnode* is defined as follows:

    .. autofunction:: Sziplus::isrealnode

    The function *isvcinforppart* is defined as follows:

    .. autofunction:: Sziplus::isvcinforppart

    '''
    nodectr = 0
    for child in clause:
        if isrealnode(child):
            nodectr += 1
        elif isbodysv1(child):
            nodectr += getnodecount(child)
        elif isvcinforppart(child):
            nodectr += getnodecount(child) - 1  # we do no count the verb because it is part of the 'gezegde'
    return nodectr


def sziplus(syntree: SynTree, i: int) -> List[SynTree]:
    '''
    The function *sziplus* takes a SynTree *syntree* and an integer *i* and uses the
    function *nodeiplus* by applying it to  *syntree*, *i*, and *clausequery*:

    .. autodata:: Sziplus::clausequery

    The function *nodeiplus* is defined as follows:

    .. autofunction:: Sziplus::nodeiplus

    '''
    results = nodeiplus(syntree, i, clausequery)
    return results

# vr5plus is obsolete because there is composed language measure for it.


def vr5plus(syntree: SynTree) -> List[SynTree]:
    '''
    The function *vr5plus* is intended to implement the TARSP language measure *Vr5+*.
    it does so by applying the function *nodeiplus* to the syntree, integr 5 and the
    Xpath query *vrquery*.

    The Xpath *vrquery* is defined as follows:

    .. autodata:: Sziplus::vrquery

    The function *nodeiplus* is defined as follows:

    .. autofunction:: Sziplus::nodeiplus
    '''
    results = nodeiplus(syntree, 5, vrquery)
    return results


def nodeiplus(syntree: SynTree,
              i: int,
              query: str) -> List[SynTree]:
    '''
    The function *nodeiplus* counts the number of real nodes in the nodes
    resulting from applying the Xpath query *query* to *syntree*. If this count is
    greater or equal to *i*, the node is added to the results.

    It makes use of the function *getnodecount*, which is defined as follows:

    .. autofunction:: Sziplus::getnodecount
    '''
    clauses = syntree.xpath(query)
    results = []
    for clause in clauses:
        nodecount = getnodecount(clause)
        if nodecount >= i:
            results.append(clause)
    return results


def sziplus6(syntree: SynTree) -> List[SynTree]:
    '''
    The function *sziplus6* implements the TARSP language measure *6+*. It makes use of
    the function *sziplus*, which is applied to the *syntree* in combination with the
    integer *6*.

    .. autofunction:: Sziplus::sziplus

    * **Remark** The function *sziplus* was written in an early stage, but probably can now be better
    rewritten as a composed language measure.

    '''
    results = sziplus(syntree, 6)
    return results
