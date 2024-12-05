import csv

from sastadev.conf import settings

tab = '\t'
mysep = tab


def readcsv(filename, sep=mysep, header=True, quotechar='"', encoding='utf8'):
    result = []
    try:
        infile = open(filename, 'r', encoding=encoding, newline='')
    except FileNotFoundError as e:
        settings.LOGGER.error(e)
        return result
    myreader = csv.reader(infile, delimiter=sep, quotechar=quotechar)
    # read the header if needed
    if header:
        next(myreader)
    rowctr = 1
    for row in myreader:
        result.append((rowctr, row))
        rowctr += 1
    infile.close()
    return result


def readheadedcsv(filename, sep=mysep, quotechar='"', encoding='utf8'):
    result = []
    header = []
    try:
        infile = open(filename, 'r', encoding=encoding, newline='')
    except FileNotFoundError as e:
        settings.LOGGER.warning(e)
        return header, result
    myreader = csv.reader(infile, delimiter=sep, quotechar=quotechar)
    # read the header
    try:
        header = next(myreader)
    except StopIteration as e:
        settings.LOGGER.warning(e)
        pass
    rowctr = 1
    for row in myreader:
        result.append((rowctr, row))
        rowctr += 1
    infile.close()
    return (header, result)


def writecsv(rows, filename, header=[], sep=tab, quotechar='"'):
    try:
        outfile = open(filename, 'w', encoding='utf8', newline='')
    except FileExistsError:
        pass
    mywriter = csv.writer(outfile, delimiter=sep, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
    if header != []:
        mywriter.writerow(header)
    for row in rows:
        mywriter.writerow(row)
    outfile.close()
