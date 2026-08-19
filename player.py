class Player:

    def __init__(self, name):
        self.name = name
        self.hands = []
        self.bankroll = None
        self.split_count = 0
        self.sidebets = []
        self.insurance_amount = 0

    def resetHands(self):
        self.hands = []
        self.split_count = 0
        self.sidebets = []
        self.insurance_amount = 0