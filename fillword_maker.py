from random import choice, randrange

debug = 1


def choose_words(size, min_l, max_l):
    min_l, max_l = sorted([min_l, max_l])
    with open(r'words_rus2.txt', encoding='utf-8') as i:
        list_of_words = list(filter(lambda x: min_l <= len(x) <= max_l and '-' not in x,
                                    i.read().strip().split()))
    words = []
    while len(''.join(words)) != size ** 2:
        if len(''.join(words)) > size ** 2:
            words.pop(randrange(len(words)))
        else:
            words.append(choice(list_of_words))
    return words


def main(size, min_l, max_l):
    words = choose_words(size, min_l, max_l)
    actions = []
    i = 0
    n = 0
    x, y = randrange(size), randrange(size)
    breaker = 2000
    while len(actions) != size ** 2:
        breaker -= 1
        if breaker == 0:
            return main(size, min_l, max_l)
        if i == 0:
            while (x, y) in actions:
                x, y = randrange(size), randrange(size)
            actions.append((x, y))
            i += 1
        else:
            p = {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)}
            p = set(filter(lambda d: 0 <= d[0] < size and 0 <= d[1] < size and d not in actions, p))
            if len(p) == 0:
                actions.pop()
                i -= 1
            else:
                actions.append(choice(list(p)))
                x, y = actions[-1]
                i += 1
        if i >= len(words[n]):
            i -= len(words[n])
            n += 1
        if i == -1:
            n -= 1
            i += len(words[n])

    mat = [['' for _ in range(size)] for _ in range(size)]
    letters = ''.join(words)
    for i in range(size ** 2):
        x, y = actions[i]
        mat[y][x] = letters[i]
    shp = []
    for i in range(len(words)):
        shp.append(actions[len(''.join(words[:i])):len(''.join(words[:i + 1]))])
    shp = tuple([tuple(q) for q in shp])
    if debug:
        print(words)
    return mat, shp
