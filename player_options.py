class PlayerOptions:

    def listPlayerOptions(self, player, hand):
        if hand.done == False:
            can_surrender = self.surrenderEval(player, hand)
            can_double = self.doubleEval(player, hand)
            can_split = self.splitEval(player, hand)
            options_list = self.createList(
                can_surrender,
                can_double,
                can_split
            )
            return options_list

    def surrenderEval(self, player, hand):
        return (
            player.hands.index(hand) == 0
            and len(hand.cards) == 2
            and not hand.splitted
        )


    def doubleEval(self, player, hand):
        return (
            len(hand.cards) == 2
            and not hand.splitted
            and hand.bet <= player.bankroll.balance
        )

    def splitEval(self, player, hand):
        return (
            len(hand.cards) == 2
            and hand.bet <= player.bankroll.balance
            and hand.cards[0].rank == hand.cards[1].rank
            and player.split_count < 3
        )

    def createList(self, can_surrender, can_double, can_split):
        options_list = ["hit", "stand"]

        if can_surrender:
            options_list.append("surrender")

        if can_double:
            options_list.append("double")

        if can_split:
            options_list.append("split")

        return options_list