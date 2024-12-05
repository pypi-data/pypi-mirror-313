from collections import Counter

from sastadev.allresults import ResultsKey, mkresultskey
from sastadev.conf import settings

qidcolheader = 'id'
uttcolheader = 'uttids'
tab = '\t'
comma = ','
platinumheaderrows = 0


def getreskey(rawcell: str) -> ResultsKey:
    '''
    older / manually created versions of a reference file can contain simply a QId here, newer ones have a ResultKey string
    :param cell:
    :return:
    '''
    cell = rawcell.strip()
    cellparts = cell.split('/')
    if len(cellparts) == 2:
        result = (cellparts[0], cellparts[1])
    elif len(cellparts) == 1:
        result = mkresultskey(cell)
    else:
        result = cell
        settings.LOGGER.error(f'Unknown value {cell} encountered')
    return result


def read_referencefile(infilename, logfile):
    '''
    a reference file is tsv file which contains a header with at least two column headers (idcolheader, uttcolheader)
    :param infilename:
    :return: a dictionary with for each ResultsKey  a Counter for the utterance ids
    '''
    infile = open(infilename, 'r')
    rowctr = 0
    results = {}
    for line in infile:
        if rowctr == platinumheaderrows:
            rowstr = line.lower()
            rowlist = rowstr.split(tab)
            try:
                qidcol = rowlist.index(qidcolheader)
            except ValueError:
                print('Error reading reference file; no ID column header',
                      infilename, file=logfile)
                exit(-1)
            try:
                uttcol = rowlist.index(uttcolheader)
            except ValueError:
                print('Error reading reference file: no uttids column header in',
                      infilename, file=logfile)
                exit(-1)
        elif rowctr > platinumheaderrows:
            rowstr = line[:-1]
            rowlist = rowstr.split(tab)
            reskey = getreskey(rowlist[qidcol])
            utts = rowlist[uttcol]
            if utts == '':
                uttlist = []
            else:
                rawuttlist = utts.split(comma)
                uttlist = [uttid.strip() for uttid in rawuttlist]
            results[reskey] = Counter(uttlist)
        rowctr += 1
    infile.close()
    return results
