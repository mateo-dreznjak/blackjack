import random

from card import Card


class Deck:

    def __init__(self):
        self.spade_deck = {}
        self.diamond_deck = {}
        self.heart_deck = {}
        self.club_deck = {}

        self.all_decks = [
            self.spade_deck,
            self.diamond_deck,
            self.heart_deck,
            self.club_deck
        ]

        self.deck_probability = [78, 78, 78, 78]
        self.deck_suits = ["Spades", "Diamonds", "Hearts", "Clubs"]
        self.shuffle_value = random.randint(62, 109)

        self.initializeDeck()

    def initializeDeck(self):
        for deck in self.all_decks:
            for keys in range(2, 15):
                deck[keys] = 6

    def neededDeckShuffle(self):
        if sum(self.deck_probability) < self.shuffle_value:
            print("The shoe is being reshuffled!")
            self.deckShuffle()
        else:
            print("No new shuffle needed!")

    def deckShuffle(self):
        self.initializeDeck()
        self.deck_probability = [78, 78, 78, 78]
        self.shuffle_value = random.randint(62, 109)

    def drawCard(self):
        card_suit = random.choices(
            self.deck_suits,
            weights=self.deck_probability
        )[0]

        index = self.deck_suits.index(card_suit)
        self.deck_probability[index] -= 1

        match card_suit:
            case "Spades":
                drawn_rank = random.choices(
                    list(self.spade_deck.keys()),
                    weights=list(self.spade_deck.values())
                )[0]
                self.spade_deck[drawn_rank] -= 1

            case "Diamonds":
                drawn_rank = random.choices(
                    list(self.diamond_deck.keys()),
                    weights=list(self.diamond_deck.values())
                )[0]
                self.diamond_deck[drawn_rank] -= 1

            case "Hearts":
                drawn_rank = random.choices(
                    list(self.heart_deck.keys()),
                    weights=list(self.heart_deck.values())
                )[0]
                self.heart_deck[drawn_rank] -= 1

            case "Clubs":
                drawn_rank = random.choices(
                    list(self.club_deck.keys()),
                    weights=list(self.club_deck.values())
                )[0]
                self.club_deck[drawn_rank] -= 1

        card_value = self.evaluateCardValue(drawn_rank)
        card_rank = self.evaluateCardRank(drawn_rank)

        new_card = Card(card_suit, card_value, card_rank)

        return new_card

    def evaluateCardValue(self, drawn_rank):
        if drawn_rank < 11:
            card_value = drawn_rank
        elif drawn_rank > 10 and drawn_rank < 14:
            card_value = 10
        else:
            card_value = 11

        return card_value

    def evaluateCardRank(self, drawn_rank):
        if drawn_rank < 11:
            card_rank = str(drawn_rank)
        elif drawn_rank == 11:
            card_rank = "J"
        elif drawn_rank == 12:
            card_rank = "Q"
        elif drawn_rank == 13:
            card_rank = "K"
        else:
            card_rank = "A"

        return card_rank