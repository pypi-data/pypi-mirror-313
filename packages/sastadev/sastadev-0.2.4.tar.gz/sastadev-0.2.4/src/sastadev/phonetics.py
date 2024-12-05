import re

c_as_s = r'c(?=[eiy])'
c_as_k = r'c(?=[^eiyh])'
qu_as_kw = r'qu'
y_as_i = r'y'
x_as_ks = r'x'
gh_as_g = r'gh'
eu_as_E = r'eu'
ei_as_J = r'ei'

#: The varibale *replacementpattenrs* contains replacements to deal with certain
#: alternative ways to spell a sound, e.g *c* is replaced by *s* in certain context,
#: by *k* in other contexts, etc.
replacementpatterns = [(y_as_i, 'ie'), (c_as_s, 's'), (c_as_k, 'k'), (qu_as_kw, 'kw'), (x_as_ks, 'ks'), (gh_as_g, 'g'),
                       (eu_as_E, 'E'), (ei_as_J, 'J')]
replacements = [(re.compile(pat), repl) for pat, repl in replacementpatterns]


def phoneticise(instr: str) -> str:
    '''
    The function *phoneticise* carries out substitutions for string patterns as given
    in the variable *replacements* derived from the variable *replacementpatterns*.

    .. autodata:: phonetics::replacementpatterns

    '''
    result = instr
    for regex, repl in replacements:
        result = regex.sub(repl, result)
    return result
