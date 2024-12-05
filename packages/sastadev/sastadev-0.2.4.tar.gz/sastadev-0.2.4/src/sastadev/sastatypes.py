'''
This module contains definitions of types used in multiple modules
'''

from collections import Counter
from typing import Callable, Dict, List, Optional, Tuple, Union

from lxml import etree

from sastadev.query import Query
from sastadev.sastatoken import Token

Level = str  # in the future perhaps NewType('Level', str)
Position = int  # in the future perhapos NewType('Position', int)
PhiTriple = Tuple[str, str, str]
QId = str  # in the futute perhaps NewType('QId', str)
SynTree = etree.Element  # type: ignore
TreeBank = etree.Element
UttId = str  # in the future perhaps NewType('UttId', str)


Item = str  # in the future perhaps NewType('Item', str)
Item2LevelsDict = Dict[Item, List[Level]]
Item_Level = Tuple[Item, Level]

AltCodeDict = Dict[Item_Level, Item_Level]
AltId = int
AnalysedTrees = List[Tuple[UttId, SynTree]]
BackPlacement = int
CapitalName = str
CountryName = str
ContinentName = str
CELEXPosCode = str
FirstName = str
LocationName = str
DCOIPt = str
DeHet = str
CELEX_INFL = str
DCOITuple = Tuple
Lemma = str
CorrectionMode = str  # Literal['0','1','n']
ErrorDict = Dict[str, List[List[str]]]
Level = str  # in the future perhaps NewType('Level', str)
Item = str  # in the future perhaps NewType('Item', str)
Item_Level = Tuple[Item, Level]
IntSpan = Tuple[int, int]
AltCodeDict = Dict[Item_Level, Item_Level]
QId = str  # in the futute perhaps NewType('QId', str)
UttId = str  # in the future perhaps NewType('UttId', str)
Position = int  # in the future perhapos NewType('Position', int)
PositionStr = str
Stage = int
SynTree = etree._Element  # type: ignore
GoldTuple = Tuple[str, str, Counter]
GoldResults = Dict[QId, GoldTuple]
Item2LevelsDict = Dict[Item, List[Level]]
Match = Tuple[SynTree, SynTree]
Matches = List[Match]
MatchesDict = Dict[Tuple[QId, UttId], Matches]
MetaElement = etree.Element
ExactResult = Tuple[UttId, Position]
ExactResults = List[ExactResult]
ExactResultsDict = Dict[QId, ExactResults]  # qid
Gender = str
Penalty = int
PhiTriple = Tuple[str, str, str]
OptPhiTriple = Optional[PhiTriple]
PositionMap = Dict[Position, Position]
QueryDict = Dict[QId, Query]
QIdCount = Dict[QId, int]
MethodName = str  # perhaps in the future NewType('MethodName', str)
FileName = str  # perhaps in the future NewType('FileName', str)
ReplacementMode = int
ResultsCounter = Counter  # Counter[UttId]  # Dict[UttId, int]
ResultsDict = Dict[QId, ResultsCounter]
SampleSizeTuple = Tuple[List[UttId], int, Optional[PositionStr]]
Span = Tuple[PositionStr, PositionStr]
Item_Level2QIdDict = Dict[Item_Level, QId]
Nort = Union[SynTree, Token]
ExactResultsFilter = Callable[[Query, ExactResultsDict, ExactResult], bool]
Targets = int
Treebank = etree.Element
TreePredicate = Callable[[SynTree], bool]
TokenTreePredicate = Callable[[Token, SynTree], bool]
URL = str
UttTokenDict = Dict[UttId, List[Token]]
UttWordDict = Dict[UttId, List[str]]
WordInfo = Tuple[Optional[CELEXPosCode], Optional[DeHet],
                 Optional[CELEX_INFL], Optional[Lemma]]
Pattern = str
# moved the following to allresuls.py
# CoreQueryFunction = Callable[[SynTree], List[SynTree]]
# PostQueryFunction = Callable[[SynTree, allresults.AllResults], List[SynTree]]
# QueryFunction = Union[CoreQueryFunction, PostQueryFunction]
