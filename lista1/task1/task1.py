from collections import deque

letters = 'abcdefgh'
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
turns = ['black', 'white']


class Chess:
    def __init__(self, filename):
        self.file_name = filename
        self.turn = None
        self.pawns = [{'color': 'white', 'figure': 'king', 'position': (0, 0)},
                      {'color': 'white', 'figure': 'tower', 'position': (0, 0)},
                      {'color': 'black', 'figure': 'king', 'position': (0, 0)}]

    @staticmethod
    def string_to_position(position):
        return letters.index(position[0]), int(position[1])

    @staticmethod
    def positions_of(xs, ys):
        moves = []
        for letter in xs:
            for number in ys:
                if 0 <= letter < 8 and 1 <= number < 9:
                    moves.append((letter, number))
        return moves

    def run(self):
        file = open(self.file_name, 'r')
        for line in file:
            self.turn, white_king, white_tower, black_king = line.split()
            self.pawns[0]['position'] = self.string_to_position(white_king)
            self.pawns[1]['position'] = self.string_to_position(white_tower)
            self.pawns[2]['position'] = self.string_to_position(black_king)
            self.play()

    def position_of_kings(self, position):
        return position == self.pawns[0]['position'] or position == self.pawns[2]['position']

    def possible_moves(self, obj, debug=False):
        moves = []
        x, y = obj['position']
        if obj['figure'] == 'tower':
            for letter in range(x, -1, -1):
                if self.position_of_kings((letter, y)):
                    break
                moves.append((letter, y))
            for letter in range(x, len(letters)):
                if self.position_of_kings((letter, y)):
                    break
                moves.append((letter, y))
            for number in range(y, len(numbers)):
                if self.position_of_kings((x, number)):
                    break
                moves.append((x, number))
            for number in range(y, 0, -1):
                if self.position_of_kings((x, number)):
                    break
                moves.append((x, number))
        else:
            x, y = obj['position']
            ys = [y - 1, y, y + 1]
            xs = [x - 1, x, x + 1]
            for letter in xs:
                for number in ys:
                    if 0 <= letter < 8 and 1 <= number < 9:
                        moves.append((letter, number))
        if debug:
            print(f"{obj['color']} {obj['figure']} {[x for x in moves if x not in self.moves_to_remove(obj)]}")
        return [x for x in moves if x not in self.moves_to_remove(obj)]

    def moves_to_remove(self, obj):
        banned_moves = [pawn['position'] for pawn in self.pawns]
        if obj['figure'] == 'king' and obj['color'] == 'white':
            x, y = self.pawns[2]['position']
            ys = [y - 1, y, y + 1]
            xs = [x - 1, x, x + 1]
            banned_moves += self.positions_of(xs, ys)
        elif obj['figure'] == 'king' and obj['color'] == 'black':
            x, y = self.pawns[0]['position']
            ys = [y - 1, y, y + 1]
            xs = [x - 1, x, x + 1]
            banned_moves += self.positions_of(xs, ys)
            banned_moves += self.possible_moves(self.pawns[1])
        return set(banned_moves)

    def is_checkmate(self, obj):
        return len(self.possible_moves(obj)) == 0

    def play(self):
        queue = deque()
        visited = set()

        # Start with the initial state
        initial_state = tuple((pawn['position'] for pawn in self.pawns))
        queue.append((initial_state, 0))
        visited.add(initial_state)

        while queue:
            state, moves = queue.popleft()
            if self.is_checkmate(self.pawns[2]):
                return visited

            # Generate possible moves for the white king and tower
            for i in range(3):
                if self.pawns[i]['color'] == self.turn:
                    # print(visited)
                    for move in self.possible_moves(self.pawns[i]):
                        print(self.pawns)
                        new_pawns = self.pawns.copy()
                        new_pawns[i]['position'] = move
                        new_state = tuple((pawn['position'] for pawn in new_pawns))

                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append((new_state, moves + 1))
            self.turn = turns[(turns.index(self.turn) + 1) % 2]


chess = Chess('zad1_input.txt')
chess.run()
