class SideBet:

    def __init__(self, amount, sidebet_type):
        self.amount = amount
        self.sidebet_type = sidebet_type
        self.win = False
        self.winning_type = None
        self.win_multiplier = 0