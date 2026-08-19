class Hand:

    def __init__(self):
        self.cards = []
        self.bet = 0
        self.done = False
        self.bust = False
        self.surrendered = False
        self.splitted = False
        self.total = 0
        self.splitted_aces = False
        self.result = None
        self.aces = 0

    def addCard(self, card):
        if card.rank == "A":
            self.aces += 1

        self.cards.append(card)
        self.total = self.calculateTotal()

        if self.total > 21:
            self.bust = True
            self.result = "lose"
            self.done = True


    def calculateTotal(self):
        aces = self.aces
        total = 0

        for card in self.cards:
            total += card.value

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def soft17Check(self):
        total = 0

        for card in self.cards:
            total += card.value

            if card.rank == "A":
                total -= 10

        if total == 7:
            return True
        else:
            return False