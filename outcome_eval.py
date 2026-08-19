class OutcomeEval:

    def evaluate(self, player, dealer):
        for hand in player.hands:
            if hand.result == "lose":
                continue

            if hand.surrendered:
                hand.result = "surrender"

                continue

            if dealer.hand.bust:
                hand.result = "win"
                continue

            if hand.total > dealer.hand.total:
                hand.result = "win"

            elif hand.total < dealer.hand.total:
                hand.result = "lose"
            else:
                hand.result = "push"

    def evaluateBlackjack(self, player_hand, dealer_hand):
        player_blackjack = False
        dealer_blackjack = False

        if player_hand.total == 21:
            player_blackjack = True

        if dealer_hand.total == 21:
            dealer_blackjack = True

        return player_blackjack, dealer_blackjack

    def sidebetEval(self, player, dealer):
        for sidebet in player.sidebets:
            if sidebet.sidebet_type == "poker":
                sidebet.win = self.evaluatePokerSB(player, dealer)

            elif sidebet.sidebet_type == "special":
                sidebet.winning_type = self.evaluateSpecialSB(player, dealer)

                if sidebet.winning_type is not None:
                    sidebet.win = True

    def evaluateStraight(self, relevant_cards):
        straightValueList = []

        for card in relevant_cards:
            match card.rank:
                case "J":
                    straightValueList.append(11)

                case "Q":
                    straightValueList.append(12)

                case "K":
                    straightValueList.append(13)

                case "A":
                    straightValueList.append(14)

                case _:
                    straightValueList.append(int(card.rank))

        if 2 in straightValueList and 3 in straightValueList and 14 in straightValueList:
            acePosition = straightValueList.index(14)
            straightValueList[acePosition] = 1

        straightValueList.sort()

        if (
            straightValueList[0] + 1 == straightValueList[1]
            and straightValueList[1] + 1 == straightValueList[2]
        ):
            return True

        return False

    def evaluateSpecialSB(self, player, dealer):
        winning_type = None

        relevant_cards = [
            player.hands[0].cards[0],
            player.hands[0].cards[1],
            dealer.hand.cards[0]
        ]

        relevant_card_total = self.calculateRelevantCardsTotal(relevant_cards)

        if (
            all(card.rank == "7" for card in relevant_cards)
            and all(card.suit == relevant_cards[0].suit for card in relevant_cards)
        ):
            winning_type = "suited777"
            return winning_type

        elif (
            any(card.rank == "6" for card in relevant_cards)
            and any(card.rank == "7" for card in relevant_cards)
            and any(card.rank == "8" for card in relevant_cards)
            and all(card.suit == relevant_cards[0].suit for card in relevant_cards)
        ):
            winning_type = "suited678"
            return winning_type

        elif all(card.rank == "7" for card in relevant_cards):
            winning_type = "unsuited777"
            return winning_type

        elif (
            any(card.rank == "6" for card in relevant_cards)
            and any(card.rank == "7" for card in relevant_cards)
            and any(card.rank == "8" for card in relevant_cards)
        ):
            winning_type = "unsuited678"
            return winning_type

        elif (
            relevant_card_total == 21
            and all(card.suit == relevant_cards[0].suit for card in relevant_cards)
        ):
            winning_type = "suited21"
            return winning_type

        elif relevant_card_total == 21:
            winning_type = "unsuited21"
            return winning_type

        elif relevant_card_total == 20:
            winning_type = "any20"
            return winning_type

        elif relevant_card_total == 19:
            winning_type = "any19"
            return winning_type

        else:
            return None

    def evaluatePokerSB(self, player, dealer):
        relevant_cards = [
            player.hands[0].cards[0],
            player.hands[0].cards[1],
            dealer.hand.cards[0]
        ]

        win = self.evaluateStraight(relevant_cards)

        if win:
            return True

        elif all(card.suit == relevant_cards[0].suit for card in relevant_cards):
            return True

        elif all(card.rank == relevant_cards[0].rank for card in relevant_cards):
            return True

        else:
            return False

    def calculateRelevantCardsTotal(self, relevant_cards):
        aces = 0

        for card in relevant_cards:
            if card.rank == "A":
                aces += 1

        total = 0

        for card in relevant_cards:
            total += card.value

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def evaluate_insurance(self, player, dealer):
        if dealer.hand.cards[0].rank == "A" and dealer.hand.cards[1].value == 10:
            return True
        return False
    