"""
The module *tblex* contains functions that require functions
from the lexicon module and from the treebankfunctions module
"""

import sastadev.lexicon as lex
from sastadev.sastatypes import SynTree
from sastadev.treebankfunctions import (all_lower_consonantsnode, getattval,
                                        is_duplicate_spec_noun, iscompound,
                                        isdiminutive, isnumber,
                                        issubstantivised_verb, sasta_long,
                                        sasta_pseudonym, short_nucl_n,
                                        spec_noun)


def recognised_wordnodepos(node: SynTree, pos: str) -> bool:
    '''
    The function *recognised_wordnodepos* determines for *node* whether it is a known
    word of part of speech code *pos*.

    It distinguishes several subcases that yield the result True:

    * the value of the *word* attribute of *node* is a known word form (as determined by the function *lex.informlexiconpos*

    * the lower-cased value of the *word* attribute of *node* is a known word form (as determined by the function *lex.informlexiconpos*

    * the node is a node for a compound, as determined by the function *iscompound*:

        .. autofunction:: treebankfunctions::iscompound
           :noindex:

    * the node is a node for a diminutive, as determined by the function *isdiminutive*:

        .. autofunction:: treebankfunctions::isdiminutive
           :noindex:

    * the node is a node for a name part, as determined by the function *lex.isa_namepart*


    '''
    word = getattval(node, 'word')
    lcword = word.lower()
    result = lex.informlexiconpos(word, pos) or lex.informlexiconpos(lcword, pos) or \
        iscompound(node) or isdiminutive(node) or lex.isa_namepart_uc(word)
    return result


def recognised_wordnode(node: SynTree) -> bool:
    '''
    The function *recognised_wordnode* determines for *node* whether it is a known word.

    It distinguishes several subcases that yield the result True:

    * the value of the *word* attribute of *node* is a known word form (as determined
    by the function *lex.informlexicon*

    * the lower-cased value of the *word* attribute of *node* is a known word form (as
    determined by the function *lex.informlexicon

    * the node is a node for a compound, as determined by the function *iscompound*:

        .. autofunction:: treebankfunctions::iscompound

    * the node is node for a diminutive, as determined by the function *isdiminutive*:

        .. autofunction:: treebankfunctions::isdiminutive

    * the node is a node for a name part, as determined by the function *lex.isa_namepart*


    '''

    word = getattval(node, 'word')
    lcword = word.lower()
    result = lex.informlexicon(word) \
        or lex.informlexicon(lcword) \
        or iscompound(node) \
        or isdiminutive(node) \
        or lex.isa_namepart(word)
    return result


def recognised_lemmanode(node: SynTree) -> bool:
    '''
    The function *recognised_lemmanode* checks whether the *lemma* of *node* is in
    the lexicon  (as determined by the function *lex.informlexicon*).

    '''
    lemma = getattval(node, 'lemma')
    result = lex.informlexicon(lemma)
    return result


def recognised_lemmanodepos(node: SynTree, pos: str) -> bool:
    '''
    The function *recognised_lemmanodepos* checks whether the *lemma* of *node* is in
    the lexicon with part of speech *pos* (as determined by * lex.informlexiconpos*).

    '''
    lemma = getattval(node, 'lemma')
    result = lex.informlexiconpos(lemma, pos)
    return result


def asta_recognised_lexnode(node: SynTree) -> bool:
    '''
    The function *asta_recognised_lexnode* determines whether *node* should count as a
    lexical verb in the ASTA method.

    This is the case if *pt* equals *ww* and the node is not a substantivised verb as
    determined by the function *issubstantivised_verb*:

    .. autofunction:: treebankfunctions::issubstantivised_verb

    '''
    if issubstantivised_verb(node):
        result = False
    else:
        result = getattval(node, 'pt') == 'ww'
    return result


def asta_recognised_nounnode(node: SynTree) -> bool:
    '''
    The function *asta_recognised_nounnode* determines whether *node* should count as a
    noun in the ASTA method.

    This is the case if

    * either the node meets the conditions of *sasta_pseudonym*

       .. autofunction:: treebankfunctions::sasta_pseudonym

    * or the node meets the conditions of *spec_noun*

       .. autofunction:: treebankfunctions::spec_noun

    * or the node meets the conditions of *is_duplicate_spec_noun*

       .. autofunction:: treebankfunctions::is_duplicate_spec_noun

    * or the node meets the conditions of *sasta_long*

       .. autofunction:: treebankfunctions::sasta_long

    * or the node meets the conditions of *recognised_wordnodepos*

       .. autofunction:: treebankfunctions::recognised_wordnodepos

    * or the node meets the conditions of *recognised_lemmanodepos(node, pos)*

       .. autofunction:: treebankfunctions::recognised_lemmanodepos(node, pos)

    However, the node should:

    * neither consist of lower case consonants only, as determined by *all_lower_consonantsnode*:

       .. autofunction:: treebankfunctions::all_lower_consonantsnode

    * nor satisfy the conditions of *short_nucl_n*:

       .. autofunction:: treebankfunctions::short_nucl_n

    '''

    if issubstantivised_verb(node):
        pos = 'ww'
    else:
        pos = 'n'
    result = sasta_pseudonym(node)
    result = result or spec_noun(node)
    result = result or is_duplicate_spec_noun(node)
    result = result or sasta_long(node)
    result = result or recognised_wordnodepos(node, pos)
    result = result or recognised_lemmanodepos(node, pos)
    result = result and not (all_lower_consonantsnode(node))
    result = result and not (short_nucl_n(node))
    return result


def asta_recognised_wordnode(node: SynTree) -> bool:
    result = sasta_pseudonym(node)
    result = result or spec_noun(node)
    result = result or is_duplicate_spec_noun(node)
    result = result or sasta_long(node)
    result = result or recognised_wordnode(node)
    result = result or recognised_lemmanode(node)
    result = result or isnumber(node)
    result = result and not (all_lower_consonantsnode(node))
    result = result and not (short_nucl_n(node))
    return result
