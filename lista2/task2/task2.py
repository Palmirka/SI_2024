from collections import deque
from queue import PriorityQueue
import random
import heapq
import math

directions = ['U', 'L', 'D', 'R']


def get_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return [list(line) for line in lines]


def save(filename, res):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(res)


class Map:
    def __init__(self, data):
        self.data = data
        self.walls = []
        self.target = []
        self.start = []
        for row, line in enumerate(data):
            for col, char in enumerate(line):
                if char == '#':
                    self.walls.append((row, col))
                if char == 'B' or char == 'S':
                    self.start.append((row, col))
                if char == 'B' or char == 'G':
                    self.target.append((row, col))


class Game:
    def __init__(self, mapa):
        self.mapa = mapa
        self.x = len(self.mapa.data[0])
        self.y = len(self.mapa.data)
        self.positions = tuple(mapa.start)
        self.distances = [math.inf for _ in range(self.x) for _ in range(self.y)]
        self.get_distances()
        self.history = []

    def get_distances(self):
        def get_distance(position):
            visited = set()
            queue = deque()

            queue.append((0, position))
            while queue:
                dist, position = queue.popleft()
                if position in visited:
                    continue
                visited.add(position)
                if dist < self.distances[position[1] + self.x * position[0]]:
                    self.distances[position[1] + self.x * position[0]] = dist
                    for d, move in self.get_possible_moves(position):
                        queue.append((dist + 1, move))

        for target in self.mapa.target:
            get_distance(target)

    @staticmethod
    def reverse(move):
        return directions[(directions.index(move) - 2) % 4]

    @staticmethod
    def get_new_position(position, direction):
        if direction == 'U':
            return position[0] - 1, position[1]
        elif direction == 'D':
            return position[0] + 1, position[1]
        elif direction == 'L':
            return position[0], position[1] - 1
        elif direction == 'R':
            return position[0], position[1] + 1

    def get_possible_moves(self, position):
        moves = [('U', (position[0] - 1, position[1])), ('D', (position[0] + 1, position[1])),
                 ('L', (position[0], position[1] - 1)), ('R', (position[0], position[1] + 1))]
        return list(filter(lambda x: x[1] not in self.mapa.walls, moves))

    def check_all(self):
        for p in self.positions:
            if p not in self.mapa.target:
                return False
        return True

    def move_check(self, direction):
        old = self.positions
        self.move(direction)
        return old == self.positions

    def move(self, direction):
        new_positions = set()
        for position in self.positions:
            new_position = self.get_new_position(position, direction)
            if new_position in self.mapa.walls:
                new_position = position
            new_positions.add(new_position)
        self.positions = tuple(new_positions)

    def best_random(self, n=1200):
        best = ()
        history = ''
        for _ in range(n):
            self.history = []
            self.positions = self.mapa.start
            self.random_moves()
            if history == '' or len(best) > len(self.positions) or \
                    (len(best) == len(self.positions) and len(history) > len(self.history)):
                best = self.positions
                history = self.history
        self.positions = best
        self.history = history

    def random_moves(self, n=80):
        local = directions
        for i in range(n):
            direction = random.choice(local)
            for _ in range(random.randint(1, 4)):
                self.history.append(direction)
                self.move(direction)
            local = directions.copy()
            local.remove(self.reverse(direction))
            if len(self.positions) <= 3 or self.check_all():
                return True
        return False

    def bfs(self):
        queue = deque()
        visited = set()
        history = {}

        visited.add(self.positions)
        queue.append(self.positions)
        history[self.positions] = ''

        while queue:
            self.positions = queue.popleft()

            if self.check_all():
                self.history.append(history[self.positions])
                return self.positions

            # print(self.positions)
            old_pos = self.positions
            for direction in directions:
                for _ in range(4):
                    prev = self.positions
                    self.move(direction)
                    if self.positions not in visited:
                        queue.append(self.positions)
                        visited.add(self.positions)
                        history[self.positions] = history[prev] + direction
                self.positions = old_pos
        return None

    def a_star(self):
        def f(pos):
            g = len(history[pos])
            h = max([self.distances[p[1] + self.x * p[0]] for p in pos])
            return g + h

        queue = []
        # queue = PriorityQueue()
        visited = set()
        history = {}

        visited.add(self.positions)
        history[self.positions] = ''
        # queue.put((f(self.positions), self.positions))
        heapq.heappush(queue, (f(self.positions), self.positions))
        while queue:
            # self.positions = queue.get()[1]
            self.positions = heapq.heappop(queue)[1]
            if self.check_all():
                self.history = history[self.positions]
                # print('Solution:', len(self.history), self.positions, self.history)
                return self.positions

            old_pos = self.positions
            for direction in directions:
                self.move(direction)
                if self.positions not in visited:
                    history[self.positions] = history[old_pos] + direction
                    visited.add(self.positions)
                    heapq.heappush(queue, (f(self.positions), self.positions))
                if self.positions in history.keys() and len(history[self.positions]) > len(history[old_pos]) + 1:
                    history[self.positions] = history[old_pos] + direction
                self.positions = old_pos


def run2(debug=False):
    data = get_data('zad_input.txt')
    game = Game(mapa=Map(data))
    game.best_random()
    if debug:
        print('Starting positions:', game.mapa.start)
        print('Random moves count:', game.random_moves())
        print('Bfs start:', game.positions)
        print('Bfs end:', game.bfs())
        his = ''.join(game.history)
        print('Count:', len(his))
        print('Random moves history:', his)
    else:
        game.bfs()
    save('zad_output.txt', ''.join(game.history))


def run3(debug=False):
    data = get_data('zad_input.txt')
    game = Game(mapa=Map(data))
    if debug:
        print('Starting positions:', game.mapa.start)
        print('A*: ', game.a_star())
        his = ''.join(game.history)
        print('Count:', len(his))
        print('Random moves history:', his)
    else:
        game.a_star()
    save('zad_output.txt', ''.join(game.history))


run3()
