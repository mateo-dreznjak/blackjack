class Bankroll:

    def __init__(self, starting_amount=500):
        self.balance = starting_amount

    def withdrawAmount(self, amount):
        self.balance -= amount

    def depositAmount(self, amount):
        self.balance += amount

    def isBankrupt(self):
        return self.balance < 25

    def canBet(self, amount):
        return amount <= self.balance

