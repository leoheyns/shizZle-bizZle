from sort import merge_pairs

ulist = ["kub", "eur", "ru", "rug", "tu delft", "tue", "ul", "um", "ut", "uu", "uva", "vu", "wu"]
uwords = [["tilburg", "kub"], ["erasmus", "rotterdam", "eur"], [], [], [], [], [], [], [], [], [], [], [], []]

ranking = [0 for x in range(len(ulist)-1)]
print(ranking)


def newranking(uid):
    global ranking
    ranking[uid] += 1


def uwordsearch(uid, text):
    global uwords
    i = 0
    while i < len(uwords[uid]):
        if text.find(uwords[uid][i]) >= 0:
            return 1
        i += 1
    return 0


def adjustranking(text):
    global ranking
    ranking = [ranking[i] + uwordsearch(i, text) for i in range(len(ulist)-1)]


def orderedranking():
    rank = merge_pairs([(ranking[i], ulist[i]) for i in range(len(ulist)-1)])
    rank.reverse()
    return rank