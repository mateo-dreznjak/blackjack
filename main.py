from blackjack_game import BlackjackGame


def main():
    blackjack = BlackjackGame()
    blackjack.setupGame()
    blackjack.gameHandler()


if __name__ == "__main__":
    main()