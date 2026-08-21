from hand import Hand
from side_bet import SideBet


class PlayerActions:

    def hit(self, hand, deck):
        new_card = deck.drawCard()
        hand.addCard(new_card)


    def stand(self, hand):
        hand.done = True

    def surrender(self, hand):
        hand.surrendered = True
        hand.done = True
        hand.result = "surrender"

    def double(self, hand, deck, player):
        additional_bet = hand.bet
        new_card = deck.drawCard()
        hand.addCard(new_card)
        player.bankroll.withdrawAmount(hand.bet)
        hand.bet += additional_bet
        hand.done = True

    def split(self, hand, deck, player):
        new_hand = Hand()
        new_hand.bet = hand.bet

        temp_index = player.hands.index(hand)
        player.hands.insert(temp_index + 1, new_hand)

        temp_card = hand.cards.pop(1)

        if temp_card.rank == "A":
            hand.aces -= 1

        new_hand.addCard(temp_card)
        new_card = deck.drawCard()
        hand.addCard(new_card)
        new_card = deck.drawCard()
        new_hand.addCard(new_card)


        hand.splitted = True
        new_hand.splitted = True

        player.bankroll.withdrawAmount(hand.bet)
        player.split_count += 1

        if hand.cards[0].rank == "A" and new_hand.cards[0].rank == "A":
            hand.done = True
            hand.splitted_aces = True
            new_hand.done = True
            new_hand.splitted_aces = True
        return new_hand

    def placeMainBet(self, hand, player):
        while True:
            try:
                amount = int(
                    input(
                        "Place the amount you want to bet "
                        "(increments of 25, max: 500): "
                    )
                )

                can_bet = player.bankroll.canBet(amount)

                if can_bet and amount % 25 == 0 and 500 >= amount > 0:
                    break
                else:
                    print("Invalid amount")

            except ValueError:
                print("Not a valid input!")

        hand.bet = amount
        player.bankroll.withdrawAmount(amount)
        

    def chooseSidebet(self, player):
        if player.bankroll.balance >= 5:
            while True:
                sidebet_type = input(
                    "Choose the type of SideBet (poker/special/both): "
                ).lower()

                while sidebet_type not in ["poker", "special", "both"]:
                    print("Invalid choice!")
                    sidebet_type = input(
                        "Choose the type of SideBet "
                        "(poker/special/both): "
                    ).lower()

                if sidebet_type == "both" and player.bankroll.balance < 10:
                    print("Not enough money for Both SBs!")
                    continue

                if sidebet_type == "both":
                    self.placeSidebet(player, "poker", True)
                    self.placeSidebet(player, "special")
                    break

                self.placeSidebet(player, sidebet_type)
                break

        else:
            print("You do not have enough money to place a SideBet")

    def placeSidebet(
        self,
        player,
        sidebet_type,
        second_sidebet_pending=False
    ):
        while True:
            try:
                amount = int(
                    input(
                        "Place the amount you want to bet "
                        "(increments of 5, max: 100): "
                    )
                )

                can_bet = player.bankroll.canBet(amount)

                if 100 >= amount > 0 and amount % 5 == 0 and can_bet:

                    if (
                        second_sidebet_pending
                        and (player.bankroll.balance - amount) < 5
                    ):
                        print("You need at least 5€ for your second SB!")
                        continue

                    break

                else:
                    print("Invalid amount")

            except ValueError:
                print("Not a valid input!")

        new_sidebet = SideBet(amount, sidebet_type)
        player.bankroll.withdrawAmount(amount)
        player.sidebets.append(new_sidebet)

    def take_insurance(self, player):
        player.bankroll.withdrawAmount(player.hands[0].bet / 2)
        player.insurance_amount = player.hands[0].bet / 2
