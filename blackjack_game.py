
from deck import Deck
from hand import Hand
from player import Player
from dealer import Dealer
from bankroll import Bankroll
from player_options import PlayerOptions
from player_actions import PlayerActions
from outcome_eval import OutcomeEval
from payout import Payout
from time import sleep
DELAY = 0


class BlackjackGame:

    def __init__(self):
        self.name = None
        self.player = None
        self.dealer = Dealer()
        self.player_options = PlayerOptions()
        self.player_actions = PlayerActions()
        self.outcome_eval = OutcomeEval()
        self.payout = Payout()
        self.starting_amount = 0
        self.current_hand_index = 0
        self.deck = None

    def setupGame(self):

        self.name = input(
            "Enter your name (between 4 and 12 characters, only letters): "
        )

        while not (12 >= len(self.name) >= 4) or not self.name.isalpha():
            print("Invalid input!")
            self.name = input(
                "Enter a name (between 4 and 12 characters, only letters): "
            )

        self.player = Player(self.name)

        while True:
            try:
                amount = int(
                    input(
                        f"Hello {self.name}, enter an amount between 500 and "
                        f"10.000€ as your starting balance "
                        f"(increments of 25): "
                    )
                )

                if 10000 >= amount >= 500 and amount % 25 == 0:
                    self.starting_amount = amount
                    break
                else:
                    print("Invalid amount")

            except ValueError:
                print("Not a valid input!")

        self.player.bankroll = Bankroll(self.starting_amount)
        print(f"You now have {self.player.bankroll.balance:.2f}€ as your starting balance.")

    def gameHandler(self):
        print("Game Initialization")
        self.gameStartingInitialisation()

        while True:
            if not self.player.bankroll.isBankrupt():
                play_game = input(
                    "You want to play a round of blackjack? (y/n): "
                ).lower()

                if play_game == "y":
                    self.roundStartingInitialisation()
                    self.mainGameLoop()

                elif play_game == "n":
                    break
            else:
                print("You are out of money!")
                break

    def gameStartingInitialisation(self):
        self.deck = Deck()
        print("A new deck has been created")

    def roundStartingInitialisation(self):
        self.deck.neededDeckShuffle()
        self.current_hand_index = 0
        self.player.resetHands()
        self.dealer.resetHand()
        print("Hands have been reset")

        new_hand = Hand()
        self.player.hands.append(new_hand)

        self.dealer.hand = Hand()

    def initialCardDeal(self):

        self.player.hands[0].addCard(self.deck.drawCard())
        self.dealer.hand.addCard(self.deck.drawCard())
        self.player.hands[0].addCard(self.deck.drawCard())
        self.dealer.hand.addCard(self.deck.drawCard())

        self.displayPlayerHands(self.player.hands[0])
        sleep(DELAY)
        self.displayDealerHand(self.dealer.hand, True)


    def playPlayerHands(self):

        while self.current_hand_index < len(self.player.hands):

            hand = self.player.hands[self.current_hand_index]

            while not hand.done:

                player_options_list = self.displayPlayerOptions(
                    self.player,
                    hand
                )

                choice = input("Choose your action! : ")

                while choice not in player_options_list:
                    choice = input("Choose a valid option: ")

                print(f"You chose {choice}")
                self.executePlayerAction(
                    choice,
                    hand,
                    self.deck,
                    self.player
                )


            self.current_hand_index += 1

    def playDealerHand(self, dealer):
        self.displayDealerHand(dealer.hand)
        sleep(DELAY)
        while dealer.hand.total < 17:
            new_card = self.deck.drawCard()
            print(f"The new dealer card is {new_card}")
            dealer.hand.addCard(new_card)
            sleep(DELAY)
            self.displayDealerHand(dealer.hand)

        if dealer.hand.total == 17 and dealer.hand.aces > 0:
            hasSoft17 = dealer.hand.soft17Check()

            if hasSoft17:
                print("The dealer has a soft-17 hand.")
                sleep(DELAY)
                new_card = self.deck.drawCard()
                print(f"The new dealer card is {new_card}")
                dealer.hand.addCard(new_card)
                self.displayDealerHand(dealer.hand)

                sleep(DELAY)
                while dealer.hand.total < 17:
                    new_card = self.deck.drawCard()
                    print(f"The new dealer card is {new_card}")
                    dealer.hand.addCard(new_card)
                    self.displayDealerHand(dealer.hand)

                    sleep(DELAY)

    def displayPlayerOptions(self, player, hand):

        player_options_list = self.player_options.listPlayerOptions(
            player,
            hand
        )
        sleep(DELAY)
        print("Your options are: ")

        for option in player_options_list:
            print(option)

        return player_options_list

    def executePlayerAction(self, choice, hand, deck, player):

        match choice:
            case "hit":
                temp_current_hand_length = len(hand.cards)-1
                self.player_actions.hit(hand, deck)
                print(f"Your new card is {hand.cards[temp_current_hand_length +1]}")
                sleep(DELAY)
                print("Your hand now consists of:")
                self.displayPlayerHands(hand)

            case "stand":
                self.player_actions.stand(hand)

            case "surrender":
                self.player_actions.surrender(hand)
                self.payout.surrenderPayout(hand, player)
                self.payout_output_handler(player, "surrender")


            case "double":
                self.player_actions.double(hand, deck, player)
                self.bet_output_handler(player, "double", hand)
                print(f"Your new card is {hand.cards[2]}")
                sleep(DELAY)
                self.displayPlayerHands(hand)

            case "split":
                new_hand = self.player_actions.split(hand, deck, player)

                self.bet_output_handler(player, "split", hand)
                if hand.splitted_aces:
                    print("You have splitted aces!")
                print("Your splitted hand now consists of:")
                self.displayPlayerHands(hand)
                print("Your new hand now consist of:")
                self.displayPlayerHands(new_hand)
                if hand.splitted_aces:
                    print("Both hands are now finished!")


    def mainGameLoop(self):

        self.player_actions.placeMainBet(
            self.player.hands[self.current_hand_index],
            self.player
        )
        self.bet_output_handler(self.player, "main_bet", self.player.hands[self.current_hand_index])

        while True:
            place_sidebet = input(
                "You want to place a sidebet? (y/n): "
            ).lower()

            if place_sidebet == "y":
                self.player_actions.chooseSidebet(self.player)
                self.bet_output_handler(self.player, "side_bet")
                break

            elif place_sidebet == "n":
                print("No sidebet chosen.")
                break

        self.initialCardDeal()

        self.outcome_eval.sidebetEval(self.player, self.dealer)
        self.payout.sidebetPayout(self.player)
        if any(sidebet.win for sidebet in self.player.sidebets):
            self.payout_output_handler(self.player, "side_bet")


        # Insurance Frage + check + payout
        if self.insurance_allowed(self.dealer.hand):
            while True:
                take_insurance = input(
                    "You want to take insurance? (y/n): "
                ).lower()

                if take_insurance == "y":
                    if self.player.bankroll.canBet(self.player.hands[0].bet / 2):
                        self.player_actions.take_insurance(self.player)
                        self.bet_output_handler(self.player, "insurance")
                        break
                    else:
                        print("Not enough money to take insurance.")
                        break

                elif take_insurance == "n":
                    print("No insurance taken.")
                    break

        player_blackjack, dealer_blackjack = self.outcome_eval.evaluateBlackjack(
            self.player.hands[0],
            self.dealer.hand
        )



        if player_blackjack or dealer_blackjack:
            self.handleInitialBlackjack(
                player_blackjack,
                dealer_blackjack
            )
            return
        if self.player.insurance_amount > 0:
            print("No dealer Blackjack!")
            print("Insurance lost!")

        self.playPlayerHands()

        if any(hand.result is None for hand in self.player.hands):
            self.playDealerHand(self.dealer)

        ##################################################################
        print(f"DEBUG dealer: total={self.dealer.hand.total} "
              f"bust={self.dealer.hand.bust} "
              f"cards={[str(c) for c in self.dealer.hand.cards]}")

        for hand in self.player.hands:
            print(f"DEBUG hand: total={hand.total} bust={hand.bust} "
                  f"result={hand.result}")
        ##################################################################

        self.outcome_eval.evaluate(self.player, self.dealer)
        # ergebnisse print
        for hand in self.player.hands:
            print(f"{self.player.hands.index(hand) + 1}. Hand")
            print(f"Result: {hand.result.capitalize()}")
            print()
        self.payout.defaultPayout(self.player)
        self.payout_output_handler(self.player, "main_bet")


    def handleInitialBlackjack(self, player_blackjack, dealer_blackjack):
        if dealer_blackjack and not player_blackjack:
            print("The dealer has a blackjack!")
            sleep(DELAY)
            if self.player.insurance_amount > 0 and self.outcome_eval.evaluate_insurance(self.player, self.dealer):
                self.payout.insurance_payout(self.player)
                self.payout_output_handler(self.player, "insurance")
            else:
                print("You lose")
                sleep(DELAY)
                self.display_balance(self.player)



        self.payout.blackjackPayout(
            player_blackjack,
            dealer_blackjack,
            self.player.hands[0],
            self.player
        )
        self.payout_output_handler(self.player, "blackjack",
                                   player_blackjack, dealer_blackjack)


    def displayPlayerHands(self, hand):
        print("Your cards are: ")
        for card in hand.cards:
            print(f"{hand.cards.index(card)+1}. {card}")
        print(f"Your total is {hand.total}")

    def displayDealerHand(self, hand, initial_card_deal = False):
        if not initial_card_deal:
            print("Dealer cards are: ")
            for card in hand.cards:
                print(f"{hand.cards.index(card)+1}. {card}")
            print(f"Dealer total is {hand.total}")
        else:
            print("The Dealer shows: ")
            print(f"1. {hand.cards[0]}")


    def insurance_allowed(self, dealer_hand):
        if dealer_hand.cards[0].rank == "A":
            return True
        return False

    def payout_output_handler(self, player, payout_type,
                            player_blackjack = False, dealer_blackjack = False):

        match payout_type:
            case "main_bet":
                for hand in player.hands:
                    if hand.result == "win":
                        print(f"{player.hands.index(hand) + 1}. Hand receives {hand.bet*2:.2f}€!")
                        sleep(DELAY)
                self.display_balance(player)

            case "side_bet":
                for sidebet in player.sidebets:
                    if sidebet.win:
                        print(f"You won the {sidebet.sidebet_type} sidebet!", end="")
                        if sidebet.sidebet_type == "special":
                            print(f"({sidebet.winning_type})")
                        else:
                            print()
                        sleep(DELAY)
                        print(f"You receive {sidebet.amount * sidebet.win_multiplier:.2f}€")
                self.display_balance(player)

            case "blackjack":
                if not dealer_blackjack and player_blackjack:
                    print("You have blackjack!")
                    sleep(DELAY)
                    print(f"You receive {player.hands[0].bet * 2.5:.2f}€")
                    sleep(DELAY)
                    self.display_balance(player)

                elif dealer_blackjack and player_blackjack:
                    print("You both have blackjack!")
                    print("Push!")
                    sleep(DELAY)
                    print(f"You receive your bet back ({player.hands[0].bet:.2f}€)")
                    sleep(DELAY)
                    self.display_balance(player)

            case "insurance":
                print("Insurance has won!")
                print(f"You received {player.insurance_amount * 3:.2f}€")
                self.display_balance(player)

            case "surrender":
                print(f"Your receive half of your bet back! ({player.hands[0].bet/2:.2f}€)")
                #sleep(DELAY)
                self.display_balance(player)

    def bet_output_handler(self, player, bet_type, hand = None):
        match bet_type:
            case "main_bet":
                print(f"Your bet of {hand.bet:.2f}€ has been placed!")
                self.display_balance(player)
            case "side_bet":
                for sidebet in player.sidebets:
                    print(f"Your bet of {sidebet.amount:.2f}€ has been placed for the {sidebet.sidebet_type} sidebet!")
                #sleep(DELAY)
                self.display_balance(player)
            case "double":
                print(f"Your bet ({hand.bet/2:.2f}€) has been doubled!")
                self.display_balance(player)
            case "split":
                print(f"Your split bet ({hand.bet:.2f}€) has been placed!")
                sleep(DELAY)
                self.display_balance(player)
            case "insurance":
                print(f"You have taken insurance ({player.insurance_amount:.2f}€)!")
                self.display_balance(player)
                sleep(DELAY)
            case _:
                pass


    def display_balance(self, player):
        print(f"Your balance is now {player.bankroll.balance:.2f}€")