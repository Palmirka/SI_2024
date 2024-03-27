import numpy as np
import random


class Game:
    def __init__(self, columns, rows) -> None:
        self.x = len(columns)
        self.y = len(rows)
        self.columns = columns
        self.rows = rows
        self.board = np.empty((self.x, self.y))
        self.column_dists = np.empty(self.x)
        self.row_dists = np.empty(self.y)
        self.bad_lines = []
        self.score_sum = 0
        self.reset()

    @staticmethod
    def _opt_dist(data) -> int:
        pref = [0]
        [pref.append(pref[-1] + num) for num in data['fields']]
        count = sum(data['fields'])
        longest = len(data['fields']) + 1
        for i in range(data['length'], longest):
            inside = pref[i] - pref[i - data['length']]
            outside = count - inside
            changed = (data['length'] - inside) + outside
            longest = min(longest, changed)
        return longest

    def __str__(self) -> str:
        return '\n'.join([''.join(['#' if 1 == self.board[x][y] else '.' for y in range(self.y)])
                          for x in range(self.x)])

    def reset(self):
        self.board = np.array([[random.randint(0, 1) for _ in range(self.y)] for _ in range(self.x)])
        self.column_dists.fill(0)
        self.row_dists.fill(0)
        self.bad_lines = []
        self.score_sum = 0
        for x in range(self.x):
            self._update_column_score(x)
        for y in range(self.y):
            self._update_row_score(y)

    def _get_row(self, n):
        return self.board[:, n].copy()

    def _get_column(self, n):
        return self.board[n].copy()

    def _update_column_score(self, x):
        column = self._get_column(x)
        score = Game._opt_dist({'fields': column, 'length': self.columns[x]})
        self.score_sum += score - self.column_dists[x]

        self.column_dists[x] = score
        self._update_bad(score, line_id=x+1)

    def _update_row_score(self, y: int):
        row = self._get_row(y)
        score = Game._opt_dist({'fields': row, 'length': self.rows[y]})
        self.score_sum += score - self.row_dists[y]

        self.row_dists[y] = score
        self._update_bad(score, line_id=-(y+1))

    def _update_bad(self, score, line_id):
        if score != 0 and line_id not in self.bad_lines:
            self.bad_lines.append(line_id)
        elif score == 0 and line_id in self.bad_lines:
            self.bad_lines.remove(line_id)

    @staticmethod
    def _flip(value):
        return -value + 1

    def _check_score(self, x, y) -> int:
        old_score = self.column_dists[x] + self.row_dists[y]
        column = self._get_column(x)
        row = self._get_row(y)
        column[y] = self._flip(column[y])
        row[x] = self._flip(row[x])
        column_score = Game._opt_dist({'fields': column, 'length': self.columns[x]})
        row_score = Game._opt_dist({'fields': row, 'length': self.rows[y]})
        new_score = column_score + row_score
        return new_score-old_score

    def change_one(self):
        line_id = random.choice(self.bad_lines)
        if line_id > 0:
            x = line_id - 1
            y = self._find_best_index(x, range(self.y), is_row=True)
        else:
            y = -line_id - 1
            x = self._find_best_index(y, range(self.x), is_row=False)
        self.board[x][y] = self._flip(self.board[x][y])
        self._update_column_score(x)
        self._update_row_score(y)

    def _find_best_index(self, fixed_coord, iterable, is_row):
        scores = [self._check_score(fixed_coord, coord) if is_row else self._check_score(coord, fixed_coord) for coord
                  in iterable]
        best_score = min(scores)
        best_indices = [i for i, score in enumerate(scores) if score == best_score]
        return random.choice(best_indices)


def get_data(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()
        [x, y] = [int(s) for s in lines[0].split()]
        rows = [int(s) for s in lines[1: x+1]]
        columns = [int(s) for s in lines[x+1: x+1+y]]
        return columns, rows


def save(file: str, game):
    with open(file, 'w') as f:
        f.write(str(game))


rows, columns = get_data("zad5_input.txt")
game = Game(columns, rows)
how_many_without_change = 0
last_score = -1

while game.score_sum > 0:
    game.change_one()
    if last_score != game.score_sum:
        last_score = game.score_sum
        how_many_without_change = 0
    else:
        how_many_without_change += 1

    if how_many_without_change > 50:
        last_score = -1
        how_many_without_change = 0
        game.reset()

save("zad5_output.txt", game)
