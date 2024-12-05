from typing import List

from sastadev.sastatypes import SynTree
from sastadev.treebankfunctions import clausecats, getattval

conjxpath = './/node[@cat="conj" and (count(node)=3 or count(node)=5)]'

#//node[@cat="conj" and (count(node)=3 or count(node)=5) and
#node[@rel="crd" and (@lemma="en" or @lemma="of")] and
#node[@rel="cnj" and @cat!="smain" and @cat!="sv1" and @cat!="whq"]
#]


def getptcat(node):
    pt = getattval(node, 'pt')
    cat = getattval(node, 'cat')
    if pt != '':
        result = pt
    elif cat != '':
        result = cat
    else:
        result = None
    return result


def xenx(tree: SynTree) -> List[SynTree]:
    '''
    The function *xenx* selects conjuncts consisting of 3 or 5 children: either two
    conjuncts and one coordinator, or three conjuncts and 2 coordinators. The conjuncts
    must have the same values for *pt*  or *cat* attributes.
    '''
    results = []
    conjs = tree.xpath(conjxpath)
    #print(conjs)
    for conj in conjs:
        include = True
        firstptcat = None
        crdresult = None
        for child in conj:
            #print('include=', include)
            #print('child', getyield(child))
            childrel = getattval(child, 'rel')
            childptcat = getptcat(child)
            childlemma = getattval(child, 'lemma')
            #print(childrel, childptcat, firstptcat, '<'+childlemma+'>')
            if include:
                if childrel == 'crd':
                    include = include and (childlemma in ['en', 'of'])
                    crdresult = child
                elif childrel == 'cnj':
                    if childptcat is None:
                        include = False
                    if firstptcat is None:
                        firstptcat = childptcat
                    include = include and (childptcat == firstptcat) and childptcat not in clausecats
            #print('include=', include)
        #print('final: include=', include)
        if include and crdresult is not None:
            results.append(crdresult)
    return results
