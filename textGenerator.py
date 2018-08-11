import random, time
from itertools import accumulate

from trainer import sentenceEndingPunc

def generateText(srcGraph, targetLen=25, startPhrase=None):
    """

    :param srcGraph:
    :param targetLen:
    :param startPhrase:     allows user choosing the starting place for a graph
                            if None or a phrase that doesn't exist in srcGraph, one will be chosen at random
    :return:
    """
    out = []
    random.seed(time.time())
    if not startPhrase or startPhrase not in srcGraph:
        startPhrase = list(srcGraph.keys())[random.randrange(len(srcGraph))]
    # TODO: capitalize this later (not now, b/c then you might not find it in the srcGraph)
    out.append(startPhrase)
    # keep generating until the length exceeds the targetLen but also require finishing a sentence
    while len(out) < targetLen or out[-1][-1] not in sentenceEndingPunc:
        # get next phrases - needs to be sorted to match probabilities properly
        nextPhrases = srcGraph[out[-1]]         # a dict of next keys and their probabilities
        sortedPhrases = sorted(nextPhrases)     # sorted keys of nextPhrases
        npp = accumulate([nextPhrases[p].prob for p in sortedPhrases])
        i = 0 if len(nextPhrases) == 1 else next(x[0] for x in enumerate(npp) if x[1] >= random.random()) - 1
        out.append(sortedPhrases[i])
    return ' '.join(out)

