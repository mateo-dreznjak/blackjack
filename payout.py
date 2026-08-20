class Payout:

    def defaultPayout(self, player):
        for hand in player.hands:
            if hand.result == "win":
                player.bankroll.depositAmount(hand.bet * 2)

            elif hand.result == "push":
                player.bankroll.depositAmount(hand.bet)

    def blackjackPayout(
        self,
        player_blackjack,
        dealer_blackjack,
        hand,
        player
    ):
        if not dealer_blackjack:
            player.bankroll.depositAmount(hand.bet * 2.5)

        else:
            if player_blackjack:
                player.bankroll.depositAmount(hand.bet)

    def surrenderPayout(self, hand, player):
        player.bankroll.depositAmount(hand.bet / 2)

    def sidebetPayout(self, player):
        for sidebet in player.sidebets:
            if sidebet.win:
                player.bankroll.depositAmount(sidebet.amount * sidebet.win_multiplier)

    def insurance_payout(self, player):
        player.bankroll.depositAmount(player.insurance_amount * 3)