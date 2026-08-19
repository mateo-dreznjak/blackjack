class Card:

    def __init__(self, card_suit, card_value, card_rank):
        self.suit = card_suit
        self.value = card_value
        self.rank = card_rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"