class Bankroll:

    def __init__(self, starting_amount=500):
        self.balance = starting_amount


    def placeBet(self, amount, hand):
        while True:
            if amount <= self.balance and amount % 25 == 0:
                hand.bet += amount
                self.balance.withDrawAmount(amount)
                print(f"Your bet of {amount} has been placed!")
                break
            else:
                amount = input("Enter a valid bet amount: ")

    def withdrawAmount(self, amount):
        self.balance -= amount

    def depositAmount(self, amount):
        self.balance += amount

    def isBankrupt(self):
        return self.balance < 25

    def canBet(self, amount):
        return amount <= self.balance


