from collections import Counter, defaultdict
from math import isnan

from sastadev import readcsv
from sastadev.conf import settings
from sastadev.counterfunctions import counter2liststr
from sastadev.xlsx import getxlsxdata, mkworkbook

permprefix = 'perm_'

permsilvercolcount = 11   # number of columns in the silverperm files

user1col = 0
user2col = 1
user3col = 2
moreorlesscol = 3
qidcol = 4
uttidcol = 8
poscol = 9

uttidscol = 4  # in paltinum-edited tsv files

nots = ['not']
oks = ['ok', 'oke']
undecideds = ['?', 'ok/not', 'not/ok']
allowedoknots = oks + nots + undecideds
legalmoreorlesses = ['More examples', 'Missed examples']
comma = ','
commaspace = ', '

platinumchecksuffix = '_platinum.check.tsv'
platinumcheckeditedsuffix = '_platinum.check-edited.tsv'
platinumsuffix = '.platinum.tsv'
platinumeditedsuffix = '.platinum-edited.tsv'


def write2excel(datadict, header, filename):
    data = [datadict[key] for key in datadict]
    workbook = mkworkbook(filename, [header], data)
    workbook.close()


def getheader(data):
    if data is None:
        result = []
    else:
        result = data.head()
    return result


def checkpermformat(header, data, colcount, strict=True):
    result = True
    lheader = len(header)
    if (lheader == 0 or header == ['']) and data == []:
        return True
    result = lheader == colcount
    if result:
        rowctr = 0
        for row in data:
            rowctr += 1
            lrow = len(row)
            result = lrow == colcount
            if not result:
                settings.LOGGER.error('Wrong # columns ({} instead of {}), row {}'.format(lrow, colcount, rowctr))
                if strict:
                    exit(-1)
                else:
                    return False
    else:
        settings.LOGGER.error('Wrong # columns ({} instead of {}) in the header'.format(lheader, colcount,))
        if strict:
            exit(-1)
        else:
            return False
    return result


def updatepermdict(fullname, permdict):
    silverheader, silverdata = getxlsxdata(fullname)
    colsok = checkpermformat(silverheader, silverdata, permsilvercolcount, strict=False)
    silverfulldatadict = silverdata2dict(silverdata)

    #Voeg silverfulldatadict toe aan permdict
    for key in silverfulldatadict:
        if key not in permdict:
            permdict[key] = silverfulldatadict[key]
        elif not rowsequal(silverfulldatadict[key], permdict[key]):
            settings.LOGGER.warning('Key: {} Value:\n ({}) \noverwritten by value:\n {};\n File: {}'.format(key, permdict[key], silverfulldatadict[key], fullname))

    return permdict, silverheader


def rowsequal(row1, row2, casesensitive=False):
    if len(row1) != len(row2):
        return False
    pairs = zip(row1, row2)
    for el1, el2 in pairs:
        if isinstance(el1, str) and isinstance(el2, str):
            if el1.lower() != el2.lower():
                return False
        elif el1 != el2:
            return False
    return True


def getsilverannotations(perm_silverfullname, platinumcheckeditedfullname,
                         platinumcheckfullname, silvercheckfullname,
                         platinumfullname, platinumeditedfullname, goldscores):

    # -lees perm_silverfulldata in, voeg toe aan perm_silverfulldatadict
    perm_silverfulldatadict = dict()
    perm_silverfulldatadict, perm_header = updatepermdict(perm_silverfullname, perm_silverfulldatadict)

    # lees platinumcheckeditedfilename in, voeg toe aan perm_silverfulldatadict
    perm_silverfulldatadict, silverheader = updatepermdict(platinumcheckeditedfullname, perm_silverfulldatadict)

    #-lees platinmumcheck in, voeg toe aan perm_silverfulldatadict
    perm_silverfulldatadict, silverheader = updatepermdict(platinumcheckfullname, perm_silverfulldatadict)

    #-schrijf de prem_silverfulldatadict weg naar een nieuwe perm_silverfilename
    write2excel(perm_silverfulldatadict, silverheader, perm_silverfullname)

    #maak de silver file (platinum)--zie functie mksilver maar herschreven want je hebt de files al gelezen
    #@@
    mksilver(perm_silverfulldatadict, silvercheckfullname, platinumfullname, platinumeditedfullname, goldscores)

    #loop alle entries af in  platinumcheck, indien in perm_silverfulldatadict, [User 1-3] + entry{3:]
    # print dit naar de platinumcheckfile@@
    # of return de perm_silverfulldatadict hier en doe bovenstaande in de main loop waar je de file nu al uitschrijft
    return perm_silverfulldatadict


def clean(inval):
    #if type(inval) != str:
    #    print('nonstring value: {}'.format(inval))
    instr = str(inval)
    result = instr.strip()
    result = result.lower()
    return result


def listminus(list1, list2):
    clist1 = Counter(list1)
    clist2 = Counter(list2)
    cresult = clist1 - clist2
    result = counter2liststr(cresult)
    return result


def nono(inval):
    result = (inval is None) or (inval == 0) or (inval == []) or (inval == '')
    return result


def myisnan(inval):
    try:
        result = isnan(inval)
    except Exception:
        result = False
    return result


def silverdata2dict(silverdata):
    #make a dictionary out of data: a list of rows
    #silverdict = dict()
    silverfulldatadict = dict()
    if silverdata is not None:
        maxrow = len(silverdata)
        for rowctr in range(maxrow):
            therow = silverdata[rowctr]
            user1 = therow[user1col]
            user2 = therow[user2col]
            user3 = therow[user3col]
            qid = therow[qidcol]
            uttid = str(therow[uttidcol])
            pos = therow[poscol]
            thekey = (qid, uttid, pos)
            # only add it when any of user1, user2, user3 has a nonempty value
            if not (nono(user1) and nono(user2) and nono(user3)):
                #silverdict[thekey] = (user1, user2, user3)
                silverfulldatadict[thekey] = silverdata[rowctr]
    return silverfulldatadict  # , silverdict


def mksilver(permsilverdict, silvercheckfullname, platinumfullname, platinumeditedfullname, goldscores):

    # read the silvercheckfile
    silverheader, silvercheckdata = getxlsxdata(silvercheckfullname)

    # determine which uttids have to be removed
    undecidedcounter = 0
    toremove = defaultdict(list)
    maxrow = len(silvercheckdata)
    for row in range(maxrow):
        currow = silvercheckdata[row]
        moreorless = currow[moreorlesscol]
        if moreorless not in legalmoreorlesses:
            settings.LOGGER.error('Unexpected value in row {}: {}. File {}'.format(row, moreorless, silvercheckfullname))
        if moreorless == 'Missed examples':
            continue
        qid = currow[qidcol]
        uttid = str(currow[uttidcol])
        pos = currow[poscol]
        if (qid, uttid, pos) in permsilverdict:
            curpermrow = permsilverdict[(qid, uttid, pos)]
            (user1, user2, user3) = curpermrow[user1col], curpermrow[user2col], curpermrow[user3col]
            cleanuser1 = clean(user1)
            if cleanuser1 not in allowedoknots:
                settings.LOGGER.error('Unexpected value in row {}: {}. File {}'.format(row, user1, silvercheckfullname))
            if cleanuser1 not in oks:
                toremove[qid].append(uttid)
            if cleanuser1 in undecideds:
                undecidedcounter += 1
        else:
            pass
            #settings.LOGGER.warning('No Silver remark for row {}: {}. File {}; qid={}, uttid={}, pos={}'.format(row, moreorless, silvercheckfullname, qid, uttid, pos))
    junk = 0
    if undecidedcounter > 0:
        settings.LOGGER.info('{} undecided in file {}'.format(undecidedcounter, silvercheckfullname))
    # read the platinumfile
    (header, platinumdata) = readcsv.readheadedcsv(platinumfullname)
    newrows = []
    for (rowctr, row) in platinumdata:
        theqid = row[0]
        if theqid in toremove:
            toremoveids = [str(x) for x in toremove[theqid]]
            olduttids_string = row[uttidscol]
            rawolduttids = olduttids_string.split(comma)
            olduttids = [clean(x) for x in rawolduttids]
            toremoveCounter = Counter(toremoveids)
            olduttsCounter = Counter(olduttids)
            goldcounter = goldscores[theqid][2] if theqid in goldscores else Counter()
            newCounter = (olduttsCounter - toremoveCounter) | goldcounter  # all gold results must stay in
            newuttids_string = counter2liststr(newCounter)
            #newuttids_string = listminus(olduttids, toremoveids)
            newrow = row[:4] + [newuttids_string] + row[uttidscol + 1:]
        else:
            newrow = row
        newrows.append(newrow)

    # write the results to a new edited platinumfile

    readcsv.writecsv(newrows, platinumeditedfullname, header=header)
