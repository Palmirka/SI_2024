from typing import Set, Dict
N = 30


def get_words_set(filename: str):
    with open(filename, encoding='utf-8') as f:
        lines = [s.strip() for s in f.readlines()]
        return set(filter(lambda s: s != "", lines))


def add_spaces(line: str, res, pos: int, results: Dict[int, tuple[int, list[int]]]) -> \
        (Dict[int, tuple[int, list[int]]], tuple[int, list[int]]):
    if pos in results:
        return results, (results[pos][0], results[pos][1].copy())

    best = -1
    spaces = []

    for i in range(1, N):
        if pos + i > len(line):
            break

        word = line[pos:pos + i]
        if word in words:
            val = i ** 2
            if pos + i == len(line):
                best = val
                spaces = []

            results, res = add_spaces(line=line, res=res, pos=pos + i, results=results)
            if res[0] > -1:
                val += res[0]
                if val > best:
                    best = val
                    spaces = res[1]
                    spaces.append(pos + i)

    results[pos] = (best, spaces.copy())
    return results, (best, spaces)


def run(filename):
    res = []
    with open(filename, encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("\n", "")
            results, (best, spaces) = add_spaces(line=line, res=res, pos=0, results={})
            arr = list(line)
            for pos in spaces:
                arr.insert(pos, ' ')
            arr.append('\n')
            res.append("".join(arr))
    return res


def save(filename, res):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(res)


words = get_words_set('words_for_ai1.txt')
res = run('pan_tadeusz_bez_spacji.txt')
save('results2.txt', res)
