from collections import deque
import copy


def get_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        [row, col] = [int(x) for x in lines[0].split()]
        row_val = [[int(el) for el in line.split(' ')] for line in lines[1:row + 1]]
        col_val = [[int(el) for el in line.split(' ')] for line in lines[row + 1:]]
        return row, col, row_val, col_val


def save(filename, res):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(res)


class Field:
    ZERO = '.'
    ONE = '#'
    UNKNOWN = ' '


class Game:
    def __init__(self, data):
        [self.row, self.col, self.row_val, self.col_val] = data
        self.board = [[Field.UNKNOWN for _ in range(self.col)] for _ in range(self.row)]
        self.not_solved = self.row * self.col
        self.col_not_solved = [i for i in range(self.col)]
        self.row_not_solved = [i for i in range(self.row)]
        self.row_domain = []
        self.col_domain = []

    def single_domain(self, row, start, end, blocks_idx):
        def flatten(xss):
            return [x for xs in xss for x in xs]

        if blocks_idx == len(row) - 1:
            return [[i] for i in range(start, end)]
        block = row[blocks_idx]
        result = [list(map(lambda l: [i] + l, self.single_domain(row, i + block + 1, end + block + 1, blocks_idx + 1)))
                  for i in range(start, end)]
        return flatten(result)

    def domain(self):
        def to_field(domain, blocks, size):
            fields = [Field.ZERO for _ in range(size)]
            for idx, start in enumerate(domain):
                for field in range(blocks[idx]):
                    fields[start + field] = Field.ONE
            return fields

        self.row_domain = [list(map(lambda d: to_field(d, row, self.col),
                                    self.single_domain(row, 0, self.col - (sum(row[0:]) + len(row) - 1) + 1, 0)))
                           for row in self.row_val]
        self.col_domain = [list(map(lambda d: to_field(d, col, self.row),
                                    self.single_domain(col, 0, self.row - (sum(col[0:]) + len(col) - 1) + 1, 0)))
                           for col in self.col_val]

        # print("row domain: ", self.row_domain)
        # print("col domain: ", self.col_domain)

    def update_board(self):
        for col_idx in self.col_not_solved:
            if len(self.col_domain[col_idx]) == 1:
                self.col_not_solved.remove(col_idx)
                for i in range(self.row):
                    self.board[i][col_idx] = self.col_domain[col_idx][0][i]

        for row_idx in self.row_not_solved:
            if len(self.row_domain[row_idx]) == 1:
                self.row_not_solved.remove(row_idx)
                self.board[row_idx] = self.row_domain[row_idx][0]

    @staticmethod
    def check_field(f1, f2):
        return f1 == f2 or f1 == Field.UNKNOWN or f2 == Field.UNKNOWN

    def reduce_domain(self):
        # print('\n', self.board, '\n')
        for row_idx in self.row_not_solved:
            to_remove = []
            for domain in self.row_domain[row_idx]:
                if not all([self.check_field(domain[idx], self.board[row_idx][idx]) for idx in range(len(domain))]):
                    to_remove.append(domain)
            self.row_domain[row_idx] = [i for i in self.row_domain[row_idx] if i not in to_remove]

        for col_idx in self.col_not_solved:
            to_remove = []
            for domain in self.col_domain[col_idx]:
                if not all([self.check_field(domain[idx], self.board[idx][col_idx]) for idx in range(len(domain))]):
                    to_remove.append(domain)
            self.col_domain[col_idx] = [i for i in self.col_domain[col_idx] if i not in to_remove]

    def domain_intersection(self):
        for row_idx in self.row_not_solved:
            first = self.row_domain[row_idx][0]
            for field in range(self.col):
                if all([self.check_field(first[field], self.row_domain[row_idx][i][field]) for i in range(len(self.row_domain[row_idx]))]):
                    if self.board[row_idx][field] == Field.UNKNOWN:
                        self.board[row_idx][field] = first[field]
                        # print("Column intersection: ", col_idx, field)

        for col_idx in self.col_not_solved:
            first = self.col_domain[col_idx][0]
            for field in range(self.row):
                if all([self.check_field(first[field], self.col_domain[col_idx][i][field]) for i in range(len(self.col_domain[col_idx]))]):
                    if self.board[field][col_idx] == Field.UNKNOWN:
                        self.board[field][col_idx] = first[field]
                        # print("Row intersection: ", field, row_idx)

    def solved(self):
        return all([self.board[row][col] == Field.ONE or self.board[row][col] == Field.ZERO
                    for row in range(self.row) for col in range(self.col)])

    def solve(self):
        self.domain()
        while not self.solved():
            self.update_board()
            self.reduce_domain()
            self.domain_intersection()
        return '\n'.join(''.join(self.board[i]) for i in range(self.row))


data = get_data('zad_input.txt')
game = Game(data)
save('zad_output.txt', game.solve())
