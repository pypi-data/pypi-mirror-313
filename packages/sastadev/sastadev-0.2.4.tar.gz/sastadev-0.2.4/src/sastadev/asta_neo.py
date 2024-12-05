from lxml import etree

from sastadev.ASTApostfunctions import neologisme, phonpar, sempar


def test(stree):
    neoresults = neologisme(stree)
    semparresults = sempar(stree)
    phonparresults = phonpar(stree)
    results = [('neo', neoresult) for neoresult in neoresults] +\
              [('sempar', semparresult) for semparresult in semparresults] +\
              [('phonpar', phonparresult) for phonparresult in phonparresults]
    return results


def main():
    for i in strees:
        results = test(strees[i])
        for result in results:
            print('{}: {}:{}'.format(result[0], result[1].attrib['word'], result[1].attrib['begin']))


streestrings = {}

streestrings[1] = """
<alpino_ds version="1.3">
  <metadata><meta name="uttid" value="1" type="text"/><meta name="xsid" value="1" type="text"/><meta name="origutt" value="ik heb geduusterd [*n]" type="text"/><xmeta annotatedposlist="[2]" annotatedwordlist="['geduusterd']" annotationposlist="[4]" annotationwordlist="['n']" atype="text" backplacement="0" cat="None" name="Error Marking" penalty="10" source="CHAT" subcat="None" value="['n']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['ik', 'heb', 'geduusterd', '[*', 'n', ']']" atype="list" backplacement="0" cat="None" name="tokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['ik', 'heb', 'geduusterd', '[*', 'n', ']']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['ik', 'heb', 'geduusterd']" atype="list" backplacement="0" cat="None" name="cleanedtokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['ik', 'heb', 'geduusterd']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="[0, 1, 2]" atype="list" backplacement="0" cat="None" name="cleanedtokenpositions" penalty="10" source="CHAT/Tokenisation" subcat="None" value="[0, 1, 2]"/></metadata><node begin="0" cat="top" end="3" id="0" rel="top">
    <node begin="0" cat="smain" end="3" id="1" rel="--">
      <node begin="0" case="nom" def="def" end="1" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="2" index="1" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
      <node begin="1" end="2" frame="verb(hebben,sg1,aux_psp_hebben)" id="3" infl="sg1" lcat="smain" lemma="hebben" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="heb" sc="aux_psp_hebben" sense="heb" stype="declarative" tense="present" word="heb" wvorm="pv"/>
      <node begin="0" cat="ppart" end="3" id="4" rel="vc">
        <node begin="0" end="1" id="5" index="1" rel="su"/>
        <node begin="2" buiging="zonder" end="3" frame="verb('hebben/zijn',psp,intransitive)" id="6" infl="psp" lcat="ppart" lemma="geduusterd" pos="verb" positie="vrij" postag="WW(vd,vrij,zonder)" pt="ww" rel="hd" root="geduusterd" sc="intransitive" sense="geduusterd" word="geduusterd" wvorm="vd"/>
      </node>
    </node>
  </node>
  <sentence sentid="1">ik heb geduusterd</sentence>
  <comments>
    <comment>Q#ng1646152422|ik heb geduusterd|1|1|-5.158487943820001</comment>
  </comments>
</alpino_ds>
"""


streestrings[2] = """
  <alpino_ds version="1.3">
  <metadata><meta name="uttid" value="1" type="text"/><meta name="xsid" value="1" type="text"/><meta name="origutt" value="ik heb ngeduusterd [*n]" type="text"/><xmeta annotatedposlist="[2]" annotatedwordlist="['ngeduusterd']" annotationposlist="[4]" annotationwordlist="['n']" atype="text" backplacement="0" cat="None" name="Error Marking" penalty="10" source="CHAT" subcat="None" value="['n']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['ik', 'heb', 'ngeduusterd', '[*', 'n', ']']" atype="list" backplacement="0" cat="None" name="tokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['ik', 'heb', 'ngeduusterd', '[*', 'n', ']']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['ik', 'heb', 'ngeduusterd']" atype="list" backplacement="0" cat="None" name="cleanedtokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['ik', 'heb', 'ngeduusterd']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="[0, 1, 2]" atype="list" backplacement="0" cat="None" name="cleanedtokenpositions" penalty="10" source="CHAT/Tokenisation" subcat="None" value="[0, 1, 2]"/></metadata><node begin="0" cat="top" end="3" id="0" rel="top">
    <node begin="0" cat="smain" end="3" id="1" rel="--">
      <node begin="0" case="nom" def="def" end="1" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="2" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
      <node begin="1" end="2" frame="verb(hebben,sg1,transitive_ndev)" id="3" infl="sg1" lcat="smain" lemma="hebben" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="heb" sc="transitive_ndev" sense="heb" stype="declarative" tense="present" word="heb" wvorm="pv"/>
      <node begin="2" end="3" frame="noun(both,both,both)" gen="both" genus="zijd" getal="ev" graad="basis" id="4" lcat="np" lemma="ngeduusterd" naamval="stan" ntype="soort" num="both" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="obj1" rnum="sg" root="ngeduusterd" sense="ngeduusterd" word="ngeduusterd"/>
    </node>
  </node>
  <sentence sentid="1">ik heb ngeduusterd</sentence>
  <comments>
    <comment>Q#ng1646219407|ik heb ngeduusterd|1|1|-1.6311900273499995</comment>
  </comments>
</alpino_ds>
"""

streestrings[3] = """
  <alpino_ds version="1.3">
  <metadata><meta name="uttid" value="2" type="text"/><meta name="xsid" value="2" type="text"/><meta name="origutt" value="ik heb nngeduusterd@n" type="text"/><xmeta annotatedposlist="[2]" annotatedwordlist="['nngeduusterd@n']" annotationposlist="[]" annotationwordlist="['@n']" atype="text" backplacement="0" cat="None" name="Special Form" penalty="10" source="CHAT" subcat="None" value="['@n']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['ik', 'heb', 'nngeduusterd@n']" atype="list" backplacement="0" cat="None" name="tokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['ik', 'heb', 'nngeduusterd@n']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['ik', 'heb', 'nngeduusterd']" atype="list" backplacement="0" cat="None" name="cleanedtokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['ik', 'heb', 'nngeduusterd']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="[0, 1, 2]" atype="list" backplacement="0" cat="None" name="cleanedtokenpositions" penalty="10" source="CHAT/Tokenisation" subcat="None" value="[0, 1, 2]"/></metadata><node begin="0" cat="top" end="3" id="0" rel="top">
    <node begin="0" cat="smain" end="3" id="1" rel="--">
      <node begin="0" case="nom" def="def" end="1" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="2" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
      <node begin="1" end="2" frame="verb(hebben,sg1,transitive_ndev)" id="3" infl="sg1" lcat="smain" lemma="hebben" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="heb" sc="transitive_ndev" sense="heb" stype="declarative" tense="present" word="heb" wvorm="pv"/>
      <node begin="2" end="3" frame="noun(both,both,both)" gen="both" genus="zijd" getal="ev" graad="basis" id="4" lcat="np" lemma="nngeduusterd" naamval="stan" ntype="soort" num="both" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="obj1" rnum="sg" root="nngeduusterd" sense="nngeduusterd" word="nngeduusterd"/>
    </node>
  </node>
  <sentence sentid="2">ik heb nngeduusterd</sentence>
  <comments>
    <comment>Q#ng1646219408|ik heb nngeduusterd|1|1|-1.6311900273499995</comment>
  </comments>
</alpino_ds>
"""
streestrings[4] = """
  <alpino_ds version="1.3">
  <metadata><meta name="uttid" value="3" type="text"/><meta name="xsid" value="3" type="text"/><meta name="origutt" value="ik heb pgeduusterd [*p]" type="text"/><xmeta annotatedposlist="[2]" annotatedwordlist="['pgeduusterd']" annotationposlist="[4]" annotationwordlist="['p']" atype="text" backplacement="0" cat="None" name="Error Marking" penalty="10" source="CHAT" subcat="None" value="['p']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['ik', 'heb', 'pgeduusterd', '[*', 'p', ']']" atype="list" backplacement="0" cat="None" name="tokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['ik', 'heb', 'pgeduusterd', '[*', 'p', ']']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['ik', 'heb', 'pgeduusterd']" atype="list" backplacement="0" cat="None" name="cleanedtokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['ik', 'heb', 'pgeduusterd']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="[0, 1, 2]" atype="list" backplacement="0" cat="None" name="cleanedtokenpositions" penalty="10" source="CHAT/Tokenisation" subcat="None" value="[0, 1, 2]"/></metadata><node begin="0" cat="top" end="3" id="0" rel="top">
    <node begin="0" cat="smain" end="3" id="1" rel="--">
      <node begin="0" case="nom" def="def" end="1" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="2" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
      <node begin="1" end="2" frame="verb(hebben,sg1,transitive_ndev)" id="3" infl="sg1" lcat="smain" lemma="hebben" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="heb" sc="transitive_ndev" sense="heb" stype="declarative" tense="present" word="heb" wvorm="pv"/>
      <node begin="2" end="3" frame="noun(both,both,both)" gen="both" genus="zijd" getal="ev" graad="basis" id="4" lcat="np" lemma="pgeduusterd" naamval="stan" ntype="soort" num="both" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="obj1" rnum="sg" root="pgeduusterd" sense="pgeduusterd" word="pgeduusterd"/>
    </node>
  </node>
  <sentence sentid="3">ik heb pgeduusterd</sentence>
  <comments>
    <comment>Q#ng1646219409|ik heb pgeduusterd|1|1|-1.6311900273499995</comment>
  </comments>
</alpino_ds>
"""

streestrings[5] = """
  <alpino_ds version="1.3">
  <metadata><meta name="uttid" value="4" type="text"/><meta name="xsid" value="4" type="text"/><meta name="origutt" value="ik heb sgeduusterd [*s]" type="text"/><xmeta annotatedposlist="[2]" annotatedwordlist="['sgeduusterd']" annotationposlist="[4]" annotationwordlist="['s']" atype="text" backplacement="0" cat="None" name="Error Marking" penalty="10" source="CHAT" subcat="None" value="['s']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['ik', 'heb', 'sgeduusterd', '[*', 's', ']']" atype="list" backplacement="0" cat="None" name="tokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['ik', 'heb', 'sgeduusterd', '[*', 's', ']']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['ik', 'heb', 'sgeduusterd']" atype="list" backplacement="0" cat="None" name="cleanedtokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['ik', 'heb', 'sgeduusterd']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="[0, 1, 2]" atype="list" backplacement="0" cat="None" name="cleanedtokenpositions" penalty="10" source="CHAT/Tokenisation" subcat="None" value="[0, 1, 2]"/></metadata><node begin="0" cat="top" end="3" id="0" rel="top">
    <node begin="0" cat="smain" end="3" id="1" rel="--">
      <node begin="0" case="nom" def="def" end="1" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="2" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
      <node begin="1" end="2" frame="verb(hebben,sg1,transitive_ndev)" id="3" infl="sg1" lcat="smain" lemma="hebben" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="heb" sc="transitive_ndev" sense="heb" stype="declarative" tense="present" word="heb" wvorm="pv"/>
      <node begin="2" end="3" frame="noun(both,both,both)" gen="both" genus="zijd" getal="ev" graad="basis" id="4" lcat="np" lemma="sgeduusterd" naamval="stan" ntype="soort" num="both" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="obj1" rnum="sg" root="sgeduusterd" sense="sgeduusterd" word="sgeduusterd"/>
    </node>
  </node>
  <sentence sentid="4">ik heb sgeduusterd</sentence>
  <comments>
    <comment>Q#ng1646219410|ik heb sgeduusterd|1|1|-1.6311900273499995</comment>
  </comments>
</alpino_ds>

"""

strees = {}
for i in streestrings:
    strees[i] = etree.fromstring(streestrings[i])

if __name__ == '__main__':
    main()
