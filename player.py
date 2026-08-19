class Player:

    def __init__(self, name):
        self.name = name
        self.hands = []
        self.bankroll = None
        self.split_count = 0
        self.sidebets = []

    def resetHands(self):
        self.hands = []
        self.split_count = 0
        self.sidebets = []