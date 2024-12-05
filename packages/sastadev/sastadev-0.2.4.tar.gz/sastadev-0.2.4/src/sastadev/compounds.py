'''
The module *compounds*:

* initialisez the compound dictionary *compounds*, which is a multidimensional Python dictionary
  Dict[str, Dict[int, str]], which maps a string (for a lemma in CELEX orthography HeadDiaNew)
  and a column number to the value of the cell with this column number in the CSV file from which it is derived:

   * e.g., compounds["aalbes"][0] == "NN"
   * e.g., compounds["aalbes"][2] == "N"


 The file from which it is derived is the CSV file (with backslash as separator) *Ncompounds-attempt2.txt*
 in subfolder compoundfiles in the code folder. It contains a header and three fields in each row:

  * FlatClass: the part of speech codes for the parts (lexical parts and affixes) e.g. NN for *aalbes*
  * HeadDiaNew: the orthography of the lemma, e.g. *aalbes*
  * Class: the part of speech code for the whole word, e.g. N for *aalbes*

  The file has been derived from the CELEX database.

* provides the functions getcompounds and iscompounds:
   * .. autofunction:: getcompounds
   * .. autofunction:: iscompound


'''


import csv
import os
from collections import defaultdict
from typing import Dict, List

from sastadev.conf import settings
from sastadev.sastatypes import SynTree
from sastadev.treebankfunctions import getattval

underscore = "_"
FlatClass = 0
HeadDiaNew = 1
Class = 2

Headers = {}
Headers[FlatClass] = "FlatClass"
Headers[HeadDiaNew] = "HeadDiaNew"
Headers[Class] = "Class"

comma = ","

dictfilename = os.path.join(settings.SD_DIR, 'data', 'compoundfiles', 'Ncompounds-attempt2.txt')
dictfile = open(dictfilename, 'r', encoding='utf8')

getwordsxpath = ".//node[@pt]"


def getcompounds(syntree: SynTree) -> List[SynTree]:
    '''
    .. _getcompounds-label:

    The function getcompounds takes a syntactic structure as input and returns a list of syntactic structures
    (nodes for words) that are compounds. It implements TARSP language measure T086 (SamZn). A node is considered
    to be a compound if its *pt* attribute has the value *n* (is a noun) and its lemma meets the
    condition iscompound(lemma).

    '''
    results = []
    tlist = syntree.xpath(getwordsxpath)
    for t in tlist:
        w = getattval(t, 'word')
        lemma = getattval(t, 'lemma')
        pt = getattval(t, 'pt')
        if pt == 'n' and iscompound(lemma):
            results.append(t)
    return results

# I do not know how to type this, because the nesting can be arbitrarily deep


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))


def iscompound(str: str) -> bool:
    '''
    The function iscompound checks whether the input string str is a compound.
    That is the case if

    * either it contains an underscore (lemmas of  strings recognised as a compound by Alpino contain an underscore),
    * or it is contained in the compound dictionary *compounds*.


    '''
    if underscore in str:
        result = True
    else:
        result = str in compounds
    return result


mysep = "\\"
myquotechar = ''

compounds: Dict[str, Dict[int, str]] = nested_dict(2, str)


# there is an error here, the file has a header, and that is also read in as a compound
# we should make  the character encoding explicit
settings.LOGGER.info("Initializing compound module...")
myreader = csv.reader(dictfile, delimiter=mysep)
for row in myreader:
    compounds[row[HeadDiaNew]][FlatClass] = row[FlatClass]
    compounds[row[HeadDiaNew]][Class] = row[Class]
