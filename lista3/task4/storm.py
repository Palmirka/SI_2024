def B(i, j):
    return 'B_%d_%d' % (i, j)


def domains(Vs):
    return [q + ' in 0..1' for q in Vs]


def vertical(R, C):
    return [B(i - 1, j) + " + 2 * " + B(i, j) + " + 3 * " + B(i + 1, j) + " #\= 2" for j in range(C)
            for i in range(1, R - 1)]


def horizontal(R, C):
    return [B(i, j - 1) + " + 2 * " + B(i, j) + " + 3 * " + B(i, j + 1) + " #\= 2" for j in range(1, C - 1)
            for i in range(R)]


def box(R, C):
    banned = [6, 7, 9, 11, 13, 14]
    return [B(i, j) + " + 2 * " + B(i, j + 1) + " + 4 * " + B(i + 1, j) + " + 8 * " + B(i + 1, j + 1) + " #\= " + str(b)
            for b in banned for j in range(C - 1) for i in range(R - 1)]


def vertical_count(R, C):
    def inner(s, j):
        for i in range(R):
            s += B(i, j)
            if i != R - 1:
                s += " + "
        return s
    return [inner('', j) + " #= " + str(cols[j]) for j in range(C)]


def horizontal_count(R, C):
    def inner(s, i):
        for j in range(C):
            s += B(i, j)
            if j != C - 1:
                s += " + "
        return s

    return [inner('', i) + " #= " + str(rows[i]) for i in range(R)]


def print_constraints(Cs, indent, d):
    position = indent
    writeln(indent * ' ')
    for c in Cs:
        writeln(c + ',')
        position += len(c)
        if position > d:
            position = indent
            writeln('')
            writeln(indent * ' ')


def storms(rows, cols, triples):
    writeln(':- use_module(library(clpfd)).')

    R = len(rows)
    C = len(cols)

    variables = [B(i, j) for i in range(R) for j in range(C)]

    writeln('solve([' + ', '.join(variables) + ']) :- ')

    bs = domains(variables) + vertical(R, C) + horizontal(R, C) + box(R, C) + vertical_count(R, C) + horizontal_count(R, C)
    # TODO: add some constraints

    for i, j, val in triples:
        bs.append('%s #= %d' % (B(i, j), val))

    print_constraints(bs, 4, 70)

    writeln('    labeling([ff], [' + ', '.join(variables) + ']).')
    writeln('')
    writeln(":- tell('prolog_result.txt'), solve(X), write(X), nl, told.")


def writeln(s):
    output.write(s + '\n')


txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')
rows = list(map(int, txt[0].split()))
cols = list(map(int, txt[1].split()))
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(list(map(int, txt[i].split())))

storms(rows, cols, triples)
