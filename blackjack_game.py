from operator import index

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
        print(f"You now have {self.player.bankroll.balance}€ as your starting balance.")

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
        while dealer.hand.total < 17:
            new_card = self.deck.drawCard()
            print(f"The new dealer card is {new_card}")
            dealer.hand.addCard(new_card)
            sleep(1)

        if dealer.hand.total == 17 and dealer.hand.aces > 0:
            hasSoft17 = dealer.hand.soft17Check()

            if hasSoft17:
                print("The dealer has a soft-17 hand.")
                new_card = self.deck.drawCard()
                print(f"The new dealer card is {new_card}")
                dealer.hand.addCard(new_card)
                sleep(1)
                while dealer.hand.total < 17:
                    dealer.hand.addCard(self.deck.drawCard())
                    new_card = self.deck.drawCard()
                    print(f"The new dealer card is {new_card}")
                    dealer.hand.addCard(new_card)
                    sleep(1)

    def displayPlayerOptions(self, player, hand):

        player_options_list = self.player_options.listPlayerOptions(
            player,
            hand
        )

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
                print("Your hand now consists of:")
                self.displayPlayerHands(hand)

            case "stand":
                self.player_actions.stand(hand)

            case "surrender":
                self.player_actions.surrender(hand)
                self.payout.surrenderPayout(hand, player)
                print(f"Your received half of your bet amount back! ({hand.bet}€)")

            case "double":
                self.player_actions.double(hand, deck, player)
                print(f"Your new card is {hand.cards[2]}")
                self.displayPlayerHands(hand)

            case "split":
                new_hand = self.player_actions.split(hand, deck, player)
                print("Your splitted hand now consists of:")
                self.displayPlayerHands(hand)
                print("Your new hand now consist of:")
                self.displayPlayerHands(new_hand)

    def mainGameLoop(self):

        self.player_actions.placeMainBet(
            self.player.hands[self.current_hand_index],
            self.player
        )

        while True:
            place_sidebet = input(
                "You want to place a sidebet? (y/n): "
            ).lower()

            if place_sidebet == "y":
                self.player_actions.chooseSidebet(self.player)
                break

            elif place_sidebet == "n":
                print("No sidebet chosen.")
                break

        self.initialCardDeal()

        self.outcome_eval.sidebetEval(self.player, self.dealer)
        for sidebet in self.player.sidebets:
            if sidebet.win:
                print(f"The {sidebet.sidebet_type} sidebet won!")
        self.payout.sidebetPayout(self.player)

        # Insurance Frage + check + payout

        player_blackjack, dealer_blackjack = self.outcome_eval.evaluateBlackjack(
            self.player.hands[0],
            self.dealer.hand
        )

        if player_blackjack or dealer_blackjack:
            print("Blackjack!")
            self.handleInitialBlackjack(
                player_blackjack,
                dealer_blackjack
            )
            return

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
            print(f"{self.player.hands.index(hand) + 1}. Hand:")
            print(hand.result)
        self.payout.defaultPayout(self.player)
        print(f"Your balance is {self.player.bankroll.balance}")

    def handleInitialBlackjack(self, player_blackjack, dealer_blackjack):
        if dealer_blackjack and not player_blackjack:
            print("The dealer has a blackjack!")
            print("You lose")
        elif not dealer_blackjack and player_blackjack:
            print("You have blackjack!")
            print("You win")
        else:
            print("You both have blackjack!")
            print("Push")

        self.payout.blackjackPayout(
            player_blackjack,
            dealer_blackjack,
            self.player.hands[0],
            self.player
        )


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


    #