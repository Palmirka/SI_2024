import random
import numpy as np

points = {'poker': 100,
          'quad': 90,
          'full': 80,
          'color': 70,
          'straight': 60,
          'triple': 50,
          'pairs': 40,
          'pair': 30,
          'higher': 20}


class Player:
    def __init__(self, figurant):
        self.cards = np.empty(5, (int, int))
        self.figurant = figurant

    def random_card(self):
        if self.figurant:
            return random.randint(11, 14), random.randint(1, 4)
        random.randint(2, 10), random.randint(1, 4)

    def random_cards(self, in_use):
        for i in range(5):
            card = self.random_card()
            while card in in_use:
                card = self.random_card()
            in_use.append(card)
            self.cards[i] = card
        self.cards.sort()

    def rate_hand(self):
        pass


figurant = Player(True)
blotkarz = Player(False)
