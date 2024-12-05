''''
This module is not used anymore
'''
from math import log

knownmethods = {'asta', 'stap', 'tarsp'}


def isknownmethod(mname):
    if mname is None:
        result = False
    else:
        result = mname.upper() in knownmethods
    return result


def getfnbases(method, maxval):
    model = knownmethods[method].basenamemodel
    width = max([2, int(log(maxval, 10)) + 1])
    results = []
    for i in range(1, maxval + 1):
        istr = str(i).rjust(width, '0')
        result = model.format(istr)
        results.append(result)
    return results
