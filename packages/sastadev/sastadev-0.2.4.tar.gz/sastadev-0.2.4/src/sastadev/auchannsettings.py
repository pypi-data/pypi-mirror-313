from auchann.align_words import AlignmentSettings

settings = AlignmentSettings()

replacements = {}
replacements['p:w'] = [('isse', 'is'), ('watte', 'wat'), ('hije', 'hij')]

for errcode, pairlist in replacements.items():
    for i, (w1, w2) in enumerate(pairlist):
        settings.replacements[errcode + f':{w1}'] = [w1, w2]


def main():
    print(settings.replacements)


if __name__ == '__main__':
    main()
