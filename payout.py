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
            if sidebet.sidebet_type == "poker" and sidebet.win:
                player.bankroll.depositAmount(sidebet.amount * 10)

            elif sidebet.sidebet_type == "special" and sidebet.win:
                match sidebet.winning_type:
                    case "suited777":
                        player.bankroll.depositAmount(sidebet.amount * 201)

                    case "suited678":
                        player.bankroll.depositAmount(sidebet.amount * 101)

                    case "unsuited777":
                        player.bankroll.depositAmount(sidebet.amount * 51)

                    case "unsuited678":
                        player.bankroll.depositAmount(sidebet.amount * 31)

                    case "suited21":
                        player.bankroll.depositAmount(sidebet.amount * 11)

                    case "unsuited21":
                        player.bankroll.depositAmount(sidebet.amount * 4)

                    case "any20":
                        player.bankroll.depositAmount(sidebet.amount * 3)

                    case "any19":
                        player.bankroll.depositAmount(sidebet.amount * 3)

                    case _:
                        print("Unknown SideBet winning type")

    def insurance_payout(self, player):
        player.bankroll.depositAmount(player.insurance_amount * 3)