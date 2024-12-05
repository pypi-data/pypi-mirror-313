from copy import deepcopy


def memoize(f):
    memory = {}

    def inner(num):
        if num not in memory or memory[num] is None:
            memory[num] = f(num)
        # added deepcopy to ensure we get a copy of the object, not just a link to it
        return deepcopy(memory[num])

    return inner
