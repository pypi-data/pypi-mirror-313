

def sumfreq(thecounter):
    result = 0
    for (_, cnt) in thecounter.items():
        result += cnt
    return result


def getevalscores(resultscount, referencecount, intersectioncount):
    if referencecount == 0:
        recall = 100
        if resultscount == 0:
            precision = 100
        else:
            precision = 0
    else:
        recall = intersectioncount / referencecount * 100
    if resultscount == 0:
        precision = 100
        if referencecount == 0:
            recall = 100
        else:
            recall = 0
    else:
        precision = intersectioncount / resultscount * 100
    if recall + precision == 0:
        f1score = 0
    else:
        f1score = (2 * recall * precision) / (recall + precision)
    return (recall, precision, f1score)


def getscores(results, reference):
    intersection = results & reference
    lintersection = sumfreq(intersection)
    lresults = sumfreq(results)
    lreference = sumfreq(reference)
    if lreference == 0:
        recall = 100
        if lresults == 0:
            precision = 100
        else:
            precision = 0
    else:
        recall = lintersection / lreference * 100

    if lresults == 0:
        precision = 100
        if lreference == 0:
            recall = 100
        else:
            recall = 0
    else:
        precision = lintersection / lresults * 100
    if recall + precision == 0:
        f1score = 0
    else:
        f1score = (2 * recall * precision) / (recall + precision)
    return (recall, precision, f1score)
