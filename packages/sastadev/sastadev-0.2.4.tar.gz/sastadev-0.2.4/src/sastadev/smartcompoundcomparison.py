'''

This module provides a function to determine whether an illegal word is to be considered as a compound,
based on its correction and the lemma of its correction.
It works for nouns only!

'''
import editdistance

from sastadev.normalise_lemma import normaliselemma


def reldistance(word, corr):
    thedistance = editdistance.distance(word, corr)
    result = thedistance / max(len(word), len(corr))
    return result


def iscompound(word, corr, rawcorrlemma):
    debug = False
    corrlemma = normaliselemma(corr, rawcorrlemma, keeplastsep=True)
    corrlemmaparts = corrlemma.split('_')
    if len(corrlemmaparts) == 1:
        return False
    corrlemmaprefixlist = corrlemmaparts[:-1]
    corrlemmaprefix = ''.join(corrlemmaprefixlist)
    lcorrlemmaprefix = len(corrlemmaprefix)
    corrdistance = editdistance.distance(word, corr)
    relcorrdistance = reldistance(word, corr)
    if corr[:lcorrlemmaprefix] == corrlemmaprefix:
        corrleft = corrlemmaprefix
        corright = corr[lcorrlemmaprefix:]

        corrleftdistance = editdistance.distance(word, corrleft)
        corrrightdistance = editdistance.distance(word, corright)

        relcorrleftdistance = reldistance(word, corrleft)
        relcorrrightdistance = reldistance(word, corright)

        result = relcorrleftdistance >= relcorrdistance and relcorrrightdistance >= relcorrdistance
    else:
        result = relcorrdistance <= 0.4
    if debug:
        print(word, corr, corrlemma, relcorrdistance,
              relcorrleftdistance, relcorrrightdistance)
        print(word, corr, corrlemma, corrdistance,
              corrleftdistance, corrrightdistance)
    return result


def main():
    testlist = [
        ('koekkok', 'koekoeksklok', 'koekoek_klok', True),
        ('zingdoppe', 'zingdoppen', 'zingen_doppen', True),
        ('chocomelluk', 'chocolademelk', 'chocolade_melk', True),
        ('zepezop', 'zeepsop', 'zeep_sop', True),
        ('verffinger', 'vingerverf', 'vinger_verf', True),
        ('welə', 'welles', 'wel_les', True),
        ('staap', 'stapelbed', 'stapel_bed', False),
        ('stape', 'stapelbed', 'stapel_bed', False),
        ('aardbeiijs', 'aardbeienijs', 'aardbei_ijs', True),
        ('slijbaan', 'glijbaan', 'glij_baan', True),
        ('zwatte+piet', 'Zwarte_Piet', 'Zwarte_Piet', True),
        ('poplepel', 'pollepel', 'pol_lepel', True),
        ('pokeepel', 'pollepel', 'pol_lepel', True),
        ('vrastauto', 'vrachtauto', 'vracht_auto', True),
        ('slaapliets', 'slaapliedje', 'slaap_lied', True),
        ('slinderjurk', 'vlinderjurk', 'vlinder_jurk', True),
        ('abbesap', 'appelsap', 'appel_sap', True),
        ('vloerplussel', 'vloerpuzzel', 'vloer_puzzel', True),
        ('bestesap', 'bessensap', 'bes_sap', True),
        ('Astepoester', 'Asseposter', 'Asse_poster', True),
        ('affesap', 'appelsap', 'appel_sap', True),
        ('risstengeltjes', 'rietstengeltjes', 'riet_stengel', True),
        ('zeemepaardjes', 'zeemeerminpaardje', 'zeemeermin_paard', True),
        ('sampejonnetje', 'lampionnetje', 'lampion_net', True),
        ('babykijn', 'babykonijn', 'baby_konijn', True),
        ('twemles', 'zwemles', 'zwem_les', True),
        ('laapkamer', 'slaapkamer', 'slaap_kamer', True),
        ('sintetlaaspaatje', 'sinterklaaspaardje',
         'sinterklaas_paardje', True),
        ('kippes', 'kippies', 'kip_pies', True),
        ('diehoek', 'driehoek', 'drie_hoek', True),
        ('jantauto', 'brandweerauto', 'brandweer_auto', True)

    ]
    # testlist = [('risstengeltjes', 'rietstengeltjes', 'riet_stengel', True)]

    max = len(testlist)
    # max = 1
    for word, corr, corrlemma, ref in testlist[:max]:
        result = iscompound(word, corr, corrlemma)
        if result != ref:
            print(f'{word}, {corr}, {corrlemma}: {result}/={ref}')


if __name__ == '__main__':
    main()
