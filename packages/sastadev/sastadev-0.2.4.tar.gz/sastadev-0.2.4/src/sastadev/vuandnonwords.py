from sastadev.vunonwordlexicons import filledpauseslexicon, nomlulexicon, normalize, vuwordslexicon



def markfilledpauses(utt):
    newtokens = []
    tokens = utt.split()
    for token in tokens:
        if token in filledpauseslexicon:
            newtoken = f'{fillermarking}{token}'
        else:
            newtoken = token
        newtokens.append(newtoken)
    oututt = space.join(newtokens)
    return oututt

def marknomluwords(utt):
    newtokens = []
    tokens = utt.split()
    ltokens = len(tokens)
    for i, token in enumerate(tokens):
        if token in nomlulexicon:
            if (i < ltokens -1  and not tokens[i+1].startswith('[:')) or i == ltokens - 1:
                newtoken = f'{nonwordmarking}{token}'
            else:
                newtoken = token
        else:
            newtoken = token
        newtokens.append(newtoken)
    oututt = space.join(newtokens)
    return oututt

def containsrealwords(utt):
    utt, _ = cleantext(utt, repkeep=False)
    cleanutt = normalize(utt)
    tokens = cleanutt.split()
    for token in tokens:
        if token not in filledpauseslexicon and \
           token not in nomlulexicon and \
           token not in vuwordslexicon and \
           token not in interpunctions and \
           token[0] != '=':
           return True
    return False


def markvuwords(utt):
    newtokens = []
    cleanutt = normalize(utt)
    tokens = cleanutt.split()
    if not containsrealwords(utt):
        for token in tokens:
            if token in vuwordslexicon:
                newtoken = f'{nonwordmarking}{token}'
            else:
                newtoken = token
            newtokens.append(newtoken)
    else:
        newtokens = []
        if len(tokens) >= 2 and tokens[0] in vuwordslexicon and tokens[1] == comma:
            newtokens.append(f'{nonwordmarking}{tokens[0]}')
            newtokens.extend(tokens[1:])
        else:
            newtokens = tokens
    oututt = space.join(newtokens)
    return oututt


