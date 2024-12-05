'''
The module *iedims* deals with diminutive forms ending in *-ie*. Alpino cannot deal with such diminutives,
but the function *getjeforms* finds for a given word ending in *-ie* what the corresponding diminutives ending in
*-je* are.
There can be many, e.g. *kassie* can correspond to *kasje* but also to *kastje*.

To our knowledge, there are no established orthographic rules for these forms. Therefore we should be robust to
several alternative ways of writing these forms, e.g.

* Kees: Keesie, Keessie, or Kesie?: all are accepted
* Huub: Huupie, Huuppie, or Hupie?: all are accepted
* wijf: wijfie, or wijffie?: we allow both
* feest: fesie, feesie, or feessie?: we require *feessie* or *feesie*
* dag: daggie, or dachie? : we require *daggie*
* truc: trucie, truuccie, truukkie, or  trukie?: we cannot deal with any at this moment
* maag: magie or maaggie, maachie?: we allow *magie* or *maaggie*
* vaas: vasie or vaassie?: both are allowed


The module has been tested against a gold reference of all words ending in ie(s) from OpenSonaR.
The module to use for a renewed test is tests.iedims_test.py, the file is tests.iediminutives.iedimsgold2.csv

.. autofunction:: iedims::getjeforms
'''


import re
from typing import List, Optional

from sastadev import lexicon

comma = ','
semicolon = ';'
bigfilesep = semicolon
slash = '/'
epsilon = ''
vertbar = '|'


def bracket(str: str) -> str:
    result = r'(' + str + r')'
    return result


def drop(pattern: str, chars: str) -> str:
    '''
    The function *drop* returns a string in which only those  characters of *pattern* are retained  if they do not
    occur in *chars*
    '''
    lpattern = [c for c in pattern]
    newlpattern = [c for c in lpattern if c not in chars]
    newpattern = epsilon.join(newlpattern)
    return newpattern


def regexor(stringlist: List[str]) -> str:
    '''
    The function *regexor* joins a list of strings by means of a vertical bar
    '''
    result = vertbar.join(stringlist)
    return result


def makecic1j() -> str:
    '''
    The function *makecic1j* creates a string that is a regular expression in which any of the consonants from c1 (
    =pfksg) is preceded by an arbitrary distinct consonant.

    '''
    parts = []
    for c in c1:
        if c not in '[]':
            newpart1 = drop(call, c1)
            newpart = '[' + newpart1 + ']' + c
            parts.append(newpart)
    pattern = regexor(parts)
    return pattern


begin = r'^(.*)'

vowel = r'[aeiouy]'
bvowel = bracket(vowel)
call = r'[bcdfghjklmnpqrstvwxz]'
bcall = bracket(call)
wb = '^'
callorwb = call + '|' + wb
bcallorwb = bracket(callorwb)
doublevowel = r'aa|ee|oo|uu'
diphthong = 'au|ei|eu|ie|ij|oe|ou|ui'
c1 = r'[pfksg]'
bc1 = bracket(c1)
ie = r'(ie)'
s = '(s?)'
end = r'$'
v4 = r'\4'
v3 = r'\3'
v2 = r'\2'
twovowels = doublevowel + '|' + diphthong
btwovowels = bracket(twovowels)
bdiphthong = bracket(diphthong)
cic1j = makecic1j()
bcic1j = bracket(cic1j)

#: * **Pattern**  vvssie: words ending in two vowels, two identicsl consonants from [pfksg] plus *ie*, optionally followed by *s*
#: * **Replacement**: degeminate the consonants and replace *ie* by *je* and *tje*
#: * **Examples**  meissie -> meisje; Keessie -> keessie; feessie -> feestje;  wijffie -> wijfje, lieffie -> liefje,
# boekkie -> boekje;
#:
vvssiepattern = begin + btwovowels + bc1 + v3 + r'ie' + s + end
vvssiere = re.compile(vvssiepattern, re.IGNORECASE)
# vvssiereplace: degeminate the consonants and replace *ie* by *je*
vvssiereplace = r'\1\2\3je\4'
# vvssiereplacet: degeminate the consonants and replce *ie* by *tje*
vvssiereplacet = r'\1\2\3tje\4'

#: * **Pattern** vvsie: the same as vvssie but now with a single consonant.
#: * **Replacement**: simply replace *íe* by *je* and *tje*
#: * **Examples**: koopie -> koopje, weekie -> weekje, feesie -> feestje, beesie -> beestje
#:
vvsiepattern = begin + btwovowels + bc1 + r'ie' + s + end
vvsiere = re.compile(vvsiepattern, re.IGNORECASE)
vvsiereplace = r'\1\2\3je\4'
vvsiereplacet = r'\1\2\3tje\4'


#: * **Pattern** CVCiCiie : ending in consonant (C), single vowel (V), two identical consonants (CiCi) and *ie(s)*
#: * **Replacement** VCije: degeminate the consonants and replace *ie* by *je*
#: * **Examples**: bakkie -> bakje ukkie -> ukje
#:
cvcicipattern = begin + bcallorwb + bvowel + bc1 + v4 + ie + s + end
cvcicire = re.compile(cvcicipattern, re.IGNORECASE)
cvcicireplace = r'\1\2\3\4je\6'
cvcicireplacet = r'\1\2\3\4tje\6'

#: * **Pattern** DCie : Diphthong followed by a single consonant and *ie(s)*
#: * **Replacement**  V2Cje: simply replace *ie* by *je*
#: * **Examples**: buikie > buikje wijfie -> wijfje buisie _-> buisje poepie -> poepje
#:
dciepattern = begin + bdiphthong + bc1 + r'ie' + s + end
dciere = re.compile(dciepattern, re.IGNORECASE)
dciereplace = r'\1\2\3je\4'

#: * **Pattern** CiC1jie: two different consonants followed by *ie(s)*
#: * **Replacement** C1C2je: simply replace *ie* by *je*
#: * **Examples**:# bankie -> bankje binkie -> binkje bloempie -> bloempje truckie -> truckje mamsie ->
# mamsje mensie -> mensje
cic1jiepattern = begin + bcic1j + r'ie' + s + end
cic1jiere = re.compile(cic1jiepattern, re.IGNORECASE)
cic1jiereplace = r'\1\2je\3'


# test
# testlist = [('bankie', 'bankje'), ('bloempie', 'bloempje'), ('truckie', 'truckje'), ('mensie', 'mensje')]
# localtest(cic1jiere, [cic1jre], testlist)

#: * **Pattern** chie: words ending in chie(s)
#: * **Replacement**: replace *ie* by *je* and by *tje*
#: * **Examples**: 'hachie', 'hachje'), ('vrachie', 'vrachtje'),  ('kuchie', 'kuchje')
chiepattern = begin + r'chie' + s + end
chiere = re.compile(chiepattern, re.IGNORECASE)
chiereplace = r'\1chje\2'
chiereplacet = r'\1chtje\2'

# test
# testlist = [('hachie', 'hachje'), ('vrachie', 'vrachtje'),  ('kuchie', 'kuchje')]
# localtest(chiere, [chiereplace, chiereplacet], testlist)


# Cvssie messie -> mesje; schoffie -> schoftje; etc. niet voor effie -> efje; actually not needed coverd by cvcicipattern
cvssiepattern = begin + bcall + bvowel + bc1 + v4 + r'ie' + s + end
cvssiere = re.compile(cvssiepattern, re.IGNORECASE)
cvssiereplace = r'\1\2\3\4je\5'
cvssiereplacet = r'\1\2\3\4tje\5'

# test
# testlist = [('messie', 'mesje'), ('zakkie', 'zakje'), ('schriffie', 'schriftje')]
# localtest(cvssiere, [cvssiereplace, cvssiereplacet], testlist)

#: * **Pattern** vcie: vowel + consonant _ *ie*
#: * **Replacement**: duplicate the vowel, replace *ie* by *je*
#: * **Examples**: ('slapie', 'slaapje'), ('rapie', 'raapje'), ('takie', 'taakje'), ('stafie', 'staafje'), ('magie','maagje'), ('vasie', 'vaasje')
#:
vciepattern = begin + bvowel + bcall + r'ie' + s + end
vciere = re.compile(vciepattern, re.IGNORECASE)
vciereplace = r'\1\2\2\3je\4'
# test
# testlist = [('slapie', 'slaapje'), ('rapie', 'raapje'), ('takie', 'taakje'), ('stafie', 'staafje'), ('magie', 'maagje'),
#            ('vasie', 'vaasje')]
# localtest(vciere, [vciereplace], testlist)

# getbase regexes:
#: * **Pattern** ngetjepattern: words ending in *ngetje(s)*
#: * **Replacement**: replace *ngetje* by *ng* and srop *s* if present
#: * **Examples**: ('tekeningetje','tekening'), ('tekeningetjes', 'tekening')
#:
ngetjepattern = begin + r'ngetje' + s + end     # tekeningetje
ngetjere = re.compile(ngetjepattern, re.IGNORECASE)
ngetjereplace = r'\1ng\2'

# testlist = [('tekeningetje','tekening'), ('tekeningetjes', 'tekening]
# localtest(ngetjere, [ngetjereplace], testlist)

#: * **Pattern** cicietje: words ending in two identical consonants followed by *etje(s)*
#: * **Replacement**: keep only on consonant and drop etjes(s)
#: * **Examples**: ('balletje','bal'), ('balletjes','bal')
#:
cicietjepattern = begin + bcall + v2 + r'etje' + s + end  # balletje
cicietjere = re.compile(cicietjepattern, re.IGNORECASE)
cicietjereplace = r'\1\2'

# testlist = [('balletje','bal'), ('balletjes','bal')]
# localtest(cicietjere, [cicietjereplace], testlist)

#: * **Pattern** cmpje: words ending in consonant plus *mpje(s)*
#: * **Replacement**: replace *mpje* by *m*, drop *s*
#: * **Examples**: ('armpje', 'arm'), ('armpjes', 'arm'), ('darmpje', 'darm'), ('darmpjes', 'darm')
#:
cmpjepattern = begin + bcall + r'mpje' + s + end  # darmpje, armpje
cmpjere = re.compile(cmpjepattern, re.IGNORECASE)
cmpjereplace = r'\1\2m'

# testlist = [('armpje', 'arm'), ('armpjes', 'arm'), ('darmpje', 'darm'), ('darmpjes', 'darm')]
# localtest(cmpjere, [cmpjereplace], testlist)

#: * **Pattern** vmpje: words ending in consonant + (two vowels or *e*) plus *mpje(s)*
#: * **Replacement**: replaces *mpje* by *m*, drop *s*
#: * **Examples**: ('bloempje','bloem'), ('bezempje', 'bezem'), ('bloempjes', 'bloem'), ('bezempjes', 'bezem')
#:
vmpjepattern = begin + bcall + bracket(regexor([btwovowels, 'e'])) + r'mpje' + s + end  # bloempje, bezempje
vmpjere = re.compile(vmpjepattern, re.IGNORECASE)
vmpjereplace = r'\1\2\3m'

# testlist = [('bloempje','bloem'), ('bezempje', 'bezem'), ('bloempjes', 'bloem'), ('bezempjes', 'bezem')]
# localtest(vmpjere, [vmpjereplace], testlist)


#: * **Pattern** nkjepattern: words ending in *nkje(s)*
#: * **Replacement**: replace *nkje* by *ng* and drop *s*
#: * **Examples**: ('koninkje','koning'), ('koninkjes','koning')
#:
nkjepattern = begin + r'nkje' + s + end   # koninkje
nkjere = re.compile(nkjepattern, re.IGNORECASE)
nkjereplace = r'\1ng'

# testlist = [('koninkje','koning'), ('koninkjes','koning')]
# localtest(nkjere, [nkjereplace], testlist)


#: * **Pattern** vivitje: words ending in two identical vowels followed by *tjes(s)*
#: * **Replacement**: keep one vowel, drop *tje*, drop *s*
#: * **Examples**: ('laatje','la'), ('laatjes','la')
#:
vivitjepattern = begin + bvowel + v2 + r'tje' + s + end  # laatje
vivitjere = re.compile(vivitjepattern, re.IGNORECASE)
vivitjereplace = r'\1\2'

# testlist = [('laatje','la'), ('laatjes','la')]
# localtest(vivitjere, [vivitjereplace], testlist)


#: * **Pattern** vivjtje: words ending in a diphthong followed by *tje(s)*
#: * **Replacement**: drop *tje*, drop *s* if present
#: * **Examples**: ('lelietje','lelie'), ('leitje', 'lei'), ('lelietjes','lelie'), ('leitjes', 'lei')
#:
vivjtjepattern = begin + bdiphthong + r'tje' + s + end   # lelietje, leitje
vivjtjere = re.compile(vivjtjepattern, re.IGNORECASE)
vivjtjereplace = r'\1\2'

# testlist = [('lelietje','lelie'), ('leitje', 'lei'), ('lelietjes','lelie'), ('leitjes', 'lei')]
# localtest(vivjtjere, [vivjtjereplace], testlist)


#: * **Pattern** je:  words ending in *je(s)*
#: * **Replacement**: drop *je*, drop *s* if present
#: * **Examples**: ('huisje','huis'), ('bakje', 'bak'), ('huisjes','huis'), ('bakjes', 'bak')
#:
jepattern = begin + r'je' + s + end  # huisje, bakje
jere = re.compile(jepattern, re.IGNORECASE)
jereplace = r'\1'

# testlist = [('huisje','huis'), ('bakje', 'bak'), ('huisjes','huis'), ('bakjes', 'bak')]
# localtest(jere, [jereplace], testlist)


voiceless = 'pst'
voiced = 'bzd'


def voicing(str: str) -> str:
    '''
    The function *voicing* replaces p by b, s by z and  t by d, for any other input string it returns the input string
    '''
    theindex = voiceless.find(str[0])
    if theindex >= 0:
        result = voiced[theindex]
    else:
        result = str
    return result


def getbaseinlexicon(dim: str) -> Optional[str]:
    '''
    The function *getbaseinlexicon* a lemma that occurs in the lexicon for the form *dim*, or None if no such lemma
    is found.

    '''
    result = None
    candidates = getbase(dim)
    for candidate in candidates:
        if lexicon.informlexicon(candidate):
            result = candidate
            break
    return result


def getbase(dim: str) -> List[str]:
    '''
    The function *getbase* computes a list of candidate lemmas for the input diminutive form (ending in *je*) *dim*.

    It makes use of various patterns and replacements:

    * .. autodata:: ngetjepattern
    * .. autodata:: cicietjepattern
    * .. autodata:: cmpjepattern
    * .. autodata:: vmpjepattern
    * .. autodata:: nkjepattern
    * .. autodata:: vivitjepattern
    * .. autodata:: vivjtjepattern
    * .. autodata:: jepattern

    '''
    results = []
    if ngetjere.match(dim):
        newresult = ngetjere.sub(ngetjereplace, dim)
        results.append(newresult)
    if cicietjere.match(dim):
        newresult = cicietjere.sub(cicietjereplace, dim)
        results.append(newresult)
    if cmpjere.match(dim):
        newresult = cmpjere.sub(cmpjereplace, dim)
        results.append(newresult)
    if vmpjere.match(dim):
        newresult = vmpjere.sub(vmpjereplace, dim)
        results.append(newresult)
    if nkjere.match(dim):
        newresult = nkjere.sub(nkjereplace, dim)
        results.append(newresult)
    if vivitjere.match(dim):
        newresult = vivitjere.sub(vivitjereplace, dim)
        results.append(newresult)
    if vivjtjere.match(dim):
        newresult = vivjtjere.sub(vivjtjereplace, dim)
        results.append(newresult)
    if jere.match(dim):
        newresult = jere.sub(jereplace, dim)
        results.append(newresult)
    return results


def getjeforms(ieform: str) -> List[str]:
    '''
    The function *getjeforms* when applied to a string  returns a list of strings that are diminutives ending in
    *-je* of which the lemma occurs in the lexicon. If no such string is found, it returns the empty list.

    It crucially makes use of the functions *getjeformsnolex* and *getbase*

    .. autofunction:: iedims::getjeformsnolex
    .. autofunction:: iedims::getbase

    '''
    results1 = getjeformsnolex(ieform)
    lemmas = []
    candpairs = []
    for result1 in results1:
        lemmas += getbase(result1)
        for lemma in lemmas:
            candpairs.append((result1, lemma))
    results = []
    for (form, lemma) in candpairs:
        if lexicon.known_word(lemma):
            # result = '[ @add_lex {} {} ]'.format(ieform, result)
            results.append(form)
    return results


def getjeformsnolex(ieform: str) -> List[str]:
    '''
    The function getjeformsnolex when applied to a string *ieform* returns a list of candidate
    diminutive strings ending in *-je* corresponding to  *ieform*. If no such candidates are found, it returns the
    empty list.

    The function applies a range of relevant regular expressions for *ie*-diminutives, and, if a match is found,
    it applies one or more appropriate replacements.

    The relevant regular expressions are:

    .. autodata:: cvcicipattern
    .. autodata:: dciepattern
    .. autodata:: vvsiepattern
    .. autodata:: vvssiepattern
    .. autodata:: vciepattern
    .. autodata:: chiepattern
    .. autodata:: cic1jiepattern

    For all patterns except for the last two mentioned also a voiced replacement is carried out.



    '''
    results = []
    if cvcicire.match(ieform):
        m = cvcicire.match(ieform)
        result = cvcicire.sub(cvcicireplace, ieform)
        results.append(result)
        result = cvcicire.sub(cvcicireplacet, ieform)
        results.append(result)
        bdg = voicing(m.group(4))
        result = cvcicire.sub(r'\1\2\3' + bdg + r'je\6', ieform)  # cluppie -> clubje, fessie -> fezje
        results.append(result)
    elif dciere.match(ieform):
        m = dciere.match(ieform)
        result = dciere.sub(dciereplace, ieform)
        results.append(result)
        bdg = voicing(m.group(3))
        result = dciere.sub(r'\1\2' + bdg + r'je\4', ieform)   # Huipie -> Huibje
        results.append(result)
    elif vvssiere.match(ieform):
        m = vvssiere.match(ieform)
        result = vvssiere.sub(vvssiereplace, ieform)
        results.append(result)
        result = vvssiere.sub(vvssiereplacet, ieform)
        results.append(result)
        bdg = voicing(m.group(3))
        result = vvssiere.sub(r'\1\2' + bdg + r'je\4', ieform)  # Huuppie -> Huubje
        results.append(result)
    elif vvsiere.match(ieform):
        m = vvsiere.match(ieform)
        result = vvsiere.sub(vvsiereplace, ieform)
        results.append(result)
        result = vvsiere.sub(vvsiereplacet, ieform)
        results.append(result)
        bdg = voicing(m.group(3))
        result = vvsiere.sub(r'\1\2' + bdg + r'je\4', ieform)  # Huupie -> Huubje
        results.append(result)
    elif vciere.match(ieform):  # must crucially occur after the previous two (otherwise beesie -> beeestje)
        m = vciere.match(ieform)
        result = vciere.sub(vciereplace, ieform)
        results.append(result)
        bdg = voicing(m.group(3))
        result = vciere.sub(r'\1\2\2' + bdg + r'je\4', ieform)   # Hupie -> Huubje
        results.append(result)
    elif chiere.match(ieform):
        # m = chiere.match(ieform)
        result = chiere.sub(chiereplace, ieform)
        results.append(result)
        result = chiere.sub(chiereplacet, ieform)
        results.append(result)
    elif cic1jiere.match(ieform):
        # m = cic1jiere.match(ieform)
        result = cic1jiere.sub(cic1jiereplace, ieform)
        results.append(result)
    else:
        results = []
    return results
