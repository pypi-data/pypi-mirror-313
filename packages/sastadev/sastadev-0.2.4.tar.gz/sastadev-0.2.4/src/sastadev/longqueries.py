from lxml import etree

declarative = """
(@cat="smain" or (@cat="ssub" and not(((@cat="sv1" or @cat="ssub") and @rel="body" and parent::node[@cat="whq" or @cat="whsub" ]) )) or (@cat="sv1" and not(((@cat="sv1" and
                      not((ancestor::node[@cat="top" and node[(@pt="let" and @word="?")]])) and
                      (not( (ancestor::node[@cat="top" and node[(@pt="let" and @word=".")]])) or ((node[@rel="mod" and (@lemma="maar" or @lemma="eens")]) or node[(@rel="vc" and (@cat="inf" or @cat="ppart"))  and (node[@rel="mod" and (@lemma="maar" or @lemma="eens")])])) and
                      (@rel="--" or @rel="nucl") and
                      (not(node[(@rel="su")]) or (node[(@rel="su") and (@rel="su" and (@word="jij" or @word="u"))] and (((node[@rel="mod" and (@lemma="maar" or @lemma="eens")]) or node[(@rel="vc" and (@cat="inf" or @cat="ppart"))  and (node[@rel="mod" and (@lemma="maar" or @lemma="eens")])])  or  (ancestor::node[@cat="top" and node[(@pt="let" and @word="!")]])))) and
                     node[( ((@rel="hd" and @pt="ww" and @pvtijd="tgw" and @pvagr="ev" and @wvorm="pv")  or (@rel="hd" and @pt="ww" and @wvorm="inf") ) and
         not((contains(@frame,"modal"))) and
         (not(@lemma="zijn") or @word="wees" or @word="weest")       and
         (not(contains(@lemma,"moeten") or contains(@lemma,"hoeven") or
              contains(@lemma,"zullen") or contains(@lemma,"kunnen") or
              contains(@lemma,"mogen") or @lemma="hebben" or contains(@lemma, "_hebben") or contains(@lemma, "weten")
             )
         )
        )]
)
 or (( ((@rel="hd" and @pt="ww" and @pvtijd="tgw" and @pvagr="ev" and @wvorm="pv")  or (@rel="hd" and @pt="ww" and @wvorm="inf") ) and
         not((contains(@frame,"modal"))) and
         (not(@lemma="zijn") or @word="wees" or @word="weest")       and
         (not(contains(@lemma,"moeten") or contains(@lemma,"hoeven") or
              contains(@lemma,"zullen") or contains(@lemma,"kunnen") or
              contains(@lemma,"mogen") or @lemma="hebben" or contains(@lemma, "_hebben") or contains(@lemma, "weten")
             )
         )
        ) and  (@rel="--" or @rel="nucl")  and parent::node[@cat="top"] and not((ancestor::node[@cat="top" and node[(@pt="let" and @word="?")]])) and not( (ancestor::node[@cat="top" and node[(@pt="let" and @word=".")]])))  )) and not(@cat="sv1" and
            (@rel="--" or @rel="dp") and
            not( (ancestor::node[@cat="top" and node[(@pt="let" and @word=".")]])) and
            not( (ancestor::node[@cat="top" and node[(@pt="let" and @word="!")]])) and
            node[@rel="hd" and @pt="ww" and @pvtijd !="conj" and (@stype="ynquestion" or (ancestor::node[@cat="top" and node[(@pt="let" and @word="?")]]) ) ] and
            (node[@rel="su"] or (ancestor::node[@cat="top" and node[(@pt="let" and @word="?")]]))    and
            (not(((node[@rel="mod" and (@lemma="maar" or @lemma="eens")]) or node[(@rel="vc" and (@cat="inf" or @cat="ppart"))  and (node[@rel="mod" and (@lemma="maar" or @lemma="eens")])])) or (ancestor::node[@cat="top" and node[(@pt="let" and @word="?")]]) )
          ) and not(((@cat="sv1" or @cat="ssub") and @rel="body" and parent::node[@cat="whq" or @cat="whsub" ]) )) )

"""

tbxcount = """
 count(node[(
       ((((@rel="mod" or @rel="ld" or @rel="predm") and
          (not(@cat) or @cat!="conj") and
          (not(@pt) or @pt!="tsw")
         )or
         ((@rel="predc" and
           (@pt="adj" or @pt="bw" or @cat="ap" or @cat="advp") and
           ../node[@rel="obj1"]
         )
         )
         ) and
         (../node[@pt="ww" and @rel="hd"])
        ) or
        ((@pt="vz" or @pt="bw" or (@pt='vnw' and (@lemma='er' or @lemma='hier' or @lemma='daar' or @lemma='waar' or @lemma='ergens' or @lemma='nergens' or @lemma='overal'))
) and (@rel="dp" or @rel="--" or @rel="nucl" or @rel="body") and (parent::node[count(node[((not(@pt) or (@pt!="let" and @pt!="tsw")) and (not(@postag) or @postag!="NA()"))])>1])) or
        (@cat="pp" and (@rel="--" or @rel="dp") and (parent::node[count(node[((not(@pt) or (@pt!="let" and @pt!="tsw")) and (not(@postag) or @postag!="NA()"))])>1])) or
        (@rel="pc" and ../node[@rel="hd" and (@lemma="staan" or @lemma="zitten" or @lemma="rijden" or @lemma="vallen" or @lemma="doen" or @lemma="gaan" or @lemma="komen" or @lemma="zijn"  or  (@lemma="kunnen" or @lemma="moeten" or @lemma="hoeven" or @lemma="willen" or @lemma="mogen") )
]) or
        (@rel="cnj" and parent::node[@rel="mod" or @rel="ld" or @rel="predm"]) or
        (@rel="mod" and @pt="bw" and parent::node[@cat="np"] ) or
        (@cat="cp" and (@rel="dp" or @rel="--") and node[@pt="vg" and @conjtype="onder" and @lemma!="dat" and @lemma!="of" ] ) or
        ( ( @rel="pc" and node[@rel = "hd" and @lemma="af"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="aan"] and ../node[@rel="hd" and @pt="ww" and @lemma="gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="om"] and ../node[@rel="hd" and @pt="ww" and @lemma="draaien"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="sabbelen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="zien"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="af"] and ../node[@rel="hd" and @pt="ww" and @lemma="krijgen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="dansen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="zitten"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="over"] and ../node[@rel="hd" and @pt="ww" and @lemma="struikelen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="tussendoor"] and ../node[@rel="hd" and @pt="ww" and @lemma="gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="tegen"] and ../node[@rel="hd" and @pt="ww" and @lemma="zijn"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="bij"] and ../node[@rel="hd" and @pt="ww" and @lemma="helpen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="omheen"] and ../node[@rel="hd" and @pt="ww" and @lemma="kunnen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="aan"] and ../node[@rel="hd" and @pt="ww" and @lemma="plakken"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="uit"] and ../node[@rel="hd" and @pt="ww" and @lemma="hebben"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="staan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="aan"] and ../node[@rel="hd" and @pt="ww" and @lemma="vast_knopen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="vanaf"] and ../node[@rel="hd" and @pt="ww" and @lemma="vallen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="achteraan"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="vanaf"] and ../node[@rel="hd" and @pt="ww" and @lemma="af_brengen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="overheen"] and ../node[@rel="hd" and @pt="ww" and @lemma="gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="met"] and ../node[@rel="hd" and @pt="ww" and @lemma="mee_gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="zoeken"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="voor"] and ../node[@rel="hd" and @pt="ww" and @lemma="zijn"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="tot"] and ../node[@rel="hd" and @pt="ww" and @lemma="tellen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="slaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="voor"] and ../node[@rel="hd" and @pt="ww" and @lemma="staan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="in"] and ../node[@rel="hd" and @pt="ww" and @lemma="spelen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="in"] and ../node[@rel="hd" and @pt="ww" and @lemma="lukken"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="tot"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="door_gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="om"] and ../node[@rel="hd" and @pt="ww" and @lemma="gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="voor"] and ../node[@rel="hd" and @pt="ww" and @lemma="houden"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="krijgen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="in"] and ../node[@rel="hd" and @pt="ww" and @lemma="uit_komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="om"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="rijden"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="doorheen"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="voor"] and ../node[@rel="hd" and @pt="ww" and @lemma="gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="bij"] and ../node[@rel="hd" and @pt="ww" and @lemma="passen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="bouwen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="bij"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="varen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="vanaf"] and ../node[@rel="hd" and @pt="ww" and @lemma="af_komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="overheen"] and ../node[@rel="hd" and @pt="ww" and @lemma="doen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="voor"] and ../node[@rel="hd" and @pt="ww" and @lemma="zitten"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="af"] and ../node[@rel="hd" and @pt="ww" and @lemma="hebben"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="van"] and ../node[@rel="hd" and @pt="ww" and @lemma="hebben"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="van"] and ../node[@rel="hd" and @pt="ww" and @lemma="eten"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="bij"] and ../node[@rel="hd" and @pt="ww" and @lemma="liggen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="in "] and ../node[@rel="hd" and @pt="ww" and @lemma="zeggen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="af_komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="van"] and ../node[@rel="hd" and @pt="ww" and @lemma="af_komen"] ) )
        )

] | node[(@rel="vc" and (@cat="inf" or @cat="ppart")) ]/node[(
       ((((@rel="mod" or @rel="ld" or @rel="predm") and
          (not(@cat) or @cat!="conj") and
          (not(@pt) or @pt!="tsw")
         )or
         ((@rel="predc" and
           (@pt="adj" or @pt="bw" or @cat="ap" or @cat="advp") and
           ../node[@rel="obj1"]
         )
         )
         ) and
         (../node[@pt="ww" and @rel="hd"])
        ) or
        ((@pt="vz" or @pt="bw" or (@pt='vnw' and (@lemma='er' or @lemma='hier' or @lemma='daar' or @lemma='waar' or @lemma='ergens' or @lemma='nergens' or @lemma='overal'))
) and (@rel="dp" or @rel="--" or @rel="nucl" or @rel="body") and (parent::node[count(node[((not(@pt) or (@pt!="let" and @pt!="tsw")) and (not(@postag) or @postag!="NA()"))])>1])) or
        (@cat="pp" and (@rel="--" or @rel="dp") and (parent::node[count(node[((not(@pt) or (@pt!="let" and @pt!="tsw")) and (not(@postag) or @postag!="NA()"))])>1])) or
        (@rel="pc" and ../node[@rel="hd" and (@lemma="staan" or @lemma="zitten" or @lemma="rijden" or @lemma="vallen" or @lemma="doen" or @lemma="gaan" or @lemma="komen" or @lemma="zijn"  or  (@lemma="kunnen" or @lemma="moeten" or @lemma="hoeven" or @lemma="willen" or @lemma="mogen") )
]) or
        (@rel="cnj" and parent::node[@rel="mod" or @rel="ld" or @rel="predm"]) or
        (@rel="mod" and @pt="bw" and parent::node[@cat="np"] ) or
        (@cat="cp" and (@rel="dp" or @rel="--") and node[@pt="vg" and @conjtype="onder" and @lemma!="dat" and @lemma!="of" ] ) or
        ( ( @rel="pc" and node[@rel = "hd" and @lemma="af"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="aan"] and ../node[@rel="hd" and @pt="ww" and @lemma="gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="om"] and ../node[@rel="hd" and @pt="ww" and @lemma="draaien"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="sabbelen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="zien"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="af"] and ../node[@rel="hd" and @pt="ww" and @lemma="krijgen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="dansen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="zitten"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="over"] and ../node[@rel="hd" and @pt="ww" and @lemma="struikelen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="tussendoor"] and ../node[@rel="hd" and @pt="ww" and @lemma="gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="tegen"] and ../node[@rel="hd" and @pt="ww" and @lemma="zijn"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="bij"] and ../node[@rel="hd" and @pt="ww" and @lemma="helpen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="omheen"] and ../node[@rel="hd" and @pt="ww" and @lemma="kunnen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="aan"] and ../node[@rel="hd" and @pt="ww" and @lemma="plakken"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="uit"] and ../node[@rel="hd" and @pt="ww" and @lemma="hebben"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="staan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="aan"] and ../node[@rel="hd" and @pt="ww" and @lemma="vast_knopen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="vanaf"] and ../node[@rel="hd" and @pt="ww" and @lemma="vallen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="achteraan"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="vanaf"] and ../node[@rel="hd" and @pt="ww" and @lemma="af_brengen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="overheen"] and ../node[@rel="hd" and @pt="ww" and @lemma="gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="met"] and ../node[@rel="hd" and @pt="ww" and @lemma="mee_gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="zoeken"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="voor"] and ../node[@rel="hd" and @pt="ww" and @lemma="zijn"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="tot"] and ../node[@rel="hd" and @pt="ww" and @lemma="tellen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="slaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="voor"] and ../node[@rel="hd" and @pt="ww" and @lemma="staan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="in"] and ../node[@rel="hd" and @pt="ww" and @lemma="spelen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="in"] and ../node[@rel="hd" and @pt="ww" and @lemma="lukken"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="tot"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="door_gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="om"] and ../node[@rel="hd" and @pt="ww" and @lemma="gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="voor"] and ../node[@rel="hd" and @pt="ww" and @lemma="houden"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="krijgen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="in"] and ../node[@rel="hd" and @pt="ww" and @lemma="uit_komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="om"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="rijden"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="doorheen"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="voor"] and ../node[@rel="hd" and @pt="ww" and @lemma="gaan"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="bij"] and ../node[@rel="hd" and @pt="ww" and @lemma="passen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="bouwen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="bij"] and ../node[@rel="hd" and @pt="ww" and @lemma="komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="varen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="vanaf"] and ../node[@rel="hd" and @pt="ww" and @lemma="af_komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="overheen"] and ../node[@rel="hd" and @pt="ww" and @lemma="doen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="voor"] and ../node[@rel="hd" and @pt="ww" and @lemma="zitten"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="af"] and ../node[@rel="hd" and @pt="ww" and @lemma="hebben"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="van"] and ../node[@rel="hd" and @pt="ww" and @lemma="hebben"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="van"] and ../node[@rel="hd" and @pt="ww" and @lemma="eten"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="bij"] and ../node[@rel="hd" and @pt="ww" and @lemma="liggen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="in "] and ../node[@rel="hd" and @pt="ww" and @lemma="zeggen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="op"] and ../node[@rel="hd" and @pt="ww" and @lemma="af_komen"] ) or ( @rel="pc" and node[@rel = "hd" and @lemma="van"] and ../node[@rel="hd" and @pt="ww" and @lemma="af_komen"] ) )
        )

])


"""

queryboth = f'//node[{declarative} and {tbxcount}]'
querydeclarative = f'//node[{declarative}]'
querytbxcount = f'//node[{tbxcount}]'

streestring = """<node cat="top" />"""
stree = etree.fromstring(streestring)

resultsdeclarative = stree.xpath(querydeclarative)
resultstbxcount = stree.xpath(querytbxcount)
resultsboth = stree.xpath(queryboth)
