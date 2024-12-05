import os

from sastadev.conf import settings
from sastadev.constants import intreebanksfolder, outtreebanksfolder
from sastadev.dedup import filledpauseslexicon
from sastadev.treebankfunctions import (getattval, getnodeyield, getstree,
                                        getuttid, getyield, onbvnwdet)

digits2 = r'\d\d'

asta = 'asta'
tarsp = 'tarsp'
stap = 'stap'
dld = 'dld'
schl = 'schlichting'
auris = 'auris'


def shorten(fullname):
    _, filename = os.path.split(fullname)
    basename, _ = os.path.splitext(filename)
    return basename


def getpaths(dataset):
    result = [os.path.join(settings.DATAROOT, 'VKLStap', intreebanksfolder),
              os.path.join(settings.DATAROOT, 'VKLStap', outtreebanksfolder)]
    return result


paths = {}

paths[stap] = getpaths('VKLStap')
paths[asta] = getpaths('VKLASTA')
paths[tarsp] = getpaths('VKLTarsp')
paths[dld] = getpaths('Auris')

ext = '.xml'


class Ngram:
    def __init__(self, n, cond):
        self.n = n
        self.cond = cond


def commonancestor(node1, node2, stree, ancestorcond):
    nodes = stree.xpath('.//node')
    ancestorcandidates = [n for n in nodes if ancestorcond(n)]
    for anc in ancestorcandidates:
        descendants = anc.xpath('.//node')
        if node1 in descendants and node2 in descendants:
            return True
    return False


def lemma(x):
    return getattval(x, 'lemma')


def word(x):
    return getattval(x, 'word')


# det = lambda x : pt(x) == 'lw' or (pt(x) == 'vnw' and getattval(x, 'vwtype') in {'aanw', 'bez'})

def pt(x):
    return getattval(x, 'pt')


def findmatches(ngram, leaves):
    matches = []
    for i in range(len(leaves) - ngram.n + 1):
        if ngram.cond(leaves[i:i + ngram.n], leaves, i):
            newmatch = (i, i + ngram.n)
            matches.append(newmatch)
    return matches


def getfilenames(ds, session=None):
    inpath = paths[ds]
    if session is not None:
        def cond(x): return (x + 1 == session)
    else:
        def cond(_): return True
    infullnames = [os.path.join(path, ifn) for path in paths[ds] for ifn in os.listdir(path)]
    return infullnames


def Rpronoun(el):
    result = lemma(el) in {'er', 'hier', 'daar'}
    return result


def ispv(n):
    result = pt(n) == 'ww' and getattval(n, 'wvorm') == 'pv'
    return result


def sipvjpvjsi(ns, stree):
    resultmatches = []
    ngram1 = Ngram(2, cond13)
    matches = findmatches(ngram1, ns)
    for (b, e) in matches:
        vnw1 = ns[b]
        pv1 = ns[e - 1]
        pv2found = False
        for mc in range(e, len(ns) - 2):
            if ispv(ns[mc]):
                if word(ns[mc]).lower() == word(pv1).lower():
                    pv2 = ns[mc]
                    if not commonancestor(pv1, pv2, stree, lambda x: getattval(x, 'cat') == 'smain'):
                        pv2found = True
                        pv2pos = mc
                    break
            else:
                mc += 1
        if pv2found:
            vnw2found = word(ns[pv2pos + 1]).lower() == word(vnw1).lower()
            if vnw2found:
                resultmatch = (b, e, mc, mc + 2)
                resultmatches.append(resultmatch)
    return resultmatches


def cond17f(ns, lvs, i):
    result = lemma(ns[0]) == 'te'
    result = result and getattval(ns[1], 'his') == 'te_verb'
    result = result and lemma(ns[2]) == 'te'
    return result


def cond1(ns, _, i): return pt(ns[0]) == 'vnw' and pt(ns[1]) == 'ww' and getattval(ns[1], 'wvorm') == 'pv' and \
    pt(ns[2]) == 'vnw' and lemma(ns[0]) == lemma(ns[2]) and pt(ns[3]) == 'ww' and \
    getattval(ns[3], 'wvorm') == 'pv'


def det(el): return (pt(el) == 'lid'
                     or (pt(el) == 'vnw' and getattval(el, 'vwtype') in {'aanw', 'bez'})
                     or (pt(el) == 'vnw' and getattval(el, 'vwtype') == 'onbep' and onbvnwdet(el))
                     ) and \
    not Rpronoun(el)   # and getattval(el, 'positie') == 'prenom' left out


def erhierdaar(el): return lemma(el) in {'er', 'hier', 'daar'}


def cond2(ns, _, i): return pt(ns[0]) == 'vz' and det(ns[1]) and (not erhierdaar(ns[1])) and pt(ns[2]) == 'vz' and \
    det(ns[3]) and (not erhierdaar(ns[3]))


def cond3(ns, _, i): return pt(ns[0]) == 'n' and pt(ns[1]) == 'n'
def cond4(ns, lvs, i): return lemma(ns[0]) == "," and ns[1] == lvs[-1]
def cond4a(ns, lvs, i): return lemma(ns[0]) == "," and pt(ns[2]) == 'let' and ns[2] == lvs[-1]
def cond5(ns, _, i): return lemma(ns[0]) == 'nou' and lemma(ns[1]) == 'ja'
def cond6(ns, lvs, i): return pt(ns[0]) == 'n' and len([lv for lv in lvs[:i - 1] if lemma(lv) == lemma(ns[0])]) > 1
def cond7(ns, lvs, i): return pt(ns[0]) == 'vg' and det(ns[1]) and lemma(ns[2]) == lemma(ns[0]) and det(ns[3])
def cond8(ns, lvs, i): return word(ns[2]).startswith(word(ns[0])) and word(ns[3]).startswith(word(ns[1]))


def cond9(ns, _, i): return pt(ns[0]) == 'vnw' and getattval(ns[0], 'vwtype') == 'pers' and pt(ns[1]) == 'ww' and \
    getattval(ns[1], 'wvorm') == 'pv' and pt(ns[2]) == 'vnw' and pt(ns[3]) == 'ww' and \
    getattval(ns[3], 'wvorm') == 'pv'  # and \
# (word(ns[0]) == word(ns[2]) or word(ns[1]) == word(ns[3]) or lemma(ns[1]) == lemma(ns[3]))


def cond10(ns, lvs, i): return pt(ns[0]) == 'vnw' and getattval(ns[0], 'vwtype') == 'pers' and \
    pt(ns[1]) == 'ww' and getattval(ns[1], 'wvorm') == 'pv' and \
    pt(ns[2]) != 'ww' and word(ns[3]) == word(ns[1]) and word(ns[4]) == word(ns[0])


def cond11(ns, lvs, i): return lemma(ns[0]) == lemma(ns[2]) and lemma(ns[1]) == lemma(ns[3]) and \
    (word(ns[0]) != word(ns[2]) or word(ns[1]) != word(ns[3]))


def cond12(ns, lvs, i): return pt(ns[0]) == 'vz' and det(ns[1]) and pt(ns[2]) == 'vz' and det(ns[3])  # == cond2


def cond13(ns, lvs, i): return pt(ns[0]) == 'vnw' and getattval(ns[0], 'vwtype') == 'pers' and pt(ns[1]) == 'ww' and \
    getattval(ns[1], 'wvorm') == 'pv'


def cond14(ns, lvs, i): return ns[0] != lvs[0] and lemma(ns[0]) != 'nou' and (lemma(ns[1]) in filledpauseslexicon or pt(ns[0]) == 'tsw') and lemma(ns[2]) == 'nee'
def cond15(ns, lvs, i): return ns[0] != lvs[0] and lemma(ns[1]) == 'nee'


def cond16(ns, lvs, i): return det(ns[0]) and det(ns[2]) and lemma(ns[1]) == lemma(ns[3]) \
    and pt(ns[1]) == 'n' and pt(ns[3]) == 'n'
def cond16a(ns, lvs, i): return lemma(ns[0]) in {'een', 'geen'} and lemma(ns[2]) in {'een', 'geen'} and lemma(ns[1]) == lemma(ns[3]) \
    and pt(ns[1]) == 'n' and pt(ns[3]) == 'n'


def cond17(ns, lvs, i): return lemma(ns[0]) == 'te' and getattval(ns[1], 'his') == 'te_verb' and lemma(ns[2]) == 'te'
# cond17 = cond17f
def cond17a(ns, lvs, i): return lemma(ns[0]) == 'te' and word(ns[1]) == 'kregen' and lemma(ns[2]) == 'te'


def cond18(ns, lvs, i): return pt(ns[0]) == 'vz' and lemma(ns[1]) in {'dit', 'dat', 'deze', 'die'}


ngram1 = Ngram(4, cond1)
ngram2 = Ngram(4, cond2)
ngram3 = Ngram(2, cond3)
ngram4 = Ngram(2, cond4)  # uitloop maar zonder punc daarachter
ngram4a = Ngram(3, cond4a)  # uitlopp maar met punc daarachter
ngram5 = Ngram(2, cond5)
ngram6 = Ngram(1, cond6)
ngram7 = Ngram(4, cond7)
ngram8 = Ngram(4, cond8)  # partial repeat sequence
ngram9 = Ngram(4, cond9)  # vnw pv vnw pv
ngram10 = Ngram(5, cond10)  # vnwj pvi x pvi vnwj
ngram11 = Ngram(4, cond11)  # lemma_i lemma_j lemma_i lemma_j
ngram12 = Ngram(4, cond12)  # vz det vz det
ngram14 = Ngram(3, cond14)  # fp/tsw + nee , to apply to the uncleaned leaves
ngram15 = Ngram(2, cond15)  # word + nee, to apply to the cleanleaves
ngram16 = Ngram(4, cond16)  # geen beroerte een beroerte
ngram16a = Ngram(4, cond16a)  # geen beroerte een beroerte test
ngram17 = Ngram(4, cond17)  # te kregen te krijgen
ngram17a = Ngram(4, cond17a)  # te kregen te krijgen test
ngram18 = Ngram(2, cond18)  # met dit


def main():

    infullnames = []
    for ds in [tarsp, asta, stap, dld]:
        infullnames += getfilenames(ds)

    # for ds in [asta]:
    #    infullnames += getfilenames(ds, session=4)

    for infullname in infullnames:
        short = shorten(infullname)
        fulltreebank = getstree(infullname)
        if fulltreebank is not None:
            treebank = fulltreebank.getroot()
            for tree in treebank:
                uttid = getuttid(tree)
                leaves = getnodeyield(tree)
                cleanleaves = [leave for leave in leaves if getattval(leave, 'word') not in filledpauseslexicon]
                cleanwordlist = [getattval(leave, 'word') for leave in cleanleaves]
                matches = findmatches(ngram18, cleanleaves)
                # matches = sipvjpvjsi(cleanleaves, tree)
                for match in matches:
                    uttid = getuttid(tree)
                    cleanleaves_str = [word(el) for el in cleanleaves]
                    print(short, uttid, match, cleanleaves_str, getyield(tree))


if __name__ == '__main__':
    main()
