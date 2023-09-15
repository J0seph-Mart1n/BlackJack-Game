import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True


class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.values = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                card_deck = Card(rank, suit)
                self.deck.append(card_deck)

    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()  # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Enter no of chips to bet:"))
        except TypeError:
            print("You have entered a string")
        else:
            if chips.bet > chips.total:
                print("Sorry the bet cannot exceed",chips.total)
            else:
                break


def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        hos = input("Do you want to Hit or stand enter (h or s): ")
        if hos == "h":
            hit(deck, hand)
        elif hos == "s":
            print("Player stand, Dealer plays")
            playing = False
        else:
            print("Enter valid input")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's hand")
    print("\ncard hidden")
    print(dealer.cards[1])
    print("\n Player's hand: ", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's hand:", *dealer.cards, sep='\n')
    print("Dealer's hand:", dealer.value)
    print("\nPlayer's hand:", *player.cards, sep='\n')
    print("Player's hand:", player.value)


def player_busts(player, dealer, chips):
    print("Player busted")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Player wins")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Dealer busted")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("Dealer wins")
    chips.lose_bet()


def push(player, dealer):
    print("Dealer and player tie! Its a push")


while True:
    # Print an opening statement
    print("Welcome to BlackJack")

    # Create & shuffle the deck, deal two cards to each player
    card_deck = Deck()
    card_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    for _ in range(2):
        player_hand.add_card(card_deck.deal())
        dealer_hand.add_card(card_deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(card_deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        if dealer_hand.value < 17:
            hit(card_deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    # Inform Player of their chips total
    print("No of chips player has: ", player_chips.total)
    # Ask to play again
    new_game = input("Do you want to play an another game (y or n)")

    if new_game == 'y':
        playing = True
        continue
    elif new_game == 'n':
        break
    else:
        print("Enter valid input")