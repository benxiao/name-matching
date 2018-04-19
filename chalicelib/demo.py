from . import ed
from . import data
import multiprocessing as mp
import logging
from functools import partial


username = "Ran"

method_names = [
    'lcs',
    'levenshtein',
    'dlevenshtein',
    'soundex',
    'double_meta'
]

def lcs(x):
    return ed.lcs_sim(username, x)

def levenshtein(x):
    return ed.levenshtein_sim(username, x)

def dlevenshtein(x):
    return ed.damerau_levenshtein_sim(username, x)

def soundex(x):
    return ed.soundex_sim(username, x)

def double_meta(x):
    return ed.double_metaphone_sim(username, x)


methods = [
    lcs,
    levenshtein,
    dlevenshtein,
    soundex,
    double_meta
]


class FakeLogger:
    def __init__(self):
        pass

    def debug(self, *args):
        pass

def top(lst, indexes, n=20):
    result = []
    for i in indexes[:n]:
        result.append(lst[i])
    return result


def read_csv(filename, sep=','):
    result = []
    with open(filename, "r") as fp:
        for line in fp:
            result.append(line.rstrip().split(sep))

    if len(result) == 0:
        raise ValueError("file is empty!")

    length = len(result[0])

    for row in result:
        if length != len(row):
            raise ValueError("malformed result")
    return result



def sm(logger, name, top_n=50):
    logger.debug("start...")
    pool = mp.Pool(4)
    names = [k for k in data.names]
    counts = [v for _, v in data.names.items()]
    similarities = {}
    logger.debug("finish reading input")
    for method_name, method in zip(method_names, methods):

        similarities[method_name] = pool.map(method, names)
    logger.debug("finish computing-heavy taskes")


    similarities['double_meta'] = list(zip(similarities['double_meta'], similarities["dlevenshtein"]))

    result = {}
    for method_name in similarities:
        values = similarities[method_name]
        indexes = list(range(len(names)))
        indexes.sort(key=lambda x: (values[x], counts[x]), reverse=True)
        result[method_name] = top(names, indexes, n=top_n)
    return result


if __name__ == '__main__':
    import time

    start = time.time()
    fl = FakeLogger()
    NAME = "Cathlaen"
    N = 100
    print(sm(fl, NAME, N))
    print(time.time() - start, "s", sep="")
