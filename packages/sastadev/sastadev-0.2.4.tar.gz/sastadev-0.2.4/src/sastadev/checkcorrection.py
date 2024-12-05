'''
The script *checkcorrections* compares the errorlogging file with the error reference file

The error reference file can be found in the bronze subfolder of a dataset and is called <dataset>_error_ref.xlsx.

Warning: The error reference files are attempts to get to reference files. They mainly check for precision,
not for recall. They will very likely require several new versions.
'''

import os
from optparse import OptionParser

from sastadev.conf import settings
from sastadev.constants import bronzefolder, loggingfolder, resultsfolder
from sastadev.stringfunctions import nono
from sastadev.xlsx import getxlsxdata, mkworkbook


def main():

    parser = OptionParser()
    parser.add_option("-d", "--dataset", dest="dataset",
                      help="Dataset to be dealt with")
    parser.add_option("-r", "--reference", dest="referencepath",
                      help="Path to the referencedata")

    (options, args) = parser.parse_args()

    if nono(options.dataset):
        print('No dataset specified. Aborting')
        exit(-1)

    if nono(options.referencepath):

        options.referencepath = os.path.join(settings.DATAROOT, options.dataset, bronzefolder)

    missedcorrectionslist = []
    originalsents = {}

    resultspath = os.path.join(settings.DATAROOT, options.dataset, resultsfolder)
    loggingpath = os.path.join(settings.DATAROOT, options.dataset, loggingfolder)

    dataprefix = options.dataset

    errorloggingfilename = dataprefix + '_errorlogging.xlsx'
    errorloggingfullname = os.path.join(loggingpath, errorloggingfilename)

    errorreffilename = dataprefix + '_error_ref.xlsx'
    errorreffullname = os.path.join(options.referencepath, errorreffilename)

    logheader, logdata = getxlsxdata(errorloggingfullname)
    refheader, refdata = getxlsxdata(errorreffullname)

    refdict = {(row[0].lower(), row[1]): row[3] for row in refdata}

    correctcorrections = 0
    missedcorrections = 0
    wrongcorrections = 0
    for row in logdata:
        key = (row[0].lower(), row[5])
        if 'Original' in row[4]:
            originalsents[key] = row[7]
        if 'BEST' in row[10]:
            logsent = row[9]
            if key not in refdict:
                print('Missing example in refdict: {}'.format(key))
                print(row[9])
                missedcorrections += 1
                origsent = originalsents[key] if key in originalsents else ''
                newmissedcorrection = [row[0], row[5], origsent, logsent]
                missedcorrectionslist.append(newmissedcorrection)
            else:
                refsent = refdict[key]
                if refsent != logsent:
                    print('Mismatch: {}'.format(key))
                    print('refsent=<{}>'.format(refsent))
                    print('logsent=<{}>'.format(logsent))
                    wrongcorrections += 1
                else:
                    correctcorrections += 1

    allcorrections = correctcorrections + wrongcorrections + missedcorrections

    correctioncounts = [correctcorrections, wrongcorrections, missedcorrections]
    labels = ['correct corrections', 'wrong corrections', 'missed corrections']
    labeled_corrections = zip(labels, correctioncounts)

    print('\nSummary:\n')
    for label, corr in labeled_corrections:
        print('{} = {} ({:.2f}%)'.format(label, corr, corr / allcorrections * 100))

    refaddfilename = f'{options.dataset}_newrefcandidates.xlsx'
    refadditions = os.path.join(options.referencepath, refaddfilename)
    wb = mkworkbook(refadditions, [refheader], missedcorrectionslist, freeze_panes=(0, 1))
    wb.close()


if __name__ == '__main__':
    main()
