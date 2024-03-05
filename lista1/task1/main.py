letters = 'abcdefgh'
numbers = [1, 2, 3, 4, 5, 6, 7, 8]


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

    def run(self):
        file = open(self.file_name, 'r')
        for line in file:
            self.turn, white_king, white_tower, black_king = line.split()
            # self.white_king['position'] = self.string_to_position(white_king)
            # self.white_tower['position'] = self.string_to_position(white_tower)
            # self.black_king['position'] = self.string_to_position(black_king)
            self.pawns[0]['position'] = self.string_to_position(white_king)
            self.pawns[1]['position'] = self.string_to_position(white_tower)
            self.pawns[2]['position'] = self.string_to_position(black_king)
            self.play()

    def possible_moves(self, obj):
        moves = []
        x, y = obj['position']
        if obj['figure'] == 'tower':
            for letter in letters:
                moves.append((letter, y))
            for number in numbers:
                moves.append((x, number))
        else:
            x, y = obj['position']
            ys = [y - 1, y, y + 1]
            xs = [x - 1, x, x + 1]
            for letter in xs:
                for number in ys:
                    if 0 <= letter < 8 and 1 <= number < 9:
                        moves.append((letter, number))
        return self.remove_moves(moves)

    def moves_to_remove(self, obj):
        pass

    def play(self):
        pass


chess = Chess('zad1_input.txt')
chess.run()
