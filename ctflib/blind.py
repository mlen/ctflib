from functools import partial
import string


def extract(oracle, charset=string.printable):
    'Performs blind injection using oracle function with given charset'

    result = ''
    while True:
        c = bsearch(partial(oracle, position=len(result)), charset)
        if not c:
            return result

        result += c


def bsearch(oracle, collection):
    'Binary search through the given collection using an oracle function'

    l = len(collection)
    if l == 0:
        return None
    elif l == 1:
        if oracle(collection[:1]):
            return collection[0]
        else:
            return None
    else:
        head, tail = collection[:l//2], collection[l//2:]
        if oracle(head):
            return bsearch(oracle, head)
        else:
            return bsearch(oracle, tail)
