import os
import re

from sastadev.xlsx import getxlsxdata


def remove(patlist, rawstr):
    result = rawstr
    for pat in patlist:
        result = re.sub(pat, '', result)
    return result


def clean(rawutt):
    pats = [r'dd:', r'\[', r'\]', r'<', r'>', r'0', r'\*', r'c:', r'\+', r'com:', r'=']
    result = remove(pats, rawutt)
    result = re.sub(r'(?i)iemand\s*\|\s*iets', 'iemand', result)
    result = re.sub(r'(?i)iets\s*\|\s*iemand', 'iemand', result)
    result = re.sub(r'\u2018', "'", result)
    result = re.sub(r'\u2019', "'", result)

    return result


metamodel = '##META text {att} = {val}'

inpath = r'C:\Users\Odijk101\Dropbox\jodijk\Utrecht\researchproposals\MWEs'
infilename = 'UitdrukkingenNL expanded_dedup Current.xlsx'

infullname = os.path.join(inpath, infilename)

rawheader, data = getxlsxdata(infullname, sheetname='Data')

header = [re.sub(r'\s', '_', rh) for rh in rawheader]

utterancecol = 4  # kolom E

peplines = []
for row in data:
    lrow = len(row)
    for i in range(lrow):
        att = header[i]
        val = row[i]
        newmeta = metamodel.format(att=att, val=val)
        peplines.append(newmeta)
    rawutt = row[utterancecol]
    cleanutt = clean(rawutt)
    peplines.append(cleanutt)
    peplines.append('')     # blank line to finish input for this utterance

outpath = inpath
outfilename = 'MWE2022-08-03.txt'
outfullname = os.path.join(outpath, outfilename)
with open(outfullname, 'w', encoding='utf8') as outfile:
    for pepline in peplines:
        print(pepline, file=outfile)
