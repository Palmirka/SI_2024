import random

points = {'poker': 20,
          'straight flush': 8,
          'quad': 7,
          'full': 6,
          'flush': 5,
          'straight': 4,
          'triple': 3,
          'pairs': 2,
          'pair': 1}


class Player:
    def __init__(self, figurant: bool):
        self.cards = []
        self.figurant = figurant

    def random_card(self):
        if self.figurant:
            return random.randint(11, 14), random.randint(1, 4)
        return random.randint(2, 10), random.randint(1, 4)

    def random_cards(self, in_use):
        for i in range(5):
            card = self.random_card()
            while card in in_use:
                card = self.random_card()
            in_use.append(card)
            self.cards.append(card)

    def rate_hand(self):
        self.cards.sort()
        suits = [card[1] for card in self.cards]
        ranks = [card[0] for card in self.cards]
        counts = [ranks.count(rank) for rank in set(ranks)]

        if (len(set(suits))) == 1:
            if ranks == [10, 11, 12, 13, 14]:
                return points['poker']
            elif ranks[0] - ranks[-1] == 4:
                return points['straight flush']
            return points['flush']
        if ranks[0] - ranks[-1] == 4:
            return points['straight']

        if 4 in counts:
            return points['quad']
        elif 3 in counts and 2 in counts:
            return points['full']
        elif 3 in counts:
            return points['triple']
        elif counts.count(2) == 2:
            return points['pairs']
        elif 2 in counts:
            return points['pair']
        return 0


def play(remove_cards):
    figurant = Player(True)
    figurant.random_cards(in_use=[])
    f_points = figurant.rate_hand()

    blotkarz = Player(False)
    blotkarz.random_cards(in_use=remove_cards)
    b_points = blotkarz.rate_hand()

    return b_points > f_points


def all_of_value(num: int):
    return [(num, 1), (num, 2), (num, 3), (num, 4)]


def calculate_win_rate(iters: int, remove_cards):
    results = [play(remove_cards.copy()) for _ in range(iters)]
    return results.count(True) / iters


weakest_3 = [] + all_of_value(2) + all_of_value(3) + all_of_value(4)
weakest_4 = weakest_3 + all_of_value(5)
weakest_5 = weakest_4 + all_of_value(6)
weakest_6 = weakest_5 + all_of_value(7)
weakest_7 = weakest_6 + all_of_value(8)

print("All cards:", calculate_win_rate(100000, []))
print("Without 2 - 4:", calculate_win_rate(1000, weakest_3))
print("Without 2 - 5:", calculate_win_rate(1000, weakest_4))
print("Without 2 - 6:", calculate_win_rate(1000, weakest_5))
print("Without 2 - 7:", calculate_win_rate(1000, weakest_6))
print("Without 2 - 8:", calculate_win_rate(1000, weakest_7))

#print(blotkarz_cards())
